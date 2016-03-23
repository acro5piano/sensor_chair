#!/usr/bin/env python

import spidev
import time
import subprocess
import requests

SERVER_URL = 'http://localhost:8080'
IGNOERE_MIN = 1

def get_pressure():
	
	spi = spidev.SpiDev()
	spi.open(0,0)

	resp = spi.xfer2([0xc68,0x00])
	value = (resp[0] * 256 + resp[1]) & 0x3ff
	spi.close()
	return value

def is_pressed():
	if get_pressure() > 0:
		return 1
	else:
		return 0
	
def send_request():
	requests.post( SERVER_URL + '/api/chair_log',{"value":is_pressed()} )
	print('request sent',is_pressed())

if __name__ =='__main__':
	while True:
		current_status = is_pressed()
		send_request()
		time.sleep(5*60)

