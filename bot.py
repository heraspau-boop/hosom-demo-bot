"""
Bot Telegram súper simple para la DEMO HOSOM
- Deep-link: /start demo_<territory_id>_<topic_id>
- Responde con "wizard simulado" + botones:
  - Abrir miniapp
  - Ver grupo demo (opcional)
"""
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())
import os
import re
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MINIAPP_URL = os.getenv("MINIAPP_URL", "")
FALLBACK_GROUP_URL = os.getenv("FALLBACK_GROUP_URL", "")

START_RE = re.compile(r"^demo_([a-z0-9\-]+)_([a-z0-9\-]+)$", re.IGNORECASE)

WIZARD_TEXT_DEFAULT = (
    "Aquest adjetiu encara no té grup en aquest territori.\n"
    "A la versió real, aquí hi hauria un wizard per crear-lo."
)

def build_keyboard(miniapp_url: str, fallback_group_url: str) -> InlineKeyboardMarkup:
    rows = []
    if miniapp_url:
        rows.append([InlineKeyboardButton("Obrir miniapp", web_app=WebAppInfo(url=miniapp_url))])
    if fallback_group_url:
        rows.append([InlineKeyboardButton("Veure grup demo", url=fallback_group_url)])
    return InlineKeyboardMarkup(rows) if rows else InlineKeyboardMarkup([])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args or []
    payload = args[0] if args else ""

    territory_id = None
    topic_id = None

    m = START_RE.match(payload) if payload else None
    if m:
        territory_id, topic_id = m.group(1), m.group(2)

    wizard_text = os.getenv("WIZARD_TEXT", WIZARD_TEXT_DEFAULT)

    if territory_id and topic_id:
        text = (
            f"🧩 *Wizard simulat*\n\n"
            f"Territori: `{territory_id}`\n"
            f"Adjetiu (topic_id): `{topic_id}`\n\n"
            f"{wizard_text}"
        )
    else:
        text = (
            "👋 Hola! Sóc el bot de la *DEMO HOSOM*.\n\n"
            "Si vens de la miniapp, rebré un deep-link com:\n"
            "`/start demo_<territory_id>_<topic_id>`\n\n"
            "Obre la miniapp i clica un adjetiu 'per crear'."
        )

    kb = build_keyboard(MINIAPP_URL, FALLBACK_GROUP_URL)
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit("Missing BOT_TOKEN. Set it in environment or .env")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
