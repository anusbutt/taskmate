// [Task]: T022 [P] [US6], T061 | [Spec]: specs/003-phase-03-ai-chatbot/spec.md
/**
 * ChatSidebar - Main chat container component.
 * Displays message history, input field, and handles chat state.
 * T061: Includes user-friendly error message display.
 */
'use client'

import { useRef, useEffect } from 'react'
import { X, Bot, AlertCircle, RefreshCw } from 'lucide-react'
import { ChatMessage, Message } from './chat-message'
import { ChatInput } from './chat-input'

interface ChatSidebarProps {
  isOpen: boolean
  onClose: () => void
  messages: Message[]
  onSendMessage: (message: string) => void
  isLoading?: boolean
  error?: string | null
  onRetry?: () => void
  // T065: Controlled input for preserving text on error
  inputValue?: string
  onInputChange?: (value: string) => void
}

export function ChatSidebar({
  isOpen,
  onClose,
  messages,
  onSendMessage,
  isLoading = false,
  error = null,
  onRetry,
  inputValue,
  onInputChange,
}: ChatSidebarProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages])

  return (
    <>
      {/* Backdrop for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/20 dark:bg-black/40 z-40 lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed top-0 right-0 h-full z-50
          w-full sm:w-96 max-w-full
          bg-white dark:bg-gray-800
          shadow-2xl
          transform transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : 'translate-x-full'}
          flex flex-col
        `}
        aria-label="Chat sidebar"
        aria-hidden={!isOpen}
      >
        {/* Header */}
        <header className="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-blue-600 dark:bg-blue-500 flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="font-semibold text-gray-900 dark:text-white">
                Task Assistant
              </h2>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                Manage tasks with natural language
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            aria-label="Close chat"
          >
            <X className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          </button>
        </header>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="text-center py-8">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                <Bot className="w-8 h-8 text-blue-600 dark:text-blue-400" />
              </div>
              <h3 className="font-medium text-gray-900 dark:text-white mb-2">
                Welcome to Task Assistant
              </h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 max-w-xs mx-auto">
                I can help you manage your tasks. Try saying:
              </p>
              <div className="mt-4 space-y-2">
                <p className="text-sm text-gray-600 dark:text-gray-300">
                  &quot;Add buy groceries&quot;
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-300">
                  &quot;Show my tasks&quot;
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-300">
                  &quot;Mark task 1 as done&quot;
                </p>
              </div>
            </div>
          ) : (
            <>
              {/* T066: Show timestamps on messages */}
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} showTimestamp={true} />
              ))}
              {isLoading && (
                <div className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-gray-600 dark:bg-gray-500 flex items-center justify-center">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div className="bg-gray-100 dark:bg-gray-700 px-4 py-2 rounded-2xl rounded-bl-md">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                  </div>
                </div>
              )}
              {/* T061: User-friendly error message display */}
              {error && (
                <div className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-red-500 flex items-center justify-center">
                    <AlertCircle className="w-4 h-4 text-white" />
                  </div>
                  <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 px-4 py-2 rounded-2xl rounded-bl-md max-w-[85%]">
                    <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
                    {onRetry && (
                      <button
                        onClick={onRetry}
                        className="mt-2 flex items-center gap-1 text-xs text-red-600 dark:text-red-400 hover:underline"
                      >
                        <RefreshCw className="w-3 h-3" />
                        Try again
                      </button>
                    )}
                  </div>
                </div>
              )}
            </>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <ChatInput
          onSend={onSendMessage}
          disabled={isLoading}
          placeholder="Ask me to manage your tasks..."
          value={inputValue}
          onChange={onInputChange}
          clearOnSend={false}
        />
      </aside>
    </>
  )
}
