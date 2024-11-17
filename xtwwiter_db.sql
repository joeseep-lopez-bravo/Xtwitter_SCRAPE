CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE public.publicacion (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(255),
    descripcion TEXT,
    group_name VARCHAR(255),
    likes VARCHAR(255),
    id_unico UUID DEFAULT uuid_generate_v4()
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

CREATE TABLE public.retweet (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL,
    publicacion_id INTEGER NOT NULL,
    FOREIGN KEY (publicacion_id) REFERENCES publicacion(id)
);



