// [Task]: T078, T108 [US3, US6] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign with priority breakdown
/**
 * Task statistics component with glassmorphism styling.
 * Shows total tasks, completion rate, and priority breakdown.
 */
'use client'

import { clsx } from 'clsx'
import {
  CheckCircle2,
  Circle,
  TrendingUp,
  Flame,
  ArrowUp,
  Minus,
} from 'lucide-react'
import type { Priority } from '@/types'

interface TaskStatsProps {
  stats: {
    total: number
    completed: number
    incomplete: number
    completion_percentage: number
    by_priority?: Record<Priority, number>
  }
}

export function TaskStats({ stats }: TaskStatsProps) {
  const { total, completed, incomplete, completion_percentage, by_priority } = stats

  // Show context-aware message when no tasks exist
  if (total === 0) {
    return (
      <div className="glass-card p-6">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-full gradient-primary flex items-center justify-center">
            <Circle className="w-6 h-6 text-white" />
          </div>
          <div>
            <p className="text-lg font-semibold text-white">
              No tasks yet
            </p>
            <p className="text-sm text-gray-400">
              Get started by adding your first task!
            </p>
          </div>
        </div>
      </div>
    )
  }

  const statItems = [
    {
      label: 'Total',
      value: total,
      icon: Circle,
      color: 'text-gray-300',
      bgColor: 'bg-white/10',
    },
    {
      label: 'Completed',
      value: completed,
      icon: CheckCircle2,
      color: 'text-green-400',
      bgColor: 'bg-green-500/20',
    },
    {
      label: 'Pending',
      value: incomplete,
      icon: Circle,
      color: 'text-amber-400',
      bgColor: 'bg-amber-500/20',
    },
  ]

  const priorityItems = by_priority
    ? [
        {
          priority: 'P1' as Priority,
          label: 'Critical',
          count: by_priority.P1 || 0,
          icon: Flame,
          color: 'text-red-400',
          bgColor: 'bg-red-500/20',
        },
        {
          priority: 'P2' as Priority,
          label: 'High',
          count: by_priority.P2 || 0,
          icon: ArrowUp,
          color: 'text-amber-400',
          bgColor: 'bg-amber-500/20',
        },
        {
          priority: 'P3' as Priority,
          label: 'Medium',
          count: by_priority.P3 || 0,
          icon: Minus,
          color: 'text-indigo-400',
          bgColor: 'bg-indigo-500/20',
        },
      ]
    : []

  return (
    <div className="glass-card gradient-border p-6 space-y-6">
      {/* Main stats row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {statItems.map((item) => (
          <div key={item.label} className="flex items-center gap-3">
            <div className={clsx('p-2 rounded-lg', item.bgColor)}>
              <item.icon className={clsx('w-5 h-5', item.color)} />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{item.value}</p>
              <p className="text-xs text-gray-400">{item.label}</p>
            </div>
          </div>
        ))}

        {/* Completion rate */}
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-indigo-500/20">
            <TrendingUp className="w-5 h-5 text-indigo-400" />
          </div>
          <div>
            <p className="text-2xl font-bold text-white">{completion_percentage}%</p>
            <p className="text-xs text-gray-400">Complete</p>
          </div>
        </div>
      </div>

      {/* Progress bar */}
      <div className="space-y-2">
        <div className="flex justify-between text-xs text-gray-400">
          <span>Progress</span>
          <span>{completed} of {total} tasks</span>
        </div>
        <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
          <div
            className="h-full gradient-primary rounded-full transition-all duration-500 ease-out"
            style={{ width: `${completion_percentage}%` }}
          />
        </div>
      </div>

      {/* Priority breakdown */}
      {priorityItems.length > 0 && (
        <div className="pt-4 border-t border-white/10">
          <p className="text-xs text-gray-400 mb-3">By Priority</p>
          <div className="flex flex-wrap gap-3">
            {priorityItems.map((item) => (
              <div
                key={item.priority}
                className={clsx(
                  'flex items-center gap-2 px-3 py-1.5 rounded-lg',
                  item.bgColor
                )}
              >
                <item.icon className={clsx('w-4 h-4', item.color)} />
                <span className="text-sm text-gray-200">{item.label}</span>
                <span className={clsx('font-semibold', item.color)}>
                  {item.count}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
