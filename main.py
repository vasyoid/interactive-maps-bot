import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters


from transform import Transform
from image import ImageGenerator

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
    updater = Updater(token='1681865021:AAFbfIlHUtTyBCnSoZznVPq_tIzSybbl9dM')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(MessageHandler(filters=Filters.location, callback=location_handler))
    logging.info("app started")
    updater.start_polling()

