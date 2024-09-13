

 

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
            id_usuario= cache_ids_usuarios[user_id] 
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
         
    print ('TEXTO INGRESADO:' + text)
    print ( user_states)
        
    # elimino espacios dobles
    temp = text.split(" ")
    text = " ".join(temp)

    # quito espacios al principio y al final
    text = text.strip()

    
    if estado.startswith( 'nueva_categoria'):
    #    print(user_states[user_id]['estado'])
           
        guardar_nueva_categoria(text)        
        
        print('Se creo una nueva categoria llamada "'+text+'"')          
        await update.message.reply_text('Se creo una nueva categoria llamada "'+text+'"')
        
        #limpio el estado
        user_states[user_id] = {"estado":""}

    elif estado.startswith( 'modificar_categoria_') and estado.endswith( 'descripcion')  :
         # saco el id del estado
        id = estado.split('_')[2]
        descripcion = estado.split('_')[3]
        
        actualizar_descripcion_categoria(id,text)
        print('Se reemplazo la descripcion de la categoria "'+descripcion+'" por "'+text+'"')
        await update.message.reply_text('Se reemplazo la descripcion de la categoria "'+descripcion+'" por "'+text+'"')
     
        #limpio el estado
        user_states[user_id] = {"estado":""}

    elif estado.startswith( 'nueva_sub_') and estado.endswith( '_desc')  :    
         # saco los datos del estado    nueva_sub_1_5_Esparcimiento ⚽🛣_cat

        tipo = estado.split('_')[2]
        id_cat = estado.split('_')[3]
        descripcion_cat = estado.split('_')[4]
        
        desc_tipo='Gasto'
        if tipo==0:
            desc_tipo='Ingreso'
        
        crear_nueva_categoria(tipo,id_cat,text)
        print('Se creo la nueva subcategoria "'+text+'" de tipo "'+desc_tipo+ '" en la categoria "'+descripcion_cat + '"')
        await update.message.reply_text('Se creo la nueva subcategoria "'+text+'" de tipo "'+desc_tipo+ '" en la categoria "'+descripcion_cat + '"')
     
        #limpio el estado
        user_states[user_id] = {"estado":""}        
        

    elif estado.startswith( 'mod_sub_') and estado.endswith( '_desc')  : 
        
        id = estado.split('_')[2]
        descripcion = estado.split('_')[3]
        
        actualizar_descripcion_categoria(id,text)        
        
       # print('Se reemplazo la descripcion de la sucategoria "'+descripcion+'" por "'+text+'"')          
        await update.message.reply_text('Se cambio la descripcion de la subcategoria "'+descripcion+'" por "'+text+'"')
        
        #limpio el estado
        user_states[user_id] = {"estado":""}

    elif estado.startswith( 'nuevo_medio_') and estado.endswith( '_desc'): 
        tipo = estado.split('_')[2]
             
        crear_nuevo_medio_pago(tipo,text)        
        
       # print('Se reemplazo la descripcion de la sucategoria "'+descripcion+'" por "'+text+'"')          
        await update.message.reply_text('Se creo el nuevo medio de pago "'+text+'"')
        
        #limpio el estado
        user_states[user_id] = {"estado":""}
        

    elif estado.startswith( 'modif_medio_') and estado.endswith( '_desc'): 
        id = estado.split('_')[2]
        
        resultado_ok = update_sql('medios_pago',['descripcion'],(text,),'id = '+str(id))     
        
      # update_sql('usuarios',['nombre'],('otrousuario',),'id = 5')  
        
       # print('Se reemplazo la descripcion de la sucategoria "'+descripcion+'" por "'+text+'"')      
        if resultado_ok:    
            await update.message.reply_text('Se cambio la descripcion del medio de pago por "'+text+'"')
        else:
            await update.message.reply_text('ERROR guradando la descripcion "'+text+'" en el medio de pago')
        
        #limpio el estado
        user_states[user_id] = {"estado":""}
        
    elif estado.startswith('modif_medio_') and estado.endswith('_saldo'): 
        #  modif_medio_12_1_1_saldo 
        id = estado.split('_')[2]       
           
        if es_numero(text):
            
            #reemplazo el punto por la coma
            text=text.replace(',','.')
        
            resultado_ok = update_sql('medios_pago',['saldo'],(text,),'id = '+str(id))     
            
            if resultado_ok:    
                await update.message.reply_text('Se cambio el saldo a "'+text+'"')
            else:
                await update.message.reply_text('ERROR cambiando el saldo en el medio de pago')
            
        else:
            await update.message.reply_text('El valor ingresado no es un numero, no se actualizo el saldo del medio de pago')
                             
        #limpio el estado
        user_states[user_id] = {"estado":""}

           
    elif estado.startswith('modif_medio_') and estado.endswith('_cierre'): 
        #  modif_medio_10_2_1_cierre 
        id = estado.split('_')[2]   
         
        #quito puntos y comas
        text=text.replace(',','').replace('.','')
        
        dia = int(text)  
           
        if es_numero(text) and dia >0 and dia < 32:

        
            resultado_ok = update_sql('medios_pago',['dia_cierre'],(dia,),'id = '+str(id))     
            
            if resultado_ok:    
                await update.message.reply_text('Se cambio el dia de pago a "'+str(dia)+'"')
            else:
                await update.message.reply_text('ERROR cambiando el dia de pago en el medio de pago')
                
        else:
            await update.message.reply_text('El valor ingresado no es un numero entre 1 y 31, no se actualizo el dia de cierre del medio de pago')
                             
    
    elif estado.startswith('modif_medio_') and estado.endswith('_pago'): 
        #  modif_medio_10_2_1_cierre 
        id = estado.split('_')[2]    
        
        text=text.replace(',','').replace('.','')
        
        dia = int(text)  
           
        if es_numero(text) and dia >0 and dia < 32:
            #quito puntos y comas
                   
            resultado_ok = update_sql('medios_pago',['dia_pago'],(dia,),'id = '+str(id))     
            
            if resultado_ok:    
                await update.message.reply_text('Se cambio el dia de pago a "'+str(dia)+'"')
            else:
                await update.message.reply_text('ERROR cambiando el dia de pago en el medio de pago')
                
        else:
            await update.message.reply_text('El valor ingresado no es un numero entre 1 y 31, no se actualizo el dia de pago del medio de pago')
                             
    
                    
                  
    elif es_numero(text):
        
        #reemplazo el punto por la coma
        text=text.replace(',','.')
    
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

    print("BOTON MENU: " + option)

    user_id = query.from_user.id   
    chat_id =query.message.chat.id
    id_usuario = await id_usuario_db(user_id)


   # print( user_states[user_id] )
    
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
       # print('nueva_categoria ' + str(user_id))   
        user_states[user_id] ={"estado":'nueva_categoria'}   
        await query.edit_message_text("Ingrese la descripcion de la nueva categoria:")

    elif option.startswith( 'modificar_categoria_') and option.endswith( '_descripcion')  :
       # print('cambiar descripcion categoria ')
        user_states[user_id] ={"estado":option}
        descripcion_anterior = option.split('_')[3]
        await query.edit_message_text("Ingrese el nuevo nombre de la categoria '"+descripcion_anterior+"':")

    elif option.startswith( 'modificar_categoria_'):
       # print('modificar categoria')
        await menu_elegir_tipo_modificacion_categoria( update.callback_query)         
                 
    elif option.startswith( 'modificar_categoria_') and option.endswith( '_eliminar')  :
        print('eliminar categoria')
        
        # obtengo el id de la categoria a eliminar
        descripcion = option.split('_')[3]
        id = option.split('_')[2]
        
        # elimino la categoria
        eliminar_categoria(id)
        
        print('Se elimino la categoria "'+descripcion+'"')      
        await query.edit_message_text('Se elimino la categoria "'+descripcion+'"')
        
        #limpio estado
        user_states[user_id] = {"estado":""}

