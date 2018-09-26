import fit_values


command_value=0

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Bot iniciado!! Este bot, permite reconocer a las personas "
                                                          "registradas, en cada foto que se envíe. También permite "
                                                          "registrar nuevas personas, usando el comando "
                                                          "'/addperson <nombre_persona>' antes de enviar una foto de la "
                                                          "persona a añadir (solo debe aparecer esa persona en la foto).\n "
                                                          "¡¡Gracias por usar el Bot!!")


def fit(bot, update, args):
    if not str(' '.join(args)).strip().__eq__(""):
        fit_values.NAME = ' '.join(args)
        fit_values.FIT=1
        bot.send_message(chat_id=update.message.chat_id, text="Envia una foto de "+str(fit_values.NAME)+" (solo debe aparecer él/ella)")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="El nombre no debe estar en blanco")
