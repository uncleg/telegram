from telegram.ext import Updater, CommandHandler
import telegram
import datetime
import commands
#from ifparser import Ifcfg
import picamera 
import ConfigParser


#loading sensitive variables from config file
config = ConfigParser.ConfigParser()
config.read("../sensorCAM.conf")
token=config.get('Telegram','token')
chat_id=config.getint('Telegram','chat_id')


def start(bot, update):
    update.message.reply_text('Hello World!')

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def ip(bot, update):
	#output = Ifcfg(commands.getoutput('ifconfig -a'))
	resultado = output.interfaces
	update.message.reply_text(resultado)

def ip_detalle(bot, update, args):
	argumento="output."+args	
	resultado = argumento
	update.message.reply_text(args)	

def who(bot, update):
	chatID = update.get_updates()[-1].message.chat_id
	print chatID
	update.message.reply_text(chatID)

def capture(bot, update):
    cantidad=5
	for i in range(cantidad):
		imagen="evento_on-demand_image-"+strftime("%d%b%Y-%H:%M:%S", gmtime())+".jpg"
		camera.capture(imagen)
		sleep(2)
		bot.send_photo(chat_id=chat_id, photo=open(imagen, 'rb'))
    

#output = Ifcfg(commands.getoutput('ifconfig -a'))
'''
def hora(bot, update):
     update.message.reply_text(
     	'{}'.format(datetime.datetime.now())
'''
camera = picamera.PiCamera()

updater = Updater(token)


valid_chat_id = [chat_id]

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('ip', ip))
updater.dispatcher.add_handler(CommandHandler('who', who))
updater.dispatcher.add_handler(CommandHandler('capture', capture))
ip_handler = CommandHandler('ip_detalle', ip_detalle, pass_args=True)
updater.dispatcher.add_handler(ip_handler)

#updater.dispatcher.add_handler(CommandHandler('hora', hora))

updater.start_polling()
updater.idle()

