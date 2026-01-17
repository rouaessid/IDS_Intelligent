import { Navbar } from "@/components/navbar"

export default function About() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="px-6 py-8 max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-foreground mb-8">About IDS Dashboard</h1>

        <div className="space-y-8">
          <section className="bg-card border border-border rounded-lg p-8">
            <h2 className="text-2xl font-bold text-foreground mb-4">System Architecture</h2>
            <p className="text-muted-foreground">
              This Intelligent Intrusion Detection System uses a hierarchical three-level detection approach to classify
              network threats with precision and speed.
            </p>
          </section>

          <section className="bg-card border border-border rounded-lg p-8">
            <h2 className="text-2xl font-bold text-foreground mb-6">Detection Pipeline</h2>
            <div className="space-y-4">
              <div className="bg-background border border-border rounded p-4">
                <h3 className="text-lg font-semibold text-primary mb-2">Level 1: Binary Classification</h3>
                <p className="text-muted-foreground">Identifies if traffic is benign or an attack</p>
              </div>
              <div className="bg-background border border-border rounded p-4">
                <h3 className="text-lg font-semibold text-primary mb-2">Level 2: Family Classification</h3>
                <p className="text-muted-foreground">
                  Classifies attacks into families (DoS, BruteForce, WebAttack, RareAttack)
                </p>
              </div>
              <div className="bg-background border border-border rounded p-4">
                <h3 className="text-lg font-semibold text-primary mb-2">Level 3: Expert Specialization</h3>
                <p className="text-muted-foreground">
                  Specialized models for each family to identify specific attack types
                </p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}
