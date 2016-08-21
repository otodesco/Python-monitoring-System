import subprocess

class CollecteurRam:
	def getMbRamTotal(self):
		output = subprocess.check_output(["bash","getMbRamTotal.bash"])
		return output.splitlines()[0]
	def getMbRamUsed(self):
		output = subprocess.check_output(["bash","getMbRamUsed.bash"])
		return output.splitlines()[0]
	def getPcRamUsed(self):
		output = subprocess.check_output(["bash","getPcRamUsed.bash"])
		return output.splitlines()[0]
