CREATE TABLE public.publicacion (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(255),
    descripcion TEXT,
    group_name VARCHAR(255)
);

-- Tabla 'comentario'
CREATE TABLE public.comentario (
    id SERIAL PRIMARY KEY,
    publicacion_id INTEGER REFERENCES public.publicacion(id),
    usuario VARCHAR(255),
    descripcion_comentario TEXT
);

-- Tabla 'imagen'
CREATE TABLE public.imagen (
    id SERIAL PRIMARY KEY,
    url TEXT,
    publicacion_id INTEGER REFERENCES public.publicacion(id),
    comentario_id INTEGER REFERENCES public.comentario(id),
    contenido VARCHAR,
    type_img VARCHAR
);

CREATE TABLE public.videos (
    id SERIAL PRIMARY KEY,
    url TEXT,
    publicacion_id INTEGER REFERENCES public.publicacion(id),
    comentario_id INTEGER REFERENCES public.comentario(id)
);
