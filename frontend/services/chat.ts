// [Task]: T041 [US1] | [Spec]: specs/003-phase-03-ai-chatbot/contracts/chat-api.md
/**
 * Chat API service for AI chatbot interactions.
 */

import { post } from '@/lib/api-client'

export interface ChatRequest {
  message: string
  conversation_id?: string
}

export interface ChatResponse {
  response: string
  conversation_id: string
  task_updated: boolean
  timestamp: string
}

/**
 * Send a message to the AI assistant.
 *
 * @param message - User's natural language message
 * @param conversationId - Optional existing conversation ID
 * @returns ChatResponse with AI response and metadata
 */
export async function sendChatMessage(
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  const request: ChatRequest = {
    message,
    ...(conversationId && { conversation_id: conversationId }),
  }

  return post<ChatResponse>('/api/chat', request)
}
