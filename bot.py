# Requisitos:
#   pip install python-telegram-bot==21.4
# Start local: python bot.py
# Start en Render: Start Command -> python bot.py

import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

# ===== LOGGING =====
logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s | %(message)s", level=logging.INFO)
log = logging.getLogger("mundovapo-bot")

# ===== TU CONFIG =====
TOKEN = "PEGA_AQUI_EL_TOKEN_NUEVO"
CHANNEL_URL = "https://t.me/+jS_YKiiHgcw3OTRh"
GROUP_URL   = "https://t.me/+kL7eSPE27805ZGRh"
SORTEO_URL  = "https://www.mundovapo.cl"
FORM_URL    = "https://docs.google.com/forms/d/e/1FAIpQLSct9QIex5u95sdnaJdXDC4LeB-WBlcdhE7GXoUVh3YvTh_MlQ/viewform"
WHATSAPP_TXT = "+56 9 9324 5860"
WHATSAPP_URL = "https://www.mundovapo.cl"  # luego cámbialo a tu wa.me

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

# ===== Handlers =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name or "amig@"
    mensaje = (
        f"👋 ¡Bienvenid@, {nombre}!<br><br>"
        "Nos alegra mucho tenerte por aquí 🌿<br>"
        "En plataformas como Instagram es muy difícil mantener una cuenta dedicada a vaporizadores, "
        "por eso decidimos crear esta comunidad exclusiva para quienes confían en nosotros 💚<br><br>"
        "📣 <b>En el canal</b> podrás estar al tanto de:<br>"
        "— Nuevos lanzamientos<br>— Descuentos especiales<br>— Sorteos mensuales<br>— Y más<br><br>"
        "💬 <b>En el chat</b> puedes resolver dudas y participar en una comunidad respetuosa (+18, sin spam).<br><br>"
        "Gracias por tu compra 🤝 Ya estás participando en el sorteo mensual. "
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
        texto = "❓ <b>Preguntas frecuentes</b><br><br>Selecciona una categoría:"
        await cq.edit_message_text(
            texto, reply_markup=kb_faq_menu(),
            disable_web_page_preview=True, parse_mode=ParseMode.HTML
        )
        return

    if data == "faq_envios":
        texto = (
            "✈️ <b>Envíos</b><br><br>"
            "Envíos a todo Chile por courier. Despacho en máximo 48 h hábiles.<br>"
            "Al enviar, te llegará el tracking por correo.<br><br>"
            f"📩 ¿No recibiste el tracking? Escríbenos por WhatsApp: {WHATSAPP_TXT}"
        )
    elif data == "faq_garantias":
        texto = (
            "🛠️ <b>Garantías</b><br><br>"
            "Cada artículo tiene garantía original del fabricante (ver descripción del producto).<br><br>"
            "No cubre daños por mal uso. Para evaluación, completa el formulario y espera respuesta (≤ 48 h hábiles):<br>"
            f"🔗 <a href=\"{FORM_URL}\">Formulario de garantía</a><br><br>"
            "📬 Soporte: <a href=\"mailto:soporte@mundovapo.cl\">soporte@mundovapo.cl</a> o WhatsApp."
        )
    else:
        texto = "Selecciona una opción válida."

    await cq.edit_message_text(
        texto, reply_markup=kb_faq_menu(),
        disable_web_page_preview=True, parse_mode=ParseMode.HTML
    )

# ===== Arranque asíncrono correcto (PTB 21) =====
async def main():
    if not TOKEN or TOKEN.startswith("PEGA_AQUI"):
        raise RuntimeError("⚠️ Pega tu TOKEN nuevo antes de ejecutar.")

    app: Application = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(faq_router, pattern="^faq"))

    # 1) Elimina cualquier webhook previo y descarta updates pendientes
    await app.bot.delete_webhook(drop_pending_updates=True)

    # 2) Inicializa y arranca polling
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
