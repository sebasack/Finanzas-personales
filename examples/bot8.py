from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes

# Estados de la conversación
ASK_FOR_INPUT, SHOW_SECOND_MENU = range(2)

# Token del bot
TOKEN = 'YOUR_BOT_TOKEN'

# Función que maneja el comando /start y muestra el menú principal
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Opción 1", "Opción 2"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Elige una opción del menú principal:", reply_markup=reply_markup)

    return ASK_FOR_INPUT

# Función que se activa cuando el usuario selecciona "Opción 1" y pide un texto
async def ask_for_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Opción 1":
        await update.message.reply_text("Por favor, ingresa un texto:")
        return SHOW_SECOND_MENU
    else: # es la opcion 2
        await update.message.reply_text("Has seleccionado otra opción.")
        return ConversationHandler.END

# Función que maneja el texto de entrada y muestra el segundo menú
async def show_second_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await update.message.reply_text(f"Gracias por tu texto: {user_input}")

    # Mostrar segundo menú
    second_menu = [
        ["Submenú Opción A", "Submenú Opción B"],
        ["Submenú Opción C"]
    ]
    reply_markup = ReplyKeyboardMarkup(second_menu, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Elige una opción del segundo menú:", reply_markup=reply_markup)

    return ConversationHandler.END

def main():
    # Crear la aplicación y agregar el token
    application = ApplicationBuilder().token(TOKEN).build()

    # Configurar la conversación
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            ASK_FOR_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_for_input)],
            SHOW_SECOND_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_second_menu)],
        },
        fallbacks=[]
    )

    # Añadir el manejador de la conversación
    application.add_handler(conversation_handler)

    # Iniciar el bot
    print("El bot está funcionando...")
    application.run_polling()

if __name__ == '__main__':
    main()
