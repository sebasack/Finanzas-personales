-- Crear una tabla para almacenar los usuarios

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    user_id INTEGER,        
    nivel INTEGER
);

    

-- Inserto usuario administrador

INSERT INTO usuarios ( nombre, user_id, nivel) VALUES  
    ('Sebastian', 1252230064,0);
         


-- Crear una tabla para almacenar las medios de pago

CREATE TABLE IF NOT EXISTS medios_pago (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo INTEGER,     -- 0=efectivo, 1=debito, 2=credito
    descripcion TEXT,
    saldo REAL,
    dia_cierre INTEGER,        
    dia_pago INTEGER
);
        
       
INSERT INTO medios_pago (tipo, descripcion, saldo) VALUES
    (0,'Efectivo',0),
    (1,'Mercado pago',0), 
    (2,'VISA',0);


-- Crear una tabla para almacenar la relacion entre medios de pago y usuarios

CREATE TABLE IF NOT EXISTS medios_pago_usuarios (
    id_medio_pago INTEGER,     
    id_usuario INTEGER,
    foreign key(id_medio_pago) references medios_pago(id),
    foreign key(id_usuario) references usuarios(id)
);
    

INSERT INTO medios_pago_usuarios (id_medio_pago, id_usuario) VALUES 
    (1,1),
    (2,1),
    (3,1);
    

-- Crear una tabla de categorias

CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT,
    tipo INTEGER -- (0=entrada,1=salida, 2=ambas)
);

    
INSERT INTO categorias (descripcion, tipo) VALUES
    ('Ingresos',0), 
    ('Impuestos',1),
    ('Supermercado',1),
    ('Transferencias',2);

-- Crear una tabla de subcategorias

CREATE TABLE IF NOT EXISTS subcategorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT,
    id_categoria INTEGER,
    foreign key(id_categoria) references categorias(id)
);

INSERT INTO subcategorias (descripcion, id_categoria)  VALUES 
    ('Acreditacion sueldo',1), 
    ('Municipal',2), 
    ('Franco',3),     
    ('Chango Mas',3),
    ('Cooperativa',3);                          
  



-- Crear una tabla para almacenar las operaciones

CREATE TABLE IF NOT EXISTS operaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    id_subcategoria INTEGER,
    fecha  DATETIME DEFAULT CURRENT_TIMESTAMP,
    monto REAL,        
    id_medio_pago INTEGER,
    cuota INTEGER,
    foreign key(id_usuario) references usuarios(id),     
    foreign key(id_subcategoria) references subcategorias(id),     
    foreign key(id_medio_pago) references medios_pago(id)    
);