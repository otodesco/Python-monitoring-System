#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import curses
from curses import wrapper
from math import floor
import sqlite3
import pygal
from datetime import datetime

from bddHelper import BddHelper


# Constants
TMP_FOLDER = "tmp"
DATE_PATTERN = '%d/%m/%y %H:%M'
DEFAULT_MAX_CPU = 1000
DEFAULT_MAX_RAM = 1000
DEFAULT_MAX_HDD = 1000
DEFAULT_MAX_ALERTE = 10


# Enum values for windows type #
# 1 = Main Menu                #
# 2 = Devices list             #
# 3 = Device stats plots       #
# 4 = Configuration            #
# 5 = History config           #
# 6 = Crisis config            #
# ============================ #

# Init curses
screen = curses.initscr()
curses.start_color()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)
screen.refresh()
subprocess.call(["mkdir", TMP_FOLDER]) # Crée le dossier contenant les fichiers temporaires crées

# Colors
curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)

# Globals
TITLE = "Interface d'administration"
WIN_HEIGHT, WIN_WIDTH = screen.getmaxyx()
WINDOW_TYPE = 0
bddH = BddHelper()
list_mac = list()
list_digits = list()
currentIdDev = -1;
idPanelHist = 0


# Main
def main() : 
	init_MainMenu()
	while True:
		event = screen.getch()
		if event == ord("q"): 
			break
		elif WINDOW_TYPE == 1 and event == ord("h"): 
			init_SettingsMenu();
		elif WINDOW_TYPE in (1,3) and event == ord("l"): 
			init_DevicesList()


		elif WINDOW_TYPE in (2,4,5) and event == ord("m"): 
			init_MainMenu()
		elif WINDOW_TYPE == 2 and event <= 256 and chr(event).isdigit(): # Appuie sur un chiffre
			addDigit(chr(event))
		elif WINDOW_TYPE == 2 and event == 263: # Appui sur retour
			removeDigit()
		elif WINDOW_TYPE == 2 and event == 10: # Appui entrée
			res = getDigitsResult()
			clearDigits()
			if(res != None and res < len(list_mac)):
				init_DeviceStats(res)


		elif WINDOW_TYPE == 3 and event in (ord("1"),ord("t"),ord("p"),ord("c")): 
			display_CpuGraph(list_mac[currentIdDev], chr(event))
		elif WINDOW_TYPE == 3 and event in (ord("2"),ord("m"),ord("k")): 
			display_RamGraph(list_mac[currentIdDev], chr(event))
		elif WINDOW_TYPE == 3 and event in (ord("3"),ord("e"),ord("r")): 
			display_HddGraph(list_mac[currentIdDev], chr(event))

		elif WINDOW_TYPE == 4 and event in (ord("1"),ord("2"),ord("3"),ord("4")): 
			init_ConfigHistory(chr(event))
		elif WINDOW_TYPE == 4 and event in (ord("5"),ord("6"),ord("7")): 
			init_ConfigCrisis(chr(event))

		elif WINDOW_TYPE in (5,6) and event == ord("m"):
			init_MainMenu()
		elif WINDOW_TYPE in (5,6) and event == ord("h"):
			init_SettingsMenu();
		elif WINDOW_TYPE in (5,6) and event <= 256 and chr(event).isdigit(): # Appuie sur un chiffre
			addDigit(chr(event))
		elif WINDOW_TYPE in (5,6) and event == 263: # Appui sur retour
			removeDigit()
		elif WINDOW_TYPE == 5 and event == 10: # Appui entrée
			res = getDigitsResult()
			clearDigits()
			if(res > 5):
				setHistoryValue(res) # Inscrit le nouveau paramétre dans la base de donnée
				init_ConfigHistory(str(idPanelHist))

		elif WINDOW_TYPE == 6 and event == 10: # Appui entrée
			res = getDigitsResult()
			clearDigits()
			if(res >= 5 and res <= 100):
				setCrisisValue(res) # Inscrit le nouveau paramétre dans la base de donnée
				init_ConfigCrisis(str(idPanelHist))


	# Quitter
	curses.endwin()


