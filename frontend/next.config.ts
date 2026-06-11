import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
  typescript: {
    ignoreBuildErrors: false,
  },
  // Proxy /api/* requests to backend service
  // Vercel: set INTERNAL_API_URL to Railway backend URL
  // Docker: falls back to http://backend:8000 for local development
  async rewrites() {
    const backendUrl = process.env.INTERNAL_API_URL
    if (!backendUrl) {
      return []
    }
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ]
  },
}

export default nextConfig
