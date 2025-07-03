import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from telegram_bot import (
    start, menu_handler, recibir_nombre, recibir_codigo_estudiante, recibir_dni,
    recibir_empresa, recibir_ruc_empresa, recibir_direccion, cancel, descargar_carta_callback,
    MENU, NOMBRE, CODIGO, DNI, EMPRESA, RUC_EMPRESA, DIRECCION
)

TOKEN = os.environ.get("TELEGRAM_TOKEN", "TU_TOKEN_AQUI")
bot = Bot(token=TOKEN)

app = Flask(__name__)

dispatcher = Dispatcher(bot, None, workers=4, use_context=True)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        MENU: [MessageHandler(Filters.text & ~Filters.command, menu_handler)],
        NOMBRE: [MessageHandler(Filters.text & ~Filters.command, recibir_nombre)],
        CODIGO: [MessageHandler(Filters.text & ~Filters.command, recibir_codigo_estudiante)],
        DNI: [MessageHandler(Filters.text & ~Filters.command, recibir_dni)],
        EMPRESA: [MessageHandler(Filters.text & ~Filters.command, recibir_empresa)],
        RUC_EMPRESA: [MessageHandler(Filters.text & ~Filters.command, recibir_ruc_empresa)],
        DIRECCION: [MessageHandler(Filters.text & ~Filters.command, recibir_direccion)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
    allow_reentry=True
)
dispatcher.add_handler(conv_handler)
dispatcher.add_handler(CallbackQueryHandler(descargar_carta_callback, pattern=r"^descargar_carta\|"))

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def health():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8443) 