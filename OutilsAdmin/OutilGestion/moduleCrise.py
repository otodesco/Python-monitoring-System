#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bddHelper import BddHelper
import sys
sys.dont_write_bytecode = True

def isCrisis():
	"""
	Renvoie True si au moins un collecteur est en situation de crise, sinon False
	"""
	bddHelper = BddHelper()
	data = bddHelper.getAllMacAndLastModif()
	for row in data :
		mac = row[0]
		pc_ram = bddHelper.getRamPcUseByMac(mac)[-1][1]
		pc_cpu = bddHelper.getCpuPcUseByMac(mac)[-1][1]
		pc_hdd = bddHelper.getHddPcUseByMac(mac)[-1][1]
		ramTresh = bddHelper.getRamCrisisTreshold()[0]
		hddTresh = bddHelper.getHddCrisisTreshold()[0]
		cpuTresh = bddHelper.getCpuCrisisTreshold()[0]

		if pc_cpu > cpuTresh or pc_ram > ramTresh or pc_hdd > hddTresh :
 			return True
	return False
