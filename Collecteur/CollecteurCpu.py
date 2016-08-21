import psutil
import os
import platform
class CollecteurCpu:
#=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=Processeur=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=#
	def getNbrCpu(self,boolean):
		nbrProcessor = psutil.cpu_count(logical=boolean)
		return nbrProcessor
	# Recuperation de nombre de processus en cours d'execution
	def getNbrProcess(self):
		iter = psutil.process_iter()
		nbrProcess = 0
		for process in iter:
			# print process.name
		   	nbrProcess = nbrProcess+1
		return nbrProcess
	# Recuperation de la memoire utilisee du processeur 
	def getProcessorSpaceUsed(self):
		processorSpaceUsed = psutil.cpu_percent()
		return processorSpaceUsed
	
	# Recuperation de la chaleur du processeur 	
	def hwcheck(self):
		if os.path.exists("/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp") == True:
			return  4

		elif os.path.exists("/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/temp") == True:
			return  5
					
		elif os.path.exists("/proc/acpi/thermal_zone/THM0/temperature") == True:
			return  1

		elif os.path.exists("/proc/acpi/thermal_zone/THRM/temperature") == True :
			return  2

		elif os.path.exists("/proc/acpi/thermal_zone/THR1/temperature") == True :
			return  3
			
		else:
			return 0
			
	def getTemp(self,hardware):
		if hardware == 1 :
			temp = open("/proc/acpi/thermal_zone/THM0/temperature").read().strip().lstrip('temperature :').rstrip(' C')
		elif hardware == 2 :
			temp = open("/proc/acpi/thermal_zone/THRM/temperature").read().strip().lstrip('temperature :').rstrip(' C')
		elif hardware == 3 :
			temp = open("/proc/acpi/thermal_zone/THR1/temperature").read().strip().lstrip('temperature :').rstrip(' C')
		elif hardware == 4 :
			temp = open("/sys/devices/LNXSYSTM:00/LNXTHERM:00/LNXTHERM:01/thermal_zone/temp").read().strip().rstrip('000')
		elif hardware == 5 :
			temp = open("/sys/bus/acpi/devices/LNXTHERM:00/thermal_zone/temp").read().strip().rstrip('000')
			temp = str(float(temp))
		else:
			return 0
		return temp
	# Recuperation de l'achitecture du processeur 
	def getTypeCpu(self):
		return platform.processor()
	

""" 
print "#=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=CPU=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=#"	
print "nombre de processeur logique et physique : ",CollecteurCpu().getNbrCpu(True)
print "nombre de processus en cours d'execution : ",CollecteurCpu().getNbrProcess()
print "Espace utilise CPU : ",CollecteurCpu().getProcessorSpaceUsed() ,"%"
print "temperature du CPU : ",CollecteurCpu().getTemp(CollecteurCpu().hwcheck()),"Celius"
print "Type du processeur : ",CollecteurCpu().getTypeCpu()
"""