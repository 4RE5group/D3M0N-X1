from machine import Pin
import time

class IRcontroller:
	def __init__(self, pin):
		self.pin = Pin(pin, Pin.OUT)

	def send(self, data):
		for i in range(len(data)):
			for j in range(8):
				if data[i] & (1 << j):
					self.pin.on()
					time.sleep_us(600)
					self.pin.off()
					time.sleep_us(600)
				else:
					self.pin.on()
					time.sleep_us(600)
					self.pin.off()
					time.sleep_us(200)
			self.pin.on()
			time.sleep_us(600)
			self.pin.off()
			time.sleep_us(600)
