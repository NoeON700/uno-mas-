-- PLANTILLA NNA · NEGOCIO (v1) — base de datos del módulo "registro"
-- Pégalo completo en Supabase → SQL Editor → Run, en el proyecto del cliente.
-- Se puede correr más de una vez sin dañar nada.

create table if not exists public.registros (
  id          uuid primary key,
  created_at  timestamptz not null default now(),
  folio       text not null unique check (folio ~ '^[A-Z2-9]{4}-[A-Z2-9]{4}$'),
  nombre      text check (char_length(nombre) <= 120),
  telefono    text check (char_length(telefono) <= 30),
  email       text check (char_length(email) <= 160),
  datos       jsonb not null default '{}'::jsonb
              check (jsonb_typeof(datos) = 'object' and pg_column_size(datos) <= 8000),
  -- Solo el negocio cambia estas dos (desde Supabase o un panel con sesión):
  asistio     boolean not null default false,
  notas       text
);

create index if not exists registros_created_at_idx on public.registros (created_at desc);

alter table public.registros enable row level security;

-- El público solo puede ENVIAR su registro. No puede leer, cambiar ni borrar.
drop policy if exists "Publico puede registrarse" on public.registros;
create policy "Publico puede registrarse"
  on public.registros for insert
  to anon, authenticated
  with check (asistio = false and notas is null);

revoke all on public.registros from anon, authenticated;
grant insert (id, folio, nombre, telefono, email, datos) on public.registros to anon, authenticated;
