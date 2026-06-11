// [Task]: T049 [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign
/**
 * Login page with glass card styling.
 */
import Link from 'next/link'
import { LogIn } from 'lucide-react'
import { LoginForm } from '@/components/forms/LoginForm'

export default function LoginPage() {
  return (
    <div className="glass-card p-8 animate-scale-in">
      {/* Gradient accent */}
      <div className="absolute top-0 left-0 right-0 h-1 gradient-primary rounded-t-2xl" />

      <div className="space-y-6">
        {/* Header */}
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl gradient-primary flex items-center justify-center">
            <LogIn className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-2xl font-bold text-white">
            Welcome back
          </h2>
          <p className="text-sm text-gray-400 mt-2">
            Log in to your account to continue
          </p>
        </div>

        {/* Form */}
        <LoginForm />

        {/* Link to signup */}
        <div className="text-center text-sm">
          <span className="text-gray-400">
            Don't have an account?{' '}
          </span>
          <Link
            href="/signup"
            className="text-indigo-400 hover:text-indigo-300 font-medium transition-colors"
          >
            Sign up
          </Link>
        </div>
      </div>
    </div>
  )
}
