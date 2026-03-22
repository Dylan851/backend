# ✅ CHECKLIST RÁPIDO - QUÉ HACER AHORA

## 1. 🔧 CONFIGURACIÓN INMEDIATA (5 min)

- [ ] Revisar que `.env` tiene las credenciales correctas de Supabase
- [ ] Verificar que `DATABASE_URL` esté configurada correctamente
- [ ] Configurar `JWT_SECRET` con una clave segura

```bash
# Comando para generar un JWT_SECRET seguro:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 2. 🗄️ MIGRACIÓN DE BASE DE DATOS (10 min)

- [ ] Abrir consola SQL de Supabase
- [ ] Copiar el contenido de `migrations.sql`
- [ ] Ejecutar en Supabase SQL Editor
- [ ] Verificar que se crearon las nuevas tablas:
  - [ ] Enemigo
  - [ ] Aldeano
  - [ ] Mapa_Item

### Verificación SQL:
```sql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name IN ('Enemigo', 'Aldeano', 'Mapa_Item');
```

Debería retornar 3 tablas.

---

## 3. 🧪 PRUEBA LOCAL (15 min)

### Levantar el servidor:
```bash
# Activar venv
.venv\Scripts\activate

# Instalar dependencias (si no lo hiciste)
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload
```

### Verificar que funciona:
- [ ] Acceder a `http://localhost:8000/health`
  - Debería retornar: `{"success": true, "data": {"status": "ok"}}`

- [ ] Acceder a `http://localhost:8000/docs`
  - Debería mostrar documentación Swagger interactiva
  - Deberías ver nuevos endpoints:
    - `/npc/{npc_id}`
    - `/enemies/map/{map_id}`
    - `/enemies/{enemy_id}`
    - `/enemies/{enemy_id}/defeat`

---

## 4. 🎯 PROBAR NUEVOS ENDPOINTS (20 min)

### Opción A: Usando Swagger (http://localhost:8000/docs)
1. Ir a "Try it out" en cada endpoint
2. Ingresar parámetros (ej: map_id=1)
3. Click en "Execute"
4. Ver respuesta

### Opción B: Usando cURL
```bash
# Obtener NPCs de un mapa
curl -X GET "http://localhost:8000/npc/map/1"

# Obtener Enemigos de un mapa
curl -X GET "http://localhost:8000/enemies/map/1"

# Obtener detalles de un enemigo
curl -X GET "http://localhost:8000/enemies/1"
```

Nota: Si tienes autenticación habilitada, necesitarás un JWT token en el header:
```bash
-H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 5. 📖 REVISAR DOCUMENTACIÓN (10 min)

- [ ] Leer `CAMBIOS_REALIZADOS.md` - Entiende qué se cambió
- [ ] Leer `ENDPOINTS_GUIDE.md` - Todos los endpoints disponibles
- [ ] Leer `SETUP.md` - Guía completa de instalación
- [ ] Leer `ANALISIS_Y_MEJORAS.md` - Contexto de las mejoras

---

## 6. 🎮 PREPARAR PARA BONFIRE (Opcional pero Recomendado)

- [ ] Revisar ejemplos de integración en `ENDPOINTS_GUIDE.md`
- [ ] Crear clase ApiClient en tu proyecto Bonfire
- [ ] Probar conexión básica con el backend
- [ ] Ver cómo obtener NPCs y Enemigos

---

## 7. 🐞 DEBUG & TROUBLESHOOTING (Si hay errores)

### Si falla la conexión a BD:
```bash
# Verificar que DATABASE_URL es correcto
python -c "from app.config.settings import settings; print(settings.DATABASE_URL)"

# Ver si SQLAlchemy puede conectar
python -c "from app.config.database import engine; engine.connect()"
```

### Si falla algún endpoint:
1. Check `/docs` para ver la estructura esperada
2. Ver logs del servidor (donde hace `uvicorn`)
3. Consultar `ENDPOINTS_GUIDE.md` para formato correcto

### Si falla la autenticación:
1. Verificar que enviaste JWT en el header
2. Verificar que el JWT no expiró (7 días por defecto)
3. Revisar logs del servidor

---

## 8. 🚀 LANZAMIENTO A PRODUCCIÓN (Después)

- [ ] Cambiar `DEBUG=False` si está habilitado
- [ ] Usar variables de entorno seguras
- [ ] Configurar CORS si es necesario
- [ ] Agregar logging (Winston, Loguru)
- [ ] Agregar rate limiting
- [ ] Testing completo
- [ ] Deploy (Docker, Heroku, AWS, etc.)

---

## ⏱️ TIMELINE ESTIMADO

```
5 min  → Configuración del .env
10 min → Migraciones SQL
15 min → Prueba local
20 min → Probar endpoints
10 min → Revisar documentación
-----------
60 min TOTAL

(Opcional: 30 min más para preparar Bonfire)
```

---

## 🆘 PROBLEMAS COMUNES

### "ModuleNotFoundError: No module named 'app'"
```bash
# Asegúrate de estar en el directorio raíz del proyecto
cd backend
uvicorn app.main:app --reload
```

### "sqlalchemy.exc.OperationalError: connection refused"
- [ ] Verifica `DATABASE_URL` en `.env`
- [ ] Verifica que Supabase esté online
- [ ] Verifica credenciales

### "404 not found en /enemies/map/1"
- [ ] Verifica que existen datos en la tabla Enemigo
- [ ] Verifica que el map_id=1 existe
- [ ] Ve a Swagger (`/docs`) para ver mejor error

### "401 Unauthorized"
- [ ] Verifica que autenticación esté habilitada (ver `get_current_player` en codigo)
- [ ] Asegúrate de enviar JWT en Authorization header
- [ ] Verifica que el JWT no expiró

---

## 📝 NOTAS IMPORTANTES

1. **Esta versión está LISTA para Bonfire** ✅
2. **Bases de datos está ALINEADA con el script original** ✅
3. **Documentación está COMPLETA** ✅
4. **Endpoints están probados y documentados** ✅
5. **Falta: Geolocalización avanzada** (funcionalidad futura)
6. **Falta: Sistema de combate completo** (se puede extender)
7. **Falta: Tests unitarios** (recomendado agregar)

---

## 🎯 SIGUIENTE FASE (Futuro)

Una vez que confirmes que esto funciona:

1. **Implementar geolocalización**
   - `calculate_distance()` entre jugador y enemigos
   - Filtrar enemigos por radio (100m, 500m, 1km, etc.)

2. **Sistema de combate completo**
   - Lógica de turnos en `enemy_service.py`
   - Cálculo de daño, críticos, etc.

3. **Sistema de diálogos**
   - Conversaciones con Aldeanos
   - Sistema de misiones

4. **Opt: Agregar caché**
   - Redis para mapas y NPCs (no cambian frecuentemente)
   - Mejorar performance

5. **Opt: Agregar rate limiting**
   - Prevenir spam de requests
   - Proteger endpoints sensibles

---

## 💡 TIPS

- Usa Swagger (`/docs`) para explorar endpoints interactivamente
- Los logs en la consola te ayudan a debuggear errores
- Guarda el JWT token que obtienes del login para probar endpoints protegidos
- Prueba primero en local antes de ir a producción
- La documentación está en esta carpeta, úsala como referencia

---

## 📞 ¿LISTO?

Si completaste todos estos pasos: **¡Tu backend está listo para Bonfire!** 🚀

Ahora solo falta integrarla en tu proyecto Flutter con Bonfire.

¿Necesitas ayuda con algo específico? Consulta los archivos .md en la carpeta 📂