def new_line(nbLine=1):
	y, x = screen.getyx() 
	screen.move(y+nbLine,0)

def str_center(strElem):
	length = len(strElem)
	return int(floor((WIN_WIDTH/2)-(length/2)))

# Prend un nombre d'item en paramétre et renvoit une liste des hauteurs pour chacun de ces items (pour peu d'items)
def center_items(nbItems):
	yItems = list()
	for i in range(0, nbItems):
		yItems.append((i+1) * (WIN_HEIGHT/(nbItems+1)))
	return yItems

def addDigit(digit):
	size = len(list_digits)
	if size < 6:
		screen.addch(WIN_HEIGHT-2, size , digit, curses.color_pair(5) | curses.A_BOLD )
		list_digits.append(digit)
	elif size == 6 :
		screen.addch(WIN_HEIGHT-2, size-1 , digit, curses.color_pair(5) | curses.A_BOLD)
		list_digits[-1] = digit # On peut avoir au max 3 digits

def removeDigit():
	size = len(list_digits)
	if size > 0:
		screen.addch(WIN_HEIGHT-2, size-1 , ' ')
		del list_digits[-1]
def clearDigits():
	size = len(list_digits)
	while size > 0:
		screen.addch(WIN_HEIGHT-2, size-1 , ' ')
		del list_digits[-1]
		size -= 1

# Retourne le nombre donnée par tout les digits
def getDigitsResult():
	size = len(list_digits)
	if(size == 0):
		return None
	else:
		strRes = ""
		for digit in list_digits:
			strRes += str(digit)
		return int(strRes)

def init_MainMenu():
	global WINDOW_TYPE
	screen.clear()
	WINDOW_TYPE = 1
	init_CommandBar()
	marginLeft = int(WIN_WIDTH*0.05)
	title = TITLE + " - Menu Principal"
	screen.addstr(0, str_center(title) ,title ,curses.color_pair(1)  | curses.A_BOLD )

	y = 5
	screen.addstr(y+1,  WIN_WIDTH/5 ,"'l' Listes des machines connectees" ,curses.color_pair(2)  | curses.A_BOLD)
	screen.addstr(y+2,  WIN_WIDTH/5 ,"'h' Configuration" ,curses.color_pair(2)  | curses.A_BOLD)

def init_DevicesList():
	global WINDOW_TYPE
	screen.clear()
	WINDOW_TYPE = 2
	init_CommandBar()
	marginLeft = int(WIN_WIDTH*0.05)
	title = TITLE + " - Liste des appareils connectes"
	screen.addstr(0, str_center(title) ,title ,curses.color_pair(1) | curses.A_BOLD)
	new_line()
	# Affiches les machine de la DB
	rowsDevices = bddH.getAllMacAndLastModif()
	nbMachine = len(rowsDevices)
	if rowsDevices > 0:
		del list_mac[:] # Clear the list
		for i in range(0, nbMachine):
			new_line()
			adr_mac = rowsDevices[i][0]
			last_modif = rowsDevices[i][1]
			screen.addstr(str(i) + " - MAC: " ,curses.color_pair(2))
			screen.addstr(adr_mac, curses.color_pair(2) | curses.A_BOLD)
			screen.addstr(" - Derniere Connexion : ", curses.color_pair(2))
			screen.addstr(str(last_modif), curses.color_pair(3))
			list_mac.append(adr_mac)
	else:
		new_line()
		screen.addstr("Pas de machines inscrites dans la base de donnees...",curses.color_pair(2))

