
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters,ConversationHandler


from lib_db import * #Importamos todas las funciones de base de datos


# Diccionario para almacenar el estado de cada usuario
user_states = {}




#####################################################################################################################
#                                                CARGA OPERACIONES                                                  #
#####################################################################################################################

# Función que muestra el menú de botones
async def menu_categoria(update: Update):
    
    
    # cargo las categorias desde la db
    filas = await consulta_sql("SELECT id, descripcion FROM categorias")
  
    keyboard = []
    for fila in filas:             
        descripcion = fila[1] 
        id = 'categoria_' + repr(fila[0]) + '_' + fila[1] 
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
    filas = await consulta_sql("SELECT id, descripcion FROM subcategorias WHERE id_categoria=" + str(id_categoria ))
  

  #  print(filas)

    keyboard = []
    for fila in filas:              
        descripcion = fila[1]
        id = 'subcategoria_' + repr(fila[0]) + '_' + fila[1] 
        keyboard.append([InlineKeyboardButton(descripcion, callback_data= id)])

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

    # cargo los medios de pago de la subcategoria desde la db
    #filas = await  listar_medios_pago(id_subcategoria)
    filas = await consulta_sql('''
                     select mp.id,
                            mp.descripcion
                        from usuarios us  
                            JOIN medios_pago_usuarios mpu ON mpu.id_usuario = us.id
                            JOIN medios_pago mp  ON mp.id=mpu.id_medio_pago
                        where  us.id=''' + str(id_usuario))


   # print("medios de pago para "+ user_states[query.from_user.id]['subcategoria'] + " (" + str(id_subcategoria) +")")
   # print(filas)
    keyboard = []
    for fila in filas:              
        descripcion = fila[1] 
        id = 'mediopago_' + repr(fila[0])+ '_' +  fila[1]

        keyboard.append([InlineKeyboardButton(descripcion, callback_data= id)])

    keyboard.append([InlineKeyboardButton('Cambiar Subcategoria', callback_data= 'cambiar_subcategoria')])
    keyboard.append([InlineKeyboardButton('Cancelar', callback_data= 'cancelar')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    texto = 'Elige un medio de pago:'
    if len(filas) == 0:
        texto = 'FALTA CARGAR MEDIOS DE PAGO!'
    
     # Edita el mensaje actual para mostrar el submenú
    #await query.edit_message_text("Elige una opción del submenú:", reply_markup=reply_markup)   
    await query.edit_message_text("Ingresaste $" + str(user_states[user_id]['importe'])  + " en '"+ user_states[user_id]['subcategoria']  +"', "+texto, reply_markup=reply_markup)



#####################################################################################################################
#                                                 MENU PRINCIPAL                                                    #
#####################################################################################################################

async def menu_contextual(message):
    # Crea botones del menú principal
    keyboard = [
        ["Saldos","Operaciones"],
        ["Categorias","Subcategorias"],
        ["Medios de Pago","Usuarios"]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    # Envía o edita el mensaje para mostrar el menú
    await message.reply_text("Elige una opción del menú principal:", reply_markup=reply_markup)
    #user_states[user_id]['importe']


    
# Función que muestra el menú principal
async def menu_principal(update: Update):  
    
    
    #muestro el menu contextual
   # await menu_contextual(update.message)    
           
    keyboard = [[InlineKeyboardButton('Saldos', callback_data= 'saldos')],
                [InlineKeyboardButton('Operaciones', callback_data= 'operaciones')],
                [InlineKeyboardButton('Configuraciones', callback_data= 'configuraciones')],
                [InlineKeyboardButton('Salir', callback_data= 'cancelar')]]    
    
    reply_markup = InlineKeyboardMarkup(keyboard)    
   
    # Envía el menú de botones
    await update.message.reply_text("Menu principal:", reply_markup=reply_markup)
   

     
# Función que muestra el menú de configuraciones
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


                                    ###################################
                                    #        MENU CATEGORIAS          #
                                    ###################################
#estado =''

async def menu_editar_categorias(update: Update):   
      
    
   # print(update.from_user)
    
  # user_id = update.from_user.id
    
    
    keyboard = [[InlineKeyboardButton('Nueva Categoria', callback_data= 'nueva_categoria')]]         
        
    # cargo las categoria desde la db
    filas = await consulta_sql("SELECT id,descripcion FROM categorias")

    for fila in filas:              
        descripcion = fila[1] 
        id = 'modificar_categoria_' + repr(fila[0])+ '_' +  fila[1]

        keyboard.append([InlineKeyboardButton(descripcion, callback_data= id)])
        
    keyboard.append( [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')])
        
    reply_markup = InlineKeyboardMarkup(keyboard)  
    
    
    #establezco el estado para poder actualizar cuado cargue el nombre
   # estado = 'modificando_categoria_' 
     
    # Envía el menú de botones
    await update.edit_message_text("Elija la categoria a modificar:", reply_markup=reply_markup)
    
    


async def menu_cargar_nueva_categoria(update: Update):     
        
   # user_id = update.from_user.id
    
       
    keyboard = [
                [InlineKeyboardButton('Gastos', callback_data= 'nueva_categoria_gastos')],
                [InlineKeyboardButton('Ingresos', callback_data= 'nueva_categoria_ingresos')],
                [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')]]    
    
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.edit_message_text("Ingrese el tipo de la nueva categoria:", reply_markup=reply_markup)
    


async def menu_elegir_tipo_modificacion_categoria(update: Update):     
  
    datos_categoria = update.data

    descripcion_anterior = datos_categoria.split('_')[3]
       
    keyboard = [
                [InlineKeyboardButton('Descripcion', callback_data= datos_categoria+'_descripcion')],
                [InlineKeyboardButton('Tipo', callback_data= datos_categoria+'_tipo')],
                [InlineKeyboardButton('Eliminar', callback_data= datos_categoria+'_eliminar')],
                [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')]]    
    
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.edit_message_text("Elija que desea cambiar de la categoria '"+descripcion_anterior+"':", reply_markup=reply_markup)
            

                              
                                    ###################################
                                    #        MENU SUBCATEGORIAS       #
                                    ###################################


async def menu_editar_subcategorias(update: Update):   

    keyboard = [[InlineKeyboardButton('Nueva Subcategoria', callback_data= 'nueva_subcategoria')]]         
  

    # cargo las subcategoria desde la db
    filas = await consulta_sql("SELECT id,descripcion FROM subcategorias")

    for fila in filas:              
        descripcion = fila[1] 
        id = 'modificar_subcategoria_' + repr(fila[0])+ '_' +  fila[1]

        keyboard.append([InlineKeyboardButton(descripcion, callback_data= id)])
        
    keyboard.append( [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')])
        
    reply_markup = InlineKeyboardMarkup(keyboard)  
       
    # Envía el menú de botones
    await update.edit_message_text("Menu Subcategorias:", reply_markup=reply_markup)

                                    ###################################
                                    #        MENU MEDIOS DE PAGO      #
                                    ###################################

async def menu_editar_medios_pago(update: Update):            
    keyboard = [
                [InlineKeyboardButton('Nuevo Medio de Pago', callback_data= 'nuevo_medo_pago')],
                [InlineKeyboardButton('Modificar Medio de Pago', callback_data= 'modificar_medo_pago')],
                [InlineKeyboardButton('Eliminar Medio de Pago', callback_data= 'eliminar_medo_pago')],
                [InlineKeyboardButton('Salir', callback_data= 'cancelar')]]    
    
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.edit_message_text("Menu Medios de Pago:", reply_markup=reply_markup)
    
    
                                    ###################################
                                    #          MENU USUARIOS          #
                                    ###################################
    
async def menu_editar_usuarios(update: Update):          
    keyboard = [
                [InlineKeyboardButton('Nuevo Usuario', callback_data= 'nuevo_usuario')],
                [InlineKeyboardButton('Modificar Usuario', callback_data= 'modificar_usuario')],
                [InlineKeyboardButton('Eliminar Usuario', callback_data= 'eliminar_usuario')],
                [InlineKeyboardButton('Salir', callback_data= 'cancelar')]]    
    
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.edit_message_text("Menu Usuarios:", reply_markup=reply_markup)
    
   
   
