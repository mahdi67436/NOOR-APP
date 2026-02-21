'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  return (
    <main className="flex min-h-screen flex-col">
      {/* Header */}
      <header className="bg-emerald-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <span className="text-3xl">🛡️</span>
            <h1 className="text-2xl font-bold">NoorGuard</h1>
          </div>
          <nav className="flex space-x-6">
            <Link href="/login" className="hover:text-emerald-200 transition">
              Login
            </Link>
            <Link href="/register" className="hover:text-emerald-200 transition">
              Register
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-b from-emerald-600 to-emerald-800 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-5xl font-bold mb-6">
            Islamic Digital Protection Ecosystem
          </h2>
          <p className="text-xl mb-8 text-emerald-100">
            Protect your family with AI-powered content filtering, behavioral monitoring,
            and Islamic features
          </p>
          <div className="flex justify-center space-x-4">
            <Link
              href="/register"
              className="bg-white text-emerald-600 px-8 py-3 rounded-lg font-semibold hover:bg-emerald-50 transition"
            >
              Get Started
            </Link>
            <Link
              href="#features"
              className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white/10 transition"
            >
              Learn More
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h3 className="text-3xl font-bold text-center mb-12 text-gray-800">
            Key Features
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
              <div className="text-4xl mb-4">🛡️</div>
              <h4 className="text-xl font-semibold mb-2">Smart Content Shield</h4>
              <p className="text-gray-600">
                AI-powered content filtering with DNS-level blocking and keyword filtering
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
              <div className="text-4xl mb-4">📊</div>
              <h4 className="text-xl font-semibold mb-2">AI Behavioral Monitoring</h4>
              <p className="text-gray-600">
                Detect suspicious patterns and late-night usage with addiction risk scoring
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
              <div className="text-4xl mb-4">📱</div>
              <h4 className="text-xl font-semibold mb-2">App Control System</h4>
              <p className="text-gray-600">
                Time-based restrictions, daily quotas, and salah-time auto lock
              </p>
            </div>

            {/* Feature 4 */}
            <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
              <div className="text-4xl mb-4">🕌</div>
              <h4 className="text-xl font-semibold mb-2">Salah Integration</h4>
              <p className="text-gray-600">
                Auto prayer times, adhan notifications, and app pause during salah
              </p>
            </div>

            {/* Feature 5 */}
            <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
              <div className="text-4xl mb-4">🔐</div>
              <h4 className="text-xl font-semibold mb-2">Security Layer</h4>
              <p className="text-gray-600">
                AES-256 encryption, JWT auth, biometric support, and anti-tamper
              </p>
            </div>

            {/* Feature 6 */}
            <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition">
              <div className="text-4xl mb-4">📈</div>
              <h4 className="text-xl font-semibold mb-2">Analytics & Reports</h4>
              <p className="text-gray-600">
                Weekly PDF reports, screen time graphs, and Islamic habit improvement
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="container mx-auto px-4 text-center">
          <p className="text-gray-400">
            © 2024 NoorGuard Ultimate. Built with ❤️ for Muslim families.
          </p>
        </div>
      </footer>
    </main>
  )
}
