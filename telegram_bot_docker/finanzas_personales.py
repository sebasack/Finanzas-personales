

 

from menues import * #Importamos todas las funciones de menues
import os
import re       
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
  
# Obtener el token desde la variable de entorno
TOKEN = os.getenv('TELEGRAM_TOKEN')
 
def es_numero(texto):
    try:
        # Intentamos convertir el texto a un número flotante
        float(texto)
        return True
    except ValueError:
        return False
    

# Diccionario para almacenar los ids de usuarios y no ir a la db cada vez que se necesita
cache_ids_usuarios = {}    
async def id_usuario_db(user_id):

    if  user_id in cache_ids_usuarios:
        # uso en valor en el cache
        id_usuario= cache_ids_usuarios[user_id]         
    else:             
        # Obtener el resultado
        id_usuario = await consulta_sql("SELECT id FROM usuarios where user_id = "+str(user_id))        
       
        if len( id_usuario) == 1:          
            cache_ids_usuarios[user_id]=id_usuario[0][0]    
        else:
            print ('USUARIO '+ str(user_id) +' NO CARGADO')
            cache_ids_usuarios[user_id]=-1       
  
    return id_usuario


# Función que muestra el contenido de la base de datos
async def mostrar_operaciones(query):    
    
    items_str="No hay operaciones para mostrar."

    items = await consulta_sql('''SELECT op.fecha  || ' ' || us.nombre || ' $' || op.monto 
                                    FROM operaciones op
                                         JOIN usuarios us on us.id=op.id_usuario
                                   ORDER BY op.fecha
                               ''')

    if items:
        # Crear un string con los nombres de los items
        items_str = '\n'.join([item[0] for item in items])
        items_str="Operaciones:\n" + items_str
      

 
    if query.message.text.lower() == 'operaciones': # se escribio saldos o se apreto el boton
        await query.message.reply_text(items_str)       
    else: # se pidieron saldos desde el menu ppal        
        await query.edit_message_text(items_str)
      

# Función que muestra el contenido de la base de datos
async def mostrar_saldos(query):
    
     
    items_str="No hay saldos para mostrar."
   
    items = await consulta_sql("SELECT descripcion || ' $' || saldo FROM medios_pago mp   ")
    
    
    if items:
        # Crear un string con los nombres de los items
        items_str = '\n'.join([item[0] for item in items])
        items_str="Saldos:\n" + items_str
    
    
    if query.message.text.lower() == 'saldos': # se escribio saldos o se apreto el boton
        await query.message.reply_text(items_str)       
    else: # se pidieron saldos desde el menu ppal        
        await query.edit_message_text(items_str)
      
        
           

# Función que procesa los mensajes de texto
async def process_message(update: Update, context):
        
        
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    
    
    
    await id_usuario_db(user_id)
        
    text = update.message.text
    
    estado = ''
    
    if user_id in user_states:
        if 'estado' in user_states[user_id].keys():
            estado = user_states[user_id]['estado']
    else:
         print ('USERID NO DEFINIDO')
         
    print ('ingreso:' + text)
    print ( user_states)
        
    # elimino espacios dobles
    temp = text.split(" ")
    text = " ".join(temp)

    # quito espacios al principio y al final
    text = text.strip()

    #reemplazo el punto por la coma
    text=text.replace(',','.')
    
    if estado.startswith( 'nueva_categoria'):
    #    print(user_states[user_id]['estado'])
   #     print('estoy creando nueva categoria! '+text)
        tipo = 0 
        texto_tipo='Ingreso'
        if estado.endswith('gastos'):
            tipo = 1 
            texto_tipo='Gasto'

        await update.message.reply_text('Se creo una nueva categoria de tipo "'+texto_tipo+'" llamada "'+text+'"')
        guardar_nueva_categoria(tipo,text)
      #  print('FALTA GUARDAR EN DB LA CATEGORIA')
        user_states[user_id] = {"estado":""}

    elif estado.startswith( 'modificar_categoria_') and estado.endswith( 'descripcion')  :
           # saco el id del estado
        id = estado.split('_')[2]
        descripcion = estado.split('_')[3]
        
        actualizar_descripcion_categoria(id,text)
        await update.message.reply_text('Se reemplazo la descripcion de la categoria "'+descripcion+'" por "'+text+'"')
     

        user_states[user_id] = {"estado":""}
        
    elif es_numero(text):
        importe = text
        # inicializo el usuario en vacio
        user_states[user_id] = {"estado":"cargando_operacion"}

        # Actualiza el estado del usuario
        user_states[user_id]['importe'] =importe
        await menu_categoria(update) 
    else:
        user_states[user_id] = {"estado":""}
        if text.lower() == 'menu':
            await menu_principal(update)  
        if text.lower() == 'saldos':  
            await mostrar_saldos(update)       
        if text.lower() == 'operaciones':  
            await mostrar_operaciones(update)       
        if text.lower() == 'matar bot':  
            exit()
        else:
            await update.message.reply_text('"' + text + '" no es una opcion valida!')




