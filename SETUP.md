# 🚀 GUÍA DE INSTALACIÓN Y SETUP

## 1️⃣ Configuración Inicial

### Instalar Dependencias
```bash
# Crear virtual environment (si no lo hiciste)
python -m venv .venv

# Activar virtual environment
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

# Instalar requirements
pip install -r requirements.txt
```

### Configurar Variables de Entorno
```bash
# Copiar .env.example a .env
cp .env.example .env

# Editar .env con tus datos de Supabase
# DATABASE_URL=postgresql+psycopg2://user:password@host:port/database
# JWT_SECRET=tu_clave_secreta_muy_segura
```

---

## 2️⃣ Configuración de Base de Datos

### Ejecutar Migraciones
1. **Ir a la consola SQL de Supabase**
   - Entra a [supabase.com](https://supabase.com)
   - Abre tu proyecto
   - Ve a "SQL Editor"

2. **Ejecutar el script SQL original** (si aún no lo hiciste)
   - Copiar contenido de `schema.sql` 
   - Ejecutar en la consola SQL

3. **Ejecutar las migraciones adicionales**
   - Copiar contenido de `migrations.sql`
   - Ejecutar en la consola SQL

### Verificar Tablas Creadas
```sql
-- En Supabase SQL Editor
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';
```

Deberías ver:
- ✅ Usuario
- ✅ Jugador
- ✅ Animales
- ✅ Item
- ✅ Mapa
- ✅ NPC
- ✅ Enemigo (NUEVA)
- ✅ Aldeano (NUEVA)
- ✅ Mapa_Item (NUEVA)
- ✅ Captura
- ✅ Jugador_Item
- ✅ Mapa_NPC
- ✅ Mapa_Animales

---

## 3️⃣ Ejecutar el Backend

### Opción 1: Desarrollo Local
```bash
# Activar virtual environment
.venv\Scripts\activate

# Ejecutar FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

### Opción 2: Usar Docker (Recomendado para Producción)
```bash
# Construir imagen
docker build -t animal-go-api .

# Ejecutar contenedor
docker run -p 8000:8000 --env-file .env animal-go-api
```

---

## 4️⃣ Probar Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Autenticarse (JWT)
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123"}'
```

### Obtener NPCs de un Mapa
```bash
curl -X GET "http://localhost:8000/npc/map/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Obtener Enemigos de un Mapa
```bash
curl -X GET "http://localhost:8000/enemies/map/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 5️⃣ Conectar con Flutter/Bonfire

### En tu código Dart de Bonfire:

```dart
// 1. Instalar packages en pubspec.yaml
dependencies:
  dio: ^5.0.0
  bonfire: ^3.0.0

// 2. Crear cliente HTTP
class ApiClient {
  final String baseUrl = "http://tu-servidor.com:8000";
  final Dio dio = Dio();
  
  Future<Map> getNpcsByMap(int mapId) async {
    try {
      final response = await dio.get(
        '$baseUrl/npc/map/$mapId',
        options: Options(
          headers: {'Authorization': 'Bearer $jwtToken'}
        ),
      );
      return response.data;
    } catch (e) {
      print('Error: $e');
      return {};
    }
  }
  
  Future<Map> getEnemiesByMap(int mapId) async {
    try {
      final response = await dio.get(
        '$baseUrl/enemies/map/$mapId',
        options: Options(
          headers: {'Authorization': 'Bearer $jwtToken'}
        ),
      );
      return response.data;
    } catch (e) {
      print('Error: $e');
      return {};
    }
  }
}

// 3. Usar en Bonfire
Future<void> loadMapEntities() async {
  final npcs = await apiClient.getNpcsByMap(currentMapId);
  final enemies = await apiClient.getEnemiesByMap(currentMapId);
  
  // Añadir a Bonfire
  for (var npc in npcs['data']['npcs']) {
    addNpcToMap(npc);
  }
  
  for (var enemy in enemies['data']['enemies']) {
    addEnemyToMap(enemy);
  }
}
```

---

## 6️⃣ Troubleshooting

### Error: "Connection refused"
- ✅ Verifica que el servidor esté corriendo: `uvicorn app.main:app --reload`
- ✅ Verifica el puerto: asegúrate que sea 8000
- ✅ Verifica firewall

### Error: "Database connection failed"
- ✅ Verifica `DATABASE_URL` en `.env`
- ✅ Verifica que Supabase esté online
- ✅ Verifica credenciales en Supabase

### Error: "401 Unauthorized"
- ✅ Verifica que enviaste el JWT token en headers
- ✅ Verifica que el token no haya expirado
- ✅ Verifica que `JWT_SECRET` sea el mismo en `.env`

### Error: "404 Not Found"
- ✅ Verifica el endpoint URL
- ✅ Verifica que el recurso exista (ej: NPC/Enemigo con ese ID)
- ✅ Consulta la documentación en `/docs`

---

## 7️⃣ Estructura de Carpetas (Resumen)

```
backend/
├── app/
│   ├── config/          # Configuración (DB, JWT)
│   ├── models/          # Modelos SQLAlchemy
│   │   ├── player.py
│   │   ├── animal.py
│   │   ├── npc.py
│   │   ├── enemigo.py      # NUEVO
│   │   ├── aldeano.py      # NUEVO
│   │   └── map.py          # Actualizado
│   ├── controllers/     # Lógica de endpoints
│   │   ├── player_controller.py
│   │   ├── npc_controller.py
│   │   ├── enemy_controller.py # NUEVO
│   │   └── animal_controller.py
│   ├── services/        # Lógica de negocio
│   │   ├── npc_service.py      # NUEVO
│   │   ├── enemy_service.py    # NUEVO
│   │   └── player_service.py
│   ├── repositories/    # Acceso a datos
│   │   ├── npc_repository.py       # NUEVO
│   │   ├── enemy_repository.py     # NUEVO
│   │   └── player_repository.py
│   ├── routes/          # Definición de endpoints
│   │   ├── player_routes.py
│   │   ├── map_routes.py           # Actualizado
│   │   └── animal_routes.py
│   ├── schemas/         # Validación Pydantic
│   │   ├── npc_schema.py           # NUEVO
│   │   ├── enemy_schema.py         # NUEVO
│   │   └── player_schema.py
│   └── main.py          # Entrada principal
├── requirements.txt     # Dependencias Python
├── .env                 # Variables de entorno
├── migrations.sql       # Migraciones SQL      # NUEVO
├── ENDPOINTS_GUIDE.md   # Guía de endpoints   # NUEVO
└── SETUP.md             # Este archivo        # NUEVO
```

---

## 8️⃣ Próximos Pasos

1. ✅ Completar setup
2. ✅ Ejecutar migraciones SQL
3. ✅ Probar endpoints con Swagger (`/docs`)
4. ✅ Integrar con Bonfire
5. ⏳ Implementar caching (Redis)
6. ⏳ Agregar rate limiting
7. ⏳ Añadir logging estructurado
8. ⏳ Crear tests unitarios
9. ⏳ Deployar a producción

---

## 📞 Soporte

Si tienes problemas:
1. Consulta ENDPOINTS_GUIDE.md
2. Consulta ANALISIS_Y_MEJORAS.md
3. Revisa los logs de la API
4. Verifica /docs (Swagger) para ver endpoints disponibles
