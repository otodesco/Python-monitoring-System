#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
import re
import sqlite3
from bs4 import BeautifulSoup

PATH_BDD = "../Stockage/adsys.db"



pattern = re.compile('ALE') # Pattern correspondant à une référence d'alerte
db = sqlite3.connect(PATH_BDD)
r = requests.get("http://www.cert.ssi.gouv.fr/")
soup = BeautifulSoup(r.content, "html.parser")
for elem in soup.find("body").find_all("a" , {"class":{"mg"}}):
	if(elem.string is not None):
		strElem =  elem.string.encode('utf-8') # Convertit pour comparaison avec expression reguliére
		if(pattern.search(strElem) is not None):
			reference = strElem
			print reference
			description =  elem.parent.parent.find_all("td" , {"class":{"mg"}})[1].renderContents() # Récupére la référence graçe au parent
			cursor = db.execute("SELECT id FROM alerte WHERE reference LIKE '"+reference+"'") # Regarde si la référence existe dans la bdd
			data=cursor.fetchall()
			if len(data)==0:
				db.execute("INSERT INTO alerte (reference,description) \
      			VALUES(?,?)", (sqlite3.Binary(reference), sqlite3.Binary(description)));
				print "Ajout de la réference à la BDD"
			else:
				print "Reference non ajoutée car déja existante"
db.commit()
db.close()



