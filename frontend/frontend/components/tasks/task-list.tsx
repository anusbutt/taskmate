// [Task]: T068 [P] [US2] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign with animations
/**
 * Task list component displaying tasks with staggered animations.
 * Shows empty state when no tasks exist.
 */
'use client'

import { clsx } from 'clsx'
import { ClipboardList } from 'lucide-react'
import { TaskItem } from './task-item'
import type { Task } from '@/types'

interface TaskListProps {
  tasks: Task[]
  onToggleComplete?: (taskId: number, completed: boolean) => Promise<void>
  onEdit?: (task: Task) => void
  onDelete?: (task: Task) => void
  isFiltered?: boolean  // True if filters are active
}

export function TaskList({
  tasks,
  onToggleComplete,
  onEdit,
  onDelete,
  isFiltered = false,
}: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="glass-card p-12 text-center">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-indigo-500/20 flex items-center justify-center">
          <ClipboardList className="w-8 h-8 text-indigo-400" />
        </div>
        <h3 className="text-xl font-semibold text-white mb-2">
          {isFiltered ? 'No matching tasks' : 'No tasks yet'}
        </h3>
        <p className="text-gray-400 max-w-md mx-auto">
          {isFiltered
            ? 'Try adjusting your filters or search query to find what you\'re looking for.'
            : 'Create your first task to get started. Use the "Add Task" button above.'}
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {tasks.map((task, index) => (
        <div
          key={task.id}
          className={clsx(
            'animate-fade-in opacity-0',
            // Staggered animation delays
            index === 0 && 'stagger-1',
            index === 1 && 'stagger-2',
            index === 2 && 'stagger-3',
            index === 3 && 'stagger-4',
            index >= 4 && 'stagger-5'
          )}
          style={{
            animationFillMode: 'forwards',
            animationDelay: index >= 5 ? `${0.25 + (index - 4) * 0.05}s` : undefined,
          }}
        >
          <TaskItem
            task={task}
            onToggleComplete={onToggleComplete}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        </div>
      ))}
    </div>
  )
}
