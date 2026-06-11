// [Task]: T034 [P] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign
/**
 * Reusable Card component with glassmorphism styling.
 * Supports hover effects, gradient borders, and priority-based border colors.
 */
import { HTMLAttributes } from 'react'
import { clsx } from 'clsx'

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  hover?: boolean
  glass?: boolean
  gradientBorder?: boolean
  priority?: 'P1' | 'P2' | 'P3' | 'P4'
}

export function Card({
  hover = false,
  glass = true,
  gradientBorder = false,
  priority,
  className,
  children,
  ...props
}: CardProps) {
  // Base glass card styles
  const glassStyles = glass
    ? 'glass-card dark:glass-card glass-card-light'
    : 'bg-white dark:bg-gray-800 rounded-xl shadow-md border border-gray-200 dark:border-gray-700'

  // Hover effects
  const hoverStyles = hover
    ? 'transition-all duration-200 hover-lift hover-glow cursor-pointer'
    : 'transition-all duration-200'

  // Gradient border
  const borderStyles = gradientBorder ? 'gradient-border' : ''

  // Priority-based left border
  const priorityStyles = priority
    ? {
        P1: 'priority-p1-border',
        P2: 'priority-p2-border',
        P3: 'priority-p3-border',
        P4: 'priority-p4-border',
      }[priority]
    : ''

  return (
    <div
      className={clsx(
        'p-4',
        glassStyles,
        hoverStyles,
        borderStyles,
        priorityStyles,
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}
