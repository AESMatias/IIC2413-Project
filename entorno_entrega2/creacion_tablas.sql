SET datestyle = 'SQL, DMY';

-- Comuna
CREATE TABLE Comuna (
    cut INTEGER NOT NULL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    provincia VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL
);


-- Sucursal
CREATE TABLE Sucursal (
    id SERIAL PRIMARY KEY,
    sucursal VARCHAR(200) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    telefono VARCHAR(100) NOT NULL CHECK (
        telefono ~ '^\+56.*$'
    ),
    area_despacho VARCHAR(100) NOT NULL,
    repartomin INTEGER,
    puntaje INTEGER DEFAULT 0 CHECK (puntaje BETWEEN 0 AND 5),
    veces_punteado INTEGER DEFAULT 0 CHECK (veces_punteado >= 0)
    );


-- Restaurante
CREATE TABLE Restaurante (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL UNIQUE,
    estilo VARCHAR(200) NOT NULL,
    vigente BOOLEAN NOT NULL,
    prec_min_repar_gratis INTEGER NOT NULL,
    puntaje INTEGER DEFAULT 0 CHECK (puntaje BETWEEN 0 AND 5),
    veces_punteado INTEGER DEFAULT 0 CHECK (veces_punteado >= 0)
    -- telefono INTEGER NOT NULL (No tendra telefono, porque las sucursales tienen)
);

-- Agregar la llave foranea a Sucursal
ALTER TABLE Sucursal
ADD COLUMN nombre_restaurante VARCHAR(200) NOT NULL,
ADD CONSTRAINT fk_sucursal_restaurante FOREIGN KEY (nombre_restaurante) REFERENCES Restaurante(nombre);
-- -- Agregar la llave foranea a Restaurante
-- ALTER TABLE Restaurante
-- ADD COLUMN nombre_sucursal VARCHAR(30) NOT NULL,
-- ADD CONSTRAINT fk_restaurante_sucursal FOREIGN KEY (nombre_sucursal) REFERENCES Sucursal(nombre);


-- Delivery
CREATE TABLE Delivery (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    vigente BOOLEAN NOT NULL,
    telefono VARCHAR(100) UNIQUE NOT NULL CHECK (
        telefono ~ '^\+56.*$'
    ),
    tiempo_despacho INTEGER NOT NULL,
    precio_uni_despacho INTEGER,
    precio_sus_mensual INTEGER CHECK (precio_sus_mensual <= 4 * precio_uni_despacho),
    precio_sus_anual INTEGER CHECK (precio_sus_mensual <= 12 * precio_uni_despacho),
    puntaje INTEGER DEFAULT 0 CHECK (puntaje BETWEEN 0 AND 5),
    veces_punteado INTEGER DEFAULT 0 CHECK (veces_punteado >= 0)
);

-- Despachador
CREATE TABLE Despachador (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(200) UNIQUE CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$'),
    telefono VARCHAR(100) NOT NULL CHECK (
        telefono ~ '^\+56.*$'
    ),
    puntaje INTEGER DEFAULT 0 CHECK (puntaje BETWEEN 0 AND 5),
    veces_punteado INTEGER DEFAULT 0 CHECK (veces_punteado >= 0)

--deberia ir atiende pedido? o algo asi

    -- atiende_delivery INTEGER,
    -- atiende_restaurante INTEGER,
    -- atiende_sucursal INTEGER,
    -- FOREIGN KEY (atiende_delivery) REFERENCES Delivery(id),
    -- FOREIGN KEY (atiende_restaurante) REFERENCES Restaurante(id),
    -- FOREIGN KEY (atiende_sucursal) REFERENCES Sucursal(id)
);



-- Plato
CREATE TABLE Plato (
    id INTEGER NOT NULL PRIMARY KEY,
    nombre_restaurante VARCHAR(1000) NOT NULL,
    nombre VARCHAR(1000) NOT NULL,
    descripcion VARCHAR(1000) NOT NULL,
    precio INTEGER NOT NULL,
    ingredientes VARCHAR(1000),
    disponibilidad BOOLEAN NOT NULL,
    porciones INTEGER NOT NULL DEFAULT 1 CHECK (porciones >= 1),
    tiempo_preparacion INTEGER NOT NULL DEFAULT 5 
    CHECK (tiempo_preparacion BETWEEN 5 AND 60),
    estilo VARCHAR(1000) NOT NULL,
    restriccion INTEGER,--(vegano,vegetariano,alergénos,etc)
    FOREIGN KEY (nombre_restaurante) REFERENCES Restaurante(nombre),
    vigente BOOLEAN NOT NULL,
    repartomin INTEGER NOT NULL
);

