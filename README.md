# AnimalGO Backend

Backend FastAPI de AnimalGO.

## Objetivo

Este README esta pensado para lanzar el backend en local manteniendo:

- la base de datos en la nube
- la autenticacion en la nube
- el frontend ejecutandose en local

Es decir: el backend corre en tu PC, pero sigue usando Supabase / PostgreSQL
cloud y, si configuras las variables, tambien el flujo de autenticacion cloud.

## Requisitos

- Python 3.11 o 3.12
- `pip`

## Archivo de entorno recomendado para local

Usa [`.env.local.example`](</C:/Users/dylan/Desktop/proyecto/proyecto/backend/.env.local.example>) como plantilla para levantar el backend en local conectado a la nube.

Pasos:

1. Copia `.env.local.example` a `.env`
2. Rellena los valores reales del proyecto cloud

### Variables importantes

- `DATABASE_URL`
  Debe ser la URL SQLAlchemy de PostgreSQL / Supabase.
- `JWT_SECRET`
  Debe coincidir con el secreto usado por tu backend.
- `SUPABASE_URL`
  URL del proyecto Supabase.
- `SUPABASE_ANON_KEY`
  Clave anon/public de Supabase.
- `FRONTEND_URL`
  Para web local usa `http://localhost:8080`
- `CORS_ORIGINS`
  Debe incluir al menos `http://localhost:8080`

### Variables opcionales

- `GOOGLE_CLIENT_IDS`
  Solo necesaria si quieres probar login Google.
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`

## Arranque local paso a paso

### Windows PowerShell

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.local.example .env
# Edita .env y pega las credenciales reales cloud
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Si `python` no esta en el `PATH`, puedes sustituirlo por `py`.

### Linux / macOS

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.local.example .env
# Edita .env y pega las credenciales reales cloud
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Comprobacion de arranque

Cuando el backend este levantado, abre:

- `http://localhost:8000/health`
- `http://localhost:8000/docs`

Si `/health` responde, el backend local esta funcionando correctamente contra la configuracion cloud.

## Como se conecta el frontend local

Si el backend corre en local en el puerto `8000`, el frontend debe usar:

- Web: `http://localhost:8000`
- Android Emulator: `http://10.0.2.2:8000`
- Movil fisico: `http://IP_DEL_PC:8000`

## Notas importantes

- Este README no cambia el despliegue actual.
- La base de datos sigue siendo cloud.
- La autenticacion puede seguir siendo cloud si rellenas `SUPABASE_URL` y `SUPABASE_ANON_KEY`.
- No subas `.env` al repositorio.
