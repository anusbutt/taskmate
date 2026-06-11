// [Task]: T109 [P] [US7] | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Theme management utilities for dark mode toggle.
 * Handles theme persistence in localStorage and theme switching.
 */

export type Theme = 'light' | 'dark'

const THEME_STORAGE_KEY = 'todo-app-theme'

/**
 * Get the current theme from localStorage.
 * Defaults to 'light' if no theme is stored.
 */
export function getTheme(): Theme {
  if (typeof window === 'undefined') {
    return 'light'
  }

  const storedTheme = localStorage.getItem(THEME_STORAGE_KEY)

  if (storedTheme === 'dark' || storedTheme === 'light') {
    return storedTheme
  }

  return 'light'
}

/**
 * Set the theme in localStorage and update the document.
 * Adds/removes 'dark' class on <html> element.
 */
export function setTheme(theme: Theme): void {
  if (typeof window === 'undefined') {
    return
  }

  localStorage.setItem(THEME_STORAGE_KEY, theme)

  const html = document.documentElement

  if (theme === 'dark') {
    html.classList.add('dark')
  } else {
    html.classList.remove('dark')
  }
}

/**
 * Toggle between light and dark themes.
 * Returns the new theme.
 */
export function toggleTheme(): Theme {
  const currentTheme = getTheme()
  const newTheme: Theme = currentTheme === 'light' ? 'dark' : 'light'

  setTheme(newTheme)

  return newTheme
}

/**
 * Initialize theme on page load.
 * Should be called as early as possible to prevent flash of wrong theme.
 */
export function initializeTheme(): void {
  const theme = getTheme()
  setTheme(theme)
}
