# Requisitos:
#   pip install python-telegram-bot==21.4
# Start local:  python bot.py
# En Render:    Start Command -> python bot.py

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

# ===== LOGGING =====
logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s | %(message)s", level=logging.INFO)
log = logging.getLogger("mundovapo-bot")

# ===== CONFIG =====
TOKEN = "8375588470:AAHM8HX5_Z0wq4qHEglmB9sJ6el3DTy5dEM"
CHANNEL_URL = "https://t.me/+jS_YKiiHgcw3OTRh"
GROUP_URL   = "https://t.me/+kL7eSPE27805ZGRh"
SORTEO_URL  = "https://www.mundovapo.cl"
FORM_URL    = "https://docs.google.com/forms/d/e/1FAIpQLSct9QIex5u95sdnaJdXDC4LeB-WBlcdhE7GXoUVh3YvTh_MlQ/viewform"
WHATSAPP_TXT = "+56 9 9324 5860"
WHATSAPP_URL = "https://www.mundovapo.cl"   # Cambia luego por tu wa.me

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
        [InlineKeyboardButton("⬅️ Volver", callback_data="faq_menu")]
    ])

# ===== UTIL =====
async def safe_edit(cq, text, markup):
    """Edita el mensaje; si el contenido es idéntico, ignora el error."""
    try:
        await cq.edit_message_text(
            text, reply_markup=markup,
            disable_web_page_preview=True, parse_mode=ParseMode.HTML
        )
    except BadRequest as e:
        if "message is not modified" in str(e).lower():
            # Ya estás en ese menú; no pasa nada
            await cq.answer("Ya estás en este menú.", show_alert=False)
        else:
            raise

# ===== Handlers =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name or "amig@"
    mensaje = (
        f"👋 ¡Bienvenid@, {nombre}!\n\n"
        "Nos alegra mucho tenerte por aquí 🌿\n"
        "En plataformas como Instagram es muy difícil mantener una cuenta dedicada a vaporizadores, "
        "por eso decidimos crear esta comunidad exclusiva para quienes confían en nosotros 💚\n\n"
        "📣 <b>En el canal</b> podrás estar al tanto de:\n"
        "— Nuevos lanzamientos\n— Descuentos especiales\n— Sorteos mensuales\n— Y más\n\n"
        "💬 <b>En el chat</b> puedes resolver dudas y participar en una comunidad respetuosa (+18, sin spam).\n\n"
        "Gracias por tu compra 🤝 Ya estás participando en el sorteo mensual.\n"
        "Revisa las bases y formulario en el enlace 👇"
    )
    await update.message.reply_text(
        mensaje, reply_markup=kb_principal(),
        disable_web_page_preview=True, parse_mode=ParseMode.HTML
    )

async def faq_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cq = update.callback_query
    await cq.answer()
    data = cq.data or "faq_menu"

    if data == "faq_menu":
        texto = "❓ <b>Preguntas frecuentes</b>\n\nSelecciona una categoría:"
        await safe_edit(cq, texto, kb_faq_menu())
        return

    if data == "faq_envios":
        texto = (
            "✈️ <b>Envíos</b>\n\n"
            "Envíos a todo Chile por courier. Despacho en máximo 48 h hábiles.\n"
            "Al enviar, te llegará el tracking por correo.\n\n"
            f"📩 ¿No recibiste el tracking? Escríbenos por WhatsApp: {WHATSAPP_TXT}"
        )
        await safe_edit(cq, texto, kb_faq_menu())
        return

    if data == "faq_garantias":
        texto = (
            "🛠️ <b>Garantías</b>\n\n"
            "Cada artículo tiene garantía original del fabricante (ver descripción del producto).\n\n"
            "No cubre daños por mal uso. Para evaluación, completa el formulario y espera respuesta (≤ 48 h hábiles):\n"
            f"🔗 <a href=\"{FORM_URL}\">Formulario de garantía</a>\n\n"
            "📬 Soporte: <a href=\"mailto:soporte@mundovapo.cl\">soporte@mundovapo.cl</a> o WhatsApp."
        )
        await safe_edit(cq, texto, kb_faq_menu())
        return

    # Fallback
    await safe_edit(cq, "❓ <b>Preguntas frecuentes</b>\n\nSelecciona una categoría:", kb_faq_menu())

# ===== MAIN =====
if __name__ == "__main__":
    if not TOKEN or TOKEN.startswith("PEGA_AQUI"):
        raise SystemExit("⚠️ Pega tu TOKEN nuevo antes de ejecutar.")
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(faq_router, pattern="^faq"))
    application.run_polling(drop_pending_updates=True)


