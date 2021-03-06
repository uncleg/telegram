#!/usr/bin/python
from time import sleep #Import time library
from time import gmtime, localtime, strftime
import serial
import json
import telegram
import picamera
import ConfigParser

ser = serial.Serial('/dev/ttyACM0', 115200)
camera = picamera.PiCamera()

eventID=0

#loading sensitive variables from config file
config = ConfigParser.ConfigParser()
config.read("/etc/sensorCAM/sensorCAM.conf")
token=config.get('Telegram','token')
chat_id=config.get('Telegram','chat_id').split(',')
bot = telegram.Bot(token=token)

def capture(cantidad, evento=0):
    i=0
    imagenes = []
    for i in range(cantidad):
		imagen="evento_"+str(evento)+"_image-"+strftime("%d%b%Y-%H:%M:%S", gmtime())+".jpg"
                imagenes.append(imagen)
		camera.capture(imagen)
		sleep(2)
    return imagenes[2]

try:
    while (True):
    	line = ser.readline()
        data = {}	
        if "motion detected" in line:
            eventID+=1
            start_time= strftime("%d%b%Y-%H:%M:%S", localtime())
            imagen_telegram=capture(5, eventID)
        elif "motion ended" in line:
            stop_time= strftime("%d%b%Y-%H:%M:%S", localtime())	
            data['Description']="Movimiento detectado"
            data['eventID']=eventID 
            data['start']=start_time
            data['stop']=stop_time 
            json_data = json.dumps(data)
            mensaje_a_telegram=data['Description']+" Incio:"+data['start']+" Fin:"+data['stop']
            for chat_owner in chat_id: 
                bot.send_message(chat_id=chat_owner, text=mensaje_a_telegram)
                bot.send_photo(chat_id=chat_owner, photo=open(imagen_telegram, 'rb'))

except KeyboardInterrupt:
        print "Exit PIR Sensoring..."	
     
