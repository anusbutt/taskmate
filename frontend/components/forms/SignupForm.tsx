// [Task]: T050 [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
// [Task]: Phase 5 - Glassmorphism redesign
/**
 * Signup form component with glass styling.
 * Validates email format, name length, and password strength.
 */
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { AlertCircle } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { apiRequest, ApiError } from '@/lib/api-client'

// Zod schema matching backend validation
const signupSchema = z.object({
  email: z.string().email('Invalid email address'),
  name: z.string().min(1, 'Name is required').max(255, 'Name must be less than 255 characters'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[a-zA-Z]/, 'Password must contain at least one letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),
})

type SignupFormData = z.infer<typeof signupSchema>

export function SignupForm() {
  const router = useRouter()
  const [apiError, setApiError] = useState<string | null>(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
  })

  const onSubmit = async (data: SignupFormData) => {
    setIsSubmitting(true)
    setApiError(null)

    try {
      await apiRequest('/api/auth/signup', {
        method: 'POST',
        body: JSON.stringify(data),
      })

      router.push('/tasks')
    } catch (error) {
      if (error instanceof ApiError) {
        setApiError(error.message)
      } else {
        setApiError('An unexpected error occurred. Please try again.')
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
      <Input
        label="Email"
        type="email"
        placeholder="you@example.com"
        error={errors.email?.message}
        {...register('email')}
        fullWidth
        autoComplete="email"
      />

      <Input
        label="Name"
        type="text"
        placeholder="Your name"
        error={errors.name?.message}
        {...register('name')}
        fullWidth
        autoComplete="name"
      />

      <Input
        label="Password"
        type="password"
        placeholder="At least 8 characters with letter and number"
        error={errors.password?.message}
        {...register('password')}
        fullWidth
        autoComplete="new-password"
      />

      {apiError && (
        <div className="p-3 rounded-lg bg-red-500/20 border border-red-500/30 flex items-start gap-2">
          <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-400">{apiError}</p>
        </div>
      )}

      <Button type="submit" variant="primary" fullWidth disabled={isSubmitting}>
        {isSubmitting ? 'Creating account...' : 'Sign Up'}
      </Button>
    </form>
  )
}
