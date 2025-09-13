# Requisitos:
#   pip install python-telegram-bot==21.4
# Ejecutar:
#   python bot.py

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

# ===== LOGGING =====
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("mundovapo-bot")

# ===== CONFIGURA AQUÍ (TU INFO) =====
TOKEN = "8375588470:AAHuxxlHvHeDcnAYbs5pI39aZoqySIFUDaI"
CHANNEL_URL = "https://t.me/+jS_YKiiHgcw3OTRh"   # Enlace de invitación o @usuario si es público
GROUP_URL   = "https://t.me/+kL7eSPE27805ZGRh"   # Enlace de invitación o @usuario si es público
SORTEO_URL  = "https://www.mundovapo.cl"        # Página con bases / formulario (temporal)
FORM_URL    = "https://docs.google.com/forms/d/e/1FAIpQLSct9QIex5u95sdnaJdXDC4LeB-WBlcdhE7GXoUVh3YvTh_MlQ/viewform"
WHATSAPP_URL = "https://www.mundovapo.cl"       # Cuando esté listo: p.ej. https://wa.me/56993245860
WHATSAPP_TXT = "+56 9 9324 5860"                # Texto que mostramos en FAQ Envíos

# ===== TECLADOS =====
def kb_principal():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📣 Canal", url=CHANNEL_URL),
         InlineKeyboardButton("💬 Chat", url=GROUP_URL)],
        [InlineKeyboardButton("📋 Bases del sorteo", url=SORTEO_URL)],
        [InlineKeyboardButton("❓ Preguntas frecuentes", callback_data="faq_menu")],
        [InlineKeyboardButton("🟢📱 Atención por WhatsApp", url=WHATSAPP_URL)]
    ])

def kb_faq_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚚 Envíos", callback_data="faq_envios")],
        [InlineKeyboardButton("🛠️ Garantías", callback_data="faq_garantias")],
        [InlineKeyboardButton("⬅️ Volver", callback_data="faq_back")]
    ])

# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
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
        await update.message.reply_text(
            mensaje,
            reply_markup=kb_principal(),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        log.exception("Error en /start: %s", e)

# ===== FAQ (router de callbacks) =====
async def faq_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cq = update.callback_query
    try:
        await cq.answer()
        data = cq.data or ""

        if data in ("faq_menu", "faq_back"):
            texto = (
                "❓ <b>Preguntas frecuentes</b><br><br>"
                "Selecciona una categoría para ver más información:"
            )
            await cq.edit_message_text(
                texto,
                reply_markup=kb_faq_menu(),
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML
            )
            return

        if data == "faq_envios":
            texto = (
                "✈️ <b>Envíos</b><br><br>"
                "Realizamos envíos a todo Chile mediante empresas de courier.<br>"
                "Los pedidos se despachan en un máximo de 48 horas hábiles.<br>"
                "Una vez enviado, recibirás un correo con el número de seguimiento.<br><br>"
                f"📩 Si no has recibido tu tracking por correo, contáctanos por WhatsApp: {WHATSAPP_TXT}"
            )
            await cq.edit_message_text(
                texto,
                reply_markup=kb_faq_menu(),
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML
            )
            return

        if data == "faq_garantias":
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
            await cq.edit_message_text(
                texto,
                reply_markup=kb_faq_menu(),
                disable_web_page_preview=True,
                parse_mode=ParseMode.HTML
            )
            return

        # Cualquier otra callback: volver al menú FAQ
        await cq.edit_message_text(
            "❓ <b>Preguntas frecuentes</b><br>Selecciona una categoría:",
            reply_markup=kb_faq_menu(),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        log.exception("Error en faq_router (%s): %s", getattr(cq, "data", "?"), e)
        try:
            await cq.edit_message_text(
                "⚠️ Ocurrió un error al cargar la información. Intenta de nuevo.",
                reply_markup=kb_faq_menu(),
                parse_mode=ParseMode.HTML
            )
        except Exception:
            pass

# ===== MAIN =====
def main():
    if not TOKEN or TOKEN.startswith("PEGA_AQUI"):
        raise RuntimeError("⚠️ Debes pegar tu TOKEN de @BotFather en la variable TOKEN.")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(faq_router, pattern="^faq"))

    log.info("✅ Bot iniciado. Presiona Ctrl+C para detener.")
    app.run_polling()

if __name__ == "__main__":
    main()
