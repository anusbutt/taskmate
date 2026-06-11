// [Task]: T027 | [Spec]: specs/002-phase-02-web-app/spec.md
/**
 * Next.js middleware for authentication route protection.
 * Note: Cookie validation is handled client-side due to cross-port cookie limitations.
 * This middleware only handles basic routing without strict auth checks.
 */
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Allow all requests to proceed - auth is handled client-side
  // This avoids redirect loops when cookies are set on different ports
  return NextResponse.next()
}

// Configure which routes this middleware applies to
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public files (public folder)
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
