// [Task]: T021 [P] [US6] | [Spec]: specs/003-phase-03-ai-chatbot/spec.md
/**
 * ChatToggle - Button to open/close the chat sidebar.
 * Fixed position button in the bottom right corner.
 */
'use client'

import { MessageCircle, X } from 'lucide-react'

interface ChatToggleProps {
  isOpen: boolean
  onClick: () => void
}

export function ChatToggle({ isOpen, onClick }: ChatToggleProps) {
  return (
    <button
      onClick={onClick}
      className={`
        fixed bottom-6 right-6 z-50
        w-14 h-14 rounded-full
        flex items-center justify-center
        shadow-lg transition-all duration-300
        ${isOpen
          ? 'bg-gray-600 hover:bg-gray-700 dark:bg-gray-700 dark:hover:bg-gray-600'
          : 'bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600'
        }
        text-white
        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
        dark:focus:ring-offset-gray-900
      `}
      aria-label={isOpen ? 'Close chat' : 'Open chat'}
      title={isOpen ? 'Close chat assistant' : 'Open chat assistant'}
    >
      {isOpen ? (
        <X className="w-6 h-6" />
      ) : (
        <MessageCircle className="w-6 h-6" />
      )}
    </button>
  )
}
