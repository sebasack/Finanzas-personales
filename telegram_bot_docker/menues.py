
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
    
    

async def menu_elegir_tipo_modificacion_categoria(update: Update):     
  
    datos_categoria = update.data

    descripcion_anterior = datos_categoria.split('_')[3]
    id_anterior = datos_categoria.split('_')[2]
    
    keyboard = [[InlineKeyboardButton('Descripcion', callback_data= datos_categoria+'_descripcion')]]    
    
    #busco en la db si la categoria esta en uso, si lo esta no puedo eliminarla
    en_uso = await consulta_sql("select count(*) from subcategorias  where id_categoria = "+id_anterior)
    if en_uso[0][0] == 0:
        keyboard.append([InlineKeyboardButton('Eliminar', callback_data= datos_categoria+'_eliminar')])
    
    keyboard.append([InlineKeyboardButton('Cancelar', callback_data= 'cancelar')])
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.edit_message_text("Elija que desea cambiar de la categoria '"+descripcion_anterior+"':", reply_markup=reply_markup)
            
                             
                                    ###################################
                                    #        MENU SUBCATEGORIAS       #
                                    ###################################


async def menu_editar_subcategorias(update: Update):   
    
    
    user_id = update.from_user.id

    keyboard = [[InlineKeyboardButton('Nueva Subcategoria', callback_data= 'nueva_subcategoria')]]         
  

    # cargo las subcategoria desde la db
    filas = await consulta_sql('''
                               SELECT sub.id, sub.descripcion, cat.descripcion
                                 FROM subcategorias sub
                                      JOIN categorias as cat on cat.id = sub.id_categoria 
                             ORDER BY cat.id, sub.descripcion 
                             ''')

    for fila in filas:              
        descripcion = fila[1] +' ('+ fila[2]+')' 
        id = 'mod_sub_' + repr(fila[0]) 
       # print(id)

        keyboard.append([InlineKeyboardButton(descripcion, callback_data= id)])
        
    keyboard.append( [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')])
        
    reply_markup = InlineKeyboardMarkup(keyboard)  
       
    # Envía el menú de botones
    await update.edit_message_text("Menu Subcategorias:", reply_markup=reply_markup)



async def menu_cargar_nueva_subcategoria_tipo(update: Update):     
        
   # user_id = update.from_user.id
    
       
    keyboard = [
                [InlineKeyboardButton('Gastos', callback_data= 'nueva_sub_1')],
                [InlineKeyboardButton('Ingresos', callback_data= 'nueva_sub_0')],
                [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')]]    
    
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.edit_message_text("Ingrese el tipo de la nueva subcategoria:", reply_markup=reply_markup)
    

async def menu_cargar_nueva_subcategoria_categoria(update: Update):     
        
   # user_id = update.from_user.id
    
    
    datos_categoria = update.data
  
    # cargo las categorias desde la db
    filas = await consulta_sql('''
                               SELECT id, descripcion
                                 FROM categorias sub                                    
                             ORDER BY descripcion 
                             ''')

    keyboard = []
    for fila in filas:              
        descripcion = fila[1] 
        id = datos_categoria +'_'+ repr(fila[0]) + '_desc'        
      #  print(id)

        keyboard.append([InlineKeyboardButton(descripcion, callback_data= id)])
        
    keyboard.append( [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')])
        
    reply_markup = InlineKeyboardMarkup(keyboard)  
           
    # Envía el menú de botones
    await update.edit_message_text("Ingrese a que categoria pertenece la nueva subcategoria:", reply_markup=reply_markup)
    
async def menu_modificar_subcategoria(update: Update):  
          
    datos_categoria = update.data

    id_subcategoria = datos_categoria.split('_')[2]
    #descripcion_anterior = datos_categoria.split('_')[3]

 
    keyboard = [[InlineKeyboardButton('Descripcion', callback_data= datos_categoria+'_desc')],
                [InlineKeyboardButton('Categoria', callback_data=  datos_categoria+'_cat')],
                [InlineKeyboardButton('Tipo', callback_data=  datos_categoria+'_tipo')]]
    
    #busco en la db si la subcategoria esta en uso, si lo esta no puedo eliminarla
    en_uso = await consulta_sql(''' select (select count(*) from operaciones ope where ope.id_subcategoria = sub.id ),
                                           sub.descripcion
                                      from subcategorias sub
                                     where id='''+id_subcategoria)
  #  print(en_uso)
    if en_uso[0][0] == 0:
        keyboard.append( [InlineKeyboardButton('Eliminar', callback_data=  datos_categoria+'_eliminar')])
    
    keyboard.append( [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.edit_message_text("Que desea modificar de la subcategoria "+en_uso[0][1]+":", reply_markup=reply_markup)


async def menu_cargar_nueva_categoria_subcategoria(update: Update):  
    
    datos_categoria = update.data

    #id_anterior = datos_categoria.split('_')[2]
   # descripcion_anterior = datos_categoria.split('_')[3]    
  
    # cargo las categorias desde la db
    filas = await consulta_sql('''
                               SELECT id, descripcion
                                 FROM categorias sub                                    
                             ORDER BY descripcion 
                             ''')
    
    keyboard = []
    for fila in filas:              
        descripcion = fila[1] 
        id = datos_categoria +'_'+ repr(fila[0])  + '_ncat'
      #  print(id)

        keyboard.append([InlineKeyboardButton(descripcion, callback_data= id)])
        
    keyboard.append( [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')])
        
    reply_markup = InlineKeyboardMarkup(keyboard)  
           
    # Envía el menú de botones
    await update.edit_message_text("Ingrese la nueva categoria para la subcategoria:", reply_markup=reply_markup)
    


async def menu_cambiar_tipo_subcategoria(update: Update):  
          
    datos_categoria = update.data
   
    keyboard = [[InlineKeyboardButton('Gastos', callback_data= datos_categoria+'_0')],
                [InlineKeyboardButton('Ingresos', callback_data=  datos_categoria+'_1')],
                [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')]]    
      
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.edit_message_text("Ingrese el nuevo tipo para la subcategoria:", reply_markup=reply_markup)
    
        
                                    ###################################
                                    #        MENU MEDIOS DE PAGO      #
                                    ###################################

async def menu_editar_medios_pago(update: Update):    
    
    
   # datos_medio_pago = update.data
    
    keyboard = [[InlineKeyboardButton('Nuevo Medio de Pago', callback_data= 'nuevo_medio')]]    
    
    #busco en la db si la categoria esta en uso, si lo esta no puedo eliminarla
    filas = await consulta_sql("SELECT id, descripcion, tipo, activo FROM medios_pago ORDER BY tipo, id")
    
   
    for fila in filas:     
         
        descripcion_tipo=' (Efectivo)'
        if fila[2]==1:   
            descripcion_tipo=' (Debito)'
        elif fila[2]==2: 
            descripcion_tipo=' (Credito)'

        if fila[3]==0:
            descripcion_tipo += ' INACTIVO'
            
        keyboard.append([InlineKeyboardButton(fila[1]+descripcion_tipo, callback_data= 'modif_medio_'+str(fila[0])+'_'+str(fila[2])+'_'+str(fila[3]))])
    
    keyboard.append([InlineKeyboardButton('Cancelar', callback_data= 'cancelar')])
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.edit_message_text("Modificar Medios de Pago:", reply_markup=reply_markup)
    
   
async def menu_nuevo_medio_pago_elegir_tipo(update: Update):    
    
    keyboard = [
                [InlineKeyboardButton('Efectivo', callback_data= 'nuevo_medio_0')],
                [InlineKeyboardButton('Debito', callback_data= 'nuevo_medio_1')],
                [InlineKeyboardButton('Credito', callback_data= 'nuevo_medio_2')],
                [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')]]    
    
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.edit_message_text("Elija el tipo del nuevo medio de pago:", reply_markup=reply_markup)  
       
       
async def menu_modificar_medio_pago(update: Update):    
    
    #desgloso los datos de entrada
    datos_medio_pago = update.data    
    partes = datos_medio_pago.split('_')
    tipo = partes[3]
    estado = partes[4]    
        
    keyboard = [
                [InlineKeyboardButton('Descripcion', callback_data= datos_medio_pago + '_desc')],
                [InlineKeyboardButton('Saldo Actual', callback_data=  datos_medio_pago + '_saldo')],
                [InlineKeyboardButton('Tipo', callback_data=  datos_medio_pago + '_tipo')]]    
               
    if tipo == '2': # es una tarjeta de credito            
        keyboard.append( [InlineKeyboardButton('Dia de Cierre', callback_data=  datos_medio_pago +'_cierre')])
        keyboard.append( [InlineKeyboardButton('Dia de pago', callback_data=  datos_medio_pago +'_pago')])    
        
    if estado == '1':
        keyboard.append( [InlineKeyboardButton('Desactivar Medio', callback_data=  datos_medio_pago +'_desac')])
    else:
        # esta desactivado, solo permito reactivarlo
        keyboard = [[InlineKeyboardButton('Reactivar Medio', callback_data=  datos_medio_pago +'_reac')]]
                
    keyboard.append( [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')])
  
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.edit_message_text("Elija que desea modificar del medio de pago:", reply_markup=reply_markup)  
       
       

   
async def menu_modificar_medio_pago_elegir_tipo(update: Update):    
    
    datos_medio_pago = update.data    
    
    keyboard = [
                [InlineKeyboardButton('Efectivo', callback_data= datos_medio_pago+ '_0_mtipo')],
                [InlineKeyboardButton('Debito', callback_data= datos_medio_pago+'_1_mtipo')],
                [InlineKeyboardButton('Credito', callback_data= datos_medio_pago+'_2_mtipo')],
                [InlineKeyboardButton('Cancelar', callback_data= 'cancelar')]]    
    
    reply_markup = InlineKeyboardMarkup(keyboard)   
     
    # Envía el menú de botones
    await update.edit_message_text("Elija el nuevo tipo del medio de pago:", reply_markup=reply_markup)  
              
       
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
    
   
   
