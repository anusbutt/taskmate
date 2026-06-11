// [Task]: T069-T071, T076, T079-T080, T087, T090-T091, T100, T105, T106 [US2, US3, US4, US6, US7, US8] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: T026, T027, T028, T042-T045 [US6, US1] | [Spec]: specs/003-phase-03-ai-chatbot/spec.md
// [Task]: Phase 5 - Glassmorphism + Filters/Sort/Tags + URL Persistence
/**
 * Tasks page - main task management interface with glassmorphism styling.
 * Features: task list, filters (priority, tags, status), sort, search, stats, AI chat.
 * URL persistence for filters and sort state.
 */
'use client'

import { useState, useEffect, useMemo, useCallback } from 'react'
import { useSearchParams, useRouter, usePathname } from 'next/navigation'
import { Plus, Loader2 } from 'lucide-react'
import { TaskList } from '@/components/tasks/task-list'
import { TaskForm } from '@/components/tasks/task-form'
import { TaskStats } from '@/components/tasks/task-stats'
import { TaskFilters, type FilterState, type SortState } from '@/components/tasks/task-filters'
import { Modal } from '@/components/ui/modal'
import { ConfirmDialog } from '@/components/ui/confirm-dialog'
import { Button } from '@/components/ui/button'
import { ChatSidebar, ChatToggle, type Message } from '@/components/chat'
import { apiRequest, ApiError } from '@/lib/api-client'
import { sendChatMessage } from '@/services/chat'
import type { Task, Tag, Priority } from '@/types'

interface TaskStatistics {
  total: number
  completed: number
  incomplete: number
  completion_percentage: number
  by_priority?: Record<Priority, number>
}

// Priority sort order (lower = higher priority)
const priorityOrder: Record<Priority, number> = {
  P1: 1,
  P2: 2,
  P3: 3,
}

