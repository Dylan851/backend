from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes import auth_routes, player_routes, animal_routes, map_routes, shop_routes
from app import models  # noqa: F401
from app.config.database import Base, engine
from app.config.settings import settings

app = FastAPI(
    title="Animal GO API",
    version="1.0.0",
    description="API para Animal GO - Juego de captura de animales"
)

# Configure CORS for Flutter app and development
cors_origins = settings.get_cors_origins()
allow_all_origins = "*" in cors_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=not allow_all_origins,
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


@app.on_event("startup")
def startup():
    if settings.AUTO_CREATE_TABLES:
        Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"success": True, "data": {"status": "ok"}}
