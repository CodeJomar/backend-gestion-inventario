-- =====================================
-- 1. Insert base roles
-- =====================================
INSERT INTO public.roles (id, name)
VALUES 
  (gen_random_uuid(), 'Admin'),
  (gen_random_uuid(), 'Empleado')
ON CONFLICT (name) DO NOTHING;

-- =====================================
-- 2. Insert base permissions
-- =====================================
INSERT INTO public.permissions (id, name)
VALUES
  (gen_random_uuid(), 'create_productos', 'Can create products'),
  (gen_random_uuid(), 'update_productos', 'Can update products'),
  (gen_random_uuid(), 'delete_productos', 'Can delete products'),
  (gen_random_uuid(), 'view_productos', 'Can view products'),
  (gen_random_uuid(), 'create_movimientos', 'Can create movements'),
  (gen_random_uuid(), 'update_movimientos', 'Can update movements'),
  (gen_random_uuid(), 'delete_movimientos', 'Can delete movements'),
  (gen_random_uuid(), 'view_movimientos', 'Can view movements'),
  (gen_random_uuid(), 'create_users', 'Can create users'),
  (gen_random_uuid(), 'update_users', 'Can update users'),
  (gen_random_uuid(), 'delete_users', 'Can delete users'),
  (gen_random_uuid(), 'view_users', 'Can view users')
ON CONFLICT (name) DO NOTHING;

-- =====================================
-- 3. Assign all permissions to Admin
-- =====================================
INSERT INTO public.role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM public.roles r
CROSS JOIN public.permissions p
WHERE r.name = 'Admin'
ON CONFLICT (role_id, permission_id) DO NOTHING;

-- =====================================
-- 4. Assign limited permissions to Empleado
-- =====================================
INSERT INTO public.role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM public.roles r
CROSS JOIN public.permissions p
WHERE r.name = 'Empleado'
  AND p.name IN ('create_movimientos','update_movimientos','view_movimientos','view_productos')
ON CONFLICT (role_id, permission_id) DO NOTHING;

-- =====================================
-- 5. Insert initial admin user
-- =====================================
-- Replace 'admin-uuid' with a specific UUID if desired
-- Replace 'admin@example.com' with your email
-- INSERT INTO public.perfiles (id, email, nombres, apellidos, role_id)
-- VALUES (
--     '00000000-0000-0000-0000-000000000001', 
--     'admin@example.com', 
--     'Super', 
--     'Admin', 
--     (SELECT id FROM public.roles WHERE name='Admin')
-- )
-- ON CONFLICT (id) DO NOTHING;
