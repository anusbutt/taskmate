# TaskMate — AI-Powered Task Manager

Manage your tasks by chatting with an AI assistant.

[![Live Demo](https://img.shields.io/badge/Live_Demo-Vercel-black?style=for-the-badge&logo=vercel)](https://evolution-of-todo-coral.vercel.app/)

---

## Features

- **Full CRUD via natural language chat** — Create, update, complete, and delete tasks by talking to the AI assistant
- **MCP tools as subprocess** — Task operations run through a Model Context Protocol server spawned as a subprocess for reliable tool execution
- **JWT authentication** — Secure signup and login with httpOnly cookie tokens and per-user data isolation
- **Dark mode** — Glassmorphism UI with light/dark theme support
- **Modern stack** — Built with Next.js, FastAPI, PostgreSQL, and Claude AI

---

## Tech Stack

| Layer | Technology |
|:------|:-----------|
| **Frontend** | Next.js, Tailwind CSS, TypeScript |
| **Backend** | FastAPI, PostgreSQL, SQLModel |
| **AI** | Claude API, MCP Tools |

---

## Getting Started

### Prerequisites

- **Node.js** 22+
- **Python** 3.13+
- **PostgreSQL** 16+ (local instance or a hosted provider such as [Neon](https://neon.tech))

### Installation

```bash
git clone https://github.com/anusbutt/evolution-of-todo.git
cd evolution-of-todo
```

**Backend dependencies:**

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
```

**Frontend dependencies:**

```bash
cd frontend
npm install
```

### Environment Variables

**Backend** — create `backend/.env`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/taskmate
JWT_SECRET=your-secret-key-change-in-production
GROQ_API_KEY=your-llm-api-key
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

| Variable | Description |
|:---------|:------------|
| `DATABASE_URL` | Async PostgreSQL connection string |
| `JWT_SECRET` | Secret used to sign authentication tokens |
| `GROQ_API_KEY` | API key for the AI assistant (OpenAI-compatible LLM provider) |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins |

**Frontend** — create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

| Variable | Description |
|:---------|:------------|
| `NEXT_PUBLIC_API_URL` | Base URL of the FastAPI backend |

### Running locally

Start the backend and frontend in separate terminals:

```bash
# Terminal 1 — Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
npm run dev
```

Open **http://localhost:3000**, sign up, and start managing tasks through the chat sidebar.

---

## Live Demo

**https://evolution-of-todo-coral.vercel.app/**

Sign up for a free account to try the full experience — task list, filters, and the built-in AI assistant.

---

## Architecture

```
┌─────────────┐     REST API      ┌─────────────┐     SQL      ┌────────────┐
│   Next.js   │ ────────────────► │   FastAPI   │ ───────────► │ PostgreSQL │
│  Frontend   │ ◄──────────────── │   Backend   │ ◄─────────── │     DB     │
└─────────────┘                   └──────┬──────┘              └────────────┘
                                       │
                                       │ spawns subprocess
                                       ▼
                                ┌─────────────┐
                                │ MCP Server  │
                                │  (stdio)    │
                                └──────┬──────┘
                                       │
                                       ▼
                                ┌─────────────┐
                                │  Claude AI  │
                                │  (via API)  │
                                └─────────────┘
```

The Next.js frontend talks to a FastAPI backend backed by PostgreSQL. When a user sends a chat message, the backend orchestrates an AI agent that spawns an MCP tool server as a subprocess. The MCP server exposes task CRUD operations as tools, letting the AI create, update, complete, and delete tasks on the user's behalf.

---

## License

MIT
