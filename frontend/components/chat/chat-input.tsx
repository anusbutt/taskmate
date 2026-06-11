// [Task]: T024 [P] [US6], T065 | [Spec]: specs/003-phase-03-ai-chatbot/spec.md
/**
 * ChatInput - Text input component for sending messages.
 * Includes send button and handles form submission.
 * T065: Supports controlled mode to preserve input on send failure.
 */
'use client'

import { useState, useRef, useEffect, KeyboardEvent } from 'react'
import { Send } from 'lucide-react'

interface ChatInputProps {
  onSend: (message: string) => void
  disabled?: boolean
  placeholder?: string
  // T065: Controlled mode props for preserving input on error
  value?: string
  onChange?: (value: string) => void
  clearOnSend?: boolean
}

export function ChatInput({
  onSend,
  disabled = false,
  placeholder = 'Type a message...',
  value,
  onChange,
  clearOnSend = true,
}: ChatInputProps) {
  // Support both controlled and uncontrolled modes
  const [internalMessage, setInternalMessage] = useState('')
  const message = value !== undefined ? value : internalMessage
  const setMessage = onChange || setInternalMessage
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`
    }
  }, [message])

  const handleSubmit = () => {
    const trimmedMessage = message.trim()
    if (trimmedMessage && !disabled) {
      onSend(trimmedMessage)
      // T065: Only clear if clearOnSend is true (default behavior)
      if (clearOnSend) {
        setMessage('')
      }
    }
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Submit on Enter (without Shift)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="flex items-end gap-2 p-4 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
      <textarea
        ref={textareaRef}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        rows={1}
        className={`
          flex-1 resize-none
          px-4 py-2 rounded-2xl
          border border-gray-300 dark:border-gray-600
          bg-gray-50 dark:bg-gray-700
          text-gray-900 dark:text-white
          placeholder-gray-500 dark:placeholder-gray-400
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
          disabled:opacity-50 disabled:cursor-not-allowed
          text-sm
        `}
        style={{ minHeight: '40px', maxHeight: '120px' }}
      />
      <button
        onClick={handleSubmit}
        disabled={disabled || !message.trim()}
        className={`
          flex-shrink-0 w-10 h-10 rounded-full
          flex items-center justify-center
          transition-colors duration-200
          ${message.trim() && !disabled
            ? 'bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white'
            : 'bg-gray-200 dark:bg-gray-600 text-gray-400 dark:text-gray-500 cursor-not-allowed'
          }
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
          dark:focus:ring-offset-gray-800
        `}
        aria-label="Send message"
      >
        <Send className="w-5 h-5" />
      </button>
    </div>
  )
}
