# [Task]: T026a | [Spec]: specs/005-phase-05-cloud-native/spec.md
# Dockerfile for Next.js frontend
# Using node:22-slim instead of alpine due to lightningcss native module issues

FROM node:22-slim

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

# Build the application
ENV NEXT_PUBLIC_API_URL=""
RUN npm run build

# Expose port
EXPOSE 3000

ENV NODE_ENV=production
ENV HOSTNAME="0.0.0.0"
ENV PORT=3000

# Run with next start (not standalone server.js)
CMD ["npx", "next", "start", "-H", "0.0.0.0", "-p", "3000"]