###################################################################################           
    elif option ==  'subcategorias' :
        await menu_editar_subcategorias( update.callback_query) 
    
    elif option ==  'nueva_subcategoria' :
      #  print('nueva_subcategoria ' + option)   
        
        await menu_cargar_nueva_subcategoria_tipo(update.callback_query)

    elif option.startswith( 'nueva_sub_') and option.endswith( '_desc'):
       # print('cambiar descripcion categoria ')
        user_states[user_id] ={"estado":option}
       # descripcion_categoria = option.split('_')[3]
        await query.edit_message_text("Ingrese el nombre de la nueva subcategoria:")
            
    elif option ==  'nueva_sub_0' or  option ==  'nueva_sub_1' :
     #   print('nueva_subcategoria ' + option)   
        
        await menu_cargar_nueva_subcategoria_categoria(update.callback_query)

    elif option.startswith( 'mod_sub_') and option.endswith( '_desc'):
        user_states[user_id] ={"estado":option}
      #  descripcion_anterior = option.split('_')[3]
        await query.edit_message_text("Ingrese el nuevo nombre de la subcategoria:")        

    elif option.startswith( 'mod_sub_') and option.endswith( '_ncat'):
        
        # obtengo el id de la subcategoria a modificar
        id_subcategoria = option.split('_')[2]
        id_nueva_categoria = option.split('_')[4]
        
        # cambio la categoria de la subcategoria
        cambiar_categoria_de_subcategoria(id_subcategoria,id_nueva_categoria)
        
       # print('Se elimino la categoria "'+descripcion+'"')      
        await query.edit_message_text('Se asigno la categoria "'+id_nueva_categoria+'"' + " a la categoria")
       
   
                
        user_states[user_id] ={"estado":option}

    elif option.startswith( 'mod_sub_') and option.endswith( '_cat'):
        #user_states[user_id] ={"estado":option}
        #descripcion_anterior = option.split('_')[3]
        
        await menu_cargar_nueva_categoria_subcategoria(update.callback_query)

    elif option.startswith( 'mod_sub_') and option.endswith( '_tipo'):
        #user_states[user_id] ={"estado":option}
        #descripcion_anterior = option.split('_')[3]
        
        await menu_cambiar_tipo_subcategoria(update.callback_query)     
        
        
    elif option.startswith( 'mod_sub_') and (option.endswith( '_tipo_0') or  option.endswith( '_tipo_1')):
        #   print('nueva_subcategoria ' + option)   
        id_subcategoria = option.split('_')[2]
        tipo = option.split('_')[4]
        
        descripcion_tipo='Ingreso'
        if tipo==0:
            descripcion_tipo='Gasto'
                
        # cambio el tipo de la subcategoria
        cambiar_tipo_de_subcategoria(id_subcategoria,tipo)    
        
        # print('Se elimino la categoria "'+descripcion+'"')      
        await query.edit_message_text('Se asigno el tipo "'+descripcion_tipo+'"' + " a la categoria")
       
                  
            
    elif option.startswith( 'mod_sub_') and option.endswith( '_eliminar'):        
               
        # obtengo el id de la categoria a eliminar
        descripcion = option.split('_')[3]
        id = option.split('_')[2]
        
        # elimino la categoria
        eliminar_categoria(id)
        
        print('Se elimino la categoria "'+descripcion+'"')      
        await query.edit_message_text('Se elimino la categoria "'+descripcion+'"')
       
    elif option.startswith( 'mod_sub_'):
        #mod_sub_78

        await menu_modificar_subcategoria(update.callback_query)

       
