import telegram
from telegram.ext import (Updater,
                          CommandHandler, #para responder ante los comandos
                          MessageHandler, #
                          Filters,
                          InlineQueryHandler,
                          CallbackQueryHandler, updater)

import logging
import constants
import commands
import images


def main():
    a = telegram.Bot(token=constants.TOKEN_BOT)
    print(a.get_me())

    updater= Updater(token=constants.TOKEN_BOT)
    dispatcher= updater.dispatcher #creamos un dispatcher sobre el que dspues asignaremos los manejadores

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) #herramienta para que, cuando falla el bot, sepamos porque falla


    #manejadores de comandos -- asociados a metodos de commands.py

    start_handler= CommandHandler("start",commands.start) #creamos un manejador, asignando a un comando un método
    fit_handler= CommandHandler("addperson", commands.fit, pass_args=True)


    #manejador de imagenes -- asociados a metodos de images.py
    image_handler = MessageHandler(Filters.photo, images.recognizer)


    #añadimos los manejadores que hemos creado antes

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(fit_handler)
    dispatcher.add_handler(image_handler)

    updater.start_polling() #escuchar peticiones. Bucle infinito


if __name__=="__main__":
    main()

    # para que podamos usar el bot en grupos:
    #     *BotFather
    #     */setPrivacy
    #     * si le ponemos DISABLED se puecde usar en grupo, si ponemos ENABLED no se puede usar en grupos
    #
