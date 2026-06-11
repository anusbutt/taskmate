// [Task]: Phase 5 - New Component
/**
 * Priority select dropdown for task forms.
 * Shows colored badge preview for each option.
 */
'use client'

import { useState, useRef, useEffect } from 'react'
import { clsx } from 'clsx'
import { ChevronDown } from 'lucide-react'
import { PriorityBadge, type DisplayPriority } from './priority-badge'
import type { Priority } from '@/types'

interface PrioritySelectProps {
  value: Priority
  onChange: (value: Priority) => void
  className?: string
  disabled?: boolean
}

const priorityOptions: { value: Priority; label: string }[] = [
  { value: 'P1', label: 'Critical' },
  { value: 'P2', label: 'High' },
  { value: 'P3', label: 'Medium' },
]

export function PrioritySelect({
  value,
  onChange,
  className,
  disabled = false,
}: PrioritySelectProps) {
  const [isOpen, setIsOpen] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Close on escape
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsOpen(false)
      }
    }

    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [])

  const handleSelect = (priority: Priority) => {
    onChange(priority)
    setIsOpen(false)
  }

  return (
    <div ref={containerRef} className={clsx('relative', className)}>
      <button
        type="button"
        onClick={() => !disabled && setIsOpen(!isOpen)}
        disabled={disabled}
        className={clsx(
          'w-full flex items-center justify-between gap-2',
          'px-3 py-2 rounded-xl',
          'glass-input text-gray-900 dark:text-white',
          'transition-all duration-200',
          disabled && 'opacity-50 cursor-not-allowed',
          isOpen && 'ring-2 ring-indigo-500/50'
        )}
      >
        <PriorityBadge priority={value} size="sm" />
        <ChevronDown
          className={clsx(
            'w-4 h-4 text-gray-400 transition-transform duration-200',
            isOpen && 'rotate-180'
          )}
        />
      </button>

      {isOpen && (
        <div
          className={clsx(
            'absolute z-50 w-full mt-1',
            'glass-card py-1',
            'animate-scale-in origin-top'
          )}
        >
          {priorityOptions.map((option) => (
            <button
              key={option.value}
              type="button"
              onClick={() => handleSelect(option.value)}
              className={clsx(
                'w-full flex items-center gap-2 px-3 py-2',
                'text-left transition-colors',
                value === option.value
                  ? 'bg-indigo-500/20'
                  : 'hover:bg-gray-100 dark:hover:bg-white/10'
              )}
            >
              <PriorityBadge priority={option.value} size="sm" />
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
