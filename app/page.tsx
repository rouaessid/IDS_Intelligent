"use client"

import { Navbar } from "@/components/navbar"
import { ArrowRight, AlertCircle, BarChart3, Zap } from "lucide-react"
import Link from "next/link"

export default function Home() {
  const stats = [
    { label: "Threats Detected", value: "1,247", icon: AlertCircle },
    { label: "Detection Rate", value: "90%", icon: BarChart3 },
    { label: "Avg Response", value: "5ms", icon: Zap },
  ]

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <section className="px-6 py-20 max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center mb-20">
          <div>
            <h1 className="text-5xl font-bold text-foreground mb-6">
              Intelligent Network <span className="text-primary">Intrusion Detection</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-8">
              Advanced three-level hierarchical threat detection system with real-time monitoring and detailed attack
              classification.
            </p>
            <div className="flex gap-4">
              <Link
                href="/dashboard"
                className="bg-primary hover:opacity-90 text-primary-foreground px-8 py-3 rounded-lg font-semibold transition flex items-center gap-2 w-fit"
              >
                Start Monitoring <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                href="/about"
                className="border border-border hover:bg-card text-foreground px-8 py-3 rounded-lg font-semibold transition w-fit"
              >
                Learn More
              </Link>
            </div>
          </div>

          <div className="bg-card border border-border rounded-lg p-8">
            <div className="space-y-4">
              <div className="bg-background rounded p-4 border border-border">
                <div className="space-y-2">
                  <div className="h-2 bg-gradient-to-r from-destructive to-transparent rounded w-3/4"></div>
                  <div className="h-2 bg-gradient-to-r from-chart-2 to-transparent rounded w-1/2"></div>
                  <div className="h-2 bg-gradient-to-r from-chart-4 to-transparent rounded w-1/3"></div>
                </div>
              </div>
              <p className="text-muted-foreground text-sm">Real-time threat detection across 3 classification levels</p>
            </div>
          </div>
        </div>

        <div className="bg-card border border-border rounded-lg p-8 mb-20">
          <h2 className="text-3xl font-bold text-foreground mb-12">System Overview</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {stats.map((stat, idx) => (
              <div key={idx} className="bg-background border border-border rounded p-6">
                <div className="flex items-center gap-3 mb-4">
                  <stat.icon className="w-6 h-6 text-primary" />
                  <p className="text-muted-foreground text-sm">{stat.label}</p>
                </div>
                <p className="text-3xl font-bold text-foreground">{stat.value}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="mb-20">
          <h2 className="text-3xl font-bold text-foreground mb-8 text-center">Three-Level Detection Pipeline</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              { level: "Level 1", title: "Binary Detection", desc: "Identifies attack vs benign traffic" },
              { level: "Level 2", title: "Family Classification", desc: "Classifies specific attack families" },
              { level: "Level 3", title: "Expert Analysis", desc: "Identifies detailed attack types" },
            ].map((f, idx) => (
              <div key={idx} className="bg-card border border-border rounded-lg p-6 hover:border-primary transition">
                <p className="text-primary font-semibold text-sm mb-2">{f.level}</p>
                <h3 className="text-xl font-bold text-foreground mb-3">{f.title}</h3>
                <p className="text-muted-foreground">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
