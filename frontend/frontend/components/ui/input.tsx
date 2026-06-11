// [Task]: T032 [P] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign
/**
 * Reusable Input component with glass styling.
 * Supports text, email, password input types with error states.
 */
import { InputHTMLAttributes, forwardRef } from 'react'
import { clsx } from 'clsx'

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  fullWidth?: boolean
  glass?: boolean
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, fullWidth = false, glass = true, className, ...props }, ref) => {
    const baseStyles =
      'px-4 py-2.5 text-base rounded-xl transition-all duration-200 focus:outline-none'

    const glassStyles = glass
      ? 'glass-input text-white placeholder:text-gray-400'
      : 'bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'

    const errorStyles = error
      ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
      : ''

    const widthStyles = fullWidth ? 'w-full' : ''

    const inputStyles = clsx(
      baseStyles,
      glassStyles,
      errorStyles,
      widthStyles,
      className
    )

    return (
      <div className={clsx('flex flex-col gap-1.5', fullWidth && 'w-full')}>
        {label && (
          <label
            htmlFor={props.id}
            className="text-sm font-medium text-gray-300 dark:text-gray-300"
          >
            {label}
          </label>
        )}
        <input ref={ref} className={inputStyles} {...props} />
        {error && (
          <span className="text-sm text-red-400 flex items-center gap-1">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            {error}
          </span>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'
