// [Task]: Phase 5 - New Component
/**
 * Tag chip component for displaying task tags.
 * Shows colored dot + tag name with optional remove button.
 */
import { clsx } from 'clsx'
import { X } from 'lucide-react'
import type { Tag } from '@/types'

interface TagChipProps {
  tag: Tag
  onRemove?: () => void
  size?: 'sm' | 'md'
  className?: string
}

export function TagChip({ tag, onRemove, size = 'sm', className }: TagChipProps) {
  const sizeStyles = {
    sm: 'px-2 py-0.5 text-xs gap-1.5',
    md: 'px-2.5 py-1 text-sm gap-2',
  }

  const dotSizes = {
    sm: 'w-2 h-2',
    md: 'w-2.5 h-2.5',
  }

  return (
    <span
      className={clsx(
        'inline-flex items-center font-medium rounded-full',
        'bg-white/10 border border-white/20',
        'text-gray-200',
        sizeStyles[size],
        className
      )}
    >
      {/* Colored dot */}
      <span
        className={clsx('rounded-full', dotSizes[size])}
        style={{ backgroundColor: tag.color }}
      />
      <span>{tag.name}</span>
      {onRemove && (
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation()
            onRemove()
          }}
          className="ml-0.5 p-0.5 rounded-full hover:bg-white/20 transition-colors"
          aria-label={`Remove ${tag.name} tag`}
        >
          <X className={size === 'sm' ? 'w-3 h-3' : 'w-3.5 h-3.5'} />
        </button>
      )}
    </span>
  )
}

// Tag color presets for creating new tags
export const tagColorPresets = [
  '#ef4444', // red
  '#f97316', // orange
  '#f59e0b', // amber
  '#eab308', // yellow
  '#84cc16', // lime
  '#22c55e', // green
  '#14b8a6', // teal
  '#06b6d4', // cyan
  '#3b82f6', // blue
  '#6366f1', // indigo
  '#8b5cf6', // violet
  '#a855f7', // purple
  '#d946ef', // fuchsia
  '#ec4899', // pink
  '#f43f5e', // rose
]
