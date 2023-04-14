import wifi
import socketpool
from adafruit_httpserver.mime_type import MIMEType
from adafruit_httpserver.request import HTTPRequest
from adafruit_httpserver.response import HTTPResponse
from adafruit_httpserver.server import HTTPServer
import ipaddress
import storage
import os
import board
import busio
import time
import mfrc522
from adafruit_character_lcd.character_lcd_rgb_i2c import Character_LCD_RGB_I2C
import adafruit_character_lcd.character_lcd_i2c as character_lcd


def read_rfid():
	rdr = mfrc522.MFRC522lib(board.GP2, board.GP3, board.GP4, board.GP9, board.GP5)
	print('')
	print("Place card before reader to read from address 0x08")
	print('')
	try:
		while True:
			(stat, tag_type) = rdr.request(rdr.REQIDL)
			if stat == rdr.OK:
				(stat, raw_uid) = rdr.anticoll()
				if stat == rdr.OK:
					print("New card detected")
					print("  - tag type: 0x%02x" % tag_type)
					print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print('')
					if rdr.select_tag(raw_uid) == rdr.OK:
						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							print("Address 8 data: %s" % rdr.read(8))
							rdr.stop_crypto1()
						else:
							print("Authentication error")
					else:
						print("Failed to select tag")
	except KeyboardInterrupt:
		print("Bye")

def write_rfid():
	print('')
	print("Place card before reader to write to address 0x08")
	print('')
	try:
		while True:
			(stat, tag_type) = rdr.request(rdr.REQIDL)
			if stat == rdr.OK:
				(stat, raw_uid) = rdr.anticoll()
				if stat == rdr.OK:
					print("New card detected")
					print("  - tag type: 0x%02x" % tag_type)
					print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print('')
					if rdr.select_tag(raw_uid) == rdr.OK:
						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							stat = rdr.write(
									8, b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
									)
							rdr.stop_crypto1()
							if stat == rdr.OK:
								print("Data written to card")
							else:
								print("Failed to write data to card")
						else:
							print("Authentication error")
					else:
						print("Failed to select tag")
	except KeyboardInterrupt:
		print("Bye")
		
#read_rfid()


def main_screen():
	lcd_columns = 16
	lcd_rows = 2

	i2c = busio.I2C(board.GP15, board.GP14)
	#lcd = Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
	lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

	# Turn backlight on
	lcd.backlight = False
	# Print a two line message
	lcd.message = "Hello\nCircuitPython"
	
	time.sleep(5)
	lcd.clear()

main_screen()


# set access point credentials
ap_ssid = "never gonna give u up"
ap_password = "password"

# start access point
wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)

# print access point settings
print("Access point created with SSID: {}, password: {}".format(ap_ssid, ap_password))

print("My IP address is", str(ipv4))
ipv4 =  ipaddress.IPv4Address(wifi.radio.ipv4_address_ap)

# create http server
server = HTTPServer(socketpool.SocketPool(wifi.radio))

@server.route("/") 
def base(request):
	response = HTTPResponse(request)
	if request.path == "/":
		with open("/index.html", "r") as fp:
			result = fp.readline()
	elif os.path.isfile(request.path):
		with open(request.path, "r") as fp:
			result = fp.readline()
	else:
		result = "404: not found :p"  
	response.send(result, content_type="text/html")

print(f"Listening on http://"+str(ipv4)+":80")
server.serve_forever(str(ipv4), port=80) # never returns

