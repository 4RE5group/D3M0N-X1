from machine import Pin, SoftSPI, I2C
import time
from I2C_LCD import I2CLcd



class settings_module:
	global lastdisplay2
	lastdisplay2=""
	
	i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
	devices = i2c.scan()
	lcd = I2CLcd(i2c, 0x3f, 2, 16)
	
	def __init__(self):
		self.button_up = Pin(20, Pin.IN, Pin.PULL_UP)	 
		self.button_ok = Pin(19, Pin.IN, Pin.PULL_UP)	
		self.button_down = Pin(18, Pin.IN, Pin.PULL_UP)
	
	def deleteSetting(name, file="D3M0N_settings.txt"):
		lines = ""
		with open("/"+file, "r") as fp:
			temp = fp.read().split("\n")
			for line in temp:
				if ": " in line:
					foundname = line.split(": ")[0]
					if not name==foundname:
						lines=lines+line+"\n"
			fp.write(lines)
			fp.close()
		return len(temp)
	
	def getSettingsLength(file="D3M0N_settings.txt"):
		with open("/"+file, "r") as fp:
			temp = fp.read().split("\n")
			fp.close()
		return len(temp)
	
	def getSettingsList(file="D3M0N_settings.txt"):
		settingslist = []
		settingsvalues = []
		with open("/"+file, "r") as fp:
			temp = fp.read().split("\n")
			for line in temp:
				if ": " in line:
					name = line.split(": ")[0]
					value = line.split(": ")[1]
					settingslist.append(name.replace("\r", ""))
					settingsvalues.append(value.replace("\r", ""))
			fp.close()
		return settingslist, settingsvalues
	
	# Function definition area
	def getSetting(name, file="D3M0N_settings.txt"):
		result = "Setting not found"
		with open("/"+file, "r") as fp:
			temp = fp.read().split("\r\n")
			for line in temp:
				if line.startswith(name+": "):
					result = line.replace(name+": ", "")
					print("FOUND ("+name+") value ("+result+")")
			fp.close()
		return result

	def setSetting(name, value, file="D3M0N_settings.txt"):
		settingsfinal=""
		with open("/"+file, "r") as fp:
			settings = fp.read().split("\n")
			for line in settings:
				if line.startswith(name+": "):
					settingsfinal+="\n"+name+": "+value
				else:
					settingsfinal+="\n"+line
			fp.close()
		with open("/"+file, "w") as fp:
			fp.write(settingsfinal)
			fp.close()
			
	def addSetting(name, value, file="D3M0N_settings.txt"):
		settingsfinal=""
		with open("/"+file, "r") as fp:
			settingsfinal = fp.read()
			fp.close()
		with open("/"+file, "w") as fp:
			fp.write(settingsfinal+"""
"""+name+": "+value)
			fp.close()

