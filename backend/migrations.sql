-- ============================================================================
-- SQL Migration - Alineación con Script Original
-- ============================================================================
-- Este archivo contiene las correcciones necesarias para alinear la BD
-- con el script SQL original y el código Python actualizado
-- ============================================================================

-- 1. Agregar campos faltantes a tabla existente
-- ============================================================================

-- Agregar campo 'tipo' a tabla Animales (del script original)
ALTER TABLE "Animales" ADD COLUMN IF NOT EXISTS "tipo" VARCHAR(50);

-- Agregar campo 'zona' a tabla Mapa (del script original)
ALTER TABLE "Mapa" ADD COLUMN IF NOT EXISTS "zona" VARCHAR(100);

-- 2. Crear tabla Mapa_Item (relación 1:N - Mapa DA Items)
-- ============================================================================
-- Solo si no existe
CREATE TABLE IF NOT EXISTS "Mapa_Item" (
    "id" SERIAL PRIMARY KEY,
    "id_mapa" INTEGER NOT NULL REFERENCES "Mapa"(id) ON DELETE CASCADE,
    "id_item" INTEGER NOT NULL REFERENCES "Item"(id) ON DELETE CASCADE,
    "quantity_available" INTEGER DEFAULT 1 NOT NULL,
    UNIQUE("id_mapa", "id_item")
);

CREATE INDEX IF NOT EXISTS idx_mapa_item_map ON "Mapa_Item"("id_mapa");
CREATE INDEX IF NOT EXISTS idx_mapa_item_item ON "Mapa_Item"("id_item");

-- 3. Crear tabla Enemigo (ISA - hereda de NPC)
-- ============================================================================
CREATE TABLE IF NOT EXISTS "Enemigo" (
    "id_npc" INTEGER PRIMARY KEY REFERENCES "NPC"(id) ON DELETE CASCADE,
    "nivel" INTEGER DEFAULT 1 NOT NULL CHECK ("nivel" > 0 AND "nivel" <= 100),
    "dano" INTEGER DEFAULT 10 NOT NULL CHECK ("dano" > 0)
);

CREATE INDEX IF NOT EXISTS idx_enemigo_nivel ON "Enemigo"("nivel");

-- 4. Crear tabla Aldeano (ISA - hereda de NPC)
-- ============================================================================
CREATE TABLE IF NOT EXISTS "Aldeano" (
    "id_npc" INTEGER PRIMARY KEY REFERENCES "NPC"(id) ON DELETE CASCADE
);

-- 5. Optimizaciones - Crear índices para mejorar performance
-- ============================================================================

-- Índices en tablas principales
CREATE INDEX IF NOT EXISTS idx_jugador_user_id ON "Jugador"("user_id");
CREATE INDEX IF NOT EXISTS idx_jugador_mapa_id ON "Jugador"("current_map_id");
CREATE INDEX IF NOT EXISTS idx_captura_jugador ON "Captura"("player_id");
CREATE INDEX IF NOT EXISTS idx_captura_animal ON "Captura"("animal_id");
CREATE INDEX IF NOT EXISTS idx_jugador_item_player ON "Jugador_Item"("player_id");
CREATE INDEX IF NOT EXISTS idx_jugador_item_item ON "Jugador_Item"("item_id");
CREATE INDEX IF NOT EXISTS idx_mapa_npc_map ON "Mapa_NPC"("id_mapa");
CREATE INDEX IF NOT EXISTS idx_mapa_npc_npc ON "Mapa_NPC"("id_npc");

-- 6. Agregar datos de ejemplo (OPCIONAL)
-- ============================================================================

-- Insertar Mapas de ejemplo si están vacíos
INSERT INTO "Mapa" (name, zona, required_level) VALUES
    ('Bosque Encantado', 'Verde', 1),
    ('Montaña Sagrada', 'Montaña', 5),
    ('Templo Oscuro', 'Ruinas', 10)
ON CONFLICT DO NOTHING;

