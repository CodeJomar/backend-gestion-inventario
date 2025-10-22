
create table if not exists productos (
    id uuid primary key default gen_random_uuid(),
    nombre text not null,
    marca text not null,
    categoria text not null,
    descripcion text,
    precio numeric(10,2) not null check (precio >= 0),
    stock integer default 0 check (stock >= 0),
    tipo text check (tipo in ('electrodomestico', 'accesorio', 'consumible')) default 'electrodomestico',
    imagen_url text, -- imagen para mostrar en el frontend
    created_at timestamp with time zone default timezone('utc'::text, now()),
    updated_at timestamp with time zone default timezone('utc'::text, now())
);

create table if not exists movimientos (
    id uuid primary key default gen_random_uuid(),
    producto_id uuid references productos(id) on delete cascade,
    tipo_movimiento text check (tipo_movimiento in ('entrada', 'salida')) not null,
    cantidad integer check (cantidad > 0) not null,
    motivo text check (motivo in ('venta', 'devolución', 'reposición', 'ajuste')) not null,
    usuario text,
    fecha timestamp with time zone default timezone('utc'::text, now()),
    dia integer,
    mes integer,
    anio integer,
    hora text,
    created_at timestamp with time zone default timezone('utc'::text, now())
);