-- -- Administrador
-- CREATE TABLE Administrador (
--     id SERIAL PRIMARY KEY,
--     nombre VARCHAR(100) NOT NULL,
--     email VARCHAR(200) UNIQUE NOT NULL CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$'),
--     clave VARCHAR(200) NOT NULL
-- );

-- Usuario
CREATE TABLE Usuario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$'),
    telefono VARCHAR(100) UNIQUE NOT NULL CHECK (
        telefono ~ '^\+56.*$'
    ),
    clave VARCHAR(200) NOT NULL,
    puntaje INTEGER DEFAULT 0 CHECK (puntaje BETWEEN 0 AND 5),
    veces_punteado INTEGER DEFAULT 0 CHECK (veces_punteado >= 0),
    tipo VARCHAR(100) DEFAULT 'cliente' CHECK (tipo IN ('cliente', 'administrador'))
);

-- Direccion
CREATE TABLE Direccion (
    id SERIAL PRIMARY KEY,
    cliente_email VARCHAR(200) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    comuna_cut INTEGER NOT NULL,
    -- calle VARCHAR(100) NOT NULL,
    -- numero INTEGER, -- Puede ser nulo en ciertos casos.
    -- region VARCHAR(50) NOT NULL,
    -- comuna VARCHAR(50) NOT NULL,
    -- departamento INTEGER,
    FOREIGN KEY (cliente_email) REFERENCES Usuario(email),
    FOREIGN KEY (comuna_cut) REFERENCES Comuna(cut)
);

-- Pedido
CREATE TABLE Pedido (
    id INTEGER PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME WITH TIME ZONE NOT NULL,
    costo INTEGER DEFAULT 0 CHECK (costo >= 0),
    plato VARCHAR(200) NOT NULL,
    estado VARCHAR(100) NOT NULL CHECK (estado IN ('en preparacion', 'pendiente', 
    'entregado a despachador', 'entregado a cliente', 'Cliente cancela',
    'delivery cancela','restaurant cancela')),
    -- calificacion_cliente INTEGER CHECK (calificacion_cliente BETWEEN 1 AND 5),
    -- calificacion_pedido INTEGER CHECK (calificacion_pedido BETWEEN 1 AND 5),
    -- id_sucursal INTEGER,

    -- id_sucursal INTEGER NOT NULL,
    nombre_delivery VARCHAR(100) NOT NULL,
    nombre_despachador VARCHAR(100) NOT NULL,
    email VARCHAR(200) NOT NULL CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$'),
    sucursal VARCHAR(200) NOT NULL,
    id_sucursal INTEGER NOT NULL,

    -- FOREIGN KEY (nombre_sucursal) REFERENCES Sucursal(sucursal),
    FOREIGN KEY (nombre_despachador) REFERENCES Despachador(nombre),
    FOREIGN KEY (nombre_delivery) REFERENCES Delivery(nombre),
    -- FOREIGN KEY (id_sucursal) REFERENCES Sucursal(id),
    FOREIGN KEY (email) REFERENCES Usuario(email),
    FOREIGN KEY (id_sucursal) REFERENCES Sucursal(id)
);

-- Calificacion
CREATE TABLE Calificacion (
    id SERIAL PRIMARY KEY,
    id_pedido INTEGER NOT NULL,
    calificacion_pedido INTEGER NOT NULL CHECK (calificacion_pedido BETWEEN 1 AND 5),
    calificacion_cliente INTEGER NOT NULL CHECK (calificacion_cliente BETWEEN 1 AND 5),
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id)
);

