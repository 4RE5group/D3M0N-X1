from machine import Pin, SoftSPI, I2C
import time
from I2C_LCD import I2CLcd
from mfrc522 import MFRC522



class rfid_module:
	global lastdisplay2
	lastdisplay2=""
	
	i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
	devices = i2c.scan()
	lcd = I2CLcd(i2c, 0x3f, 2, 16)
	
	
	def __init__(self):
		self.button_up = Pin(20, Pin.IN, Pin.PULL_UP)	 
		self.button_ok = Pin(19, Pin.IN, Pin.PULL_UP)	
		self.button_down = Pin(18, Pin.IN, Pin.PULL_UP)

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
