// [Task]: T023 [P] [US6] | [Spec]: specs/003-phase-03-ai-chatbot/spec.md
/**
 * ChatMessage - Individual message bubble component.
 * Displays user and assistant messages with appropriate styling.
 */
'use client'

import { User, Bot } from 'lucide-react'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp?: Date
}

interface ChatMessageProps {
  message: Message
  showTimestamp?: boolean
}

export function ChatMessage({ message, showTimestamp = false }: ChatMessageProps) {
  const isUser = message.role === 'user'

  return (
    <div
      className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
    >
      {/* Avatar */}
      <div
        className={`
          flex-shrink-0 w-8 h-8 rounded-full
          flex items-center justify-center
          ${isUser
            ? 'bg-blue-600 dark:bg-blue-500'
            : 'bg-gray-600 dark:bg-gray-500'
          }
        `}
      >
        {isUser ? (
          <User className="w-4 h-4 text-white" />
        ) : (
          <Bot className="w-4 h-4 text-white" />
        )}
      </div>

      {/* Message Bubble */}
      <div
        className={`
          max-w-[80%] px-4 py-2 rounded-2xl
          ${isUser
            ? 'bg-blue-600 dark:bg-blue-500 text-white rounded-br-md'
            : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-bl-md'
          }
        `}
      >
        <p className="text-sm whitespace-pre-wrap break-words">{message.content}</p>
        {showTimestamp && message.timestamp && (
          <p
            className={`
              text-xs mt-1
              ${isUser
                ? 'text-blue-200'
                : 'text-gray-500 dark:text-gray-400'
              }
            `}
          >
            {message.timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
        )}
      </div>
    </div>
  )
}
