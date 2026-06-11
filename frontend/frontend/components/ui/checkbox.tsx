// [Task]: T035 [P] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign
/**
 * Reusable Checkbox component with indigo accent and smooth animations.
 * Controlled component for task completion status.
 */
import { InputHTMLAttributes, forwardRef } from 'react'
import { clsx } from 'clsx'

export interface CheckboxProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label?: string
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, className, id, ...props }, ref) => {
    const checkboxStyles = clsx(
      'h-5 w-5 rounded-md',
      'border-2 border-gray-400 dark:border-gray-500',
      'text-indigo-500 focus:ring-indigo-500 focus:ring-2 focus:ring-offset-2 focus:ring-offset-transparent',
      'accent-indigo-500',
      'cursor-pointer transition-all duration-200',
      'bg-transparent checked:bg-indigo-500 checked:border-indigo-500',
      'hover:border-indigo-400',
      className
    )

    const inputId = id || `checkbox-${Math.random().toString(36).substr(2, 9)}`

    return (
      <div className="flex items-center gap-2">
        <input
          ref={ref}
          type="checkbox"
          id={inputId}
          className={checkboxStyles}
          {...props}
        />
        {label && (
          <label
            htmlFor={inputId}
            className="text-sm font-medium text-gray-300 dark:text-gray-300 cursor-pointer select-none hover:text-white transition-colors"
          >
            {label}
          </label>
        )}
      </div>
    )
  }
)

Checkbox.displayName = 'Checkbox'
