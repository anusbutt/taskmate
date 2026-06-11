// [Task]: T030, T099, T110, T122 | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Root layout component for Next.js App Router.
 * Provides HTML structure, Tailwind CSS, font optimization, viewport configuration, dark mode support, and error boundary.
 */
import type { Metadata, Viewport } from 'next'
import { ThemeProvider } from '@/components/providers/theme-provider'
import { ErrorBoundary } from '@/components/error-boundary'
import './globals.css'

export const metadata: Metadata = {
  title: 'TaskMate — AI-Powered Task Manager',
  description:
    'TaskMate is an AI-powered todo app. Create, update, complete and delete tasks by just chatting with the AI assistant.',
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning className="scroll-smooth">
      <body className="antialiased">
        <ErrorBoundary>
          <ThemeProvider>
            {children}
          </ThemeProvider>
        </ErrorBoundary>
      </body>
    </html>
  )
}
