// [Task]: T031 [P] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign
/**
 * Reusable Button component with gradient and glass variants.
 * Supports primary (gradient), secondary, danger, and ghost styles.
 */
import { ButtonHTMLAttributes } from 'react'
import { clsx } from 'clsx'

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  fullWidth?: boolean
}

export function Button({
  variant = 'primary',
  size = 'md',
  fullWidth = false,
  className,
  children,
  ...props
}: ButtonProps) {
  const baseStyles =
    'inline-flex items-center justify-center font-medium rounded-xl transition-all duration-200 focus:outline-none focus-ring-primary disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none'

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  const variantStyles = {
    primary:
      'gradient-primary text-white hover:brightness-110 hover:shadow-lg hover:shadow-indigo-500/25 active:brightness-95',
    secondary:
      'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 border border-gray-300 dark:border-gray-600',
    danger:
      'bg-red-500 text-white hover:bg-red-600 hover:shadow-lg hover:shadow-red-500/25 active:bg-red-700',
    ghost:
      'bg-transparent text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 border border-transparent hover:border-indigo-200 dark:hover:border-indigo-800',
  }

  const widthStyles = fullWidth ? 'w-full' : ''

  return (
    <button
      className={clsx(
        baseStyles,
        sizeStyles[size],
        variantStyles[variant],
        widthStyles,
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}
