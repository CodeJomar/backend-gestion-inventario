-- ============================================================
-- FULL SCHEMA: APP-LEVEL ROLES & PERMISSIONS
-- ============================================================

-- ----------------------------
-- Roles table
-- ----------------------------
CREATE TABLE public.roles (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name text NOT NULL UNIQUE,
    description text,
    created_at timestamptz NOT NULL DEFAULT now(),
    modified_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT roles_pkey PRIMARY KEY (id)
);

-- ----------------------------
-- Permissions table
-- ----------------------------
CREATE TABLE public.permissions (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    name text NOT NULL UNIQUE,
    description text,
    created_at timestamptz NOT NULL DEFAULT now(),
    modified_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT permissions_pkey PRIMARY KEY (id)
);

-- ----------------------------
-- Role-Permissions mapping
-- ----------------------------
CREATE TABLE public.role_permissions (
    role_id uuid NOT NULL REFERENCES public.roles(id) ON DELETE CASCADE,
    permission_id uuid NOT NULL REFERENCES public.permissions(id) ON DELETE CASCADE,
    CONSTRAINT role_permissions_pkey PRIMARY KEY (role_id, permission_id)
);

-- ----------------------------
-- Productos table
-- ----------------------------
CREATE TABLE public.productos (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    nombre text NOT NULL,
    marca text NOT NULL,
    categoria text NOT NULL,
    descripcion text,
    precio numeric NOT NULL CHECK (precio >= 0),
    stock integer DEFAULT 0 CHECK (stock >= 0),
    tipo text DEFAULT 'electrodomestico' CHECK (tipo = ANY (ARRAY['electrodomestico','accesorio','consumible'])),
    imagen_url text,
    created_at timestamptz DEFAULT timezone('utc', now()),
    updated_at timestamptz DEFAULT timezone('utc', now()),
    modified_at timestamptz DEFAULT timezone('utc', now()),
    CONSTRAINT productos_pkey PRIMARY KEY (id)
);

-- ----------------------------
-- Perfiles table (users)
-- ----------------------------
CREATE TABLE public.perfiles (
    id uuid NOT NULL,
    email text NOT NULL UNIQUE,
    nombres text,
    apellidos text,
    usuario text,
    celular text,
    dni text,
    role_id uuid REFERENCES public.roles(id),
    creado_por uuid,
    actualizado_por uuid,
    eliminado_por uuid,
    created_at timestamptz DEFAULT timezone('utc', now()),
    actualizado_en timestamptz,
    deleted_at timestamptz,
    modified_at timestamptz DEFAULT timezone('utc', now()),
    CONSTRAINT perfiles_pkey PRIMARY KEY (id),
    CONSTRAINT perfiles_id_fkey FOREIGN KEY (id) REFERENCES auth.users(id),
    CONSTRAINT perfiles_creado_por_fkey FOREIGN KEY (creado_por) REFERENCES auth.users(id),
    CONSTRAINT perfiles_actualizado_por_fkey FOREIGN KEY (actualizado_por) REFERENCES auth.users(id),
    CONSTRAINT perfiles_eliminado_por_fkey FOREIGN KEY (eliminado_por) REFERENCES auth.users(id)
);

-- ----------------------------
-- Movimientos table
-- ----------------------------
CREATE TABLE public.movimientos (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    producto_id uuid NOT NULL REFERENCES public.productos(id),
    tipo_movimiento text NOT NULL CHECK (tipo_movimiento = ANY (ARRAY['entrada','salida'])),
    cantidad integer NOT NULL CHECK (cantidad > 0),
    motivo text NOT NULL CHECK (motivo = ANY (ARRAY['venta','devolución','reposición','ajuste'])),
    usuario text,
    fecha timestamptz DEFAULT timezone('utc', now()),
    created_at timestamptz DEFAULT timezone('utc', now()),
    modified_at timestamptz DEFAULT timezone('utc', now()),
    CONSTRAINT movimientos_pkey PRIMARY KEY (id)
);

-- ============================================================
-- Triggers for modified_at
-- ============================================================
CREATE OR REPLACE FUNCTION public.touch_modified_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER trigger_roles_modified_at BEFORE UPDATE ON public.roles
FOR EACH ROW EXECUTE FUNCTION public.touch_modified_at();

CREATE TRIGGER trigger_permissions_modified_at BEFORE UPDATE ON public.permissions
FOR EACH ROW EXECUTE FUNCTION public.touch_modified_at();

CREATE TRIGGER trigger_role_permissions_modified_at BEFORE UPDATE ON public.role_permissions
FOR EACH ROW EXECUTE FUNCTION public.touch_modified_at();

CREATE TRIGGER trigger_productos_modified_at BEFORE UPDATE ON public.productos
FOR EACH ROW EXECUTE FUNCTION public.touch_modified_at();

CREATE TRIGGER trigger_perfiles_modified_at BEFORE UPDATE ON public.perfiles
FOR EACH ROW EXECUTE FUNCTION public.touch_modified_at();

CREATE TRIGGER trigger_movimientos_modified_at BEFORE UPDATE ON public.movimientos
FOR EACH ROW EXECUTE FUNCTION public.touch_modified_at();

-- ============================================================
-- RLS only for ownership (no role-based restrictions)
-- ============================================================
ALTER TABLE public.perfiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.movimientos ENABLE ROW LEVEL SECURITY;

-- Users can only access their own profiles
CREATE POLICY "perfiles_select_own" ON public.perfiles
FOR SELECT USING (id = auth.uid());

CREATE POLICY "perfiles_update_own" ON public.perfiles
FOR UPDATE USING (id = auth.uid());

CREATE POLICY "perfiles_insert_own" ON public.perfiles
FOR INSERT WITH CHECK (id = auth.uid());

-- Users can only access their own movimientos
CREATE POLICY "movimientos_select_own" ON public.movimientos
FOR SELECT USING (usuario = auth.uid());

CREATE POLICY "movimientos_insert_own" ON public.movimientos
FOR INSERT WITH CHECK (usuario = auth.uid());
