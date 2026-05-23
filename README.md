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

## Tests

Para ejecutar los tests del backend:

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest test -q
```

Actualmente hay tests de salud, autenticacion y perfil.

| Test | Que comprueba | Por que es importante |
|---|---|---|
| `test_health` | Que `/health` responde `200` y devuelve estado `ok`. | Verifica que la API esta viva. |
| `test_register_creates_user_and_player` | Que al registrarte se crea el usuario, se crea su player y se devuelve token. | Confirma que el alta basica funciona de verdad. |
| `test_register_normalizes_email_to_lowercase` | Que el email se guarda en minusculas aunque el usuario lo escriba con mayusculas. | Evita duplicados raros y problemas al iniciar sesion. |
| `test_register_rejects_duplicate_email` | Que no se puede registrar dos veces el mismo correo. | Protege la integridad de cuentas. |
| `test_register_rejects_duplicate_username` | Que no se puede reutilizar un nombre de usuario ya existente. | Evita colisiones entre jugadores. |
| `test_login_with_email_returns_token_and_profile` | Que el login con email y contrasena correctos devuelve token y perfil. | Comprueba el acceso normal a la aplicacion. |
| `test_login_with_username_works` | Que tambien se puede iniciar sesion usando el nombre de usuario. | Verifica una via de login que usa el frontend. |
| `test_login_rejects_wrong_password` | Que una contrasena incorrecta devuelve error `401`. | Garantiza que la autenticacion no acepta credenciales invalidas. |
| `test_auth_methods_reports_existing_password_account` | Que `/auth/methods` detecta una cuenta existente con contrasena. | Sirve para flujos de login y registro mas inteligentes. |
| `test_auth_methods_reports_non_existing_account` | Que `/auth/methods` indica correctamente que el correo no existe. | Evita decisiones erroneas en frontend. |
| `test_password_recovery_returns_generic_message_for_existing_password_user` | Que la recuperacion de contrasena responde correctamente si la cuenta existe. | Comprueba el flujo de recuperacion. |
| `test_password_recovery_returns_generic_message_for_non_existing_user` | Que la recuperacion no rompe aunque el correo no exista. | Evita filtracion de informacion y errores innecesarios. |
| `test_profile_requires_authentication` | Que `/player/profile` no se puede consultar sin token. | Asegura que el perfil esta protegido. |
| `test_get_profile_returns_registered_player_data` | Que el perfil autenticado devuelve nickname, nivel, monedas e inventario correctos. | Verifica que los datos del jugador se guardan y leen bien. |
| `test_update_profile_changes_nickname` | Que cambiar el nickname desde `/player/profile` realmente lo actualiza. | Comprueba persistencia de cambios del usuario. |
| `test_update_location_changes_coordinates` | Que `/player/location` guarda bien latitud y longitud. | Verifica que el backend actualiza estado del jugador. |

## Notas importantes

- Este README no cambia el despliegue actual.
- La base de datos sigue siendo cloud.
- La autenticacion puede seguir siendo cloud si rellenas `SUPABASE_URL` y `SUPABASE_ANON_KEY`.
- No subas `.env` al repositorio.
