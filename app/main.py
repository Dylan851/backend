from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes import auth_routes, player_routes, animal_routes, map_routes, shop_routes
from app import models  # noqa: F401
from app.config.settings import settings

app = FastAPI(
    title="Animal GO API",
    version="1.0.0",
    description="API para Animal GO - Juego de captura de animales"
)

# Configure CORS for Flutter app and development
cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
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


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"success": True, "data": {"status": "ok"}}
