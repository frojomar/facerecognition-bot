import fit_values
import base64
import cv2
import requests
from PIL import Image
import io
import numpy as np
import json


def get_image_base64_encoded(name_image):
    img_received = cv2.imread(name_image)
    retval, buffer = cv2.imencode('.jpg', img_received)
    img_received_encoded = base64.b64encode(buffer)
    #print("opencv")
    # print(img_received_encoded)
    # print(img_received_encoded.decode('utf-8'))
    return img_received_encoded.decode('utf-8')

# Take in base64 string and return PIL image
def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))

# convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

def recognizer(bot, update, remove_caption=False, custom_caption=None):
    print("NUEVA SOLICITUD")

    message = update.message

    caption = custom_caption

    file_id = message.photo[-1].file_id

    chat_id= message.chat_id

    newFile = bot.getFile(file_id,timeout=300)
    newFile.download('images/received.jpg')


###OPCION 1
    img_received_encoded=get_image_base64_encoded('images/received.jpg')

###OPCION 2
    # with open('images/received.jpg', 'r+') as f:
    #     jpgdata = f.read()
    #     f.close()
    #
    #     img_received_encoded = base64.b64encode(jpgdata)
    #
    #     print("python files")
    #     print(img_received_encoded)
##~FIN OPCIONES

    if fit_values.FIT==1:
        print("Solicitando entrenar con nombre '"+str(fit_values.NAME)+"'")

        data = {'image': str(img_received_encoded), 'name': str(fit_values.NAME)}
        print(data)
        fit_values.NAME=""
        fit_values.FIT=0

        response = requests.post('http://127.0.0.1:2090/addPerson', json=data)

        json_data=str(response.text)[1:-2]
        json_data=json_data.replace("'","\"")
        print(json_data)
        json_data = json.loads(json_data)

        print ("ESTADO DE LA RESPUESTA DEL ENTRENAMIENTO: "+ str(response))
        print ("RESPUESTA DEL ENTRENAMIENTO: "+str(response.text))

        response_value=json_data['status']

        if response_value.__eq__("ok"):
            bot.send_message(chat_id=update.message.chat_id, text="Bot entrenado!!")
        elif response_value.__eq__("errorName"):
            bot.send_message(chat_id=update.message.chat_id, text="Entrenamiento fallido: Debe especificar un nombre")
        elif response_value.__eq__("errorImage"):
            bot.send_message(chat_id=update.message.chat_id, text="Entrenamiento fallido: La imagen no contiene personas")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Entrenamiento fallido: Causa desconocida")


    else:

        data={ 'image': str(img_received_encoded)}
        print(data)

        response = requests.post('http://127.0.0.1:2090/', json=data)

        print(response.text)
        img_tosend_encoded=response.text

        imgdata = stringToImage(img_tosend_encoded)
        imgCV = toRGB(imgdata)
        cv2.imwrite('images/result.jpg', imgCV)

        bot.send_photo(chat_id=chat_id, photo=open('images/result.jpg', 'rb'))
