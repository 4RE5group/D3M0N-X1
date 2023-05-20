from machine import Pin, SoftSPI, I2C, ADC
import time
import micropython
from I2C_LCD import I2CLcd
from settings import settings_module


class about_module(object):
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
		
		about_text = "D3M0N X1, is made by 4RE5 Team, 4re5.com"
		aboutchars=list(about_text)
		self.display(self, "About", 0, True)
		i=0
		
		while button_ok.value():
			try:
				finalvar=aboutchars[i]+aboutchars[i+1]+aboutchars[i+2]+aboutchars[i+3]+aboutchars[i+4]+aboutchars[i+5]+aboutchars[i+6]+aboutchars[i+7]+aboutchars[i+8]+aboutchars[i+9]+aboutchars[i+10]+aboutchars[i+11]+aboutchars[i+12]+aboutchars[i+13]+aboutchars[i+14]+aboutchars[i+15]
				i=i+1
				self.display(self, finalvar, 1)
				sleep(0.5)
			except:
				i=0
		return
	def display(self, text, line, middle=False, lastdisplay=lastdisplay2):
		if middle:
			self.lcd.move_to(int(8-len(text)/2), line)
		else:
			self.lcd.move_to(0, line)
		if text!=lastdisplay:
			self.lcd.putstr(text)
		lastdisplay=text