def init_DeviceStats(idDevice):
	global WINDOW_TYPE
	screen.clear()
	WINDOW_TYPE = 3
	init_CommandBar()
	marginLeft = int(WIN_WIDTH*0.05)
	title = TITLE + " - Statistiques appareil " + str(idDevice)
	mac = list_mac[idDevice]
	screen.addstr(0, str_center(title) ,title ,curses.color_pair(1)  | curses.A_BOLD)
	# Init collecteurs options
	y = 4; # Début
	screen.addstr(y,  WIN_WIDTH/5 ,"'1' Afficher statistiques du CPU" ,curses.color_pair(2)  | curses.A_BOLD)
	screen.addstr(y+1,  WIN_WIDTH/5 ,"   't' Temperature" ,curses.color_pair(2) )
	screen.addstr(y+2,  WIN_WIDTH/5 ,"   'p' Nombre de processus" ,curses.color_pair(2) )
	screen.addstr(y+3,  WIN_WIDTH/5 ,"   'c' Pourcentage utilisation" ,curses.color_pair(2) )
	screen.addstr(y+4, WIN_WIDTH/5 ,"'2' Afficher statistiques de le RAM" ,curses.color_pair(2)  | curses.A_BOLD)
	screen.addstr(y+5,  WIN_WIDTH/5 ,"   'm' Memoire utilisee (Mb)" ,curses.color_pair(2) )
	screen.addstr(y+6,  WIN_WIDTH/5 ,"   'k' Memoire utilisee (%)" ,curses.color_pair(2) )
	screen.addstr(y+7, WIN_WIDTH/5 ,"'3' Afficher statistiques du HDD principal" ,curses.color_pair(2)  | curses.A_BOLD)
	screen.addstr(y+8,  WIN_WIDTH/5 ,"   'e' Espace disque utilise (Mb)" ,curses.color_pair(2) )
	screen.addstr(y+9,  WIN_WIDTH/5 ,"   'r' Espace disque utilise (%)" ,curses.color_pair(2) )

	currentIdDev = idDevice

def init_SettingsMenu():
	global WINDOW_TYPE
	screen.clear()
	WINDOW_TYPE = 4
	init_CommandBar()
	marginLeft = int(WIN_WIDTH*0.05)
	title = TITLE + " - Configuration"
	screen.addstr(0, str_center(title) ,title ,curses.color_pair(1)  | curses.A_BOLD)
	y = 4; # Début
	screen.addstr(y,  WIN_WIDTH/5 ," Configurer taille historique" ,curses.color_pair(2)  | curses.A_BOLD)
	screen.addstr(y+1,  WIN_WIDTH/5 ,"'1' CPU" ,curses.color_pair(2))
	screen.addstr(y+2,  WIN_WIDTH/5 ,"'2' RAM" ,curses.color_pair(2))
	screen.addstr(y+3,  WIN_WIDTH/5 ,"'3' HDD" ,curses.color_pair(2))
	screen.addstr(y+4,  WIN_WIDTH/5 ,"'4' Alertes" ,curses.color_pair(2))
	screen.addstr(y+6,  WIN_WIDTH/5 ," Configurer pourcentage critique" ,curses.color_pair(2)  | curses.A_BOLD)
	screen.addstr(y+7,  WIN_WIDTH/5 ,"'5' CPU" ,curses.color_pair(2))
	screen.addstr(y+8,  WIN_WIDTH/5 ,"'6' RAM" ,curses.color_pair(2))
	screen.addstr(y+9,  WIN_WIDTH/5 ,"'7' HDD" ,curses.color_pair(2))

	# Charge les paramétres par défaut si pas de paramétres
	if bddH.getMaxHistoryKeyCount() != 4 :
		loadDefaultHistorySettings()


def loadDefaultHistorySettings():
	bddH.setMaxCpuHistory(DEFAULT_MAX_CPU)
	bddH.setMaxRamHistory(DEFAULT_MAX_RAM)
	bddH.setMaxHddHistory(DEFAULT_MAX_HDD)
	bddH.setMaxAlerteHistory(DEFAULT_MAX_ALERTE)


