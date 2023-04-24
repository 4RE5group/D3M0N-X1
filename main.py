import network
from machine import Pin,PWM
from time import sleep
from irrecvdata import irGetCMD
from machine import Pin, SoftSPI, I2C
from I2C_LCD import I2CLcd
from mfrc522 import MFRC522
import socket
import _thread
import micropython



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
	ap_if.active(True)
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
			display('uid: 0x%02x%02x%02x%02x' % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]), 0)
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
		lcd.putstr(">Settings       ")
		lcd.putstr(" About          ")
	if menu == 4:
		lcd.clear()
		lcd.putstr(" Settings       ")

		lcd.putstr(">About          ")
	if menu == 5:
		menu = 4

def selectoption(menu):
	if menu == 1:
		lcd.clear()
		display("      RFID      press ok to scan", 0)
		running=True
		while running:
			if not button_ok.value():
				running=False
				while True:
					if not button_ok.value():
						print("ok")
						break
					read_rfid_uid()
	if menu == 2:
		lcd.clear();
		display("Infrared", 0, True)
		display("waiting for signal", 0, True)
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
		display("Settings", 0, True)
		
	if menu == 4:
		lcd.clear()
		display("About", 0, True)
		display("About", 1)

		lcd.putstr(">About")



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
sleep(3)
lcd.clear()
lcd.putstr(">RFID           ")
lcd.putstr(" Infrared       ")

menu = 1
while True:
	if not button_down.value():
		menu=menu+1
		update_menu(menu)
		while not button_down.value():
			sleep(0)
	elif not button_up.value():
		menu=menu-1
		update_menu(menu)
		while not button_up.value():
			sleep(0)
	elif not button_ok.value():
		selectoption(menu)
		while not button_ok.value():
			sleep(0)

