from telegram.ext import Updater, CommandHandler
import telegram
import datetime
import subprocess
import ConfigParser
#import picamera 


#loading sensitive variables from config file
config = ConfigParser.ConfigParser()
config.read("/etc/sensorCAM/sensorCAM.conf")
token=config.get('Telegram','token')
chat_id=config.get('Telegram','chat_id').split(',')


#setting other variables
global p

#@authenticate

def help(bot, update):
	if str(update.message.chat_id) in chat_id: 
		update.message.reply_text('Tienes disponibles los siguientes comandos:')
		update.message.reply_text('/up  Inicia el sensorCAM')
		update.message.reply_text('/down  Apaga el sensorCAM')
		update.message.reply_text('/status  Muestra el status del sensorCAM')
	else:
		update.message.reply_text('Sorry. Action not allowed for you')
    	print "Access not allowed"+update.message.chat_id

def up_sensor(bot, update):
	if str(update.message.chat_id) in chat_id: 
		update.message.reply_text('Starting sensorCAM...')
	        global p	
                p = subprocess.Popen(["python","/home/pi/telegram/sensoring2telegram.py"],stdout=subprocess.PIPE)
		update.message.reply_text(p.pid)
	else:
		update.message.reply_text('Sorry. Action not allowed for you')
    	print "Access not allowed"+update.message.chat_id

def down_sensor(bot, update):
	global p
	print sensorCAM
	if str(update.message.chat_id) in chat_id: 
		update.message.reply_text('Stopping sensorCAM...')
		#p.kill()
		p.terminate()
	else:
		update.message.reply_text('Sorry. Action not allowed for you')
    	print "Access not allowed"+update.message.chat_id

def status(bot, update):
	global p
	if str(update.message.chat_id) in chat_id: 
		update.message.reply_text('sensorCAM Status:')
		if p.poll() == None:
			update.message.reply_text('sensorCAM Alive with PID:')
			update.message.reply_text(p.pid)
		else: 
			update.message.reply_text('sensorCAM is NOT Alive')
	else:
		update.message.reply_text('Sorry. Action not allowed for you')
    	print "Access not allowed"+update.message.chat_id

#@authenticate
def start(bot, update):
    if str(update.message.chat_id) in chat_id:
   		update.message.reply_text(
        'Hello {}. Welcome to BotAlarma!'.format(update.message.from_user.first_name))
    else: 
    	update.message.reply_text('Sorry. Action not allowed for you')
    	print type(update.message.chat_id)

updater = Updater(token)
updater.dispatcher.add_handler(CommandHandler('?', help))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('up', up_sensor))
updater.dispatcher.add_handler(CommandHandler('down', down_sensor))
updater.dispatcher.add_handler(CommandHandler('status', status))

updater.start_polling()
updater.idle()