def init_ConfigHistory(input):
	global WINDOW_TYPE
	global idPanelHist
	screen.clear()
	WINDOW_TYPE = 5
	init_CommandBar()

	if(input == "1"):
		idPanelHist = 1
		title = TITLE + " - Configuration entrees CPU"
		size = bddH.getMaxCpuHistory()[0]
	elif(input == "2"):
		idPanelHist = 2
		title = TITLE + " - Configuration entrees RAM"
		size = bddH.getMaxRamHistory()[0]
	elif(input == "3"):
		idPanelHist = 3
		title = TITLE + " - Configuration entrées HDD"
		size = bddH.getMaxHddHistory()[0]
	elif(input == "4"):
		idPanelHist = 4
		title = TITLE + " - Configuration entrees Alertes"
		size = bddH.getMaxAlerteHistory()[0]

	str1 = "La nombre maximal d'entrees est de "
	str2 = "Vous pouvez entrer une nouvelle valeur"
	screen.addstr(0, str_center(title) ,title ,curses.color_pair(1)  | curses.A_BOLD)
	screen.addstr(5,  str_center(str1)-len(str(size)) ,str1,curses.color_pair(2) )
	screen.addstr(str(size), curses.color_pair(2)  | curses.A_BOLD)
	screen.addstr(6,  str_center(str2) ,	str2 ,curses.color_pair(2))

def init_ConfigCrisis(input):
	global WINDOW_TYPE
	global idPanelHist
	screen.clear()
	WINDOW_TYPE = 6
	init_CommandBar()

	if(input == "5"):
		idPanelHist = 5
		title = TITLE + " - Configuration seuil crise CPU"
		size = bddH.getCpuCrisisTreshold()[0]
	elif(input == "6"):
		idPanelHist = 6
		title = TITLE + " - Configuration seuil crise RAM"
		size = bddH.getRamCrisisTreshold()[0]
	elif(input == "7"):
		idPanelHist = 7
		title = TITLE + " - Configuration seuil crise HDD"
		size = bddH.getHddCrisisTreshold()[0]

	str1 = "Un mail sera envoye quand le pourcentage aura atteint "
	str2 = "Vous pouvez entrer une nouvelle valeur"
	screen.addstr(0, str_center(title) ,title ,curses.color_pair(1)  | curses.A_BOLD)
	screen.addstr(5,  str_center(str1)-len(str(size)) ,str1,curses.color_pair(2) )
	screen.addstr(str(size)+"%", curses.color_pair(2)  | curses.A_BOLD)
	screen.addstr(6,  str_center(str2) ,	str2 ,curses.color_pair(2))



def setHistoryValue(value):
	global idPanelHist
	if(idPanelHist == 1):
		bddH.setMaxCpuHistory(value)
	if(idPanelHist == 2):
		bddH.setMaxRamHistory(value)
	if(idPanelHist == 3):
		bddH.setMaxHddHistory(value)
	if(idPanelHist == 4):
		bddH.setMaxAlerteHistory(value)

def setCrisisValue(value):
	global idPanelHist
	if(idPanelHist == 5):
		bddH.setCpuCrisisTreshold(value)
	if(idPanelHist == 6):
		bddH.setRamCrisisTreshold(value)
	if(idPanelHist == 7):
		bddH.setHddCrisisTreshold(value)


def display_CpuGraph(strMac, argGraph):
	# Récupére les infos de la BDD concernant cette adresse MAC
	rowsPcUse = str_to_dateTime(bddH.getCpuPcUseByMac(strMac))
	rowsPcTemp = str_to_dateTime(bddH.getCpuTempByMac(strMac))
	rowsPcNbProcs = str_to_dateTime(bddH.getCpuNbProcsByMac(strMac))

	# Initialise les données du graph 
	graph = pygal.DateTimeLine(
	x_label_rotation=35, truncate_label=-1,
	x_value_formatter=lambda dt: dt.strftime(DATE_PATTERN))
	if argGraph == 'c': graph.add("Utilisation (%)", rowsPcUse)	 
	elif argGraph == 't': graph.add("Temperature", rowsPcTemp)
	elif argGraph == 'p': graph.add("Nombre processus", rowsPcNbProcs)
	else :
		graph.add("Utilisation (%)", rowsPcUse)
		graph.add("Temperature", rowsPcTemp)
		graph.add("Nombre processus", rowsPcNbProcs)
		
	# Display graph
	path_img = TMP_FOLDER + '/graph.png'
	graph.render_to_png(path_img)
	subprocess.call(["eog", path_img]) 

