# Deploy Backend on Render

## Service Type
- `Web Service`
- Runtime: `Docker` (uses `Dockerfile` in this repo)

## Render Settings
- Root Directory: `.`
- Health Check Path: `/health`

## Required Environment Variables
- `DATABASE_URL` = connection string from Supabase (SQLAlchemy format)
- `JWT_SECRET` = long random secret
- `SUPABASE_URL` = your Supabase project URL (`https://<project-ref>.supabase.co`)
- `SUPABASE_ANON_KEY` = Supabase anon/public key used to validate OAuth access token with Supabase Auth API

## Recommended Environment Variables
- `CORS_ORIGINS` = comma-separated frontend origins (for example `https://wildquest-frontend.onrender.com`)
- `FRONTEND_URL` = same frontend public URL
- `GOOGLE_CLIENT_IDS` = optional only if you still keep legacy `/auth/google` endpoint
- `JWT_ALGORITHM` = `HS256`
- `JWT_EXPIRES_MINUTES` = `10080`
- `AUTO_CREATE_TABLES` = `true` only on first deploy with empty database, then set back to `false`

## Notes
- The container binds to `PORT` automatically (`uvicorn ... --port ${PORT:-8000}`).
- If CORS is not configured, browser requests from the frontend will fail.
- Keep `.env` local only. Do not commit secrets.
- Supabase example:
  - `postgresql+psycopg2://postgres.<project-ref>:<password>@aws-1-eu-west-1.pooler.supabase.com:6543/postgres?sslmode=require`
