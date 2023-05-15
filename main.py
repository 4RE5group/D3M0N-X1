import network
from machine import Pin,PWM
from time import sleep
from machine import Pin, SoftSPI, I2C
from I2C_LCD import I2CLcd
import socket
import uos
import _thread
import micropython
import uasyncio as asyncio
import usocket
from settings import settings_module
import os
import gc
gc.collect()

global lastdisplay2
lastdisplay2=""

def AP_Setup(ssidAP,passwordAP):
	ap_if.disconnect()
	ap_if.ifconfig([settings_module.getSetting("web_address"),gateway,subnet,dns])
	print("Setting AP... ")
	ap_if.active(True)
	ap_if.config(essid=ssidAP, password=passwordAP)
	print('Success, IP address:', ap_if.ifconfig())
	print("Setup End\n")

async def webserver_main():
    asyncio.create_task(webserver())
    #webserver()

async def webserver():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
	s.bind(('', 80))
	s.listen(5)
	while True:
		conn, addr = s.accept()
		await print('Got a connection from %s' % str(addr))
		request = conn.recv(1024)
		path = str(request).split(" HTTP")[0]
		print("path: "+path)
		try:
			with open(settings_module.getSetting("web_path")+path, "r") as fp:
				response = fp.read()
		except:
			response = "<h2>404: not found</h2>"
		await conn.send(response)
		await conn.close()


i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
devices = i2c.scan()
lcd = I2CLcd(i2c, 0x3f, 2, 16)

def display(text, line, middle=False, lastdisplay=lastdisplay2):
	if middle:
		lcd.move_to(int(8-len(text)/2), line)
	else:
		lcd.move_to(0, line)
	if text!=lastdisplay:
		lcd.putstr(text)
	lastdisplay=text

def keylogger():
	while True:
		cmd = sys.stdin.read(1)
		if cmd == 'a':
			print("uwu")
def bad_usb():
	print("bad usb")



def hex_to_bytes(hex_code):
	# Convertir le code hexadécimal en un entier
	code = int(hex_code, 16)

	# Extraire les bits de l'entier
	bits = []
	for i in range(32):
		bits.append((code >> i) & 1)

	# Convertir les bits en un tableau de bytes
	bytes = []
	for i in range(4):
		byte = 0
		for j in range(8):
			byte |= bits[i*8+j] << j
		bytes.append(byte)

	return bytes

def sendIR(timings, dbgOutput = ''):
	print(dbgOutput)
	sender.play(timings)
    
	nec = NEC(irPin)
	nec.transmit(1, 2)  # address == 1, data == 2

def selectoption(menu):
	if menu == 1:
		lcd.clear()
		display("      RFID      waiting card", 0)
		try:
			while True:
				value = rfid_module.read_rfid_uid()
				if value:
					display("UID: "+value, 1)
					break
				if not button_ok.value:
					break
		except:
			pass
		return
	if menu == 4:
		lcd.clear()
		display("Keyboard hacks", 0, True)
		display(" > Keylogger    ", 1)
		menu2=1
		sleep(1)
		while True:
			if not button_up.value() and menu2==1:
				return
			elif not button_down.value() and not menu2==2:
				menu2=menu2+1
				if menu2==1:
					display(" > Keylogger    ", 1)
				else:
					display(" > Bad USB      ", 1)
				while not button_down.value():
					sleep(0)
			elif not button_up.value() and not menu2==1:
				menu2=menu2-1
				if menu2==1:
					display(" > Keylogger    ", 1)
				else:
					display(" > Bad USB      ", 1)
				while not button_up.value():
					sleep(0)
			elif not button_ok.value():
				if menu2==1:
					keylogger()
					display(" > Keylogger    ", 1)
				else:
					bad_usb()
					display(" > Bad USB      ", 1)
				while not button_ok.value():
					sleep(0)
	if menu == 5:
		lcd.clear()
		about_text = "D3M0N X1, is made by duckpvpteam, duckpvpteam.com"
		aboutchars=list(about_text)
		display("About", 0, True)
		i=0
		
		while button_ok.value():
			try:
				finalvar=aboutchars[i]+aboutchars[i+1]+aboutchars[i+2]+aboutchars[i+3]+aboutchars[i+4]+aboutchars[i+5]+aboutchars[i+6]+aboutchars[i+7]+aboutchars[i+8]+aboutchars[i+9]+aboutchars[i+10]+aboutchars[i+11]+aboutchars[i+12]+aboutchars[i+13]+aboutchars[i+14]+aboutchars[i+15]
				i=i+1
				display(finalvar, 1)
				sleep(0.5)
			except:
				i=0
		print("finished")
		return



