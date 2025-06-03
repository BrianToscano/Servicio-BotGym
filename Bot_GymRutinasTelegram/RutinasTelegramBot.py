import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, CallbackContext, CommandHandler
from archivotron import busca_arreglo  # Esta función debe devolver la rutina o respuesta según el texto

# Cargar token desde .env
load_dotenv()
token_telegram = os.environ['token']

# Diccionario de rutinas por grupo muscular
rutinas = {
    "pecho": "🏋️ *Rutina de Pecho:*\n- Press banca 4x10\n- Press inclinado 4x12\n- Press declinado 4x12\n -Aperturas con mancuernas 4x15",
    "espalda": "🏋️ *Rutina de Espalda:*\n- Jalón al pecho 4x12\n- Remo con barra 4x10\n- Peso muerto 4x8",
    "piernas": "🦵 *Rutina de Piernas:*\n- Sentadillas 4x10\n- Prensa 4x12\n- Extensiones de cuádriceps 4x15\n- Desplantes 4x12",
    "biceps": "💪 *Rutina de Bíceps:*\n- Curl con barra 4x12\n- Curl alterno 4x10\n- Curl martillo 4x12",
    "triceps": "💪 *Rutina de Tríceps:*\n- Press francés 4x10\n- Fondos 4x12\n- Patada de tríceps 4x12\n- Polea Alta con cuerda Trenza 4x12",
    "hombros": "🏋️ *Rutina de Hombros:*\n- Press militar 4x12\n- Elevaciones Frontales 3x12\n- Pájaros y posteriores 3x12 \n- Elevaciones Laterales 3x12 \n- Encogimientos 3x12"
}




# Función para responder al comando /start
async def start(update: Update, context: CallbackContext):
    botones = [
        [KeyboardButton("Pecho"), KeyboardButton("Espalda")],
        [KeyboardButton("Piernas"), KeyboardButton("Biceps")],
        [KeyboardButton("Triceps"), KeyboardButton("Hombros")]
    ]
    markup = ReplyKeyboardMarkup(botones, resize_keyboard=True)

    user = update.message.from_user.first_name
    await update.message.reply_text(
        f"💪 ¡Hola, {user}! Soy tu bot de rutinas de gym.\nSelecciona un grupo muscular:",
        reply_markup=markup
    )

# Función para el comando /rutina
async def rutina(update: Update, context: CallbackContext):
    if context.args:
        grupo = " ".join(context.args).lower()
        if grupo in rutinas:
            await update.message.reply_text(rutinas[grupo], parse_mode="Markdown")
        else:
            await update.message.reply_text("Grupo muscular no reconocido. Intenta con: pecho, espalda, piernas, bíceps, tríceps o hombros.")
    else:
        await update.message.reply_text("Por favor, indica un grupo muscular. Ejemplo: /rutina pecho")

# Función de Echo: responde a cualquier texto que no sea comando
async def echo(update: Update, context: CallbackContext):
    user_text = update.message.text.lower()

    if user_text in rutinas:
        await update.message.reply_text(rutinas[user_text], parse_mode="Markdown")
    else:
        value_return = busca_arreglo(user_text)
        await update.message.reply_text(value_return)

# Configuración del bot
app = Application.builder().token(token_telegram).build()

# Agregar manejadores
app.add_handler(CommandHandler("start", start))           # /start
app.add_handler(CommandHandler("rutina", rutina))         # /rutina pecho
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))  # cualquier otro texto

# Iniciar el bot
print("🤖 Bot de rutinas de gym iniciado...")
app.run_polling()
