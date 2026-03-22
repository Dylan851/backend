# 🎮 Endpoints para Bonfire/Flutter

## 📍 Autenticación
```
POST /auth/register       - Registrar nuevo usuario
POST /auth/login          - Iniciar sesión
POST /auth/refresh-token  - Refrescar token JWT
```

## 👤 Jugador
```
GET  /player/profile      - Obtener perfil del jugador
PUT  /player/location     - Actualizar ubicación (GPS)
GET  /player/inventory    - Obtener inventario del jugador
```

## 🗺️ Mapas
```
GET  /maps                      - Obtener todos los mapas
GET  /maps/unlocked             - Obtener mapas desbloqueados por jugador
POST /maps/unlock               - Desbloquear nuevo mapa
```

## 🧙 NPCs
```
GET  /npc/map/{map_id}          - Obtener NPCs de un mapa
GET  /npc/{npc_id}              - Obtener detalles de un NPC
```

## ⚔️ Enemigos
```
GET  /enemies/map/{map_id}      - Obtener Enemigos de un mapa
GET  /enemies/{enemy_id}        - Obtener detalles de un Enemigo
POST /enemies/{enemy_id}/defeat - Registrar derrota de enemigo (gana experiencia)
```

## 🦁 Animales
```
GET  /animals/nearby            - Obtener animales cercanos en el mapa actual
POST /animals/capture           - Capturar un animal
```

## 🛍️ Tienda
```
GET  /shop/items                - Obtener items disponibles
POST /shop/purchase             - Comprar item
GET  /shop/history              - Ver historial de compras
```

---

## 📊 Estructura de Respuestas

### ✅ Respuesta Exitosa
```json
{
  "success": true,
  "data": {
    // Datos específicos del endpoint
  }
}
```

### ❌ Respuesta de Error
```json
{
  "success": false,
  "error": "Descripción del error"
}
```

---

## 🎯 Ejemplos de Uso

### Obtener NPCs de un mapa
```bash
curl -X GET "http://localhost:8000/npc/map/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Respuesta:
```json
{
  "success": true,
  "data": {
    "npcs": [
      {"id": 1, "name": "Viejo Sabio", "role": "Aldeano"},
      {"id": 2, "name": "Soldado Oscuro", "role": "Enemigo"}
    ],
    "total": 2
  }
}
```

### Obtener Enemigos de un mapa
```bash
curl -X GET "http://localhost:8000/enemies/map/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Respuesta:
```json
{
  "success": true,
  "data": {
    "enemies": [
      {"id": 2, "name": "Soldado Oscuro", "nivel": 5, "dano": 15},
      {"id": 3, "name": "Goblin", "nivel": 3, "dano": 8}
    ],
    "total": 2
  }
}
```

### Derrotar un enemigo
```bash
curl -X POST "http://localhost:8000/enemies/2/defeat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Respuesta:
```json
{
  "success": true,
  "data": {
    "enemy_id": 2,
    "experience_gained": 150,
    "message": "You defeated Soldado Oscuro and gained 150 experience!"
  }
}
```

---

## 🔐 Headers Requeridos

Todos los endpoints que requieren autenticación necesitan:
```
Authorization: Bearer <JWT_TOKEN>
```

---

## 🚀 Implementación en Bonfire

### 1. Detectar Enemigos Cercanos
```dart
// En Bonfire, implementar detección de enemigos basada en GPS
Future<List<Enemy>> getNearbyEnemies(double lat, double lng) async {
  final response = await api.get('/enemies/map/${currentMapId}');
  // Filtrar por distancia GPS
  return enemies.where((e) => distanceInMeters(lat, lng, e.lat, e.lng) < 100).toList();
}
```

### 2. Interactuar con NPC
```dart
Future<void> talkToNpc(int npcId) async {
  final npc = await api.get('/npc/$npcId');
  // Mostrar diálogo
  showNpcDialog(npc);
}
```

### 3. Combate con Enemigos
```dart
Future<bool> battleEnemy(int enemyId) async {
  // Simular combate en Bonfire
  final defeated = await simulateBattle(enemy);
  if (defeated) {
    final result = await api.post('/enemies/$enemyId/defeat');
    // Actualizar experiencia del jugador
    player.addExperience(result.experience_gained);
  }
  return defeated;
}
```

---

## 📝 Notas Importantes

1. **Geolocalización**: Flutter necesita permisos GPS para obtener ubicación
2. **Rate Limiting**: Implementar limite de requests para evitar spam
3. **Caché**: Mapas y NPCs no cambian frecuentemente, guardar en caché local
4. **Sincronización**: Manejar conflictos cuando el servidor y cliente no están sincronizados
5. **Offline Mode**: Guardar datos locales para modo offline

---

## 🔄 Flujo de Juego Recomendado

1. **Carga Inicial**
   - Obtener lista de mapas
   - Guardar en caché local (sin cambios frecuentes)

2. **Cuando Entras a un Mapa**
   - Obtener ubicación GPS actual
   - Actualizar posición del jugador
   - Cargar NPCs y Enemigos del mapa

3. **Exploración**
   - Detectar animales cercanos
   - Detectar enemigos cercanos
   - Mostrar interactividad en el mapa

4. **Interacción**
   - Si encuentras un NPC: Mostrar diálogo
   - Si encuentras un Enemigo: Iniciar batalla
   - Si encuentras un Animal: Capturar

5. **Después de Interacción**
   - Actualizar experiencia/nivel si derrotaste enemigo
   - Actualizar inventario si capturaste animal
   - Actualizar ubicación continuamente