-- Insertar Animales de ejemplo
INSERT INTO "Animales" (name, tipo, rarity) VALUES
    ('Pikachu', 'Eléctrico', 'Común'),
    ('Charizard', 'Fuego/Volador', 'Raro'),
    ('Blastoise', 'Agua', 'Raro'),
    ('Venusaur', 'Planta', 'Raro')
ON CONFLICT DO NOTHING;

-- Insertar NPCs de ejemplo
INSERT INTO "NPC" (name, role) VALUES
    ('Viejo Sabio', 'Aldeano'),
    ('Soldado Oscuro', 'Enemigo'),
    ('Mercader de Hierbas', 'Aldeano'),
    ('Dragón Antiguo', 'Enemigo')
ON CONFLICT DO NOTHING;

-- Insertar Enemigos (relación ISA)
-- Nota: Asumiendo que los NPCs con ID 2 y 4 son enemigos
INSERT INTO "Enemigo" (id_npc, nivel, dano) VALUES
    (2, 5, 15),
    (4, 20, 50)
ON CONFLICT DO NOTHING;

-- Insertar Aldeanos (relación ISA)
-- Nota: Los NPCs con ID 1 y 3 son aldeanos
INSERT INTO "Aldeano" (id_npc) VALUES
    (1),
    (3)
ON CONFLICT DO NOTHING;

-- Insertar Items de ejemplo
INSERT INTO "Item" (name, description, price) VALUES
    ('Poción de Vida', 'Recupera 50 HP', 100),
    ('Poción de Mana', 'Recupera 50 MP', 150),
    ('Espada de Hierro', 'Arma básica', 500),
    ('Escudo de Madera', 'Defensa básica', 300)
ON CONFLICT DO NOTHING;

-- Insertar relaciones Mapa_Item
INSERT INTO "Mapa_Item" (id_mapa, id_item, quantity_available) VALUES
    (1, 1, 5),
    (1, 2, 3),
    (2, 3, 2),
    (3, 4, 1)
ON CONFLICT ("id_mapa", "id_item") DO NOTHING;

-- 7. Crear vistas útiles para el backend (OPCIONAL)
-- ============================================================================

-- Vista para obtener enemigos con información completa
CREATE OR REPLACE VIEW v_enemigos_info AS
SELECT 
    e.id_npc,
    n.name,
    n.role,
    e.nivel,
    e.dano
FROM "Enemigo" e
JOIN "NPC" n ON e.id_npc = n.id;

-- Vista para obtener aldeanos con información completa
CREATE OR REPLACE VIEW v_aldeanos_info AS
SELECT 
    a.id_npc,
    n.name,
    n.role
FROM "Aldeano" a
JOIN "NPC" n ON a.id_npc = n.id;

-- Vista para obtener items disponibles en un mapa
CREATE OR REPLACE VIEW v_mapa_items_info AS
SELECT 
    mi.id_mapa,
    m.name as map_name,
    mi.id_item,
    i.name as item_name,
    i.price,
    mi.quantity_available
FROM "Mapa_Item" mi
JOIN "Mapa" m ON mi.id_mapa = m.id
JOIN "Item" i ON mi.id_item = i.id;

-- ============================================================================
-- Verificación de Integridad
-- ============================================================================

-- Después de ejecutar estas migraciones, verifica:
-- SELECT * FROM "Enemigo";
-- SELECT * FROM "Aldeano";
-- SELECT * FROM "Mapa_Item";
-- SELECT * FROM v_enemigos_info;
-- SELECT * FROM v_aldeanos_info;
-- SELECT * FROM v_mapa_items_info;

-- 8. Stripe purchases (idempotencia por payment_intent_id)
CREATE TABLE IF NOT EXISTS stripe_purchase (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    payment_intent_id VARCHAR(255) NOT NULL UNIQUE,
    pack_id VARCHAR(64) NOT NULL,
    currency_type VARCHAR(32) NOT NULL,
    quantity INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    currency VARCHAR(10) NOT NULL,
    status VARCHAR(32) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
