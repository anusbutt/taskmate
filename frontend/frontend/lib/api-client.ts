// [Task]: T028 | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * API client wrapper for backend communication.
 * Handles base URL, credentials, and error handling.
 */

// Determine API base URL at request time (not module load time)
// This ensures browser hostname is available
function getApiBaseUrl(): string {
  // In browser, check the hostname to decide URL strategy
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname
    // If accessing via custom domain (e.g., todo.local), use relative URLs
    // Relative URLs go through the ingress which routes /api/* to backend
    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
      return ''
    }
  }

  // Default fallback for local development (localhost)
  return 'http://localhost:8000'
}

export class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

/**
 * Make an API request with automatic error handling.
 *
 * @param endpoint - API endpoint path (e.g., '/api/tasks')
 * @param options - Fetch options (method, body, headers)
 * @returns Parsed JSON response
 * @throws ApiError if request fails
 */
export async function apiRequest<T = any>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Get base URL at request time (handles browser vs server, localhost vs custom domain)
  const baseUrl = getApiBaseUrl()
  const url = `${baseUrl}${endpoint}`

  // Default headers
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }

  // Include credentials to send/receive httpOnly cookies
  const config: RequestInit = {
    ...options,
    headers,
    credentials: 'include', // Required for httpOnly cookies
  }

  try {
    const response = await fetch(url, config)

    // Handle non-2xx responses
    if (!response.ok) {
      let errorData
      try {
        errorData = await response.json()
      } catch {
        errorData = { detail: response.statusText, code: 'UNKNOWN_ERROR' }
      }

      throw new ApiError(
        response.status,
        errorData.code || 'API_ERROR',
        errorData.detail || errorData.message || 'An error occurred'
      )
    }

    // Handle 204 No Content responses
    if (response.status === 204) {
      return undefined as T
    }

    // Parse JSON response
    return await response.json()
  } catch (error) {
    // Re-throw ApiError as-is
    if (error instanceof ApiError) {
      throw error
    }

    // Wrap network errors
    throw new ApiError(
      0,
      'NETWORK_ERROR',
      error instanceof Error ? error.message : 'Network request failed'
    )
  }
}

/**
 * GET request helper.
 */
export async function get<T = any>(endpoint: string): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'GET' })
}

/**
 * POST request helper.
 */
export async function post<T = any>(endpoint: string, data?: any): Promise<T> {
  return apiRequest<T>(endpoint, {
    method: 'POST',
    body: data ? JSON.stringify(data) : undefined,
  })
}

/**
 * PUT request helper.
 */
export async function put<T = any>(endpoint: string, data?: any): Promise<T> {
  return apiRequest<T>(endpoint, {
    method: 'PUT',
    body: data ? JSON.stringify(data) : undefined,
  })
}

/**
 * PATCH request helper.
 */
export async function patch<T = any>(endpoint: string, data?: any): Promise<T> {
  return apiRequest<T>(endpoint, {
    method: 'PATCH',
    body: data ? JSON.stringify(data) : undefined,
  })
}

/**
 * DELETE request helper.
 */
export async function del<T = any>(endpoint: string): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'DELETE' })
}