# vars definition
ssidAP = settings_module.getSetting("ap_ssid")
passwordAP = settings_module.getSetting("ap_password")

gateway = '192.168.1.1'
subnet  = '255.255.255.0'
dns = '8.8.8.8'

button_up = Pin(20, Pin.IN, Pin.PULL_UP)
button_ok = Pin(19, Pin.IN, Pin.PULL_UP)
button_down = Pin(18, Pin.IN, Pin.PULL_UP)


# main display
display("    D3M0N X1     by duckpvpteam", 0)
# setup AP
ap_if = network.WLAN(network.AP_IF)
try:
	AP_Setup(ssidAP,passwordAP)
except:
	lcd.clear()
	display("Failed start AP", 0)
	ap_if.disconnect()

try:
	print("starting webserver")
	#webserver()
	#asyncio.run(webserver())
except Exception as e:
	lcd.clear()
	display("Failed start web server", 0)
	print(e)



sleep(float(settings_module.getSetting("startup_time")))
lcd.clear()

import sys


modulesname=[]
modulesclass=[]
for filename in os.listdir("modules"):
	f = "modules/"+filename
	try:
		os.stat(f)
		modulesname.append(settings_module.getSetting("name", "modules/"+filename+"/config"))
		modulesclass.append(settings_module.getSetting("classname", "modules/"+filename+"/config"))
		sys.path.append("modules/"+filename+"/")
	except OSError:
		continue

if len(modulesname) > 0:
	display("> "+modulesname[0][0:14], 0)
	if len(modulesname) > 1:
		display("  "+modulesname[1][0:14], 1)
	else:
		display("                ", 1)
	menu=0
	Firstline=True
	while True:
		if not button_down.value() and not menu+1==len(modulesname):
			menu=menu+1
			
			if (menu % 2) == 0:
				#pair
				Firstline=True
				print("menu: "+str(menu)+" is pair")
			elif (menu % 2) == 1:
				#impair
				Firstline=False
				print("menu: "+str(menu)+" is impair")
			
			
			#print("menu: "+str(menu)+"/total: "+str(len(modulesname)))
			#print("ISfirst?: "+str(Firstline))
			
			
			lcd.clear()
			if Firstline:
				display("> "+modulesname[menu][0:14], 0)
				if menu+1==len(modulesname):
					display("                ", 1)
				else:
					display("  "+modulesname[menu+1][0:14], 1)
				Firstline=False
			else:
				display("  "+modulesname[menu-1][0:14], 0)
				if menu==len(modulesname):
					display("> "+modulesname[menu-1][0:14], 0)
					display("                ", 1)
				else:
					display("> "+modulesname[menu][0:14], 1)
				Firstline=True
			while not button_down.value():
				sleep(0)
		if not button_up.value():
			if menu==0:
				Firstline=True
			else:
				menu=menu-1
			
			#print("menu: "+str(menu)+"/total: "+str(len(modulesname)))
			#print("ISfirst?: "+str(Firstline))
			
			lcd.clear()
			if Firstline:
				display("> "+modulesname[menu][0:14], 0)
				if menu+2>len(modulesname):
					display("                ", 1)
				else:
					display("  "+modulesname[menu+1][0:14], 1)
				Firstline=False
			else:
				display("  "+modulesname[menu-1][0:14], 0)
				if menu>len(modulesname):
					display("                ", 1)
				else:
					display("> "+modulesname[menu][0:14], 1)
				Firstline=True
			while not button_up.value():
				sleep(0)
		if not button_ok.value():
			try:
				print("module: "+modulesname[menu].lower())
				module = __import__(modulesname[menu].lower())
				classname = getattr(module, modulesclass[menu].lower())
				classname.__start__(classname)
			except Exception as e:
				print(e)
				lcd.clear()
				display("This module", 0, True)
				display("doesn't work", 1, True)
				sleep(1)
				lcd.clear()
				display("> "+modulesname[0][0:14], 0)
				if len(modulesname) > 1:
					display("  "+modulesname[1][0:14], 1)
				else:
					display("                ", 1)
				menu=0
				Firstline=True
else:
	display("No modules", 0)

