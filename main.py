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


# /!\ check https://www.youtube.com/watch?v=l254lxm78I4 for cicruitpython&micropython

#import usb_hid
#from adafruit_hid.keyboard import Keyboard
#from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
#from adafruit_hid.keycode import Keycode

#kbd = Keyboard(usb_hid.device)
#layout = KeyboardLayout(kbd)
#layout.write(Keycode.A)


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

def sort_list(list1, list2):
 
    zipped_pairs = zip(list2, list1)
 
    z = [x for _, x in sorted(zipped_pairs)]
 
    return z

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
topones=[]
bottomones=[]
topones2=[]
bottomones2=[]
topsvaluesss=[]
bottomsvaluesss=[]
for filename in os.listdir("modules"):
	f = "modules/"+filename
	try:
		os.stat(f)
		topvalue=int(settings_module.getSetting("top", "modules/"+filename+"/config"))
		bottomvalue=int(settings_module.getSetting("bottom", "modules/"+filename+"/config"))
		
		if topvalue == 0 and bottomvalue == 0:
			modulesname.append(settings_module.getSetting("name", "modules/"+filename+"/config"))
			modulesclass.append(settings_module.getSetting("classname", "modules/"+filename+"/config"))
		elif topvalue == 0 and not bottomvalue == 0:
			bottomones.append(settings_module.getSetting("name", "modules/"+filename+"/config"))
			bottomones2.append(settings_module.getSetting("classname", "modules/"+filename+"/config"))
			bottomsvaluesss.append(bottomvalue)
		elif not topvalue == 0 and bottomvalue == 0:
			topones.append(settings_module.getSetting("name", "modules/"+filename+"/config"))
			topones2.append(settings_module.getSetting("classname", "modules/"+filename+"/config"))
			topsvaluesss.append(topvalue)
		else:
			modulesname.append(settings_module.getSetting("name", "modules/"+filename+"/config"))
			modulesclass.append(settings_module.getSetting("classname", "modules/"+filename+"/config"))
		sys.path.append("modules/"+filename+"/")
	except OSError:
		continue
if not len(topones)==0:
	topones = list(reversed(sort_list(topones, topsvaluesss)))
	topones2 = list(reversed(sort_list(topones2, topsvaluesss)))
if not len(bottomones)==0:
	bottomones = list(sort_list(bottomones, bottomsvaluesss))
	bottomones2 = list(sort_list(bottomones2, bottomsvaluesss))

modulesname=topones+modulesname+bottomones
modulesclass=topones2+modulesclass+bottomones2
print("topsvaluesss: "+str(topsvaluesss))
print("top: "+str(topones))
print("---------------------------------")
print("bottomsvaluesss: "+str(bottomsvaluesss))
print("bottom: "+str(bottomones))


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
