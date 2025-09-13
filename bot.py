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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name or "amig@"
    
    mensaje = (
        f"👋 ¡Bienvenid@, {nombre}!\n\n"
        "Nos alegra mucho tenerte por aquí 🌿\n"
        "En plataformas como Instagram es muy difícil mantener una cuenta dedicada a vaporizadores, "
        "por eso decidimos crear esta comunidad exclusiva para quienes confían en nosotros 💚\n\n"
        "📣 En el canal podrás estar al tanto de:\n"
        "— Nuevos lanzamientos\n"
        "— Descuentos especiales\n"
        "— Sorteos mensuales\n"
        "— Y muchas sorpresas más\n\n"
        "💬 En el chat puedes:\n"
        "— Resolver tus dudas\n"
        "— Compartir experiencias con otros vapeadores\n"
        "— Participar de una comunidad respetuosa, solo para mayores de 18 años y libre de spam\n\n"
        "Gracias por tu compra y por ser parte de este espacio 🤝\n"
        "¡Esperamos que disfrutes tu estadía!\n\n"
        "🎁 Recuerda que con tu compra ya estás participando en nuestro sorteo mensual. "
        "Solo debes revisar las bases y completar el formulario en el siguiente enlace 👇"
    )

    kb = [
        [
            InlineKeyboardButton("📣 Canal", url=CHANNEL_URL),
            InlineKeyboardButton("💬 Chat", url=GROUP_URL),
        ],
        [
            InlineKeyboardButton("📋 Bases del sorteo", url="https://www.mundovapo.cl")
        ]
    ]

    await update.message.reply_text(
        mensaje,
        reply_markup=InlineKeyboardMarkup(kb),
        disable_web_page_preview=True
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
