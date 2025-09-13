# Requisitos: python-telegram-bot==21.4
# Ejecutar:
#   pip install python-telegram-bot==21.4
#   python bot.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

# ===== CONFIGURA AQUÍ =====
TOKEN = "8375588470:AAHuxxlHvHeDcnAYbs5pI39aZoqySIFUDaI"
CHANNEL_URL = "https://t.me/+jS_YKiiHgcw3OTRh"
GROUP_URL   = "https://t.me/+kL7eSPE27805ZGRh"
SORTEO_URL  = "https://www.mundovapo.cl"
FORM_URL    = "https://docs.google.com/forms/d/e/1FAIpQLSct9QIex5u95sdnaJdXDC4LeB-WBlcdhE7GXoUVh3YvTh_MlQ/viewform"
WHATSAPP    = "+56 9 9324 5860"

# ===== FUNCIÓN PRINCIPAL DE BIENVENIDA =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name or "amig@"
    
    mensaje = (
        f"👋 ¡Bienvenid@, {nombre}!<br><br>"
        "Nos alegra mucho tenerte por aquí 🌿<br>"
        "En plataformas como Instagram es muy difícil mantener una cuenta dedicada a vaporizadores, "
        "por eso decidimos crear esta comunidad exclusiva para quienes confían en nosotros 💚<br><br>"
        "📣 <b>En el canal</b> podrás estar al tanto de:<br>"
        "— Nuevos lanzamientos<br>"
        "— Descuentos especiales<br>"
        "— Sorteos mensuales<br>"
        "— Y muchas sorpresas más<br><br>"
        "💬 <b>En el chat</b> puedes:<br>"
        "— Resolver tus dudas<br>"
        "— Compartir experiencias con otros vapeadores<br>"
        "— Participar de una comunidad respetuosa, solo para mayores de 18 años y libre de spam<br><br>"
        "Gracias por tu compra y por ser parte de este espacio 🤝<br>"
        "¡Esperamos que disfrutes tu estadía!<br><br>"
        "🎁 Recuerda que con tu compra <b>ya estás participando</b> en nuestro sorteo mensual. "
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
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML
    )

# ===== MENÚ FAQ =====
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Responde la callback para que no quede “cargando”
    await update.callback_query.answer()
    kb = [
        [InlineKeyboardButton("🚚 Envíos", callback_data="faq_envios")],
        [InlineKeyboardButton("🛠️ Garantías", callback_data="faq_garantias")],
    ]
    await update.callback_query.message.reply_text(
        "❓ Selecciona una categoría para ver más información:",
        reply_markup=InlineKeyboardMarkup(kb),
        parse_mode=ParseMode.HTML
    )

async def faq_respuesta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cq = update.callback_query
    await cq.answer()  # siempre responder la callback

    data = cq.data
    if data == "faq_envios":
        texto = (
            "✈️ <b>Envíos</b><br><br>"
            "Realizamos envíos a todo Chile mediante empresas de courier.<br>"
            "Los pedidos se despachan en un máximo de 48 horas hábiles.<br>"
            "Una vez enviado, recibirás un correo con el número de seguimiento.<br><br>"
            f"📩 Si no has recibido tu tracking por correo, contáctanos por WhatsApp: {WHATSAPP}"
        )
    elif data == "faq_garantias":
        texto = (
            "🛠️ <b>Garantías</b><br><br>"
            "Cada artículo cuenta con una garantía original del fabricante, la cual está detallada en la descripción del producto.<br><br>"
            "Las garantías no cubren daños causados por mal uso del producto. "
            "Para solicitar una evaluación, completa el formulario y espera nuestra respuesta en un máximo de 48 horas hábiles:<br>"
            f"🔗 <a href=\"{FORM_URL}\">Formulario de garantía</a><br><br>"
            "📬 Si necesitas más información sobre el estado de tu garantía, puedes contactarnos en cualquier momento al correo "
            "<a href=\"mailto:soporte@mundovapo.cl\">soporte@mundovapo.cl</a>, "
            "a través del chat de nuestra tienda o por WhatsApp."
        )
    else:
        texto = "Selecciona una opción válida."

    await cq.message.reply_text(
        texto,
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML
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
