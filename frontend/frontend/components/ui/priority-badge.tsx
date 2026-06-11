// [Task]: Phase 5 - New Component
/**
 * Priority badge component displaying task priority with semantic colors.
 * P1 (Critical): Red with flame icon
 * P2 (High): Amber with arrow-up icon
 * P3 (Medium): Blue/Indigo with minus icon
 * P4 (Low): Green with arrow-down icon (Note: P4 added for UI, maps to P3 in backend)
 */
import { clsx } from 'clsx'
import { Flame, ArrowUp, Minus, ArrowDown } from 'lucide-react'
import type { Priority } from '@/types'

// Extended priority type for UI (P4 is UI-only, backend uses P1-P3)
export type DisplayPriority = Priority | 'P4'

interface PriorityBadgeProps {
  priority: DisplayPriority
  size?: 'sm' | 'md'
  showLabel?: boolean
  className?: string
}

const priorityConfig = {
  P1: {
    label: 'Critical',
    icon: Flame,
    bgClass: 'bg-red-500/15',
    textClass: 'text-red-500',
    borderClass: 'border-red-500/30',
  },
  P2: {
    label: 'High',
    icon: ArrowUp,
    bgClass: 'bg-amber-500/15',
    textClass: 'text-amber-500',
    borderClass: 'border-amber-500/30',
  },
  P3: {
    label: 'Medium',
    icon: Minus,
    bgClass: 'bg-indigo-500/15',
    textClass: 'text-indigo-500',
    borderClass: 'border-indigo-500/30',
  },
  P4: {
    label: 'Low',
    icon: ArrowDown,
    bgClass: 'bg-green-500/15',
    textClass: 'text-green-500',
    borderClass: 'border-green-500/30',
  },
}

export function PriorityBadge({
  priority,
  size = 'sm',
  showLabel = true,
  className,
}: PriorityBadgeProps) {
  const config = priorityConfig[priority]
  const Icon = config.icon

  const sizeStyles = {
    sm: 'px-2 py-0.5 text-xs gap-1',
    md: 'px-2.5 py-1 text-sm gap-1.5',
  }

  const iconSizes = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
  }

  return (
    <span
      className={clsx(
        'inline-flex items-center font-medium rounded-full border',
        config.bgClass,
        config.textClass,
        config.borderClass,
        sizeStyles[size],
        className
      )}
    >
      <Icon className={iconSizes[size]} />
      {showLabel && <span>{config.label}</span>}
    </span>
  )
}

// Helper to get priority color for borders
export function getPriorityBorderClass(priority: DisplayPriority): string {
  const borderClasses = {
    P1: 'border-l-red-500',
    P2: 'border-l-amber-500',
    P3: 'border-l-indigo-500',
    P4: 'border-l-green-500',
  }
  return borderClasses[priority]
}
