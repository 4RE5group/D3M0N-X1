from machine import Pin, SoftSPI, I2C
import time
from I2C_LCD import I2CLcd
from IRcontroller import IRcontroller
from irrecvdata import irGetCMD
from ir_tx import *
import usocket
from ir_tx.nec import NEC
import micropython
from settings import settings_module


class infrared_module(object):
	global lastdisplay2
	lastdisplay2=""
	
	def __start__(self):
		self.button_up = Pin(20, Pin.IN, Pin.PULL_UP)
		self.button_ok = Pin(19, Pin.IN, Pin.PULL_UP)
		self.button_down = Pin(18, Pin.IN, Pin.PULL_UP)
		irPin = Pin(21, Pin.OUT)
		sender = Player(irPin)
		dataOn = [8960,4585,492,645,493,643,494,644,492,644,493,645,494,643,494,644,493,617,520,1755,493,1757,491,1756,495,1756,492,1755,493,1755,493,1756,492,1757,491,1731,517,1734,515,1756,492,644,469,670,492,645,492,646,468,645,493,668,469,669,492,645,469,1781,467,1781,469,1779,469,1781,467,1781,467,1000]
		#sendIR(dataOn, 'on')
		tx = IRcontroller(21)
		
		nec = NEC(Pin(21, Pin.OUT, value = 0))
		nec.transmit(1, 2)  # address == 1, data == 2
		
		menu=0
		i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
		devices = i2c.scan()
		self.lcd = I2CLcd(i2c, 0x3f, 2, 16)
		self.lcd.clear()
		
		self.display(self,"INFRARED", 0, True)
		self.updatemenu(self, menu)
		
		while True:
			if not self.button_up.value() and not menu==0:
				menu=menu-1
				self.updatemenu(self, menu)
				while not self.button_up.value():
					time.sleep(0)
			if not self.button_down.value() and not menu==2:
				menu=menu+1
				self.updatemenu(self, menu)
				while not self.button_down.value():
					time.sleep(0)
			if not self.button_ok.value():
				self.selectoption(self, menu)
				while not self.button_ok.value():
					time.sleep(0)
		return
	
	def updatemenu(self, menu):
		if menu == -1:
			menu = 0
		if menu == 0:
			self.display(self," > read signal  ", 1)
		if menu == 1:
			self.display(self," > save signal  ", 1)
		if menu == 2:
			self.display(self," > play signal  ", 1)
		if menu == 3:
			self.display(self," > delete signal", 1)
		if menu == 4:
			menu = 5
	
	def selectoption(self, menu):
		if menu == 0:
			self.lcd.clear()
			self.display(self, "waiting signal", 0, True)
			recvPin = irGetCMD(15)
			
			try:
				while True:
					value = recvPin.ir_read()
					if value:
						self.display(self, "Data: "+value, 1)
						while self.button_ok.value():
							time.sleep(0)
						break
					if not self.button_ok.value():
						break
				return
			except Exception as e:
				print(e)
			return
		if menu == 1:
			self.lcd.clear()
			self.display(self, "waiting signal", 0, True)
			recvPin = irGetCMD(15)
			
			try:
				while True:
					value = recvPin.ir_read()
					if value:
						self.display(self, "Saved", 1)
						settings_module.addSetting("Save_"+str(settings_module.getSettingsLength()+1), value, "/modules/infrared/saved_ir")
						
						
						time.sleep(1.5)
						break
					if not self.button_ok.value():
						break
			except Exception as e:
				print(e)
			return
		if menu == 2:
			tmp=settings_module.getSettingsList("/modules/infrared/saved_ir")
			saved_ir_names = tmp[0]
			saved_ir_values = tmp[1]
			
			print(str(saved_ir_names))
			print(str(saved_ir_values))
			
			if len(saved_ir_names) > 0:
				menu3=1
				self.display(self,"  Select  save  ", 0, True)
				self.display(self,"> "+saved_ir_names[menu3-1][0:14], 1)
				print("after")
				time.sleep(0.5)
				while True:
					if menu3==1 and not self.button_up.value():
						break
					if not self.button_down.value() and not menu3==len(saved_ir_names):
						menu3=menu3+1
						self.display(self,"                ", 1)
						self.display(self,"> "+saved_ir_names[menu3-1][0:14], 1)
						while not self.button_down.value():
							time.sleep(0)
					if not self.button_up.value() and not menu3==1:
						menu3=menu3-1
						self.display(self,"                ", 1)
						self.display(self,"> "+saved_ir_names[menu3-1][0:14], 1)
						while not self.button_up.value():
							time.sleep(0)
					if not self.button_ok.value():
						nec = NEC(Pin(21, Pin.OUT, value = 0))
						nec.transmit(1, int(saved_ir_values[menu3-1]))  # address == 1, data == 2
						print("sent '"+str(saved_ir_names[menu3-1])+"' data: '"+str(saved_ir_values[menu3-1])+"'")
			else:
				self.display(self,"No save avaiable", 0)
				time.sleep(1)
			return
		if menu == 3:
			self.lcd.clear()
			self.display(self,"uwu2 ", 0)
			self.display(self,"uwu2 ", 1)
	def display(self, text, line, middle=False, lastdisplay=lastdisplay2):
		if middle:
			self.lcd.move_to(int(8-len(text)/2), line)
		else:
			self.lcd.move_to(0, line)
		if text!=lastdisplay:
			self.lcd.putstr(text)
		lastdisplay=text


