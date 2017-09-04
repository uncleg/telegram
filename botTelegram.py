#!/usr/bin/python

from telegram.ext import Updater, CommandHandler
import telegram
import datetime
import subprocess
import ConfigParser

#loading sensitive variables from config file
config = ConfigParser.ConfigParser()
config.read("/etc/sensorCAM/sensorCAM.conf")
token=config.get('Telegram','token')
chat_id=config.get('Telegram','chat_id').split(',')

#setting other variables
global p 
senderbot = telegram.Bot(token=token)

#@authenticate
def help(bot, update):
	if str(update.message.chat_id) in chat_id: 
		update.message.reply_text('Tienes disponibles los siguientes comandos:')
		update.message.reply_text('/up  Inicia el sensorCAM')
		update.message.reply_text('/down  Apaga el sensorCAM')
		update.message.reply_text('/status  Muestra el status del sensorCAM')
	else:
		update.message.reply_text('Sorry. Action not allowed for you')
#    	print "Access not allowed"+update.message.chat_id

def up_sensor(bot, update):
	if str(update.message.chat_id) in chat_id: 
		update.message.reply_text('Starting sensorCAM...')
       	        global p	
                p = subprocess.Popen(["python","/home/pi/telegram/sensoring2telegram.py"],stdout=subprocess.PIPE)
		update.message.reply_text(p.pid)
	else:
		update.message.reply_text('Sorry. Action not allowed for you')
    #	        print "Access not allowed"+update.message.chat_id

def down_sensor(bot, update):
	global p
	if str(update.message.chat_id) in chat_id: 
		user_bajador=update.message.from_user.first_name
		p.terminate()
		mensaje_a_telegram=user_bajador+' is Stopping sensorCAM...' 
        for chat_owner in chat_id: 
            senderbot.send_message(chat_id=chat_owner, text=mensaje_a_telegram)	
	else:
		update.message.reply_text('Sorry. Action not allowed for you'+chat_id)
#    	print "Access not allowed"+update.message.chat_id

def status(bot, update):
	global p
	if str(update.message.chat_id) in chat_id: 
		update.message.reply_text('Status:')
		if p.poll() == None:
			update.message.reply_text('sensorCAM is ALIVE with PID:')
			update.message.reply_text(p.pid)
		else: 
			update.message.reply_text('sensorCAM is NOT Alive')
	else:
		update.message.reply_text('Sorry. Action not allowed for you')
 #   	print "Access not allowed"+update.message.chat_id

def who(mac_address):
	process=subprocess.Popen(["sudo","l2ping","-c 5",mac_address], stdout=subprocess.PIPE ,stderr=subprocess.STDOUT)
	returncode = process.wait() #capturo posibles errores 
	if returncode:
		return " no esta en casa"
	else: 
		return " esta en casa"

def who_is_here(bot, update):
	for name, value in config.items('Users'):
    	    mensaje_a_telegram=name +who(value)
    	    update.message.reply_text(mensaje_a_telegram)


#@authenticate
def start(bot, update):
    if str(update.message.chat_id) in chat_id:
   		update.message.reply_text(
        'Hello {}. Welcome to BotAlarma!'.format(update.message.from_user.first_name))
    else: 
    	update.message.reply_text('Sorry. Action not allowed for you')
#    	print type(update.message.chat_id)

updater = Updater(token)
updater.dispatcher.add_handler(CommandHandler('?', help))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('up', up_sensor))
updater.dispatcher.add_handler(CommandHandler('down', down_sensor))
updater.dispatcher.add_handler(CommandHandler('status', status))
updater.dispatcher.add_handler(CommandHandler('who', who_is_here))

updater.start_polling()
updater.idle()

