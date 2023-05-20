from machine import Pin, SoftSPI, I2C, ADC
import time
import micropython
from I2C_LCD import I2CLcd
from settings import settings_module


class clock_module(object):
	global lastdisplay2
	lastdisplay2=""
	
	def __start__(self):
	    # define buttons
		self.button_up = Pin(20, Pin.IN, Pin.PULL_UP)
		self.button_ok = Pin(19, Pin.IN, Pin.PULL_UP)
		self.button_down = Pin(18, Pin.IN, Pin.PULL_UP)
		
		# set first menu line
		menu=0
    
		# connect to LCD display
		i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
		devices = i2c.scan()
		self.lcd = I2CLcd(i2c, 0x3f, 2, 16)
		# clear display
		self.lcd.clear()
		nulltext="                  "
		while self.button_ok.value():
			localtime=str(time.localtime()).replace("(", "").replace(")", "").replace(" ", "").split(",")
			hour=localtime[3]+":"+localtime[4]+":"+localtime[5]
			date=localtime[2]+"/"+localtime[1]+"/"+localtime[0]
			self.display(self, nulltext[0:int((8-len(hour))/2)]+hour+nulltext[0:int((8-len(hour))/2)], 0, True)
			self.display(self, nulltext[0:int((8-len(date))/2)]+date+nulltext[0:int((8-len(date))/2)], 1, True)
			time.sleep(0.5)
		return
	def display(self, text, line, middle=False, lastdisplay=lastdisplay2):
		if middle:
			self.lcd.move_to(int(8-len(text)/2), line)
		else:
			self.lcd.move_to(0, line)
		if text!=lastdisplay:
			self.lcd.putstr(text)
		lastdisplay=text

