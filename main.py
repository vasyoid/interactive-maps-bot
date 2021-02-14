import logging
import os
import sys

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters


from transform import Transform
from image import ImageGenerator

PORT = int(os.environ.get('PORT', 5000))
TOKEN = "1681865021:AAFbfIlHUtTyBCnSoZznVPq_tIzSybbl9dM"

tm = Transform()
image_generator = ImageGenerator()


def start_handler(update: Update, context):
    logging.info("start command received")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send me your location and I'll point it on a map")
    logging.info("start command done")


def location_handler(update: Update, context):
    logging.info("location received")
    loc = update.message.location.latitude, update.message.location.longitude
    pos = tm.apply(loc)
    image = image_generator.generate(pos)
    if not image:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Could not find location:\n{loc}")
        logging.info("location done (fail)")
    else:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=image)
        logging.info("location done (success)")


if __name__ == '__main__':
    logging.info("starting app")
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(MessageHandler(filters=Filters.location, callback=location_handler))
    if len(sys.argv) == 2 and sys.argv[1] == "polling":
        logging.info("app started")
        updater.start_polling()
    elif len(sys.argv) == 2 and sys.argv[1] == "webhook":
        logging.info("app started")
        updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
        updater.bot.set_webhook('https://interactive-maps-bot.herokuapp.com/' + TOKEN)
        updater.idle()
    else:
        logging.error(f"\tusage: python {sys.argv[0]} [MODE]")
        logging.error("\tMODES:")
        logging.error("\tpolling\t\trun in polling mode (get updates proactively)")
        logging.error("\twebhook\t\trun in webhook mode (get updates reactively)")