# Función que maneja las respuestas de los botones
async def button_handler(update: Update, context):
    query = update.callback_query
   
    await query.answer()
    
    # Obtiene el dato del botón presionado
    option = query.data

    print("ELECCION: " + option)

    user_id = query.from_user.id   
    chat_id =query.message.chat.id
    id_usuario = await id_usuario_db(user_id)


    if option == 'mostrar_db':
        # Mostrar el contenido de la base de datos
        await show_db_content(query)
        
    elif option.startswith( 'categoria_' ):
        # busco el codigo de categoria y la descripcion
        partes_categoria = option.split('_')

        # Actualiza el estado del usuario
        user_states[user_id]['id_categoria'] =partes_categoria[1]
        user_states[user_id]['categoria'] =partes_categoria[2]
        await menu_subcategoria(query)        

    elif option.startswith( 'subcategoria_' ):
        # busco el codigo de subcategoria y la descripcion
        partes_subcategoria = option.split('_')

        # Actualiza el estado del usuario
        user_states[user_id]['id_subcategoria'] =partes_subcategoria[1]
        user_states[user_id]['subcategoria'] =partes_subcategoria[2]           
        await menu_medio_de_pago(query,id_usuario)

    elif option.startswith( 'mediopago_' ):

        # busco el codigo de categoria y la descripcion
        partes_medio_pago = option.split('_')

        # Actualiza el estado del usuario
        user_states[user_id]['id_medio_pago'] =partes_medio_pago[1]
        user_states[user_id]['medio_pago'] =partes_medio_pago[2]           
        await query.edit_message_text(text=str(user_states[user_id]['importe']) + " pesos en '" + user_states[user_id]['subcategoria']+ "' con '" + user_states[user_id]['medio_pago'] + "'")

        print(str(user_states[user_id]['importe']) + ";" + user_states[user_id]['subcategoria']+ ";" + user_states[user_id]['medio_pago'])

        id_usuario = await id_usuario_db( user_id)
        
        # Guardar el mensaje en la base de datos    
        guardar_operacion(id_usuario,  datetime.today,user_states[user_id]['importe'], user_states[user_id]['id_subcategoria'],user_states[user_id]['id_medio_pago'])

        # actualizo los saldos del medio de pago
        actualizar_saldos(user_states[user_id]['id_medio_pago'],user_states[user_id]['importe'] )
        
        user_states[user_id] = {"estado":""}
        

    elif option == 'cambiar_categoria' :
        
        #establezco el estado para poder actualizar cuado cargue el nombre
        user_states[user_id]['estado'] ='agregando_nueva_categoria' 
        
        await menu_categoria(update) 

 
    elif option ==  'cambiar_subcategoria' :
        await menu_subcategoria(update.callback_query) 

    elif option ==  'cancelar' :
        await query.edit_message_text("Ingreso cancelado")
        user_states[user_id] ={}

    elif option ==  'configuraciones' :
        await menu_configuraciones(update) 

    elif option ==  'saldos' :
        await mostrar_saldos( update.callback_query) 
        
    elif option ==  'operaciones' :
        await mostrar_operaciones( update.callback_query) 

###################################################################################        
    # menues configuracion categorias
    elif option ==  'categorias' :
        await menu_editar_categorias( update.callback_query) 

    elif option ==  'nueva_categoria' :
      #  print('nueva_categoria ' + str(user_id))   
        user_states[user_id] ={"estado":'nueva_categoria'}
        await menu_cargar_nueva_categoria( update.callback_query) 
        
    elif option ==  'nueva_categoria_gastos' or option ==  'nueva_categoria_ingresos' :  
        user_states[user_id] ={"estado":option}
        await query.edit_message_text("Ingrese el nombre de la nueva categoria de tipo ingreso:")
            
    elif option.startswith( 'modificar_categoria_') and option.endswith( 'descripcion')  :
        print('cambiar descripcion categoria ')
        user_states[user_id] ={"estado":option}
        descripcion_anterior = option.split('_')[3]
        await query.edit_message_text("Ingrese el nuevo nombre de la categoria '"+descripcion_anterior+"':")

    elif option.startswith( 'modificar_categoria_') and option.endswith( 'tipo')  :
        print('cambiar tipo categoria')
    elif option.startswith( 'modificar_categoria_') and option.endswith( 'eliminar')  :
        print('eliminar categoria')

    elif option.startswith( 'modificar_categoria_'):
       # print('modificar categoria')
        await menu_elegir_tipo_modificacion_categoria( update.callback_query)         

###################################################################################           
    elif option ==  'subcategorias' :
        await menu_editar_subcategorias( update.callback_query) 
    elif option ==  'medios_pago' :
        await menu_editar_medios_pago( update.callback_query) 
    elif option ==  'usuarios' :
        await menu_editar_usuarios( update.callback_query)         

    else:
        # Responder con la opción elegida
        await query.edit_message_text(f"OPCION NO VALIDA:    {option}")
       
        user_states[user_id] = {"estado":""}
        
# Función que maneja el comando /menu
async def menu_command(update: Update, context):
    # Muestra el menú principal al ejecutar el comando /menu
    await menu_principal(update)

def main():
    # Inicializa la base de datos
    init_db()
    
       
    # Crea la aplicación y pásale tu token
    application = ApplicationBuilder().token(TOKEN).build()

    # Maneja todos los mensajes de texto
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, process_message)
    application.add_handler(message_handler)

    # Maneja las respuestas de los botones
    application.add_handler(CallbackQueryHandler(button_handler))


    # Maneja el comando /menu
    command_handler = CommandHandler("menu", menu_command)
    application.add_handler(command_handler)

    # Inicia el bot y empieza a hacer polling
    print("El bot está funcionando...")
    application.run_polling()

if __name__ == '__main__':
    main()
