from machine import Pin, SoftSPI, I2C
import time
from I2C_LCD import I2CLcd
import micropython
from settings import settings_module


class config_module(object):
	global lastdisplay2
	lastdisplay2=""
	
	def __start__(self):
		self.button_up = Pin(20, Pin.IN, Pin.PULL_UP)
		self.button_ok = Pin(19, Pin.IN, Pin.PULL_UP)
		self.button_down = Pin(18, Pin.IN, Pin.PULL_UP)
		
		menu=0
		i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
		devices = i2c.scan()
		self.lcd = I2CLcd(i2c, 0x3f, 2, 16)
		self.lcd.clear()
		
		self.display(self,"CONFIG", 0, True)
		
		settingsnames = settings_module.getSettingsList()[0]
		settingsvalues = settings_module.getSettingsList()[1]
		
		print(str(settingsnames))
		print(str(settingsvalues))
		
		if len(settingsnames) > 0:
			menu3=1
			nulltext="                             "
			
			self.display(self,settingsnames[menu3-1][0:15]+":"+nulltext[0:16-len(settingsnames[menu3-1][0:15]+":")], 0)
			self.display(self,settingsvalues[menu3-1][0:16]+nulltext[0:16-len(settingsvalues[menu3-1][0:16])], 1)
			
			while True:
				if menu3==1 and not self.button_up.value():
					break
				if not self.button_down.value() and not menu3==len(settingsnames):
					menu3=menu3+1
					self.display(self,settingsnames[menu3-1][0:15]+":"+nulltext[0:16-len(settingsnames[menu3-1][0:15]+":")], 0)
					self.display(self,settingsvalues[menu3-1][0:16]+nulltext[0:16-len(settingsvalues[menu3-1][0:16])], 1)
					while not self.button_down.value():
						time.sleep(0)
				if not self.button_up.value() and not menu3==1:
					menu3=menu3-1
					self.display(self,settingsnames[menu3-1][0:15]+":"+nulltext[0:16-len(settingsnames[menu3-1][0:15]+":")], 0)
					self.display(self,settingsvalues[menu3-1][0:16]+nulltext[0:16-len(settingsvalues[menu3-1][0:16])], 1)
					while not self.button_up.value():
						time.sleep(0)
		else:
			self.display(self,"No data avaiable", 0)
			time.sleep(1)
		return
			
	def display(self, text, line, middle=False, lastdisplay=lastdisplay2):
		if middle:
			self.lcd.move_to(int(8-len(text)/2), line)
		else:
			self.lcd.move_to(0, line)
		if text!=lastdisplay:
			self.lcd.putstr(text)
		lastdisplay=text