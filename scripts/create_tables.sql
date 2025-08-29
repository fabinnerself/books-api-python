-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create usuarios table (referenced by libros)
CREATE TABLE IF NOT EXISTS "usuarios" (
  "id_user" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "username" VARCHAR(255) NOT NULL UNIQUE,
  "email" VARCHAR(255) NOT NULL UNIQUE,
  "created_at" TIMESTAMP DEFAULT now(),
  "updated_at" TIMESTAMP DEFAULT now()
);

-- Create libros table
CREATE TABLE IF NOT EXISTS "libros" (
  "id_libro" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "name" VARCHAR(255) NOT NULL,
  "author" VARCHAR(255) NOT NULL,
  "price" NUMERIC(10,2) NOT NULL,
  "description" TEXT,
  "created_at" TIMESTAMP DEFAULT now(),
  "updated_at" TIMESTAMP DEFAULT now(),
  "id_user" UUID,
  "is_deleted" BOOLEAN DEFAULT false,
  CONSTRAINT "fk_libros_usuario" 
    FOREIGN KEY ("id_user") 
    REFERENCES "usuarios"("id_user") 
    ON DELETE SET NULL
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS "idx_libros_name" ON "libros"("name");
CREATE INDEX IF NOT EXISTS "idx_libros_author" ON "libros"("author");
CREATE INDEX IF NOT EXISTS "idx_libros_price" ON "libros"("price");
CREATE INDEX IF NOT EXISTS "idx_libros_is_deleted" ON "libros"("is_deleted");
CREATE INDEX IF NOT EXISTS "idx_libros_created_at" ON "libros"("created_at");

-- Insert sample data
INSERT INTO "usuarios" ("username", "email") VALUES
('admin', 'admin@library.com'),
('user1', 'user1@library.com')
ON CONFLICT (username) DO NOTHING;

INSERT INTO "libros" ("name", "author", "price", "description", "id_user") VALUES
('Cien años de soledad', 'Gabriel García Márquez', 25.99, 'Obra maestra del realismo mágico', (SELECT id_user FROM usuarios WHERE username = 'admin')),
('Rayuela', 'Julio Cortázar', 22.50, 'Una novela experimental única', (SELECT id_user FROM usuarios WHERE username = 'admin')),
('Ficciones', 'Jorge Luis Borges', 18.75, 'Colección de cuentos magistrales', (SELECT id_user FROM usuarios WHERE username = 'user1')),
('El Aleph', 'Jorge Luis Borges', 20.00, 'Relatos extraordinarios', (SELECT id_user FROM usuarios WHERE username = 'user1')),
('Pedro Páramo', 'Juan Rulfo', 16.50, 'Clásico de la literatura mexicana', NULL)
ON CONFLICT (id_libro) DO NOTHING;