"use client"

import { useState } from "react"
import { Navbar } from "@/components/navbar"
import { Zap, AlertCircle } from "lucide-react"

interface DetectionResult {
  Level1: string
  Level2: string
  Level3: string
  Status: string
}

export default function Analysis() {
  const [index, setIndex] = useState<number>(540822)
  const [results, setResults] = useState<DetectionResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [datasetSize, setDatasetSize] = useState<number | null>(null)
  const [error, setError] = useState<string | null>(null)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"

  const handleAnalyze = async () => {
    try {
      setLoading(true)
      setError(null)

      const response = await fetch(`${API_URL}/api/detect-by-index`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || "Analysis failed")
      }

      const data = await response.json()
      setResults(data.result)
      setDatasetSize(data.dataset_size)
      console.log("[v0] Analysis completed for index", index, data.result)
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error"
      setError(message)
      console.error("[v0] Analysis error:", message)
    } finally {
      setLoading(false)
    }
  }

  const handleRandomAttack = async () => {
    try {
      const randomIdx = Math.floor(Math.random() * (1000000 - 540814) + 540814)
      setIndex(randomIdx)
      setError(null)

      // Analyze the random index
      const response = await fetch(`${API_URL}/api/detect-by-index`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index: randomIdx }),
      })

      if (!response.ok) throw new Error("Failed to analyze")

      const data = await response.json()
      setResults(data.result)
      setDatasetSize(data.dataset_size)
    } catch (err) {
      console.error("[v0] Random attack error:", err)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="px-6 py-8 max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-foreground mb-2">Manual Analysis</h1>
        <p className="text-muted-foreground mb-8">Analyze network flows with detailed threat classification</p>

        <div className="bg-card border border-border rounded-lg p-8">
          <div className="mb-6">
            <label className="block text-foreground font-semibold mb-4">Upload Network Data (CSV)</label>
            <input
              type="file"
              accept=".csv"
              className="w-full px-4 py-3 bg-background border border-border rounded-lg text-foreground cursor-pointer file:mr-4 file:bg-primary file:text-primary-foreground file:px-4 file:py-2 file:border-0 file:rounded-md file:cursor-pointer"
            />
          </div>

          <div className="space-y-4 mb-6">
            <div>
              <label className="block text-foreground font-semibold mb-4">Flow Index (Dataset)</label>
              <p className="text-muted-foreground text-sm mb-3">
                {datasetSize ? `Dataset contains ${datasetSize.toLocaleString()} flows` : "Loading dataset info..."}
              </p>
              <p className="text-muted-foreground text-sm mb-2">Benign flows: 0-540,813 | Attack flows: 540,814+</p>
              <input
                type="number"
                value={index}
                onChange={(e) => setIndex(Math.max(0, Number.parseInt(e.target.value) || 0))}
                className="w-full px-4 py-3 bg-background border border-border rounded-lg text-foreground"
                min="0"
                max={datasetSize ? datasetSize - 1 : undefined}
              />
            </div>
          </div>

          <div className="flex gap-3 mb-6">
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="flex-1 bg-primary hover:opacity-90 disabled:opacity-50 text-primary-foreground font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2"
            >
              <Zap className="w-4 h-4" />
              {loading ? "Analyzing..." : "Run Analysis"}
            </button>
            <button
              onClick={handleRandomAttack}
              disabled={loading}
              className="flex-1 bg-secondary hover:opacity-90 disabled:opacity-50 text-secondary-foreground font-semibold py-3 rounded-lg transition"
            >
              🎲 Random Attack
            </button>
          </div>

          {error && (
            <div className="mb-6 bg-destructive/10 border border-destructive rounded-lg p-4 flex gap-3">
              <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
              <p className="text-destructive">{error}</p>
            </div>
          )}

          {results && (
            <div>
              <h3 className="text-xl font-bold text-foreground mb-4">Detection Results</h3>
              <div className="bg-background border border-border rounded p-6 grid md:grid-cols-2 gap-4">
                <div>
                  <p className="text-muted-foreground text-sm uppercase">Level 1 (Binary)</p>
                  <p className="text-foreground font-bold text-lg">{results.Level1}</p>
                </div>
                <div>
                  <p className="text-muted-foreground text-sm uppercase">Level 2 (Family)</p>
                  <p className="text-foreground font-bold text-lg">{results.Level2}</p>
                </div>
                <div>
                  <p className="text-muted-foreground text-sm uppercase">Level 3 (Type)</p>
                  <p className="text-foreground font-bold text-lg">{results.Level3}</p>
                </div>
                <div>
                  <p className="text-muted-foreground text-sm uppercase">Status</p>
                  <p
                    className={`font-bold text-lg ${results.Status === "Danger" ? "text-destructive" : "text-chart-2"}`}
                  >
                    {results.Status}
                  </p>
                </div>
              </div>

              {results.Status === "Danger" && (
                <div className="mt-4 bg-destructive/10 border border-destructive rounded-lg p-4">
                  <p className="text-destructive font-semibold">🚨 Malicious Traffic Detected: {results.Level3}</p>
                </div>
              )}

              {results.Status === "Safe" && (
                <div className="mt-4 bg-chart-2/10 border border-chart-2 rounded-lg p-4">
                  <p className="text-chart-2 font-semibold">✅ Traffic is Benign</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
