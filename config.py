#!/usr/bin/env python2

import threading

# Telegram

TOKEN = "PUT TOKEN HERE"

# Request

can_request = True
re_interval = 3

login  = ""	# Super login
passwd = ""	# Super password

# Control

terminate = 0
sem_msg = threading.Semaphore(0)
