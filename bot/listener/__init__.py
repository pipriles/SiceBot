#/usr/bin/env python2

import telebot
import threading
import config
import re

# Aqui tambien meti mano

# Puede ser global?
bot = telebot.TeleBot(config.TOKEN)
msg_lock = threading.Lock()

def get_chats():
	v = []	# v de voludo
	with open("bot/listener/chats_ids", 'r') as f:
		for line in f:
			v.append(line[:-1])
	return v

def add_chat(chat_id):
	print "Agregando a {}".format(chat_id)
	with open("bot/listener/chats_ids", 'a') as f:
		f.write("{}\n".format(chat_id))

chats = get_chats()

def is_interval_req(msg):
	return True if re.search(r'/intervalo? \d+', msg.text, re.IGNORECASE) else False

def telegram_thread():
	rthread = threading.Thread(target=hilo_respondedor)
	rthread.setDaemon(True)
	rthread.start()
	print "Hilo respondedor iniciado"

	@bot.message_handler(commands=['start'])
	def start(men):
		chat_id = men.chat.id
		print men.text
		with msg_lock:
			if str(chat_id) not in chats:
				bot.send_message(chat_id,
					"Hola, ahora recibiras informacion de SICE! /help para mas informacion")
				chats.append(str(chat_id))
				add_chat(str(chat_id))
			else:
				bot.send_message(chat_id, 
					"Ya eres parte del selecto grupo!! c:")

	@bot.message_handler(commands=['help'])
	def ayuraaa(men):
		chat_id = men.chat.id
		print men.text
		with msg_lock:
			if str(chat_id) not in chats:
				bot.send_message(chat_id,
					"Realiza /start para unirte a nosotros, si necesitas mas informacion despues de /start realiza de nuevo /help")
			else:
				bot.send_message(chat_id,
					"Tu no hablaras con este bot, el hablara cuando se sienta listo xD!")

	@bot.message_handler(commands=['disculpate', 'mmg'])
	def disculparse(men):
		chat_id = men.chat.id
		print men.text
		with msg_lock:
			if str(chat_id) not in chats:
				bot.send_message(chat_id,
					'Tu no estas inscrito.')
			else:
				bot.send_message(chat_id,
					'Disculpa :(')

	@bot.message_handler(commands=['pause', 'hakuna', 'calm'])
	def pause(men):
		chat_id = men.chat.id
		print men.text
		with msg_lock:
			if str(chat_id) not in chats:
				bot.send_message(chat_id, 'No tienes control sobre mi!')
			else:
				config.can_request = False
				bot.send_message(chat_id, 'Ok...')

	@bot.message_handler(commands=['run', 'play', 'dalepues'])
	def play(men):
		chat_id = men.chat.id
		print men.text
		with msg_lock:
			if str(chat_id) not in chats:
				bot.send_message(chat_id, 'No tienes control sobre mi!')
			else:
				config.can_request = True
				bot.send_message(chat_id, 'Gracias...')

	@bot.message_handler(func=lambda men: is_interval_req(men))
	def change_interval(men):
		chat_id = men.chat.id
		print men.text
		with msg_lock:
			msg = men.text
			print 'Solicitud de cambio de {}: {}'.format(str(chat_id), msg)
			seconds = int(re.search(r'\d{1,2}', msg).group(0))
			if seconds <= 30 and seconds > 0:
				config.re_interval = seconds
				bot.send_message(chat_id, 'Concedido!')
			else:
				bot.send_message(chat_id, 'No trates de joderme')

	@bot.message_handler(func=lambda men: not is_interval_req(men))
	def mensajes_erroneos(men):
		chat_id = men.chat.id
		print men.text
		with msg_lock:
			if str(chat_id) not in chats:
				bot.send_message(chat_id, 
					"Uuups!! aun no estas inscrito, Realiza /start antes de hacer cualquier cosa!")
			else:
				bot.send_message(chat_id, 
					"Comando incorrecto! :c")

	bot.polling()
	rthread.join()

def hilo_respondedor():
	
	while not config.terminate:	
		config.sem_msg.acquire()
		print "Mensaje de algun request"

		if not config.terminate:
			with msg_lock: topo()
	
	bot.stop_polling()

# El topo grita
def topo():
	for ids in chats:
		print "Topo para {}".format(ids)
		bot.send_message(ids,
			"Sice Acaba de Cambiar Revisalo c:")
		with open('media/topo.mp3', 'rb') as audio:
			bot.send_audio(ids, audio)
