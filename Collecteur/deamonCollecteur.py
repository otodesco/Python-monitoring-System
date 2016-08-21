# coding: utf8

"""
	Processus permettant l'envoi de toutes les informations des collecteurs via des requetes HTTP
"""

import time
import requests
import subprocess
import uuid
import re
from bs4 import BeautifulSoup

import CollecteurRam
import CollecteurCpu

# CONSTANTS #
DELAY_SEND = 8  # Nombres de secondes entre l'envoi de plusieurs informations des collecteurs
URL_SERVER = "http://localhost:5000/"
CPU_ACTION =  "serveurCentralCpu"
RAM_ACTION = "serveurCentralRam"
HDD_ACTION = "serveurCentralHdd"

# GLOBAL #
macAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
cRam = CollecteurRam.CollecteurRam()
cCpu = CollecteurCpu.CollecteurCpu()

cCpu.getProcessorSpaceUsed() # Permet d'ignorer la premiére valeur (toujours a 100)
time.sleep(1)

def getRequestResponse(url, data):
	try:
		request = requests.get(url, params=data)
		soup = BeautifulSoup(request.content, "html.parser")
		parsed = soup.find('div',{'class':'notification'}).text
		if "true" in parsed : return True
		else : return False
	except requests.ConnectionError:
		print "Erreur de connexion à " + url
	except AttributeError:
		print "Erreur d'attribut (parsing retourne null ?)"
	return False;


print ("===== Daemon Lancé =====")
while True:
	# RAM #
	mbRamTotal = cRam.getMbRamTotal()
	mbRamUsed = cRam.getMbRamUsed()
	pcRamUsed = cRam.getPcRamUsed()
	# CPU #
	nbrCpu = cCpu.getNbrCpu(True)
	nbrProcess = cCpu.getNbrProcess()
	cpuSpaceUsed = cCpu.getProcessorSpaceUsed()
	cpuCelTemp = cCpu.getTemp(cCpu.hwcheck())
	cpuType = cCpu.getTypeCpu()
	# HDD #
	hddOut = subprocess.check_output(["bash","CollecteurHdd.bash"]).splitlines()
	pcHddUsed = hddOut[0].replace('%','')
	mbHddTotal = hddOut[1]
	mbHddUsed = hddOut[2]
	 # CPU Request #
 	data = {'adr_mac' : macAddress, 'nb_core' : nbrCpu, 'nb_procs': nbrProcess, 'pc_use': cpuSpaceUsed, 'temperature': cpuCelTemp, 'type': cpuType}
	res = getRequestResponse(URL_SERVER + CPU_ACTION, data)
	print "Resultat de la requête CPU : " + str(res)
 	# RAM Request #
 	data = {'adr_mac' : macAddress, 'mb_total': mbRamTotal, 'mb_use': mbRamUsed, 'pc_use': pcRamUsed}
 	res = getRequestResponse(URL_SERVER + RAM_ACTION, data)
	print "Resultat de la requête RAM : " + str(res)
 	# HDD Request #
 	data = {'adr_mac' : macAddress, 'mb_total': mbHddTotal, 'mb_use': mbHddUsed, 'pc_use': pcHddUsed}
 	res = getRequestResponse(URL_SERVER + HDD_ACTION, data)
	print "Resultat de la requête HDD : " + str(res)

	# Wait for the next refresh
	print "Prochain envoi dans " + str(DELAY_SEND) + " secondes...\n"
	time.sleep(DELAY_SEND)
