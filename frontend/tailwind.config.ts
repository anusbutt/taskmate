// [Task]: T026 | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism + Indigo/Violet Theme
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class', // Enable dark mode with class strategy
  theme: {
    extend: {
      colors: {
        // Primary: Indigo palette
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
          950: '#1e1b4b',
          DEFAULT: '#6366f1', // indigo-500
          dark: '#4f46e5', // indigo-600
          light: '#818cf8', // indigo-400
        },
        // Accent: Violet palette
        accent: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
          DEFAULT: '#8b5cf6', // violet-500
          dark: '#7c3aed', // violet-600
          light: '#a78bfa', // violet-400
        },
        secondary: {
          DEFAULT: '#6b7280', // gray-500
          dark: '#4b5563', // gray-600
          light: '#9ca3af', // gray-400
        },
        danger: {
          DEFAULT: '#ef4444', // red-500
          dark: '#dc2626', // red-600
          light: '#f87171', // red-400
        },
        success: {
          DEFAULT: '#22c55e', // green-500
          dark: '#16a34a', // green-600
          light: '#4ade80', // green-400
        },
        warning: {
          DEFAULT: '#f59e0b', // amber-500
          dark: '#d97706', // amber-600
          light: '#fbbf24', // amber-400
        },
      },
      // Glass design tokens
      backdropBlur: {
        xs: '2px',
        glass: '16px',
        'glass-heavy': '24px',
      },
      backgroundOpacity: {
        glass: '0.08',
        'glass-hover': '0.12',
        'glass-active': '0.16',
      },
      borderOpacity: {
        glass: '0.12',
        'glass-hover': '0.18',
      },
      boxShadow: {
        glass: '0 4px 30px rgba(0, 0, 0, 0.1)',
        'glass-lg': '0 8px 32px rgba(0, 0, 0, 0.12)',
        'indigo-glow': '0 0 20px rgba(99, 102, 241, 0.15)',
        'violet-glow': '0 0 20px rgba(139, 92, 246, 0.15)',
      },
      screens: {
        sm: '640px',
        md: '768px',
        lg: '1024px',
        xl: '1280px',
        '2xl': '1536px',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'pulse-soft': 'pulseSoft 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
      },
    },
  },
  plugins: [],
}

export default config
