import sqlite3
from datetime import datetime
import os.path as path

DB_NAME = "finanzas_personales.db"
SQL_INICIAL = "finanzas_personales_mio.sql"


# Inicializa la base de datos
def init_db():

    # veo si existe el archivo de la db
    if not path.exists(DB_NAME):
        print("No existe el archivo de la db, lo creo...")
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Leer el archivo SQL
        with open(SQL_INICIAL, 'r') as archivo_sql:
            script_sql = archivo_sql.read()

        # Ejecutar el script SQL
        cursor.executescript(script_sql)

        # Confirmar los cambios
        conn.commit()  
        conn.close()
       

# Función que muestra el contenido de la base de datos
async def consulta_sql(sql):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(sql)
                   
    resultado = cursor.fetchall()
    conn.close()

    return resultado
                

# Función que guarda los mensajes en la base de datos
def guardar_operacion(id_usuario, fecha,monto,id_subcategoria,id_medio_pago):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
           
    
   # print("chat:",chat_id," id_usuario: ",id_usuario," monto: " , monto, " subcategoria:",subcategoria," fecha: ",str(fecha)," id_medio_pago:",id_medio_pago)            
            
   # Insertar el mensaje en la tabla
    cursor.execute('''
        INSERT INTO operaciones (id_usuario, id_subcategoria, monto,id_medio_pago)
        VALUES (?, ?, ?, ?)
    ''', (id_usuario, id_subcategoria, monto, id_medio_pago))

    conn.commit()
    conn.close()    

# Función que guarda nueva categoria
def guardar_nueva_categoria(tipo,descripcion):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
              
           
   # Insertar 
    cursor.execute('''
        INSERT INTO categorias (tipo, descripcion)
        VALUES (?, ?)
    ''', (tipo, descripcion))

    conn.commit()
    conn.close()        
         
def actualizar_saldos(id_medio_pago,monto):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
   # print (monto)
   # Insertar el mensaje en la tabla
    cursor.execute('''
        UPDATE medios_pago
           SET saldo = saldo - ?
        WHERE id = ?
    ''', (monto, id_medio_pago))

    conn.commit()
    conn.close()    

def actualizar_descripcion_categoria(id,descripcion):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()              
    print ("update "+id +" con "+ descripcion)
   # Insertar 
    cursor.execute('''
        UPDATE categorias 
           SET descripcion = ?
         WHERE id = ?
    ''', (descripcion,id))

    conn.commit()
    conn.close()        
