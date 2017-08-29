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
pid=0

#@authenticate
def start(bot, update):
	if update.message.chat_id == chat_id: 
		update.message.reply_text('Welcome')
	else:
		update.message.reply_text('Sorry. Action not allowed for you')
    	print "Access not allowed"+update.message.chat_id

def inicio(bot, update):
	if update.message.chat_id == chat_id: 
		update.message.reply_text('Starting BotAlarm')
		#p = subprocess.Popen(["python","/home/pi/Arduino/just-sensoring-telegram.py"],stdout=subprocess.PIPE)
		p = subprocess.Popen(["python","printing.py"],stdout=subprocess.PIPE)
		update.message.reply_text(p.pid)
		pid=p.pid
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
		for i in range(cantidad):
			imagen="evento_on-demand_image-"+strftime("%d%b%Y-%H:%M:%S", gmtime())+".jpg"
#		camera.capture(imagen)
			sleep(1)
			update.send_message(chat_id=chat_id, text="Sending images...")
			#update.send_photo(chat_id=chat_id, photo=open(imagen, 'rb'))
    else:
		update.message.reply_text('Sorry. Action not allowed for you')
		print "Access not allowed"+update.message.chat_id
    
#camera = picamera.PiCamera()

updater = Updater(token)
#bot = telegram.Bot(token='415654247:AAExstPW8p9OBka7Pt8RcTIxkZt0pug-CSQ')


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('inicio', inicio))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('capture', capture))
print pid
updater.start_polling()
updater.idle()

