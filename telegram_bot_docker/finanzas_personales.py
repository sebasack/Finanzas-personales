

 

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

    items = await consulta_sql('''SELECT op.fecha  || ' ' || us.nombre || ' $' || op.monto 
                                    FROM operaciones op
                                         JOIN usuarios us on us.id=op.id_usuario
                                   ORDER BY op.fecha
                               ''')

    if items:
        # Crear un string con los nombres de los items
        items_str = '\n'.join([item[0] for item in items])
        await query.edit_message_text(f"Operaciones guardadas:\n{items_str}")
    else:
        await query.edit_message_text("No hay operaciones para mostrar.")


# Función que muestra el contenido de la base de datos
async def mostrar_saldos(query):

    items = await consulta_sql("SELECT descripcion || ' $' || saldo FROM medios_pago mp   ")

    if items:
        # Crear un string con los nombres de los items
        items_str = '\n'.join([item[0] for item in items])
        await query.edit_message_text(f"Saldos:\n{items_str}")
    else:
        await query.edit_message_text("No hay saldos para mostrar.")
    
           

# Función que procesa los mensajes de texto
async def process_message(update: Update, context):
        
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    
    await id_usuario_db(user_id)
        
    text = update.message.text

    print ('ingreso:' + text)
        
    # elimino espacios dobles
    temp = text.split(" ")
    text = " ".join(temp)

    # quito espacios al principio y al final
    text = text.strip()

    #reemplazo el punto por la coma
    text=text.replace(',','.')

    if es_numero(text):
        importe = text
        # inicializo el usuario en vacio
        user_states[user_id] = {}

        # Actualiza el estado del usuario
        user_states[user_id]['importe'] =importe
        await menu_categoria(update) 
    else:
        if text == 'menu':
            await menu_principal(update)         
        else:
            await update.message.reply_text(text + 'no es una opcion valida!')




# Función que maneja las respuestas de los botones
async def button_handler(update: Update, context):
    query = update.callback_query
   
    await query.answer()
    
    # Obtiene el dato del botón presionado
    option = query.data

#    print("ELECCION: " + option)

    user_id = query.from_user.id   
    chat_id =query.message.chat.id
    id_usuario = await id_usuario_db(user_id)


    if option == 'mostrar_db':
        # Mostrar el contenido de la base de datos
        await show_db_content(query)
        
    elif option.startswith( 'categoria' ):
        # busco el codigo de categoria y la descripcion
        partes_categoria = option.split('_')

        # Actualiza el estado del usuario
        user_states[user_id]['id_categoria'] =partes_categoria[1]
        user_states[user_id]['categoria'] =partes_categoria[2]
        await menu_subcategoria(query)        

    elif option.startswith( 'subcategoria' ):
        # busco el codigo de subcategoria y la descripcion
        partes_subcategoria = option.split('_')

        # Actualiza el estado del usuario
        user_states[user_id]['id_subcategoria'] =partes_subcategoria[1]
        user_states[user_id]['subcategoria'] =partes_subcategoria[2]           
        await menu_medio_de_pago(query,id_usuario)

    elif option.startswith( 'mediopago' ):

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

        user_states[user_id] ={}
        

    elif option == 'cambiar_categoria' :
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
        
    else:
        # Responder con la opción elegida
        await query.edit_message_text(f"OPCION NO VALIDA:    {option}")
        user_states[user_id] ={}


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
