// [Task]: T066, T086 [P] [US2, US4] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign with priority and tags
/**
 * Task form component for creating/editing tasks.
 * Includes priority selection and tag multi-select.
 */
'use client'

import { useState, useEffect } from 'react'
import { useForm, Controller } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { clsx } from 'clsx'
import { Check, Repeat } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { PrioritySelect } from '@/components/ui/priority-select'
import { TagChip } from '@/components/ui/tag-chip'
import type { Task, Tag, Priority } from '@/types'

// Zod schema matching backend validation
const taskFormSchema = z.object({
  title: z
    .string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters')
    .refine((val) => val.trim().length > 0, 'Title cannot be only whitespace'),
  description: z
    .string()
    .max(1000, 'Description must be less than 1000 characters')
    .optional()
    .default(''),
  priority: z.enum(['P1', 'P2', 'P3']).default('P2'),
  tag_ids: z.array(z.number()).optional().default([]),
  recurrence_pattern: z.enum(['daily', 'weekly', 'monthly']).nullable().optional().default(null),
})

type TaskFormData = z.infer<typeof taskFormSchema>

interface TaskFormProps {
  task?: Task  // If provided, form is in edit mode
  availableTags?: Tag[]  // List of available tags
  onSubmit: (data: TaskFormData) => Promise<void>
  onCancel: () => void
  isSubmitting?: boolean
}

export function TaskForm({
  task,
  availableTags = [],
  onSubmit,
  onCancel,
  isSubmitting = false,
}: TaskFormProps) {
  const [apiError, setApiError] = useState<string | null>(null)
  const isEditMode = !!task

  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
    reset,
    watch,
    setValue,
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskFormSchema),
    defaultValues: {
      title: task?.title || '',
      description: task?.description || '',
      priority: task?.priority || 'P2',
      tag_ids: task?.tags?.map((t) => t.id) || [],
      recurrence_pattern: task?.recurrence_pattern || null,
    },
  })

  const selectedTagIds = watch('tag_ids') || []

  // Update form when task prop changes
  useEffect(() => {
    if (task) {
      reset({
        title: task.title,
        description: task.description || '',
        priority: task.priority,
        tag_ids: task.tags?.map((t) => t.id) || [],
        recurrence_pattern: task.recurrence_pattern || null,
      })
    }
  }, [task, reset])

  const handleFormSubmit = async (data: TaskFormData) => {
    setApiError(null)

    try {
      await onSubmit(data)
      if (!isEditMode) {
        reset() // Clear form on success (only for create mode)
      }
    } catch (error) {
      if (error instanceof Error) {
        setApiError(error.message)
      } else {
        setApiError(isEditMode ? 'Failed to update task. Please try again.' : 'Failed to create task. Please try again.')
      }
    }
  }

  const toggleTag = (tagId: number) => {
    const current = selectedTagIds
    if (current.includes(tagId)) {
      setValue('tag_ids', current.filter((id) => id !== tagId))
    } else {
      setValue('tag_ids', [...current, tagId])
    }
  }

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-5">
      {/* Title */}
      <Input
        label="Title"
        type="text"
        placeholder="Enter task title"
        error={errors.title?.message}
        {...register('title')}
        fullWidth
        autoFocus
      />

      {/* Description */}
      <div className="space-y-1.5">
        <label
          htmlFor="description"
          className="block text-sm font-medium text-gray-700 dark:text-gray-300"
        >
          Description (optional)
        </label>
        <textarea
          id="description"
          placeholder="Enter task description"
          className={clsx(
            'w-full px-4 py-2.5 rounded-xl resize-vertical min-h-[100px]',
            'glass-input text-gray-900 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-400',
            'focus:outline-none'
          )}
          {...register('description')}
        />
        {errors.description && (
          <span className="text-sm text-red-400">
            {errors.description.message}
          </span>
        )}
      </div>

      {/* Priority */}
      <div className="space-y-1.5">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Priority
        </label>
        <Controller
          name="priority"
          control={control}
          render={({ field }) => (
            <PrioritySelect
              value={field.value}
              onChange={field.onChange}
              className="w-full sm:w-48"
            />
          )}
        />
      </div>

      {/* Recurrence */}
      <div className="space-y-1.5">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Repeat
        </label>
        <Controller
          name="recurrence_pattern"
          control={control}
          render={({ field }) => (
            <div className="flex flex-wrap gap-2">
              {[
                { value: null, label: 'None' },
                { value: 'daily' as const, label: 'Daily' },
                { value: 'weekly' as const, label: 'Weekly' },
                { value: 'monthly' as const, label: 'Monthly' },
              ].map((option) => (
                <button
                  key={option.label}
                  type="button"
                  onClick={() => field.onChange(option.value)}
                  className={clsx(
                    'flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm',
                    'border transition-all duration-200',
                    field.value === option.value
                      ? 'bg-indigo-500/20 border-indigo-500/50 text-gray-900 dark:text-white'
                      : 'bg-gray-100 dark:bg-white/5 border-gray-200 dark:border-white/10 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-white/10'
                  )}
                >
                  {option.value && <Repeat className="w-3.5 h-3.5" />}
                  {option.label}
                </button>
              ))}
            </div>
          )}
        />
      </div>

      {/* Tags */}
      {availableTags.length > 0 && (
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Tags (optional)
          </label>
          <div className="flex flex-wrap gap-2">
            {availableTags.map((tag) => {
              const isSelected = selectedTagIds.includes(tag.id)
              return (
                <button
                  key={tag.id}
                  type="button"
                  onClick={() => toggleTag(tag.id)}
                  className={clsx(
                    'flex items-center gap-1.5 px-2.5 py-1 rounded-full text-sm',
                    'border transition-all duration-200',
                    isSelected
                      ? 'bg-indigo-500/20 border-indigo-500/50 text-gray-900 dark:text-white'
                      : 'bg-gray-100 dark:bg-white/5 border-gray-200 dark:border-white/10 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-white/10'
                  )}
                >
                  <span
                    className="w-2.5 h-2.5 rounded-full"
                    style={{ backgroundColor: tag.color }}
                  />
                  <span>{tag.name}</span>
                  {isSelected && <Check className="w-3.5 h-3.5 text-indigo-400" />}
                </button>
              )
            })}
          </div>
          {/* Selected tags display */}
          {selectedTagIds.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mt-2 pt-2 border-t border-gray-200 dark:border-white/10">
              <span className="text-xs text-gray-500 dark:text-gray-400 mr-1">Selected:</span>
              {selectedTagIds.map((tagId) => {
                const tag = availableTags.find((t) => t.id === tagId)
                if (!tag) return null
                return (
                  <TagChip
                    key={tag.id}
                    tag={tag}
                    size="sm"
                    onRemove={() => toggleTag(tag.id)}
                  />
                )
              })}
            </div>
          )}
        </div>
      )}

      {/* API Error */}
      {apiError && (
        <div className="p-3 rounded-lg bg-red-500/20 border border-red-500/30">
          <p className="text-sm text-red-400">{apiError}</p>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-3 justify-end pt-2">
        <Button
          type="button"
          variant="ghost"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button type="submit" variant="primary" disabled={isSubmitting}>
          {isSubmitting
            ? (isEditMode ? 'Saving...' : 'Creating...')
            : (isEditMode ? 'Save Changes' : 'Create Task')}
        </Button>
      </div>
    </form>
  )
}
