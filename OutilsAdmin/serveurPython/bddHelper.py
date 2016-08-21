#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import sys
sys.dont_write_bytecode = True

# Global
DB_PATH = '../Stockage/adsys.db'


class BddHelper(object):

	def __init__(self):
		self.db = sqlite3.connect(DB_PATH)
		self.cur = self.db.cursor() 

	def getAllMacAndLastModif(self):
		data = self.cur.execute("SELECT adr_mac, last_modif FROM machine")
		return data.fetchall()

	###########
	### CPU ###
	###########

	def getMostRecentCollecteurCpuByMac(self, strMAC):
		"""
			Retourne les derniéres informations reçues pour cette machine
		"""
		data = self.cur.execute("SELECT date,nb_procs,pc_use,temperature,type  FROM collecteurCpu, machine   \
								WHERE collecteurCpu.id_machine = machine.id AND machine.adr_mac='"+strMAC+"' \
								AND collecteurCpu.date = (SELECT MAX(date) from collecteurCpu, machine WHERE collecteurCpu.id_machine = machine.id AND machine.adr_mac='"+strMAC+"')")
		return data.fetchall()

	def getCpuTempByMac(self, strMAC):
		data = self.cur.execute("SELECT date,temperature FROM  collecteurCpu, machine  \
								WHERE collecteurCpu.id_machine = machine.id AND machine.adr_mac='"+strMAC+"'")
		return data.fetchall()

	def getCpuPcUseByMac(self, strMAC):
		data = self.cur.execute("SELECT date, pc_use FROM  collecteurCpu, machine  \
								WHERE collecteurCpu.id_machine = machine.id AND machine.adr_mac='"+strMAC+"'")
		return data.fetchall()

	def getCpuNbProcsByMac(self, strMAC):
		data = self.cur.execute("SELECT date, nb_procs FROM  collecteurCpu, machine  \
								WHERE collecteurCpu.id_machine = machine.id AND machine.adr_mac='"+strMAC+"'")
		return data.fetchall()

	###########
	### RAM ###
	###########

	def getRamMbTotalByMac(self, strMAC):
		data = self.cur.execute("SELECT date, mb_total FROM  collecteurRam, machine  \
								WHERE collecteurRam.id_machine = machine.id AND machine.adr_mac='"+strMAC+"'")
		return data.fetchall()

	def getRamMbUseByMac(self, strMAC):
		data = self.cur.execute("SELECT date, mb_use FROM  collecteurRam, machine  \
								WHERE collecteurRam.id_machine = machine.id AND machine.adr_mac='"+strMAC+"'")
		return data.fetchall()

	def getRamPcUseByMac(self, strMAC):
		data = self.cur.execute("SELECT date, pc_use FROM  collecteurRam, machine  \
								WHERE collecteurRam.id_machine = machine.id AND machine.adr_mac='"+strMAC+"'")
		return data.fetchall()

	###########
	### HDD ###
	###########
	def getHddMbTotalByMac(self, strMAC):
		data = self.cur.execute("SELECT date, mb_total FROM  collecteurHdd, machine  \
								WHERE collecteurHdd.id_machine = machine.id AND machine.adr_mac='"+strMAC+"'")
		return data.fetchall()

	def getHddMbUseByMac(self, strMAC):
		data = self.cur.execute("SELECT date, mb_use FROM  collecteurHdd, machine  \
								WHERE collecteurHdd.id_machine = machine.id AND machine.adr_mac='"+strMAC+"'")
		return data.fetchall()

	def getHddPcUseByMac(self, strMAC):
		data = self.cur.execute("SELECT date, pc_use FROM  collecteurHdd, machine  \
								WHERE collecteurHdd.id_machine = machine.id AND machine.adr_mac='"+strMAC+"'")
		return data.fetchall()

	############
	# SETTINGS #
	############

	# HISTORIQUE #

	def setMaxCpuHistory(self, value):
		data = self.cur.execute("INSERT OR REPLACE INTO parametre (key, value)  VALUES (  'cpuMaxHistory', "+str(value)+" )")
		self.db.commit()

	def setMaxRamHistory(self, value):
		data = self.cur.execute("INSERT OR REPLACE INTO parametre (key, value)  VALUES (  'ramMaxHistory', "+str(value)+" )")
		self.db.commit()

	def setMaxHddHistory(self, value):
		data = self.cur.execute("INSERT OR REPLACE INTO parametre (key, value)  VALUES (  'hddMaxHistory', "+str(value)+" )")
		self.db.commit()

	def setMaxAlerteHistory(self, value):
		data = self.cur.execute("INSERT OR REPLACE INTO parametre (key, value)  VALUES (  'alerteMaxHistory', "+str(value)+" )")
		self.db.commit()

	def getMaxCpuHistory(self):
		data = self.cur.execute("SELECT value FROM  parametre WHERE key = 'cpuMaxHistory'")
		return data.fetchone()

	def getMaxRamHistory(self):
		data = self.cur.execute("SELECT value FROM  parametre WHERE key = 'ramMaxHistory'")
		return data.fetchone()

	def getMaxHddHistory(self):
		data = self.cur.execute("SELECT value FROM  parametre WHERE key = 'hddMaxHistory'")
		return data.fetchone()

	def getMaxAlerteHistory(self):
		data = self.cur.execute("SELECT value FROM  parametre WHERE key = 'alerteMaxHistory'")
		return data.fetchone()


	# CRISE #

	def getCpuCrisisTreshold(self):
		data = self.cur.execute("SELECT value FROM  parametre WHERE key = 'cpuCrisisTreshold'")
		return data.fetchone()

	def getRamCrisisTreshold(self):
		data = self.cur.execute("SELECT value FROM  parametre WHERE key = 'ramCrisisTreshold'")
		return data.fetchone()

	def getHddCrisisTreshold(self):
		data = self.cur.execute("SELECT value FROM  parametre WHERE key = 'hddCrisisTreshold'")
		return data.fetchone()

	def setCpuCrisisTreshold(self, value):
		data = self.cur.execute("INSERT OR REPLACE INTO parametre (key, value)  VALUES (  'cpuCrisisTreshold', "+str(value)+" )")
		self.db.commit()

	def setRamCrisisTreshold(self, value):
		data = self.cur.execute("INSERT OR REPLACE INTO parametre (key, value)  VALUES (  'ramCrisisTreshold', "+str(value)+" )")
		self.db.commit()

	def setHddCrisisTreshold(self, value):
		data = self.cur.execute("INSERT OR REPLACE INTO parametre (key, value)  VALUES (  'hddCrisisTreshold', "+str(value)+" )")
		self.db.commit()



	# OTHERS # 
	def getMaxHistoryKeyCount(self):
		"""
		Retourne le nombre de paramétres liés aux historiques (en temps normal 3)
		"""
		data = self.cur.execute("SELECT COUNT(*) from parametre WHERE key LIKE '%MaxHistory' ")
		return data.fetchone()[0]