export default function TasksPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const pathname = usePathname()

  // Task data
  const [tasks, setTasks] = useState<Task[]>([])
  const [availableTags, setAvailableTags] = useState<Tag[]>([])
  const [stats, setStats] = useState<TaskStatistics | null>(null)

  // Initialize filter state from URL params
  const getInitialFilters = useCallback((): FilterState => {
    const search = searchParams.get('search') || ''
    const priority = (searchParams.get('priority') as Priority | 'all') || 'all'
    const tagsParam = searchParams.get('tags')
    const tags = tagsParam ? tagsParam.split(',').map(Number).filter(Boolean) : []
    const status = (searchParams.get('status') as 'all' | 'active' | 'completed') || 'all'
    return { search, priority, tags, status }
  }, [searchParams])

  // Initialize sort state from URL params
  const getInitialSort = useCallback((): SortState => {
    const field = (searchParams.get('sortBy') as 'created_at' | 'priority' | 'title') || 'created_at'
    const direction = (searchParams.get('sortDir') as 'asc' | 'desc') || 'desc'
    return { field, direction }
  }, [searchParams])

  // Filter and sort state (initialized from URL)
  const [filters, setFilters] = useState<FilterState>(getInitialFilters)
  const [sort, setSort] = useState<SortState>(getInitialSort)

  // Sync URL when filters/sort change
  const updateURL = useCallback((newFilters: FilterState, newSort: SortState) => {
    const params = new URLSearchParams()

    // Add filter params (only if not default)
    if (newFilters.search) params.set('search', newFilters.search)
    if (newFilters.priority !== 'all') params.set('priority', newFilters.priority)
    if (newFilters.tags.length > 0) params.set('tags', newFilters.tags.join(','))
    if (newFilters.status !== 'all') params.set('status', newFilters.status)

    // Add sort params (only if not default)
    if (newSort.field !== 'created_at') params.set('sortBy', newSort.field)
    if (newSort.direction !== 'desc') params.set('sortDir', newSort.direction)

    const queryString = params.toString()
    const newURL = queryString ? `${pathname}?${queryString}` : pathname
    router.replace(newURL, { scroll: false })
  }, [pathname, router])

  // Handle filter changes with URL sync
  const handleFiltersChange = useCallback((newFilters: FilterState) => {
    setFilters(newFilters)
    updateURL(newFilters, sort)
  }, [sort, updateURL])

  // Handle sort changes with URL sync
  const handleSortChange = useCallback((newSort: SortState) => {
    setSort(newSort)
    updateURL(filters, newSort)
  }, [filters, updateURL])

  // Loading states
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Modal states
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [deletingTask, setDeletingTask] = useState<Task | null>(null)
  const [isDeleting, setIsDeleting] = useState(false)

  // Chat sidebar state
  const [isChatOpen, setIsChatOpen] = useState(false)
  const [chatMessages, setChatMessages] = useState<Message[]>([])
  const [isChatLoading, setIsChatLoading] = useState(false)
  const [chatInputValue, setChatInputValue] = useState('')
  const [conversationId, setConversationId] = useState<string | undefined>(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('chat_conversation_id') || undefined
    }
    return undefined
  })

  // Fetch data on mount
  useEffect(() => {
    fetchTasks()
    fetchStats()
    fetchTags()
  }, [])

  const fetchTasks = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const data = await apiRequest<Task[]>('/api/tasks', { method: 'GET' })
      setTasks(data)
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message)
      } else {
        setError('Failed to load tasks. Please try again.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const data = await apiRequest<TaskStatistics>('/api/tasks/stats', { method: 'GET' })
      setStats(data)
    } catch (err) {
      console.error('Failed to fetch stats:', err)
    }
  }

  const fetchTags = async () => {
    try {
      const data = await apiRequest<Tag[]>('/api/tags', { method: 'GET' })
      setAvailableTags(data)
    } catch (err) {
      console.error('Failed to fetch tags:', err)
    }
  }

  // Client-side filtering and sorting
  const filteredAndSortedTasks = useMemo(() => {
    let result = [...tasks]

    // Filter by search
    if (filters.search) {
      const searchLower = filters.search.toLowerCase()
      result = result.filter(
        (task) =>
          task.title.toLowerCase().includes(searchLower) ||
          (task.description && task.description.toLowerCase().includes(searchLower))
      )
    }

    // Filter by priority
    if (filters.priority !== 'all') {
      result = result.filter((task) => task.priority === filters.priority)
    }

    // Filter by tags (intersection - task must have ALL selected tags)
    if (filters.tags.length > 0) {
      result = result.filter((task) => {
        const taskTagIds = task.tags?.map((t) => t.id) || []
        return filters.tags.every((tagId) => taskTagIds.includes(tagId))
      })
    }

    // Filter by status
    if (filters.status === 'active') {
      result = result.filter((task) => !task.completed)
    } else if (filters.status === 'completed') {
      result = result.filter((task) => task.completed)
    }

    // Sort
    result.sort((a, b) => {
      let comparison = 0

      switch (sort.field) {
        case 'created_at':
          comparison = new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
          break
        case 'priority':
          comparison = priorityOrder[a.priority] - priorityOrder[b.priority]
          break
        case 'title':
          comparison = a.title.localeCompare(b.title)
          break
      }

      return sort.direction === 'asc' ? comparison : -comparison
    })

    return result
  }, [tasks, filters, sort])

  const hasActiveFilters =
    !!filters.search ||
    filters.priority !== 'all' ||
    filters.tags.length > 0 ||
    filters.status !== 'all'

  // Task CRUD handlers
  const handleCreateTask = async (data: { title: string; description?: string; priority?: Priority; tag_ids?: number[]; recurrence_pattern?: string | null }) => {
    setIsSubmitting(true)

    try {
      const newTask = await apiRequest<Task>('/api/tasks', {
        method: 'POST',
        body: JSON.stringify(data),
      })

      setTasks([newTask, ...tasks])
      setIsModalOpen(false)
      await fetchStats()
    } catch (err) {
      if (err instanceof ApiError) {
        throw new Error(err.message)
      } else {
        throw new Error('Failed to create task. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEditTask = async (data: { title: string; description?: string; priority?: Priority; tag_ids?: number[]; recurrence_pattern?: string | null }) => {
    if (!editingTask) return

    setIsSubmitting(true)

    try {
      const updatedTask = await apiRequest<Task>(`/api/tasks/${editingTask.id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      })

      setTasks((prevTasks) =>
        prevTasks.map((task) => (task.id === updatedTask.id ? updatedTask : task))
      )
      setEditingTask(null)
      setIsModalOpen(false)
      await fetchStats()
    } catch (err) {
      if (err instanceof ApiError) {
        throw new Error(err.message)
      } else {
        throw new Error('Failed to update task. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleOpenEdit = (task: Task) => {
    setEditingTask(task)
    setIsModalOpen(true)
  }

  const handleOpenDelete = (task: Task) => {
    setDeletingTask(task)
  }

  const handleConfirmDelete = async () => {
    if (!deletingTask) return

    setIsDeleting(true)

    try {
      await apiRequest(`/api/tasks/${deletingTask.id}`, { method: 'DELETE' })

      setTasks((prevTasks) => prevTasks.filter((task) => task.id !== deletingTask.id))
      setDeletingTask(null)
      await fetchStats()
    } catch (err) {
      console.error('Failed to delete task:', err)
    } finally {
      setIsDeleting(false)
    }
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setEditingTask(null)
  }

  const handleToggleComplete = async (taskId: number, completed: boolean) => {
    // Optimistic update
    const previousTasks = tasks
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === taskId ? { ...task, completed } : task
      )
    )

    try {
      await apiRequest<Task>(`/api/tasks/${taskId}/status`, { method: 'PATCH' })
      // Refetch all tasks to pick up auto-created recurring task instances
      await fetchTasks()
      await fetchStats()
    } catch (err) {
      setTasks(previousTasks)
      console.error('Failed to toggle task status:', err)
    }
  }

  // Chat handler
  const handleSendChatMessage = async (message: string) => {
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: message,
      timestamp: new Date(),
    }
    setChatMessages((prev) => [...prev, userMessage])
    setIsChatLoading(true)
    setChatInputValue('')

    try {
      const response = await sendChatMessage(message, conversationId)

      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        timestamp: new Date(response.timestamp),
      }
      setChatMessages((prev) => [...prev, assistantMessage])

      setConversationId(response.conversation_id)
      if (typeof window !== 'undefined') {
        localStorage.setItem('chat_conversation_id', response.conversation_id)
      }

      if (response.task_updated) {
        await fetchTasks()
        await fetchStats()
      }
    } catch (err) {
      setChatInputValue(message)
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: err instanceof ApiError
          ? `Sorry, I encountered an error: ${err.message}`
          : 'Sorry, I\'m having trouble processing that request. Please try again.',
        timestamp: new Date(),
      }
      setChatMessages((prev) => [...prev, errorMessage])
      console.error('Chat error:', err)
    } finally {
      setIsChatLoading(false)
    }
  }

  // Loading state
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <Loader2 className="w-12 h-12 text-indigo-500 animate-spin mb-4" />
        <p className="text-gray-400">Loading tasks...</p>
      </div>
    )
  }

  // Error state
  if (error) {
    return (
      <div className="glass-card p-12 text-center">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-red-500/20 flex items-center justify-center">
          <span className="text-3xl">⚠️</span>
        </div>
        <h3 className="text-xl font-semibold text-white mb-2">Error loading tasks</h3>
        <p className="text-gray-400 mb-4">{error}</p>
        <Button variant="primary" onClick={fetchTasks}>
          Retry
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-white">My Tasks</h1>
          <p className="text-gray-400 mt-1">
            {hasActiveFilters ? (
              <>
                {filteredAndSortedTasks.length} of {tasks.length} tasks
              </>
            ) : (
              <>
                {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
              </>
            )}
          </p>
        </div>
        <Button
          variant="primary"
          size="lg"
          onClick={() => setIsModalOpen(true)}
          className="w-full sm:w-auto"
        >
          <Plus className="w-5 h-5 mr-2" />
          Add Task
        </Button>
      </div>

      {/* Stats */}
      {stats && <TaskStats stats={stats} />}

      {/* Filters */}
      <TaskFilters
        filters={filters}
        sort={sort}
        availableTags={availableTags}
        onFiltersChange={handleFiltersChange}
        onSortChange={handleSortChange}
      />

      {/* Task list */}
      <TaskList
        tasks={filteredAndSortedTasks}
        onToggleComplete={handleToggleComplete}
        onEdit={handleOpenEdit}
        onDelete={handleOpenDelete}
        isFiltered={hasActiveFilters}
      />

      {/* Create/Edit Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={editingTask ? 'Edit Task' : 'Create New Task'}
        size="md"
      >
        <TaskForm
          task={editingTask || undefined}
          availableTags={availableTags}
          onSubmit={editingTask ? handleEditTask : handleCreateTask}
          onCancel={handleCloseModal}
          isSubmitting={isSubmitting}
        />
      </Modal>

      {/* Delete Confirmation */}
      <ConfirmDialog
        isOpen={!!deletingTask}
        title="Delete Task"
        message={`Are you sure you want to delete "${deletingTask?.title}"? This action cannot be undone.`}
        confirmText="Delete"
        cancelText="Cancel"
        onConfirm={handleConfirmDelete}
        onCancel={() => setDeletingTask(null)}
        isLoading={isDeleting}
      />

      {/* Chat Sidebar */}
      <ChatToggle
        isOpen={isChatOpen}
        onClick={() => setIsChatOpen(!isChatOpen)}
      />
      <ChatSidebar
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        messages={chatMessages}
        onSendMessage={handleSendChatMessage}
        isLoading={isChatLoading}
        inputValue={chatInputValue}
        onInputChange={setChatInputValue}
      />
    </div>
  )
}
