import os

from app.main import app

# Wrapper para permitir uvicorn main:app desde /app
# Usar variables de entorno es una buena práctica en Docker para cambiar config sin tocar el código.
PORT = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
