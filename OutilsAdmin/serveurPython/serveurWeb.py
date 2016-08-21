# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import time

from bddHelper import BddHelper

# create the application object
app = Flask(__name__)

PATH_BDD = "../Stockage/adsys.db"
bddH = BddHelper()

# use decorators to link the function to a url
@app.route('/')
def home():
    db = sqlite3.connect(PATH_BDD)
    cur = db.cursor()
    cur.execute("SELECT adr_mac, last_modif FROM machine")
    data=cur.fetchall()
    return render_template('machines.html',data = data)

@app.route('/machine')
def machine():
    adrMac = request.args.get('adrMac')
    db = sqlite3.connect(PATH_BDD)
    cur = db.cursor()
    cur.execute("SELECT date, mb_use, mb_total FROM  collecteurRam, machine WHERE collecteurRam.id_machine = machine.id AND machine.adr_mac='"+adrMac+"' order by date DESC LIMIT 20")
    ram=cur.fetchall()

    cur2 = db.cursor()
    cur2.execute("SELECT date, mb_use, mb_total FROM  collecteurHdd, machine WHERE collecteurHdd.id_machine = machine.id AND machine.adr_mac='"+adrMac+"' order by date DESC LIMIT 20")
    hdd=cur2.fetchall()

    return render_template('machine.html',rame = ram, hdd=hdd)

# Collecteur cpu
@app.route('/serveurCentralCpu')
def serveurCentralCpu():
    erreur = "true"
    # Champs obligatoire CPU
    adresseMac = request.args.get('adr_mac', '')
    nbProcs = request.args.get('nb_procs', '')
    pcUse = request.args.get('pc_use', '')
    temperature = request.args.get('temperature', '')
    cpuType = request.args.get('type', '')
    date = time.strftime('%d/%m/%y %H:%M',time.localtime())

    
    
    if not adresseMac or len(adresseMac) == 0 or not nbProcs or len(nbProcs) == 0 or not pcUse or len(pcUse) == 0 or not temperature or len(temperature) == 0 or not cpuType or len(cpuType) == 0:
       erreur = "false"
    else:
        idMachine = None
        db = sqlite3.connect(PATH_BDD)
        cur = db.cursor()
        cur.execute("SELECT id FROM machine WHERE adr_mac = '"+adresseMac+"'")
        data=cur.fetchall()
        
        cur2 = db.cursor()
        cur2.execute("SELECT value FROM parametre WHERE key = 'cpuMaxHistory'")
        maxCpu = cur2.fetchone()[0]

        cur2.execute("SELECT COUNT(*) FROM collecteurCpu")
        cpuCount = cur2.fetchone()[0]
        
        if maxCpu < cpuCount:
            cur2.execute("Delete from collecteurCpu where id IN (Select id from collecteurCpu limit 1)")
	
	
        if len(data) == 0:   
            cur.execute("INSERT INTO machine (adr_mac,last_modif) VALUES('"+adresseMac+"','"+date+"')");
            idMachine = cur.lastrowid
        else:
            idMachine =  data[0][0]
            cur.execute("UPDATE machine SET last_modif = '"+date+"' WHERE id = '"+str(idMachine)+"';")
        cur.execute("INSERT INTO collecteurCpu (date,nb_procs,pc_use,temperature,type,id_machine) VALUES('"+date+"','"+nbProcs+"','"+pcUse+"','"+temperature+"','"+cpuType+"','"+str(idMachine)+"')");
        db.commit()
        db.close()
    return render_template('saveData.html', error=erreur)

#Collecteur RAM
@app.route('/serveurCentralRam')
def serveurCentralRam():
    erreur = "true"
    # Champs obligatoire RAM
    adresseMac = request.args.get('adr_mac', '')
    mbTotal = request.args.get('mb_total', '')
    mbUse = request.args.get('mb_use', '')
    pcUse = request.args.get('pc_use', '')
    date = time.strftime('%d/%m/%y %H:%M',time.localtime())

    
    
    if not adresseMac or len(adresseMac) == 0 or not mbTotal or len(mbTotal) == 0 or not pcUse or len(pcUse) == 0 or not mbUse or len(mbUse) == 0:
       erreur = "false"
    else:
        idMachine = None
        db = sqlite3.connect(PATH_BDD)
        cur = db.cursor()
        cur.execute("SELECT id FROM machine WHERE adr_mac = '"+adresseMac+"'")
        data=cur.fetchall()
        
        cur2 = db.cursor()
        cur2.execute("SELECT value FROM parametre WHERE key = 'ramMaxHistory'")
        maxCpu = cur2.fetchone()[0]

        cur2.execute("SELECT COUNT(*) FROM collecteurRam")
        cpuCount = cur2.fetchone()[0]
        
        if maxCpu < cpuCount:
            cur2.execute("Delete from collecteurRam where id IN (Select id from collecteurRam limit 1)")

        if len(data) == 0:   
            cur.execute("INSERT INTO machine (adr_mac,last_modif) VALUES('"+adresseMac+"','"+date+"')");
            idMachine = cur.lastrowid
        else:
            idMachine =  data[0][0]
            cur.execute("UPDATE machine SET last_modif = '"+date+"' WHERE id = '"+str(idMachine)+"';")
        cur.execute("INSERT INTO collecteurRam (date,mb_total,mb_use,pc_use,id_machine) VALUES('"+date+"','"+mbTotal+"','"+mbUse+"','"+pcUse+"','"+str(idMachine)+"')");
        db.commit()
        db.close()
    return render_template('saveData.html', error=erreur)


#Collecteur HDD
@app.route('/serveurCentralHdd')
def serveurCentralHdd():
    erreur = "true"
    # Champs obligatoire RAM
    adresseMac = request.args.get('adr_mac', '')
    mbTotal = request.args.get('mb_total', '')
    mbUse = request.args.get('mb_use', '')
    pcUse = request.args.get('pc_use', '')
    date = time.strftime('%d/%m/%y %H:%M',time.localtime())

    
    
    if not adresseMac or len(adresseMac) == 0 or not mbTotal or len(mbTotal) == 0 or not pcUse or len(pcUse) == 0 or not mbUse or len(mbUse) == 0:
       erreur = "false"
    else:
        idMachine = None
        db = sqlite3.connect(PATH_BDD)
        cur = db.cursor()
        cur.execute("SELECT id FROM machine WHERE adr_mac = '"+adresseMac+"'")
        data=cur.fetchall()
        
        cur2 = db.cursor()
        cur2.execute("SELECT value FROM parametre WHERE key = 'hddMaxHistory'")
        maxCpu = cur2.fetchone()[0]

        cur2.execute("SELECT COUNT(*) FROM collecteurHdd")
        cpuCount = cur2.fetchone()[0]
        
        if maxCpu < cpuCount:
            cur2.execute("Delete from collecteurHdd where id IN (Select id from collecteurHdd limit 1)")

        if len(data) == 0:   
            cur.execute("INSERT INTO machine (adr_mac,last_modif) VALUES('"+adresseMac+"','"+date+"')");
            idMachine = cur.lastrowid
        else:
            idMachine =  data[0][0]
            cur.execute("UPDATE machine SET last_modif = '"+date+"' WHERE id = '"+str(idMachine)+"';")
        cur.execute("INSERT INTO collecteurHdd (date,mb_total,mb_use,pc_use,id_machine) VALUES('"+date+"','"+mbTotal+"','"+mbUse+"','"+pcUse+"','"+str(idMachine)+"')");
        db.commit()
        db.close()
    return render_template('saveData.html', error=erreur)



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=False)