def display_RamGraph(strMac, argGraph):
	# Récupére les infos de la BDD concernant cette adresse MAC
	rowsMbTotal = str_to_dateTime(bddH.getRamMbTotalByMac(strMac))
	rowsMbUse = str_to_dateTime(bddH.getRamMbUseByMac(strMac))
	rowsPcUse = str_to_dateTime(bddH.getRamPcUseByMac(strMac))

	# Initialise les données du graph 
	graph = pygal.DateTimeLine(
	x_label_rotation=35, truncate_label=-1,
	x_value_formatter=lambda dt: dt.strftime(DATE_PATTERN))
	if argGraph == 'm': 
		graph.add("Total (Mb)", rowsMbTotal)
		graph.add("Utilisation (Mb)", rowsMbUse)	 
	elif argGraph == 'k':  
		graph.add("Utilisation (%)", rowsPcUse)
	else :
		graph.add("Total (Mb)", rowsMbTotal)
		graph.add("Utilisation (Mb)", rowsMbUse)	
		graph.add("Utilisation (%)", rowsPcUse)

	# Display graph
	path_img = TMP_FOLDER + '/graph.png'
	graph.render_to_png(path_img)
	subprocess.call(["eog", path_img]) 


def display_HddGraph(strMac, argGraph):
	# Récupére les infos de la BDD concernant cette adresse MAC
	rowsMbTotal = str_to_dateTime(bddH.getHddMbTotalByMac(strMac))
	rowsMbUse = str_to_dateTime(bddH.getHddMbUseByMac(strMac))
	rowsPcUse = str_to_dateTime(bddH.getHddPcUseByMac(strMac))

	# Initialise les données du graph 
	graph = pygal.DateTimeLine(
	x_label_rotation=35, truncate_label=-1,
	x_value_formatter=lambda dt: dt.strftime(DATE_PATTERN))
	if argGraph == 'e': 
		graph.add("Total (Mb)", rowsMbTotal)
		graph.add("Utilisation (Mb)", rowsMbUse)	 
	elif argGraph == 'r':  
		graph.add("Utilisation (%)", rowsPcUse)
	else :
		graph.add("Total (Mb)", rowsMbTotal)
		graph.add("Utilisation (Mb)", rowsMbUse)	
		graph.add("Utilisation (%)", rowsPcUse)

	# Display graph
	path_img = TMP_FOLDER + '/graph.png'
	graph.render_to_png(path_img)
	subprocess.call(["eog", path_img]) 


def str_to_dateTime(tuples):
	"""
		Convertit un set de tuples de type [(string,X)] en une liste de type [(datetime,X)]
	"""
	listConverted = list()
	for idx in range(0, len(tuples)):
		listConverted.append((datetime.strptime(tuples[idx][0], DATE_PATTERN), tuples[idx][1]))
	return listConverted

def init_CommandBar(): # Todo mettre sur plusieurs lignes si pas assez de place
	maxY, maxX = screen.getmaxyx()
	screen.move(maxY-1,0)
	strCommands = ""
	for x in range(0, maxX-1): # Add blank space on the line
		screen.addch(' ', curses.color_pair(4))
	if WINDOW_TYPE == 1:
		strCommands = "[q] Quitter "
	elif WINDOW_TYPE == 2:
		strCommands = "[q] Quitter   [m] Menu principal   [0..n] Statistiques machine"
	elif WINDOW_TYPE == 3:
		strCommands = "[q] Quitter [l] Liste des machines"
	elif WINDOW_TYPE == 4:
		strCommands = "[q] Quitter   [m] Menu principal"
	elif WINDOW_TYPE in (5,6):
		strCommands = "[q] Quitter   [m] Menu principal [h] Menu Configuration"
	screen.addstr(maxY-1, 0, strCommands, curses.color_pair(4))



if __name__ == '__main__':
	main();