-- Suscripcion
CREATE TABLE Suscripcion (
    id SERIAL PRIMARY KEY,
    nombre_delivery VARCHAR(100) NOT NULL,
    monto_ultimo_pago INTEGER,
    fecha_ultimo_pago DATE,
    estado VARCHAR(100) NOT NULL CHECK (estado IN ('Vigente', 'Cancelada')),
    ciclo_facturacion VARCHAR(100) NOT NULL CHECK (ciclo_facturacion IN ('Mensual', 'Anual')),

    id_delivery INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    email VARCHAR(200) NOT NULL CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,}$'),
    FOREIGN KEY (id_delivery) REFERENCES Delivery(id),
    FOREIGN KEY (id_cliente) REFERENCES Usuario(id),
    FOREIGN KEY (nombre_delivery) REFERENCES Delivery(nombre),
    FOREIGN KEY (email) REFERENCES Usuario(email)
);

--- TABLAS INTERMDIOAS ---

-- Asignado
CREATE TABLE Asignado (
    id_despachador INTEGER NOT NULL,
    id_pedido INTEGER NOT NULL,
    FOREIGN KEY (id_despachador) REFERENCES Despachador(id),
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id)
);

-- Se_compone
CREATE TABLE Se_compone (
    id SERIAL PRIMARY KEY,
    id_pedido INTEGER NOT NULL,
    id_plato INTEGER NOT NULL,
    cantidad INT,
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id),
    FOREIGN KEY (id_plato) REFERENCES Plato(id)
);

-- -- AdministraR
-- CREATE TABLE AdministraR (
--     id_admin INTEGER NOT NULL,
--     id_restaurante INTEGER NOT NULL,
--     accion accion_admin NOT NULL,
--     FOREIGN KEY (id_admin) REFERENCES Administrador(id),
--     FOREIGN KEY (id_restaurante) REFERENCES Restaurante(id),
--     CHECK (accion IN ('eliminar', 'modificar', 'agregar'))
-- );


-- -- AdministraD
-- CREATE TABLE AdministraD (
--     id_admin INTEGER NOT NULL,
--     id_delivery INTEGER NOT NULL,
--     accion accion_admin NOT NULL,
--     FOREIGN KEY (id_admin) REFERENCES Administrador(id),
--     FOREIGN KEY (id_delivery) REFERENCES Delivery(id),
--     CHECK (accion IN ('eliminar', 'modificar', 'agregar'))
-- );


-- Delivery_de_Sucursal
CREATE TABLE Delivery_de_Sucursal (
    id SERIAL PRIMARY KEY,
    id_sucursal INTEGER NOT NULL,
    id_delivery INTEGER NOT NULL,
    propio BOOLEAN NOT NULL,
    FOREIGN KEY (id_sucursal) REFERENCES Sucursal(id),
    FOREIGN KEY (id_delivery) REFERENCES Delivery(id)
);

-- Delivery_de_Restaurante
-- CREATE TABLE Delivery_de_Restaurante (
--     id SERIAL PRIMARY KEY,
--     id_restaurante INTEGER NOT NULL,
--     id_delivery INTEGER NOT NULL,
--     propio BOOLEAN NOT NULL,
--     FOREIGN KEY (id_restaurante) REFERENCES Restaurante(id),
--     FOREIGN KEY (id_delivery) REFERENCES Delivery(id)
-- );

-- Trigger para actualizar el cifrado de clave cliente y administrador --
CREATE EXTENSION IF NOT EXISTS pgcrypto;  -- Necesario para usar funciones de cifrado como bcrypt

CREATE OR REPLACE FUNCTION encrypt_password()
  RETURNS TRIGGER AS
$$
BEGIN
  NEW.clave := crypt(NEW.clave, gen_salt('bf'));  -- 'bf' indica el uso de bcrypt
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER encrypt_userdata
BEFORE INSERT ON usuario
FOR EACH ROW
EXECUTE FUNCTION encrypt_password();

-- -- Trigger para cifrar la clave del administrador --
-- CREATE OR REPLACE FUNCTION encrypt_password_2()
--   RETURNS TRIGGER AS
-- $$
-- BEGIN
--   NEW.clave := crypt(NEW.clave, gen_salt('bf'));  -- 'bf' indica el uso de bcrypt
--   RETURN NEW;
-- END
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER encrypt_administrador
-- BEFORE INSERT ON administrador
-- FOR EACH ROW
-- EXECUTE FUNCTION encrypt_password_2();


