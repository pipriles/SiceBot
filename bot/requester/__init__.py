#!/usr/bin/env python2
# Metiendo mano

import requests
import time
import mechanize
import config

br = mechanize.Browser()
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(False)

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Aqui el topo no puede gritar

def attempt():
	response = br.open("http://sice.facyt.uc.edu.ve/InscripcionOnline")

	br.select_form(nr=0)
	br.form['IO_login'] = config.login
	br.form['IO_passwd'] = config.passwd
	response = br.submit()

	url = response.geturl()
	title = br.title()

	return url, title

def request_thread():
	Horario = False
	temp = 1

	old_url, old_title = attempt()
	while not Horario and not config.terminate:
		if config.can_request:
			new_url, new_title = attempt()
			print "{}\n{}\n{}\n".format(temp, new_url, new_title)

			if old_url   != new_url \
			or old_title != new_title:
				Horario = True

		temp += 1
		time.sleep(config.re_interval)

	config.sem_msg.release()
	print 'Inscripcion abierta! (O tal vez solo saliste)'
	# El topo grita
