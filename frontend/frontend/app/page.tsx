// [Task]: T052 [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * TaskMate landing page — product showcase with animated AI demo.
 */
'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ArrowRight, X } from 'lucide-react'
import { Button } from '@/components/ui/button'

const DEMO_MESSAGES = [
  { role: 'user' as const, text: 'Add a task: Finish project proposal by Friday' },
  { role: 'ai' as const, text: "✅ Done! Task 'Finish project proposal by Friday' has been created." },
  { role: 'user' as const, text: 'Mark it as complete' },
  { role: 'ai' as const, text: '✔️ Task marked as complete! Great work.' },
  { role: 'user' as const, text: 'Delete all completed tasks' },
  { role: 'ai' as const, text: '🗑️ Deleted 1 completed task. Your list is clean!' },
]

const FEATURES = [
  {
    emoji: '🆕',
    title: 'Create with words',
    description: "Just say 'Add a task: call dentist tomorrow' and it's done.",
    example: 'Add a task: call dentist tomorrow',
  },
  {
    emoji: '✏️',
    title: 'Update naturally',
    description: "Say 'Rename my dentist task to call dentist at 3pm' and it updates instantly.",
    example: 'Rename my dentist task to call dentist at 3pm',
  },
  {
    emoji: '✅',
    title: 'Complete by chatting',
    description: "Tell the AI 'Mark the dentist task as done' — no clicking required.",
    example: 'Mark the dentist task as done',
  },
  {
    emoji: '🗑️',
    title: 'Clean up easily',
    description: "Say 'Delete all completed tasks' and watch your list stay tidy.",
    example: 'Delete all completed tasks',
  },
]

const TECH_STACK = ['Next.js', 'FastAPI', 'Claude AI', 'MCP Tools', 'PostgreSQL']

const BANNER_STORAGE_KEY = 'taskmate-floating-banner-dismissed'

function TypingIndicator() {
  return (
    <div className="flex items-start gap-2">
      <div className="w-7 h-7 rounded-full bg-indigo-500/20 flex items-center justify-center shrink-0">
        <span className="text-xs font-semibold text-indigo-400">AI</span>
      </div>
      <div className="bg-gray-200 dark:bg-gray-700/80 rounded-2xl rounded-tl-sm px-4 py-3">
        <div className="flex gap-1">
          <span className="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce [animation-delay:0ms]" />
          <span className="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce [animation-delay:150ms]" />
          <span className="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce [animation-delay:300ms]" />
        </div>
      </div>
    </div>
  )
}

