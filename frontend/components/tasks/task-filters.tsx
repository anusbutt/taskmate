// [Task]: Phase 5 - New Component
/**
 * Combined filter bar for tasks.
 * Includes priority filter, tag multi-select, status toggle, sort dropdown, and search.
 */
'use client'

import { useState, useRef, useEffect } from 'react'
import { clsx } from 'clsx'
import {
  Search,
  Filter,
  SortAsc,
  SortDesc,
  ChevronDown,
  X,
  Check,
} from 'lucide-react'
import { PriorityBadge } from '@/components/ui/priority-badge'
import { TagChip } from '@/components/ui/tag-chip'
import type { Priority, Tag } from '@/types'

export type StatusFilter = 'all' | 'active' | 'completed'
export type SortField = 'created_at' | 'priority' | 'title'
export type SortDirection = 'asc' | 'desc'

export interface FilterState {
  search: string
  priority: Priority | 'all'
  tags: number[]
  status: StatusFilter
}

export interface SortState {
  field: SortField
  direction: SortDirection
}

interface TaskFiltersProps {
  filters: FilterState
  sort: SortState
  availableTags: Tag[]
  onFiltersChange: (filters: FilterState) => void
  onSortChange: (sort: SortState) => void
}

export function TaskFilters({
  filters,
  sort,
  availableTags,
  onFiltersChange,
  onSortChange,
}: TaskFiltersProps) {
  const [isPriorityOpen, setIsPriorityOpen] = useState(false)
  const [isTagsOpen, setIsTagsOpen] = useState(false)
  const [isSortOpen, setIsSortOpen] = useState(false)

  const priorityRef = useRef<HTMLDivElement>(null)
  const tagsRef = useRef<HTMLDivElement>(null)
  const sortRef = useRef<HTMLDivElement>(null)

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (priorityRef.current && !priorityRef.current.contains(event.target as Node)) {
        setIsPriorityOpen(false)
      }
      if (tagsRef.current && !tagsRef.current.contains(event.target as Node)) {
        setIsTagsOpen(false)
      }
      if (sortRef.current && !sortRef.current.contains(event.target as Node)) {
        setIsSortOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const priorityOptions: { value: Priority | 'all'; label: string }[] = [
    { value: 'all', label: 'All Priorities' },
    { value: 'P1', label: 'Critical' },
    { value: 'P2', label: 'High' },
    { value: 'P3', label: 'Medium' },
  ]

  const sortOptions: { field: SortField; label: string }[] = [
    { field: 'created_at', label: 'Date Created' },
    { field: 'priority', label: 'Priority' },
    { field: 'title', label: 'Title' },
  ]

  const handleSearchChange = (value: string) => {
    onFiltersChange({ ...filters, search: value })
  }

  const handlePriorityChange = (priority: Priority | 'all') => {
    onFiltersChange({ ...filters, priority })
    setIsPriorityOpen(false)
  }

  const handleTagToggle = (tagId: number) => {
    const newTags = filters.tags.includes(tagId)
      ? filters.tags.filter((id) => id !== tagId)
      : [...filters.tags, tagId]
    onFiltersChange({ ...filters, tags: newTags })
  }

  const handleStatusChange = (status: StatusFilter) => {
    onFiltersChange({ ...filters, status })
  }

  const handleSortChange = (field: SortField) => {
    if (sort.field === field) {
      // Toggle direction
      onSortChange({ field, direction: sort.direction === 'asc' ? 'desc' : 'asc' })
    } else {
      // New field, default to desc for date, asc for others
      onSortChange({ field, direction: field === 'created_at' ? 'desc' : 'asc' })
    }
    setIsSortOpen(false)
  }

  const clearFilters = () => {
    onFiltersChange({
      search: '',
      priority: 'all',
      tags: [],
      status: 'all',
    })
  }

  const hasActiveFilters =
    filters.search ||
    filters.priority !== 'all' ||
    filters.tags.length > 0 ||
    filters.status !== 'all'

  return (
    <div className="space-y-3">
      {/* Search bar */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          placeholder="Search tasks..."
          value={filters.search}
          onChange={(e) => handleSearchChange(e.target.value)}
          className={clsx(
            'w-full pl-10 pr-4 py-2.5 rounded-xl',
            'glass-input text-gray-900 dark:text-white placeholder:text-gray-500 dark:placeholder:text-gray-400'
          )}
        />
        {filters.search && (
          <button
            onClick={() => handleSearchChange('')}
            className="absolute right-3 top-1/2 -translate-y-1/2 p-1 rounded-full hover:bg-white/10 transition-colors"
          >
            <X className="w-4 h-4 text-gray-400" />
          </button>
        )}
      </div>

      {/* Filter row */}
      <div className="flex flex-wrap items-center gap-2">
        <Filter className="w-4 h-4 text-gray-400" />

        {/* Status toggle */}
        <div className="flex rounded-lg overflow-hidden border border-gray-200 dark:border-white/10">
          {(['all', 'active', 'completed'] as StatusFilter[]).map((status) => (
            <button
              key={status}
              onClick={() => handleStatusChange(status)}
              className={clsx(
                'px-3 py-1.5 text-xs font-medium transition-colors',
                filters.status === status
                  ? 'bg-indigo-500 text-white'
                  : 'bg-gray-100 dark:bg-white/5 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-white/10'
              )}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </button>
          ))}
        </div>

        {/* Priority dropdown */}
        <div ref={priorityRef} className="relative">
          <button
            onClick={() => setIsPriorityOpen(!isPriorityOpen)}
            className={clsx(
              'flex items-center gap-2 px-3 py-1.5 rounded-lg',
              'bg-gray-100 dark:bg-white/5 border border-gray-200 dark:border-white/10',
              'text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-white/10 transition-colors'
            )}
          >
            {filters.priority === 'all' ? (
              <span>Priority</span>
            ) : (
              <PriorityBadge priority={filters.priority} size="sm" showLabel={false} />
            )}
            <ChevronDown className={clsx('w-4 h-4 transition-transform', isPriorityOpen && 'rotate-180')} />
          </button>

          {isPriorityOpen && (
            <div className="absolute z-50 top-full left-0 mt-1 glass-card py-1 min-w-[140px] animate-scale-in origin-top">
              {priorityOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => handlePriorityChange(option.value)}
                  className={clsx(
                    'w-full flex items-center gap-2 px-3 py-2 text-sm',
                    'text-left transition-colors',
                    filters.priority === option.value
                      ? 'bg-indigo-500/20'
                      : 'hover:bg-gray-100 dark:hover:bg-white/10'
                  )}
                >
                  {option.value === 'all' ? (
                    <span className="text-gray-700 dark:text-gray-300">{option.label}</span>
                  ) : (
                    <PriorityBadge priority={option.value} size="sm" />
                  )}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Tags dropdown */}
        {availableTags.length > 0 && (
          <div ref={tagsRef} className="relative">
            <button
              onClick={() => setIsTagsOpen(!isTagsOpen)}
              className={clsx(
                'flex items-center gap-2 px-3 py-1.5 rounded-lg',
                'bg-gray-100 dark:bg-white/5 border border-gray-200 dark:border-white/10',
                'text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-white/10 transition-colors'
              )}
            >
              <span>Tags {filters.tags.length > 0 && `(${filters.tags.length})`}</span>
              <ChevronDown className={clsx('w-4 h-4 transition-transform', isTagsOpen && 'rotate-180')} />
            </button>

            {isTagsOpen && (
              <div className="absolute z-50 top-full left-0 mt-1 glass-card py-1 min-w-[180px] max-h-[200px] overflow-y-auto animate-scale-in origin-top scrollbar-thin">
                {availableTags.map((tag) => (
                  <button
                    key={tag.id}
                    onClick={() => handleTagToggle(tag.id)}
                    className={clsx(
                      'w-full flex items-center gap-2 px-3 py-2 text-sm',
                      'text-left transition-colors hover:bg-gray-100 dark:hover:bg-white/10'
                    )}
                  >
                    <span
                      className={clsx(
                        'w-4 h-4 rounded border flex items-center justify-center',
                        filters.tags.includes(tag.id)
                          ? 'bg-indigo-500 border-indigo-500'
                          : 'border-gray-500'
                      )}
                    >
                      {filters.tags.includes(tag.id) && <Check className="w-3 h-3 text-white" />}
                    </span>
                    <TagChip tag={tag} size="sm" />
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Sort dropdown */}
        <div ref={sortRef} className="relative ml-auto">
          <button
            onClick={() => setIsSortOpen(!isSortOpen)}
            className={clsx(
              'flex items-center gap-2 px-3 py-1.5 rounded-lg',
              'bg-gray-100 dark:bg-white/5 border border-gray-200 dark:border-white/10',
              'text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-white/10 transition-colors'
            )}
          >
            {sort.direction === 'asc' ? (
              <SortAsc className="w-4 h-4" />
            ) : (
              <SortDesc className="w-4 h-4" />
            )}
            <span>Sort</span>
            <ChevronDown className={clsx('w-4 h-4 transition-transform', isSortOpen && 'rotate-180')} />
          </button>

          {isSortOpen && (
            <div className="absolute z-50 top-full right-0 mt-1 glass-card py-1 min-w-[150px] animate-scale-in origin-top-right">
              {sortOptions.map((option) => (
                <button
                  key={option.field}
                  onClick={() => handleSortChange(option.field)}
                  className={clsx(
                    'w-full flex items-center justify-between gap-2 px-3 py-2 text-sm',
                    'text-left transition-colors',
                    sort.field === option.field
                      ? 'bg-indigo-500/20'
                      : 'hover:bg-gray-100 dark:hover:bg-white/10'
                  )}
                >
                  <span className="text-gray-700 dark:text-gray-300">{option.label}</span>
                  {sort.field === option.field && (
                    sort.direction === 'asc' ? (
                      <SortAsc className="w-4 h-4 text-indigo-400" />
                    ) : (
                      <SortDesc className="w-4 h-4 text-indigo-400" />
                    )
                  )}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Clear filters */}
        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="flex items-center gap-1 px-2 py-1.5 text-xs text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-3 h-3" />
            Clear
          </button>
        )}
      </div>

      {/* Active tag chips */}
      {filters.tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {filters.tags.map((tagId) => {
            const tag = availableTags.find((t) => t.id === tagId)
            if (!tag) return null
            return (
              <TagChip
                key={tag.id}
                tag={tag}
                size="sm"
                onRemove={() => handleTagToggle(tag.id)}
              />
            )
          })}
        </div>
      )}
    </div>
  )
}
