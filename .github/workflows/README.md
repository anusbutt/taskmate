# CI/CD Pipeline Documentation

This document describes the GitHub Actions CI/CD pipeline for the Todo App.

## Pipeline Overview

The pipeline runs on push to `main`/`master` or the `005-phase-05-cloud-native` branch and on pull requests.

### Jobs

| Job | Trigger | Description |
|-----|---------|-------------|
| **test** | All branches, PRs | Run linting and tests for backend and frontend |
| **build** | main/master push only | Build Docker images and push to DOCR |
| **deploy** | main/master push only | Deploy to DOKS using Helm |
| **smoke-test** | main/master push only | Verify deployment health |

### Pipeline Flow

```
Push to main
    │
    ▼
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────────┐
│  Test   │────▶│  Build  │────▶│ Deploy  │────▶│ Smoke Test  │
└─────────┘     └─────────┘     └─────────┘     └─────────────┘
    │                                                    │
    │                                                    ▼
    │                                          ✓ App accessible
    │                                            via Load Balancer
    │
Push to feature branch / PR
    │
    ▼
┌─────────┐
│  Test   │ (only)
└─────────┘
```

## Required Secrets

Configure these secrets in your GitHub repository settings:

| Secret | Description | Example |
|--------|-------------|---------|
| `DIGITALOCEAN_ACCESS_TOKEN` | DigitalOcean API token | `dop_v1_...` |
| `DATABASE_URL` | Neon PostgreSQL connection string | `postgresql://user:pass@host/db?sslmode=require` |
| `JWT_SECRET` | Secret for JWT token signing | Random 32+ char string |
| `GEMINI_API_KEY` | Google Gemini API key | `AIza...` |
| `REDPANDA_BROKERS` | Redpanda Cloud bootstrap servers | `broker1:9092,broker2:9092` |
| `REDPANDA_USERNAME` | Redpanda SASL username | `username` |
| `REDPANDA_PASSWORD` | Redpanda SASL password | `password` |

### Setting Secrets

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add each secret with its name and value

## Docker Images

Images are built and pushed to DigitalOcean Container Registry (DOCR):

| Image | Registry Path |
|-------|---------------|
| Frontend | `registry.digitalocean.com/todo-app-registry/frontend` |
| Backend | `registry.digitalocean.com/todo-app-registry/backend` |
| MCP Server | `registry.digitalocean.com/todo-app-registry/mcp-server` |
| Audit Service | `registry.digitalocean.com/todo-app-registry/audit-service` |

### Image Tags

- `latest` - Most recent build from main branch
- `<sha>` - Git commit SHA (first 7 chars)

## Deployment

Deployment uses Helm with the chart at `deployment/helm/todo-app/`.

### Helm Values

Production values are in `values-prod.yaml`. The pipeline overrides:

- Image tags (from build job output)
- Environment variables (from secrets)
- Redpanda credentials (from secrets)

### Manual Deployment

To deploy manually:

```bash
# Configure kubectl
doctl kubernetes cluster kubeconfig save todo-app-cluster

# Deploy with Helm
helm upgrade --install todo-app ./deployment/helm/todo-app \
  --namespace todo-app \
  -f ./deployment/helm/todo-app/values-prod.yaml \
  --set backend.env.DATABASE_URL="$DATABASE_URL" \
  --set backend.env.JWT_SECRET="$JWT_SECRET"
```

## Troubleshooting

### View Pipeline Logs

1. Go to **Actions** tab in GitHub
2. Click on the workflow run
3. Click on the failed job to see logs

### Check Pod Status

```bash
kubectl get pods -n todo-app
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

### Rollback Deployment

```bash
helm rollback todo-app -n todo-app
```

### Force Rebuild

Add `[rebuild]` to your commit message to bypass cache:

```bash
git commit -m "Fix: issue [rebuild]"
```

## Costs

- DOKS: ~$24/month (2 nodes × $12)
- Load Balancer: ~$12/month
- DOCR: Free tier (500MB, 1 repo)
- **Total**: ~$36/month ($200 credit = ~5 months)

## Links

- [DigitalOcean Dashboard](https://cloud.digitalocean.com)
- [DOKS Documentation](https://docs.digitalocean.com/products/kubernetes/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