export default function HomePage() {
  const [visibleCount, setVisibleCount] = useState(0)
  const [showTyping, setShowTyping] = useState(false)
  const [showBanner, setShowBanner] = useState(false)

  useEffect(() => {
    let cancelled = false
    const timeouts: ReturnType<typeof setTimeout>[] = []

    const schedule = (fn: () => void, delay: number) => {
      timeouts.push(
        setTimeout(() => {
          if (!cancelled) fn()
        }, delay)
      )
    }

    const runCycle = () => {
      setVisibleCount(0)
      setShowTyping(false)

      DEMO_MESSAGES.forEach((msg, i) => {
        const delay = i * 1200
        if (msg.role === 'ai') {
          schedule(() => setShowTyping(true), delay)
          schedule(() => {
            setShowTyping(false)
            setVisibleCount(i + 1)
          }, delay + 500)
        } else {
          schedule(() => setVisibleCount(i + 1), delay)
        }
      })

      schedule(runCycle, 8000)
    }

    runCycle()

    return () => {
      cancelled = true
      timeouts.forEach(clearTimeout)
    }
  }, [])

  useEffect(() => {
    const dismissed = localStorage.getItem(BANNER_STORAGE_KEY)
    if (!dismissed) {
      const timer = setTimeout(() => setShowBanner(true), 3000)
      return () => clearTimeout(timer)
    }
  }, [])

  const dismissBanner = () => {
    localStorage.setItem(BANNER_STORAGE_KEY, 'true')
    setShowBanner(false)
  }

  return (
    <div className="min-h-screen gradient-bg dark:gradient-bg gradient-bg-light flex flex-col">
      {/* Navigation */}
      <nav className="glass-nav dark:glass-nav glass-nav-light sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
                <span className="text-white font-bold text-xl">T</span>
              </div>
              <span className="text-xl font-bold gradient-text">TaskMate</span>
            </div>
            <div className="flex items-center gap-3">
              <Link href="/login">
                <Button variant="ghost" size="sm">
                  Log In
                </Button>
              </Link>
              <Link href="/signup">
                <Button variant="primary" size="sm">
                  Sign Up
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="flex flex-col items-center justify-center px-4 py-16 sm:py-24">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-indigo-500/20 border border-indigo-500/30">
              <span className="text-sm text-indigo-600 dark:text-indigo-300">
                ✨ AI-Powered Task Management
              </span>
            </div>

            <div className="space-y-4">
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white leading-tight">
                Stop managing tasks.{' '}
                <span className="gradient-text">Just talk to your AI.</span>
              </h1>
              <p className="text-lg sm:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
                TaskMate understands plain English. Create, update, complete, and delete tasks by
                chatting — no clicks needed.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-4">
              <Link href="/signup">
                <Button variant="primary" size="lg" className="min-w-[200px]">
                  Get Started Free
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </Link>
              <a href="#demo">
                <Button variant="ghost" size="lg" className="min-w-[200px]">
                  See how it works
                </Button>
              </a>
            </div>
          </div>
        </section>

        {/* Animated AI Demo Section */}
        <section id="demo" className="px-4 py-16 sm:py-20 scroll-mt-20">
          <div className="max-w-3xl mx-auto">
            <div className="text-center mb-10 space-y-3">
              <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white">
                See TaskMate in action
              </h2>
              <p className="text-gray-600 dark:text-gray-400 text-lg">
                No signup needed to see what the AI can do
              </p>
            </div>

            <div className="glass-card p-4 sm:p-6 space-y-4 min-h-[420px]">
              <div className="flex items-center gap-2 pb-3 border-b border-gray-200/20 dark:border-white/10">
                <div className="w-3 h-3 rounded-full bg-red-400/80" />
                <div className="w-3 h-3 rounded-full bg-amber-400/80" />
                <div className="w-3 h-3 rounded-full bg-green-400/80" />
                <span className="ml-2 text-xs text-gray-500 dark:text-gray-400">
                  TaskMate AI Assistant
                </span>
              </div>

              <div className="space-y-4">
                {DEMO_MESSAGES.slice(0, visibleCount).map((msg, i) =>
                  msg.role === 'user' ? (
                    <div key={i} className="flex justify-end animate-slide-up">
                      <div className="max-w-[85%] sm:max-w-[75%] bg-indigo-600 dark:bg-indigo-500 text-white rounded-2xl rounded-tr-sm px-4 py-3 text-sm sm:text-base">
                        {msg.text}
                      </div>
                    </div>
                  ) : (
                    <div key={i} className="flex items-start gap-2 animate-slide-up">
                      <div className="w-7 h-7 rounded-full bg-indigo-500/20 flex items-center justify-center shrink-0">
                        <span className="text-xs font-semibold text-indigo-400">AI</span>
                      </div>
                      <div className="max-w-[85%] sm:max-w-[75%] bg-gray-200 dark:bg-gray-700/80 text-gray-800 dark:text-gray-200 rounded-2xl rounded-tl-sm px-4 py-3 text-sm sm:text-base">
                        {msg.text}
                      </div>
                    </div>
                  )
                )}
                {showTyping && <TypingIndicator />}
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="px-4 py-16 sm:py-20">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white text-center mb-12">
              Everything you need, nothing you don&apos;t
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {FEATURES.map((feature, index) => (
                <div
                  key={feature.title}
                  className="glass-card p-6 flex flex-col hover-lift animate-slide-up"
                  style={{ animationDelay: `${index * 0.1}s`, animationFillMode: 'backwards' }}
                >
                  <div className="text-3xl mb-3">{feature.emoji}</div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 text-sm flex-1 mb-4">
                    {feature.description}
                  </p>
                  <div className="mt-auto">
                    <code className="block text-xs sm:text-sm font-mono bg-gray-100 dark:bg-gray-800/80 text-indigo-600 dark:text-indigo-300 px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-700">
                      {feature.example}
                    </code>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Social Proof Strip */}
        <section className="px-4 py-10">
          <div className="max-w-4xl mx-auto text-center">
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">Built with</p>
            <div className="flex flex-wrap justify-center gap-3">
              {TECH_STACK.map((tech) => (
                <span
                  key={tech}
                  className="px-4 py-1.5 rounded-full text-sm font-medium bg-indigo-500/10 dark:bg-indigo-500/20 text-indigo-700 dark:text-indigo-300 border border-indigo-500/20"
                >
                  {tech}
                </span>
              ))}
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="py-8 text-center text-gray-600 dark:text-gray-500 text-sm border-t border-gray-200/20 dark:border-white/10">
        <p>
          Built by{' '}
          <a
            href="https://github.com/anusbutt"
            target="_blank"
            rel="noopener noreferrer"
            className="text-indigo-600 dark:text-indigo-400 hover:underline font-medium"
          >
            Anus Butt
          </a>{' '}
          · AI Engineer
        </p>
      </footer>

      {/* Floating Banner */}
      {showBanner && (
        <div className="fixed bottom-4 left-4 right-4 sm:left-auto sm:right-6 sm:max-w-lg z-50 animate-slide-up">
          <div className="flex items-center gap-3 bg-gray-900 dark:bg-gray-950 text-white px-4 py-3 sm:px-5 sm:py-4 rounded-xl shadow-lg shadow-black/25 border border-gray-700/50">
            <p className="flex-1 text-sm sm:text-base leading-snug">
              💬 This app has a built-in AI assistant — manage all your tasks just by chatting
            </p>
            <Link href="/signup" className="shrink-0">
              <Button
                variant="primary"
                size="sm"
                className="whitespace-nowrap text-sm"
              >
                Try it free →
              </Button>
            </Link>
            <button
              onClick={dismissBanner}
              aria-label="Dismiss banner"
              className="shrink-0 p-1 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
