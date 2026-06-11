// [Task]: T029 | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: T016 | [Spec]: specs/005-phase-05-cloud-native/spec.md - Added Priority and Tags
/**
 * TypeScript type definitions for Phase 2 frontend.
 * Defines interfaces for User, Task, API responses, and errors.
 */

/**
 * Task priority levels.
 */
export type Priority = 'P1' | 'P2' | 'P3'

/**
 * Tag entity for categorizing tasks.
 */
export interface Tag {
  id: number
  name: string
  color: string
  created_at: string
}

/**
 * User entity representing an authenticated user.
 */
export interface User {
  id: number
  email: string
  name: string
  created_at: string
  updated_at: string
}

/**
 * Task entity representing a todo item.
 */
export interface Task {
  id: number
  user_id: number
  title: string
  description: string | null
  completed: boolean
  priority: Priority
  tags: Tag[]
  recurrence_pattern: 'daily' | 'weekly' | 'monthly' | null
  due_date: string | null
  recurrence_parent_id: number | null
  created_at: string
  updated_at: string
}

/**
 * API error response structure.
 */
export interface ApiError {
  detail: string
  code: string
  field?: string
  details?: any
}

/**
 * Authentication response from signup/login endpoints.
 */
export interface AuthResponse {
  id: number
  email: string
  name: string
  created_at: string
  updated_at: string
}

/**
 * Task response from task endpoints.
 */
export interface TaskResponse {
  id: number
  user_id: number
  title: string
  description: string | null
  completed: boolean
  priority: Priority
  tags: Tag[]
  recurrence_pattern: 'daily' | 'weekly' | 'monthly' | null
  due_date: string | null
  recurrence_parent_id: number | null
  created_at: string
  updated_at: string
}

/**
 * Task list response.
 */
export interface TaskListResponse {
  tasks: TaskResponse[]
  total: number
}

/**
 * Task statistics response.
 */
export interface TaskStats {
  total: number
  completed: number
  incomplete: number
  completion_percentage: number
  by_priority?: Record<Priority, number>
}

/**
 * Task creation/update payload.
 */
export interface TaskCreatePayload {
  title: string
  description?: string
  priority?: Priority
  tag_ids?: number[]
  recurrence_pattern?: 'daily' | 'weekly' | 'monthly'
}

/**
 * Task update payload.
 */
export interface TaskUpdatePayload {
  title?: string
  description?: string
  completed?: boolean
  priority?: Priority
  tag_ids?: number[]
}

/**
 * Tag creation payload.
 */
export interface TagCreatePayload {
  name: string
  color?: string
}

/**
 * Tag list response.
 */
export interface TagListResponse {
  tags: Tag[]
  total: number
}

/**
 * User signup payload.
 */
export interface SignupPayload {
  email: string
  name: string
  password: string
}

/**
 * User login payload.
 */
export interface LoginPayload {
  email: string
  password: string
}
