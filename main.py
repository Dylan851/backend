import os

from app.main import app

# Wrapper para permitir uvicorn main:app desde /app
# Usar variables de entorno es una buena practica en Docker para cambiar config sin tocar el codigo.
PORT = int(os.getenv("PORT", 8000))
RELOAD = os.getenv("UVICORN_RELOAD", "false").lower() == "true"

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=RELOAD)