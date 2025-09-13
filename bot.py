# bot.py
# Requisitos: python-telegram-bot==21.4
# 1) Reemplaza los valores TOKEN, CHANNEL_URL y GROUP_URL
# 2) En consola: pip install -r requirements.txt
# 3) Ejecuta: python bot.py
# 4) Genera tu QR con: https://t.me/TU_BOT?start=bienvenida

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === CONFIGURA AQUÍ ===
TOKEN = "8375588470:AAHuxxlHvHeDcnAYbs5pI39aZoqySIFUDaI"
CHANNEL_URL = "https://t.me/+jS_YKiiHgcw3OTRh"   # Puedes usar enlace de invitación o @usuario si es público
GROUP_URL   = "https://t.me/+kL7eSPE27805ZGRh"    # Puedes usar enlace de invitación o @usuario si es público

WELCOME = (
    "👋 ¡Bienvenid@!\n"
    "Gracias por llegar por nuestro QR.\n\n"
    "📣 Canal con novedades y descuentos\n"
    "💬 Chat para dudas y comunidad\n\n"
    "Elige una opción:"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Soporta deep-links: t.me/TU_BOT?start=algo  -> context.args = ['algo']
    kb = [
        [
            InlineKeyboardButton("📣 Canal", url=CHANNEL_URL),
            InlineKeyboardButton("💬 Chat",  url=GROUP_URL),
        ]
    ]
    await update.message.reply_text(
        WELCOME,
        reply_markup=InlineKeyboardMarkup(kb),
        disable_web_page_preview=True,
    )

def main():
    if not TOKEN or TOKEN.startswith("PEGA_AQUI"):
        raise RuntimeError("⚠️ Debes pegar tu TOKEN de @BotFather en la variable TOKEN.")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("✅ Bot iniciado. Presiona Ctrl+C para detener.")
    app.run_polling()

if __name__ == "__main__":
    main()