-- Trigger para actualizar puntajes del cliente --
CREATE OR REPLACE FUNCTION actualizar_puntaje_cliente() RETURNS TRIGGER AS $$
DECLARE
    cliente_email TEXT;
BEGIN
    -- Obtener el email del cliente asociado al id_pedido en la nueva calificación
    SELECT email INTO cliente_email FROM Pedido WHERE id = NEW.id_pedido;
    -- Actualizar el puntaje del cliente
    UPDATE usuario
    SET puntaje = ((puntaje * veces_punteado) + NEW.calificacion_cliente) / (veces_punteado + 1),
        veces_punteado = veces_punteado + 1
    WHERE email = cliente_email;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_puntaje
AFTER INSERT ON calificacion
FOR EACH ROW
EXECUTE FUNCTION actualizar_puntaje_cliente();

-- Trigger para actualizar puntajes del despachador --
CREATE OR REPLACE FUNCTION actualizar_puntaje_despachador() RETURNS TRIGGER AS $$
DECLARE
    despachador_nombre TEXT;
    calificacion_despachador INTEGER;
BEGIN
    -- Obtener el nombre del despachador asociado al id_pedido en la nueva calificación
    SELECT nombre_despachador, calificacion_pedido INTO despachador_nombre, calificacion_despachador
    FROM Pedido INNER JOIN calificacion ON Pedido.id = NEW.id_pedido;
    
    -- Actualizar el puntaje del despachador
    UPDATE despachador
    SET puntaje = ((puntaje * veces_punteado) + calificacion_despachador) / (veces_punteado + 1),
        veces_punteado = veces_punteado + 1
    WHERE nombre = despachador_nombre;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_puntaje_despachador
AFTER INSERT ON calificacion
FOR EACH ROW
EXECUTE FUNCTION actualizar_puntaje_despachador();


-- Trigger para actualizar puntajes de la sucursal --
CREATE OR REPLACE FUNCTION actualizar_puntaje_sucursal() RETURNS TRIGGER AS $$
DECLARE
    id_sucursal_pedido INT;
    calificacion_pedido INTEGER;
BEGIN
    -- Obtener el id de la sucursal asociada al pedido en la nueva calificación
    SELECT p.id_sucursal, c.calificacion_pedido INTO id_sucursal_pedido, calificacion_pedido
    FROM pedido p INNER JOIN calificacion c ON p.id = NEW.id_pedido;
    
    -- Actualizar el puntaje de la sucursal
    UPDATE sucursal
    SET puntaje = ((puntaje * veces_punteado) + calificacion_pedido) / (veces_punteado + 1),
        veces_punteado = veces_punteado + 1
    WHERE id = id_sucursal_pedido;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- -- Trigger para actualizar puntajes de la restaurante TODO: INCOMPLETO--
-- CREATE OR REPLACE FUNCTION actualizar_puntaje_restaurante() RETURNS TRIGGER AS $$
-- DECLARE
--     id_restaurante_pedido INT;
--     sucursal_id_pedido INT;
--     calificacion_pedido INTEGER;
-- BEGIN
--     -- Obtener el id de la restaurante asociada al pedido en la nueva calificación
--     SELECT p.id_sucursal, c.calificacion_pedido, INTO id_restaurante_pedido, calificacion_pedido
--     FROM sucursal s, restaurante r INNER JOIN calificacion c ON p.id = NEW.id_pedido AND s.nombre_nombre_restaurante = r.nombre;
    
--     -- Actualizar el puntaje del restaurante
--     UPDATE restaurante
--     SET puntaje = ((puntaje * veces_punteado) + calificacion_pedido) / (veces_punteado + 1),
--         veces_punteado = veces_punteado + 1
--     WHERE id = id_restaurante_pedido;

--     RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;

-- CREATE TRIGGER trigger_actualizar_puntaje_restaurante
-- AFTER INSERT ON calificacion
-- FOR EACH ROW
-- EXECUTE FUNCTION actualizar_puntaje_restaurante();


-- Trigger para actualizar precio por suscricion mensual y anual en
-- en la tabla 