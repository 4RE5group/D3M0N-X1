import network
from machine import Pin,PWM
from time import sleep
from irrecvdata import irGetCMD
from machine import Pin, SoftSPI, I2C
from I2C_LCD import I2CLcd
from mfrc522 import MFRC522


# Function definition area
def getSetting(name):
	result = "Setting not found"
	with open("/D3M0N_settings.txt", "r") as fp:
			temp = fp.read().split("""
""")
			for line in temp:
				if line.startswith(name+": "):
					result = line.replace(name+": ", "")
					print("FOUND "+name+" value "+result)
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
	with open("/D3M0N_settings.txt", "w") as fp:
			fp.wite(settingsfinal)

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
			print('New Card Detected')
			print('  - Tag Type: 0x%02x' % tag_type)
			print('  - uid: 0x%02x%02x%02x%02x' % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
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
global lastdisplay
def display(text, line, middle=False):
	i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
	devices = i2c.scan()
	lcd = I2CLcd(i2c, 0x3f, 2, 16)
	if middle:
		lcd.move_to(int(8-len(text)/2), line)
	else:
		lcd.move_to(0, line)
	if text!=lastdisplay:
		lcd.putstr(text)
	lastdisplay=text





# vars definition
ssidAP		 = getSetting("ap_ssid") #get the router name
passwordAP	 = getSetting("ap_password")  #get the router password

local_IP	   = '192.168.1.10'
gateway		= '192.168.1.1'
subnet		 = '255.255.255.0'
dns			= '8.8.8.8'

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
	display("Failed start AP", 0)
	ap_if.disconnect()

while True:
	selected1=0
	selected2=1
	options= ["RFID           ", "Infrared       ", "Settings       ", "About          "]
	display(">"+options[selected1]+options[selected2], 0)
	if not button_up.value():
		if selected1!=0:
			selected1=selected1+1
			selected2=selected2+1
	elif not button_ok.value():
		display("ok", 0)
	elif not button_down.value():
		if selected2!=len(options):
			selected1=selected1-1
			selected2=selected2-1

# read rfid uid
#while True:
#	read_rfid_uid()

# setup IR
recvPin = irGetCMD(15)
try:
	while True:
		value = recvPin.ir_read()
		if value:
			display("Receieved: "+value, 1)
except:
	pass
