#!/usr/bin/env python

import spidev
import time
import subprocess
import requests

SERVER_URL = 'http://localhost:5000'

def wait_press():

	try:
		while True:
			value = get_pressure()
			if value > 0:
				return True
			time.sleep(0.5)
	except KeyboardInterrupt:
		spi.close()

def get_pressure():
	
	spi = spidev.SpiDev()
	spi.open(0,0)

	resp = spi.xfer2([0xc68,0x00])
	value = (resp[0] * 256 + resp[1]) & 0x3ff
	spi.close()
	return value

def post_server():
	r = requests.get( SERVER_URL + '/api' )
	print(r.status_code)
	print(r.content)
	print(r.json())
	
	
if __name__ =='__main__':
	while True:
		wait_press()
		post_server()

