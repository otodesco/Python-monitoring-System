#!/usr/bin/env python
# -*- coding: utf-8 -*-


import smtplib
import sys
sys.dont_write_bytecode = True

SERV_STMP_ADR = "smtpz.univ-avignon.fr"
LOGIN = "mickael.beguin@alumni.univ-avignon.fr"
PASS = "2SS6D2ss6d"
PATH_TEMPLATE = "mail_template"
ADMIN_MAIL = "sidfloyd84@gmail.com"

def sendMail():
	# Se connecte au serveur
	server = smtplib.SMTP(SERV_STMP_ADR)
	server.starttls()
	server.login(LOGIN, PASS)
	 
	# Charge le template (message par défaut)
	f = open(PATH_TEMPLATE, 'r')
	msg = f.read()

	# Envoie le mail
	server.sendmail(LOGIN, ADMIN_MAIL, msg)
	server.quit()


