from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import text
import logging

from app.routes import auth_routes, player_routes, animal_routes, map_routes, shop_routes, payment_routes
from app import models  # noqa: F401
from app.config.settings import settings
from app.config.database import engine

app = FastAPI(
    title="Animal GO API",
    version="1.0.0",
    description="API para Animal GO - Juego de captura de animales"
)

# Configure CORS for Flutter app and development.
# Include FRONTEND_URL as a safety net for deployments where CORS_ORIGINS is incomplete.
cors_origins = {origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()}
frontend_origin = settings.FRONTEND_URL.strip()
if frontend_origin:
    cors_origins.add(frontend_origin)
cors_origins = sorted(cors_origins)
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(auth_routes.router)
app.include_router(player_routes.router)
app.include_router(animal_routes.router)
app.include_router(map_routes.router)
app.include_router(map_routes.npc_router)
app.include_router(map_routes.enemy_router)
app.include_router(shop_routes.router)
app.include_router(payment_routes.router)

logger = logging.getLogger(__name__)


@app.on_event("startup")
def apply_runtime_migrations():
    # Ensure new economy column exists for existing databases.
    with engine.begin() as conn:
        conn.execute(
            text(
                "ALTER TABLE jugador "
                "ADD COLUMN IF NOT EXISTS diamantes INTEGER NOT NULL DEFAULT 0"
            )
        )
        conn.execute(
            text(
                "CREATE TABLE IF NOT EXISTS stripe_purchase ("
                "id SERIAL PRIMARY KEY,"
                "user_id INTEGER NOT NULL,"
                "payment_intent_id VARCHAR(255) NOT NULL UNIQUE,"
                "pack_id VARCHAR(64) NOT NULL,"
                "currency_type VARCHAR(32) NOT NULL,"
                "quantity INTEGER NOT NULL,"
                "amount INTEGER NOT NULL,"
                "currency VARCHAR(10) NOT NULL,"
                "status VARCHAR(32) NOT NULL,"
                "created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()"
                ")"
            )
        )
    if not settings.STRIPE_WEBHOOK_SECRET.strip():
        logger.warning("STRIPE_WEBHOOK_SECRET is not configured yet; /stripe/webhook will reject requests.")


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"success": True, "data": {"status": "ok"}}
