
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters


from lib_db import * #Importamos todas las funciones de base de datos


# Diccionario para almacenar el estado de cada usuario
user_states = {}



# Función que maneja el comando /menu
async def menu_command(update: Update, context):
    # Muestra el menú principal al ejecutar el comando /menu
    await menu_principal(update)


# Función que muestra el menú de botones
async def menu_principal(update: Update):   
   
    keyboard = [[InlineKeyboardButton('Saldos', callback_data= 'saldos')],
                [InlineKeyboardButton('Operaciones', callback_data= 'operaciones')],
                [InlineKeyboardButton('Configuraciones', callback_data= 'configuraciones')],
                [InlineKeyboardButton('Salir', callback_data= 'cancelar')]]    
    
    reply_markup = InlineKeyboardMarkup(keyboard)    
   
    # Envía el menú de botones
    await update.message.reply_text("Menu principal:", reply_markup=reply_markup)
   


# Función que muestra el menú de botones
async def menu_configuraciones(update: Update):   
   
    keyboard = [
                [InlineKeyboardButton('Categorias', callback_data= 'categorias')],
                [InlineKeyboardButton('Subcategorias', callback_data= 'subcategorias')],
                [InlineKeyboardButton('Medios de Pago', callback_data= 'medios_pago')],
                [InlineKeyboardButton('Usuarios', callback_data= 'usuarios')],
                [InlineKeyboardButton('Salir', callback_data= 'cancelar')]]    
    
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.callback_query.edit_message_text("Menu Configuraciones:", reply_markup=reply_markup)
    #  await update.callback_query.edit_message_text("Ingresaste $" + str(user_states[user_id]['importe'])  + " Elige una Categoria:", reply_markup=reply_markup)

   

# Función que muestra el menú de botones
async def menu_categoria(update: Update):
   
    # cargo las categorias desde la db
    filas = await consulta_sql("SELECT id,descripcion FROM categorias")
  
    keyboard = []
    for fila in filas:             
        descripcion = fila[1]
        id = 'categoria_' + repr(fila[0]) + '_' + descripcion
        keyboard.append([InlineKeyboardButton(descripcion, callback_data= id)])
    
    keyboard.append([InlineKeyboardButton('Cancelar operacion', callback_data= 'cancelar')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
      #  print('vengo de ingreso de importe')
        user_id = update.message.from_user.id
         # Envía el menú de botones
        await update.message.reply_text("Ingresaste $" + str(user_states[user_id]['importe'])  + " Elige una Categoria:", reply_markup=reply_markup)
    else:
       # print("estoy cambiando categoria")
        user_id = update.callback_query.from_user.id
        # Envía el menú de botones
        await update.callback_query.edit_message_text("Ingresaste $" + str(user_states[user_id]['importe'])  + " Elige una Categoria:", reply_markup=reply_markup)


# Función que muestra el menú de botones
async def menu_subcategoria(query):

    user_id = query.from_user.id
  
    id_categoria= user_states[user_id]['id_categoria']
 
     # cargo las subcategorias desde la db
    filas = await consulta_sql("SELECT id,descripcion FROM subcategorias WHERE id_categoria=" + str(id_categoria ))
  

  #  print(filas)

    keyboard = []
    for fila in filas:              
        descripcion = fila[1]
        id = 'subcategoria_' + repr(fila[0])+ '_' + descripcion
        desc = fila[1]
        keyboard.append([InlineKeyboardButton(desc, callback_data= id)])

    keyboard.append([InlineKeyboardButton('Cambiar Categoria', callback_data= 'cambiar_categoria')])
    keyboard.append([InlineKeyboardButton('Cancelar', callback_data= 'cancelar')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    texto ='Elige una subcategoria:'
    if len(filas) == 0:
        texto = 'FALTA CARGAR SUBCATEGORIAS!'    

    # Edita el mensaje actual para mostrar el submenú
    await query.edit_message_text("Ingresaste $" + str(user_states[user_id]['importe'])  + " en '"+ user_states[user_id]['categoria']  +"', "+texto, reply_markup=reply_markup)



    

# Función que muestra el menú de botones
async def menu_medio_de_pago(query,id_usuario):

    user_id = query.from_user.id
   # id_usuario = await id_usuario_db(user_id)

    id_subcategoria= user_states[query.from_user.id]['id_subcategoria']

    # cargo los medios de pago de la subcategoria desde la db
    #filas = await  listar_medios_pago(id_subcategoria)
    filas = await consulta_sql('''
                    select mp.id,
                           mp.descripcion 
                        from subcategorias sub
                            join subcategorias_medios_pago tomp on tomp.id_subcategoria = sub.id 
                            join medios_pago mp on mp.id = tomp.id_medio_pago 
                            JOIN medios_pago_usuarios mpu ON mpu.id_medio_pago = tomp.id_medio_pago
                            JOIN usuarios us ON us.id=mpu.id_usuario
                        where sub.id =''' + str(id_subcategoria) + ' and us.id =' + str(id_usuario))


   # print("medios de pago para "+ user_states[query.from_user.id]['subcategoria'] + " (" + str(id_subcategoria) +")")
   # print(filas)
    keyboard = []
    for fila in filas:              
        descripcion = fila[1]
        id = 'mediopago_' + repr(fila[0])+ '_' + descripcion
        desc = fila[1]
        keyboard.append([InlineKeyboardButton(desc, callback_data= id)])

    keyboard.append([InlineKeyboardButton('Cambiar Subcategoria', callback_data= 'cambiar_subcategoria')])
    keyboard.append([InlineKeyboardButton('Cancelar', callback_data= 'cancelar')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    texto = 'Elige un medio de pago:'
    if len(filas) == 0:
        texto = 'FALTA CARGAR MEDIOS DE PAGO!'
    
     # Edita el mensaje actual para mostrar el submenú
    #await query.edit_message_text("Elige una opción del submenú:", reply_markup=reply_markup)   
    await query.edit_message_text("Ingresaste $" + str(user_states[user_id]['importe'])  + " en '"+ user_states[user_id]['subcategoria']  +"', "+texto, reply_markup=reply_markup)