###################################################################################                
    elif option ==  'medios_pago' :        
        await menu_editar_medios_pago( update.callback_query)  
        
    elif option == 'nuevo_medio':        
        await menu_nuevo_medio_pago_elegir_tipo(update.callback_query)   
        
    elif option.startswith( 'nuevo_medio_'):           
        user_states[user_id] ={"estado":option + '_desc'}

        await query.edit_message_text("Ingrese la descripcion del nuevo medio de pago:")        
       

       
    elif option.startswith( 'modif_medio_') and option.endswith('_desc'):                
        user_states[user_id] ={"estado":option}        
        await query.edit_message_text("Ingrese la nueva descripcion del medio de pago:")
        
    elif option.startswith( 'modif_medio_') and option.endswith('_saldo'): 
        user_states[user_id] ={"estado":option}
        await query.edit_message_text("Ingrese el nuevo saldo del medio de pago:")             

    elif option.startswith( 'modif_medio_') and option.endswith('_tipo'):         
        await menu_modificar_medio_pago_elegir_tipo(update.callback_query)   

    elif option.startswith( 'modif_medio_') and option.endswith('_mtipo'):     
        
        # modif_medio_12_1_1_tipo_0_mtipo          
        id = option.split('_')[2] 
        tipo = option.split('_')[6]        
        
        resultado_ok = update_sql('medios_pago',['tipo'],(tipo,),'id='+id)
        
        if resultado_ok:            
            print('Se cambio el tipo del medio de pago a "'+tipo+'"')      
            await query.edit_message_text('Se cambio el tipo del medio de pago a "'+tipo+'"')
        else:        
            print('ERROR cambiando el tipo del medio de pago a "'+tipo+'"')      
            await query.edit_message_text('ERROR cambiando el tipo del medio de pago a "'+tipo+'"')
        
    
              
    elif option.startswith( 'modif_medio_') and option.endswith('_cierre'): 
        user_states[user_id] ={"estado":option}
        await query.edit_message_text("Ingrese el dia de cierre del medio de pago (entre 1 y 31):")             
    elif option.startswith( 'modif_medio_') and option.endswith('_pago'): 
        user_states[user_id] ={"estado":option}
        await query.edit_message_text("Ingrese el dia de pago del medio de pago (entre 1 y 31):")      
    elif option.startswith( 'modif_medio_') and option.endswith('_desac'): 
        
        # modif_medio_12_0_1_desac          
        id = option.split('_')[2]    
        
        resultado_ok = update_sql('medios_pago',['activo'],(0,),'id='+id)
        
        if resultado_ok:            
            print('Se desactivo el medio de pago')      
            await query.edit_message_text('Se desactivo el medio de pago')
        else:        
            print('ERROR desactivando el tipo del medio de pago')      
            await query.edit_message_text('ERROR desactivando el tipo del medio de pago')
        
    elif option.startswith( 'modif_medio_') and option.endswith('_reac'):    
        # modif_medio_12_0_1_reac         
        id = option.split('_')[2]    
        
        resultado_ok = update_sql('medios_pago',['activo'],(1,),'id='+id)
        
        if resultado_ok:            
            print('Se reactivo el medio de pago')      
            await query.edit_message_text('Se reactivo el medio de pago')
        else:        
            print('ERROR reactivando el tipo del medio de pago')      
            await query.edit_message_text('ERROR reactivando el tipo del medio de pago')
       
    elif option.startswith( 'modif_medio_'):        
        await menu_modificar_medio_pago( update.callback_query)   
        
    
###################################################################################        
    elif option ==  'usuarios' :
        await menu_editar_usuarios( update.callback_query)         
###################################################################################
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
    
    
    # insert_sql('usuarios',['id','nombre'],(5,'nuevousuario'))
    # print(select_sql('select * from usuarios'))
    
    # update_sql('usuarios',['nombre'],('otrousuario',),'id = 5') 
    # print(select_sql('select * from usuarios'))
    
    # delete_sql('usuarios','id = 5')
    # print(select_sql('select * from usuarios'))
    
     
       
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
