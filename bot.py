# Requisitos: python-telegram-bot==21.4
# Ejecutar:
#   pip install python-telegram-bot==21.4
#   python bot.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

# ===== CONFIGURA AQUÍ =====
TOKEN = "8375588470:AAHuxxlHvHeDcnAYbs5pI39aZoqySIFUDaI"
CHANNEL_URL = "https://t.me/+jS_YKiiHgcw3OTRh"
GROUP_URL   = "https://t.me/+kL7eSPE27805ZGRh"
SORTEO_URL  = "https://www.mundovapo.cl"

# ===== FUNCIÓN PRINCIPAL DE BIENVENIDA =====
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
            InlineKeyboardButton("📋 Bases del sorteo", url=SORTEO_URL)
        ],
        [
            InlineKeyboardButton("❓ Preguntas frecuentes", callback_data="faq")
        ]
    ]

    await update.message.reply_text(
        mensaje,
        reply_markup=InlineKeyboardMarkup(kb),
        disable_web_page_preview=True
    )

# ===== MENÚ FAQ =====
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🚚 Envíos", callback_data="faq_envios")],
        [InlineKeyboardButton("🛠️ Garantías", callback_data="faq_garantias")],
    ]
    await update.callback_query.message.reply_text(
        "❓ Selecciona una categoría para ver más información:",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def faq_respuesta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.callback_query.data
    if data == "faq_envios":
        texto = (
            "✈️ **Envíos**\n\n"
            "Realizamos envíos a todo Chile mediante empresas de courier.\n"
            "Los pedidos se despachan en un máximo de 48 horas hábiles.\n"
            "Una vez enviado, recibirás un correo con el número de seguimiento.\n\n"
            "📩 Si no has recibido tu tracking por correo, contáctanos por WhatsApp: +56 9 9324 5860"
        )
    elif data == "faq_garantias":
        texto = (
            "🛠️ **Garantías**\n\n"
            "Cada artículo cuenta con una garantía original del fabricante, la cual está detallada en la descripción del producto.\n\n"
            "Las garantías no cubren daños causados por mal uso del producto. "
            "Para solicitar una evaluación, completa el siguiente formulario y espera nuestra respuesta en un máximo de 48 horas hábiles:\n"
            "🔗 https://docs.google.com/forms/d/e/1FAIpQLSct9QIex5u95sdnaJdXDC4LeB-WBlcdhE7GXoUVh3YvTh_MlQ/viewform\n\n"
            "📬 Si necesitas más información sobre el estado de tu garantía, puedes contactarnos en cualquier momento al correo soporte@mundovapo.cl, "
            "a través del chat de nuestra tienda o por WhatsApp."
        )
    else:
        texto = "Selecciona una opción válida."

    await update.callback_query.message.reply_text(
        texto,
        disable_web_page_preview=True,
        parse_mode="Markdown"
    )

# ===== MAIN =====
def main():
    if not TOKEN or TOKEN.startswith("PEGA_AQUI"):
        raise RuntimeError("⚠️ Debes pegar tu TOKEN de @BotFather en la variable TOKEN.")
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(faq, pattern="^faq$"))
    app.add_handler(CallbackQueryHandler(faq_respuesta, pattern="^faq_"))
    
    print("✅ Bot iniciado. Presiona Ctrl+C para detener.")
    app.run_polling()

if __name__ == "__main__":
    main()
