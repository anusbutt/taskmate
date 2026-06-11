// [Task]: T104, T106, T107 [US6] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Task search component with debounced input and loading state.
 * Searches tasks by title or description via GET /api/tasks/search?q=query.
 */
'use client'

import { useState, useEffect, useCallback } from 'react'
import { Input } from '@/components/ui/input'
import { apiRequest, ApiError } from '@/lib/api-client'
import type { Task } from '@/types'

interface TaskSearchProps {
  onSearchResults: (tasks: Task[] | null) => void
  onSearchStateChange: (isSearching: boolean) => void
}

export function TaskSearch({ onSearchResults, onSearchStateChange }: TaskSearchProps) {
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Debounced search effect
  useEffect(() => {
    // If query is empty, clear search results
    if (query.trim() === '') {
      onSearchResults(null)
      onSearchStateChange(false)
      setError(null)
      return
    }

    // Debounce the search by 300ms
    const timeoutId = setTimeout(async () => {
      setIsLoading(true)
      setError(null)
      onSearchStateChange(true)

      try {
        // Call GET /api/tasks/search?q=query
        const tasks = await apiRequest<Task[]>(`/api/tasks/search?q=${encodeURIComponent(query)}`, {
          method: 'GET',
        })

        onSearchResults(tasks)
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message)
        } else {
          setError('Failed to search tasks. Please try again.')
        }
        onSearchResults([])
      } finally {
        setIsLoading(false)
      }
    }, 300)

    // Cleanup timeout on query change
    return () => clearTimeout(timeoutId)
  }, [query, onSearchResults, onSearchStateChange])

  const handleClearSearch = () => {
    setQuery('')
    setError(null)
    onSearchResults(null)
    onSearchStateChange(false)
  }

  return (
    <div className="space-y-2">
      <div className="relative">
        <Input
          type="text"
          placeholder="Search tasks by title or description..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          fullWidth
          className="pr-20"
        />
        {query && (
          <button
            onClick={handleClearSearch}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
            aria-label="Clear search"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        )}
      </div>

      {isLoading && (
        <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
          <svg
            className="animate-spin h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
          <span>Searching...</span>
        </div>
      )}

      {error && (
        <div className="text-sm text-red-500 dark:text-red-400">
          {error}
        </div>
      )}
    </div>
  )
}
