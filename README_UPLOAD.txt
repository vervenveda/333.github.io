333 / BUNYA API — RAILWAY DEPLOYMENT FILE

Repository:
vervenveda/333.github.io

Add this file to the repository root:
- railway.json

The repository already has the Dockerfile and Alembic migration configuration.
railway.json adds:
- Dockerfile build selection
- alembic upgrade head before deploy
- /health deployment healthcheck
- restart-on-failure

Railway service name:
333-api

This service IS public.
After first successful deployment:
1. Generate a Railway public domain for testing.
2. Then add custom domain: api.vervenveda.com

Create PostgreSQL and Redis services in the SAME Railway project.
Use 333_RAILWAY_VARIABLES.txt as the variable template.

Do NOT attach a filesystem volume to 333-api yet. The currently wired Bunya path
does not need one; PostgreSQL and Redis provide its persistent state.
