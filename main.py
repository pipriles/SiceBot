#!/usr/bin/env python2

import argparse
import getpass

import threading
import time

import config
import bot

# Y en todos lados meti mano

def get_credentials():
	parser = argparse.ArgumentParser(description="Telegram SiceBot")
	parser.add_argument('-u', '--user', help="Username")
	parser.add_argument('-p', '--passwd', help="Password", action='store_true')
	args = parser.parse_args()

	if args.user is not None:
		config.login = args.user
	if args.passwd:
		config.passwd = getpass.getpass()

def main():
	try:
		get_credentials()

		sthread = threading.Thread(target=bot.requester.request_thread)
		tthread = threading.Thread(target=bot.listener.telegram_thread)

		sthread.setDaemon(True)
		tthread.setDaemon(True)
		tthread.start()
		sthread.start()

		while True:
			time.sleep(100)

	except KeyboardInterrupt:
		config.terminate = 1
		config.sem_msg.release()
		tthread.join()
		sthread.join()

if __name__ == '__main__':
	main()