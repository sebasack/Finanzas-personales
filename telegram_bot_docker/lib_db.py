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
def select_sql(sql):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
      
    try:
        cursor.execute(sql)
    except sqlite3.Error as er:
        print("\nERROR EN SELECT\n"+sql+"\n")
                          
    resultado = cursor.fetchall()
    conn.close()

    return resultado


def insert_sql(tabla,campos,valores):                
    
    resultado_ok = True
      
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()  
    
    separador=''
    values_sql=''
    campos_sql = ''
    for campo in campos:
        campos_sql += separador+ campo  
        values_sql += separador+ ' ?'  
        separador=', '        
    
    sql="INSERT INTO " + tabla + " ("+campos_sql+")  VALUES ("+values_sql+")"
        
    try:
        # Insertar el mensaje en la tabla
        cursor.execute(sql,valores)
    
    except sqlite3.Error as er:
        print("\nERROR EN INSERT en tabla \n" + tabla + "\n")  
        print(campos)
        print(valores)
        print("\n")
        resultado_ok=False
    # get the extended result code here
   
    conn.commit()
    conn.close()  
 
    return resultado_ok

                
def update_sql(tabla,campos,valores,condicion):                
    
    resultado_ok=True
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()  
    
    sql="UPDATE " + tabla + " SET "
    
    separador=''
    for campo in campos:
        sql += separador+ campo  +" = ?"
        separador=', '
        
    sql += " WHERE "+condicion    
        
    try:
        # Insertar el mensaje en la tabla
        cursor.execute(sql,valores)
    
    except sqlite3.Error as er:
        print("\nERROR EN UPDATE en tabla "+tabla)  
        print(campos)
        print(valores)
        print(sql)
        print("\n")
        resultado_ok=False
    # get the extended result code here
   
    conn.commit()
    conn.close()  
    
    return resultado_ok
    

                
def delete_sql(tabla,condicion):  
    
    resultado_ok=True              
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()  
    
    sql="DELETE FROM " + tabla + " WHERE "+condicion    
        
    try:
        # Insertar el mensaje en la tabla
        cursor.execute(sql)
    
    except sqlite3.Error as er:
        print("\nERROR EN DELETE DE tabla "+tabla)  
        print(sql)
        print("\n")
        resultado_ok=False
    # get the extended result code here
   
    conn.commit()
    conn.close()  
    
    return resultado_ok
        
##########################################################################################
##########################################################################################
#                           BORRAR TODAS LAS FUNCIONES DE ABAJO
##########################################################################################
##########################################################################################

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
def guardar_nueva_categoria(descripcion):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
              
    #print ("guradando en db "+descripcion + " cat")
   # Insertar 
    cursor.execute("INSERT INTO categorias ( descripcion) VALUES (?)", (descripcion,))

    conn.commit()
    conn.close()     
    
#funcion que elimina una categoria
def eliminar_categoria(id):    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
              
    #print ("guradando en db "+descripcion + " cat")
   # eliminar 
    cursor.execute("DELETE FROM categorias WHERE id =?", (id,))

    conn.commit()
    conn.close()         
    

#funcion que crea una nueva subcategoria    
def crear_nueva_categoria(tipo,id_categoria,descripcion):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
              
    #print ("guradando en db "+descripcion + " cat")
   # Insertar 
    cursor.execute("INSERT INTO subcategorias ( descripcion,id_categoria,tipo,estado) VALUES (?,?,?,1)", (descripcion,id_categoria,tipo))

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
   # print ("update "+id +" con "+ descripcion)
   # Insertar 
    cursor.execute('''
        UPDATE categorias 
           SET descripcion = ?
         WHERE id = ?
    ''', (descripcion,id))

    conn.commit()
    conn.close()        

def actualizar_descripcion_categoria(id,descripcion)         :

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()              
 #   print ("update "+id +" con "+ descripcion)
   # Insertar 
    cursor.execute('''
        UPDATE subcategorias 
           SET descripcion = ?
         WHERE id = ?
    ''', (descripcion,id))

    conn.commit()
    conn.close()        
    
    
def cambiar_categoria_de_subcategoria(id_subcategoria,id_nueva_categoria):
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()              
  #  print ("update "+id +" con "+ descripcion)
   # Insertar 
    cursor.execute('''
        UPDATE subcategorias 
           SET id_categoria = ?
         WHERE id = ?
    ''', (id_nueva_categoria,id_subcategoria))

    conn.commit()
    conn.close()        
    
def cambiar_tipo_de_subcategoria(id_subcategoria,tipo):
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()              
  #  print ("update "+id +" con "+ descripcion)
   # Insertar 
    cursor.execute('''
        UPDATE subcategorias 
           SET tipo = ?
         WHERE id = ?
    ''', (tipo,id_subcategoria))

    conn.commit()
    conn.close()        


#funcion que crea un nuevo medio de pago
def crear_nuevo_medio_pago(tipo,descripcion):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
              
    #print ("guradando en db "+descripcion + " cat")
   # Insertar 
    cursor.execute("INSERT INTO medios_pago ( descripcion,tipo,activo) VALUES (?,?,1)", (descripcion,tipo))

    conn.commit()
    conn.close()     
                   

                                