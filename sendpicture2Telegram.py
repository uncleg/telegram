from telegram.ext import Updater, CommandHandler
import telegram
import datetime
import subprocess
import ConfigParser
#import picamera 


#loading sensitive variables from config file
config = ConfigParser.ConfigParser()
config.read("../sensorCAM.conf")
token=config.get('Telegram','token')
chat_id=config.getint('Telegram','chat_id')


#setting other variables
global p

#@authenticate
'''
def start(bot, update):
	if update.message.chat_id == chat_id: 
		update.message.reply_text('Welcome')
	else:
		update.message.reply_text('Sorry. Action not allowed for you')
    	print "Access not allowed"+update.message.chat_id
'''
def start(bot, update):
	if update.message.chat_id == chat_id: 
		update.message.reply_text('Starting sensorCAM...')
		#p = subprocess.Popen(["python","/home/pi/Arduino/just-sensoring-telegram.py"],stdout=subprocess.PIPE)
		global p
		p = subprocess.Popen(["python","printing.py"],stdout=subprocess.PIPE)
		update.message.reply_text(p.pid)
	else:
		update.message.reply_text('Sorry. Action not allowed for you')
    	print "Access not allowed"+update.message.chat_id

def stop(bot, update):
	global p
	if update.message.chat_id == chat_id: 
		update.message.reply_text('Stopping sensorCAM...')
		#p.kill()
		p.terminate()
	else:
		update.message.reply_text('Sorry. Action not allowed for you')
    	print "Access not allowed"+update.message.chat_id

def status(bot, update):
	global p
	if update.message.chat_id == chat_id: 
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
def hello(bot, update):
    if update.message.chat_id == chat_id:
   		update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))
    else: 
    	update.message.reply_text('Sorry. Action not allowed for you')
    	print "Access not allowed"+update.message.chat_id
    	print update.users.userFull(update.message.chat_id)

#@authenticate
def capture(bot, update):
    cantidad=5
    if update.message.chat_id == chat_id:
		stop()
		status()
		start()	
    else:
		update.message.reply_text('Sorry. Action not allowed for you')
		print "Access not allowed"+update.message.chat_id
    
#camera = picamera.PiCamera()

updater = Updater(token)
#bot = telegram.Bot(token='415654247:AAExstPW8p9OBka7Pt8RcTIxkZt0pug-CSQ')


updater.dispatcher.add_handler(CommandHandler('start', start))
#updater.dispatcher.add_handler(CommandHandler('inicio', inicio))
updater.dispatcher.add_handler(CommandHandler('stop', stop))
updater.dispatcher.add_handler(CommandHandler('status', status))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('capture', capture))

updater.start_polling()
updater.idle()

