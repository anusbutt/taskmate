// [Task]: T110 [US7] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Theme provider component to initialize dark mode on page load.
 * Prevents flash of unstyled content by applying theme as early as possible.
 */
'use client'

import { useEffect } from 'react'
import { initializeTheme } from '@/lib/theme'

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize theme on mount
    initializeTheme()
  }, [])

  return <>{children}</>
}
