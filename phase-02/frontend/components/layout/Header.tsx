// [Task]: T053, T094, T112 [US1, US5, US7] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign
/**
 * Header component with glass styling and gradient text.
 * Displays current user's name and provides logout functionality.
 */
'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'
import { LogOut, User } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { ThemeToggle } from '@/components/layout/theme-toggle'
import { apiRequest, ApiError } from '@/lib/api-client'

interface HeaderProps {
  userName: string
}

export function Header({ userName }: HeaderProps) {
  const router = useRouter()
  const [isLoggingOut, setIsLoggingOut] = useState(false)

  const handleLogout = async () => {
    setIsLoggingOut(true)

    try {
      await apiRequest('/api/auth/logout', {
        method: 'POST',
      })

      router.push('/')
    } catch (error) {
      if (error instanceof ApiError) {
        console.error('Logout failed:', error.message)
      } else {
        console.error('Unexpected error during logout')
      }
    } finally {
      setIsLoggingOut(false)
    }
  }

  return (
    <header className="sticky top-0 z-40 glass-nav dark:glass-nav glass-nav-light">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          {/* Logo/Title */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
              <span className="text-white font-bold text-xl">T</span>
            </div>
            <h1 className="text-xl sm:text-2xl font-bold gradient-text">
              TaskMate
            </h1>
          </div>

          {/* User info and actions */}
          <div className="flex items-center gap-2 sm:gap-4">
            {/* User badge */}
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/10 dark:bg-white/10">
              <User className="w-4 h-4 text-indigo-400" />
              <span className="text-sm text-gray-200 dark:text-gray-200">
                {userName}
              </span>
            </div>

            <ThemeToggle />

            <Button
              variant="ghost"
              size="sm"
              onClick={handleLogout}
              disabled={isLoggingOut}
              className="text-gray-300 hover:text-white"
            >
              <LogOut className="w-4 h-4 mr-1 sm:mr-2" />
              <span className="hidden sm:inline">
                {isLoggingOut ? 'Logging out...' : 'Log Out'}
              </span>
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
