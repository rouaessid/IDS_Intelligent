"use client"

import { useEffect, useState } from "react"
import { Navbar } from "@/components/navbar"
import { AlertCircle, CheckCircle, Clock, Loader } from "lucide-react"
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"

interface DetectionResult {
  Level1: string
  Level2: string
  Level3: string
  Status: string
}

interface SimulationData {
  total_flows: number
  benign_flows: number
  attack_flows: number
  alerts: Array<{
    index: number
    family: string
    type: string
    severity: string
  }>
  results: DetectionResult[]
}

export default function Dashboard() {
  const [loading, setLoading] = useState(false)
  const [simulating, setSimulating] = useState(false)
  const [stats, setStats] = useState({
    threats: 0,
    safe: 0,
    avgResponse: "5ms",
  })
  const [recentAlerts, setRecentAlerts] = useState<any[]>([])
  const [trafficData, setTrafficData] = useState<any[]>([])
  const [familyData, setFamilyData] = useState<any[]>([])
  const [error, setError] = useState<string | null>(null)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"

  useEffect(() => {
    const loadDashboard = async () => {
      try {
        setLoading(true)
        setError(null)
        const response = await fetch(`${API_URL}/api/stats`)
        if (response.ok) {
          console.log("[v0] Stats loaded successfully")
        }
      } catch (error) {
        setError("Failed to connect to backend. Make sure the Flask server is running on port 5000.")
        console.error("[v0] Failed to load stats:", error)
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [API_URL])

  const handleSimulate = async () => {
    try {
      setSimulating(true)
      setError(null)
      const response = await fetch(`${API_URL}/api/simulate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ num_flows: 50 }),
      })

      if (!response.ok) throw new Error("Simulation failed")

      const data: SimulationData = await response.json()

      setStats({
        threats: data.attack_flows,
        safe: data.benign_flows,
        avgResponse: "5ms",
      })

      const formattedAlerts = data.alerts.slice(0, 10).map((alert) => ({
        level1: "ATTACK",
        level2: alert.family,
        level3: alert.type,
        severity: "high",
      }))
      setRecentAlerts(formattedAlerts)

      const hours = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]
      setTrafficData(
        hours.map((time, idx) => ({
          time,
          attacks: Math.floor((data.attack_flows / 6) * (0.8 + Math.random() * 0.4)),
          benign: Math.floor((data.benign_flows / 6) * (0.8 + Math.random() * 0.4)),
        })),
      )

      const families: { [key: string]: number } = {}
      data.alerts.forEach((alert) => {
        families[alert.family] = (families[alert.family] || 0) + 1
      })
      setFamilyData(
        Object.entries(families).map(([name, count]) => ({
          name,
          count,
        })),
      )

      console.log("[v0] Simulation completed with", data.attack_flows, "attacks detected")
    } catch (error) {
      setError("Simulation error. Check console for details.")
      console.error("[v0] Simulation error:", error)
    } finally {
      setSimulating(false)
    }
  }

  const defaultTrafficData = [
    { time: "00:00", attacks: 12, benign: 89 },
    { time: "04:00", attacks: 19, benign: 95 },
    { time: "08:00", attacks: 8, benign: 76 },
    { time: "12:00", attacks: 25, benign: 102 },
    { time: "16:00", attacks: 15, benign: 88 },
    { time: "20:00", attacks: 22, benign: 98 },
  ]

  const defaultFamilyData = [
    { name: "DoS", count: 34 },
    { name: "BruteForce", count: 28 },
    { name: "WebAttack", count: 15 },
    { name: "RareAttack", count: 7 },
  ]

  const defaultRecentActivity = [
    { level1: "ATTACK", level2: "DoS", level3: "SynFlood", severity: "high" },
    { level1: "BENIGN", level2: "Normal", level3: "HTTP", severity: "safe" },
    { level1: "ATTACK", level2: "BruteForce", level3: "SSHAttack", severity: "high" },
    { level1: "BENIGN", level2: "Normal", level3: "HTTPS", severity: "safe" },
  ]

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="px-6 py-8 max-w-7xl mx-auto">
        {error && (
          <div className="mb-6 bg-destructive/10 border border-destructive rounded-lg p-4 flex gap-3">
            <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-destructive font-semibold">Connection Error</p>
              <p className="text-destructive text-sm">{error}</p>
            </div>
          </div>
        )}

        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-4xl font-bold text-foreground mb-2">Live Monitor</h1>
            <p className="text-muted-foreground">Real-time network threat analysis</p>
          </div>
          <button
            onClick={handleSimulate}
            disabled={simulating}
            className="bg-primary hover:opacity-90 disabled:opacity-50 text-primary-foreground px-6 py-3 rounded-lg font-semibold transition flex items-center gap-2"
          >
            {simulating ? (
              <>
                <Loader className="w-4 h-4 animate-spin" />
                Simulating...
              </>
            ) : (
              <>
                <Clock className="w-4 h-4" />
                Start Simulation
              </>
            )}
          </button>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-card border border-border rounded-lg p-6">
            <div className="flex items-center gap-4">
              <AlertCircle className="w-8 h-8 text-destructive" />
              <div>
                <p className="text-muted-foreground text-sm">Threats Detected</p>
                <p className="text-3xl font-bold text-foreground">{stats.threats}</p>
              </div>
            </div>
          </div>

          <div className="bg-card border border-border rounded-lg p-6">
            <div className="flex items-center gap-4">
              <CheckCircle className="w-8 h-8 text-chart-2" />
              <div>
                <p className="text-muted-foreground text-sm">Safe Packets</p>
                <p className="text-3xl font-bold text-foreground">{stats.safe}</p>
              </div>
            </div>
          </div>

          <div className="bg-card border border-border rounded-lg p-6">
            <div className="flex items-center gap-4">
              <Clock className="w-8 h-8 text-primary" />
              <div>
                <p className="text-muted-foreground text-sm">Avg Response</p>
                <p className="text-3xl font-bold text-foreground">{stats.avgResponse}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-xl font-bold text-foreground mb-6">Traffic Over Time</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trafficData.length > 0 ? trafficData : defaultTrafficData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="time" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{ backgroundColor: "#1e293b", border: "1px solid #334155", borderRadius: "8px" }}
                />
                <Legend />
                <Line type="monotone" dataKey="attacks" stroke="#dc2626" strokeWidth={2} />
                <Line type="monotone" dataKey="benign" stroke="#22c55e" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-card border border-border rounded-lg p-6">
            <h2 className="text-xl font-bold text-foreground mb-6">Threats by Family</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={familyData.length > 0 ? familyData : defaultFamilyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{ backgroundColor: "#1e293b", border: "1px solid #334155", borderRadius: "8px" }}
                />
                <Bar dataKey="count" fill="#6366f1" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <h2 className="text-xl font-bold text-foreground mb-6">Recent Activity</h2>
          <div className="space-y-3">
            {(recentAlerts.length > 0 ? recentAlerts : defaultRecentActivity).map((item, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between bg-background border border-border rounded p-4"
              >
                <div className="flex gap-8">
                  <div>
                    <p className="text-muted-foreground text-xs uppercase">Level 1</p>
                    <p className="text-foreground font-semibold">{item.level1}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground text-xs uppercase">Family</p>
                    <p className="text-foreground font-semibold">{item.level2}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground text-xs uppercase">Type</p>
                    <p className="text-foreground font-semibold">{item.level3}</p>
                  </div>
                </div>
                <span
                  className={`px-3 py-1 rounded text-xs font-semibold ${
                    item.severity === "high" ? "bg-destructive/20 text-destructive" : "bg-chart-2/20 text-chart-2"
                  }`}
                >
                  {item.severity.toUpperCase()}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
