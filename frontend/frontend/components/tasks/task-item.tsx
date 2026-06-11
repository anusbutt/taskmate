// [Task]: T067, T085, T088, T096 [P] [US2, US4, US5] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign with priority and tags
/**
 * Task item component displaying a single task with glassmorphism styling.
 * Shows priority badge, tag chips, checkbox, title, description, and action buttons.
 */
'use client'

import { useState } from 'react'
import { clsx } from 'clsx'
import { Pencil, Trash2, ChevronDown, ChevronUp, Repeat, Calendar } from 'lucide-react'
import { Checkbox } from '@/components/ui/checkbox'
import { Button } from '@/components/ui/button'
import { PriorityBadge, getPriorityBorderClass } from '@/components/ui/priority-badge'
import { TagChip } from '@/components/ui/tag-chip'
import type { Task } from '@/types'

interface TaskItemProps {
  task: Task
  onToggleComplete?: (taskId: number, completed: boolean) => Promise<void>
  onEdit?: (task: Task) => void
  onDelete?: (task: Task) => void
}

export function TaskItem({ task, onToggleComplete, onEdit, onDelete }: TaskItemProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  const shouldTruncate = task.description && task.description.length > 100
  const displayDescription =
    task.description && shouldTruncate && !isExpanded
      ? `${task.description.substring(0, 100)}...`
      : task.description

  const handleCheckboxChange = async (checked: boolean) => {
    if (onToggleComplete) {
      await onToggleComplete(task.id, checked)
    }
  }

  // Priority border color
  const priorityBorderClass = getPriorityBorderClass(task.priority)

  return (
    <div
      className={clsx(
        'glass-card p-4 border-l-4 transition-all duration-200',
        'hover-lift hover-glow',
        priorityBorderClass,
        task.completed && 'opacity-60'
      )}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <div className="flex-shrink-0 pt-1">
          <Checkbox
            checked={task.completed}
            onChange={(e) => handleCheckboxChange(e.target.checked)}
            id={`task-${task.id}`}
          />
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Header: Priority badge + Recurrence badge + Title */}
          <div className="flex items-center gap-2 flex-wrap">
            <PriorityBadge priority={task.priority} size="sm" />
            {task.recurrence_pattern && (
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-700 dark:bg-indigo-900/40 dark:text-indigo-300">
                <Repeat className="w-3 h-3" />
                {task.recurrence_pattern.charAt(0).toUpperCase() + task.recurrence_pattern.slice(1)}
              </span>
            )}
            <h3
              className={clsx(
                'text-lg font-medium text-gray-900 dark:text-white',
                task.completed && 'line-through text-gray-500 dark:text-gray-400'
              )}
            >
              {task.title}
            </h3>
          </div>

          {/* Tags */}
          {task.tags && task.tags.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mt-2">
              {task.tags.map((tag) => (
                <TagChip key={tag.id} tag={tag} size="sm" />
              ))}
            </div>
          )}

          {/* Description */}
          {task.description && (
            <div className="mt-2">
              <p className="text-sm text-gray-600 dark:text-gray-300 whitespace-pre-wrap">
                {displayDescription}
              </p>
              {shouldTruncate && (
                <button
                  onClick={() => setIsExpanded(!isExpanded)}
                  className="mt-1 flex items-center gap-1 text-xs text-indigo-400 hover:text-indigo-300 font-medium transition-colors"
                >
                  {isExpanded ? (
                    <>
                      <ChevronUp className="w-3 h-3" />
                      Show less
                    </>
                  ) : (
                    <>
                      <ChevronDown className="w-3 h-3" />
                      Read more
                    </>
                  )}
                </button>
              )}
            </div>
          )}

          {/* Meta info */}
          <div className="mt-3 flex items-center gap-3 text-xs text-gray-500 dark:text-gray-500">
            <span>Created: {formatDate(task.created_at)}</span>
            {task.due_date && (
              <>
                <span className="text-gray-400 dark:text-gray-600">•</span>
                <span className="inline-flex items-center gap-1">
                  <Calendar className="w-3 h-3" />
                  Due: {formatDate(task.due_date)}
                </span>
              </>
            )}
            <span className="text-gray-400 dark:text-gray-600">•</span>
            <span>#{task.id}</span>
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex-shrink-0 flex flex-col sm:flex-row gap-2">
          {onEdit && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onEdit(task)}
              className="min-h-[44px] min-w-[44px] sm:min-h-[36px] sm:min-w-[auto] p-2"
              aria-label="Edit task"
            >
              <Pencil className="w-4 h-4" />
              <span className="hidden sm:inline ml-1">Edit</span>
            </Button>
          )}
          {onDelete && (
            <Button
              variant="danger"
              size="sm"
              onClick={() => onDelete(task)}
              className="min-h-[44px] min-w-[44px] sm:min-h-[36px] sm:min-w-[auto] p-2"
              aria-label="Delete task"
            >
              <Trash2 className="w-4 h-4" />
              <span className="hidden sm:inline ml-1">Delete</span>
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
