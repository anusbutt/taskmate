// [Task]: T047, T093 [US1, US5] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign
/**
 * Auth layout wrapper with gradient background and centered glass card.
 */
import { ReactNode } from 'react'
import Link from 'next/link'

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen gradient-bg dark:gradient-bg gradient-bg-light flex flex-col">
      {/* Simple nav with logo */}
      <nav className="py-6 px-4">
        <Link href="/" className="flex items-center gap-3 w-fit mx-auto">
          <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
            <span className="text-white font-bold text-xl">T</span>
          </div>
          <span className="text-xl font-bold gradient-text">TaskMate</span>
        </Link>
      </nav>

      {/* Centered content */}
      <main className="flex-1 flex items-center justify-center px-4 sm:px-6 md:px-8 py-8">
        <div className="max-w-md w-full mx-auto">
          {children}
        </div>
      </main>

      {/* Footer */}
      <footer className="py-4 text-center text-gray-500 text-sm">
        <p>Secure authentication powered by JWT</p>
      </footer>
    </div>
  )
}
