#!/usr/bin/env python

import spidev
import time
import subprocess
import requests

SERVER_URL = 'http://localhost:5000'
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
		return True
	else:
		return False

def wait_status_change(current_status):
	while True:
		new_status = is_pressed()
		if current_status != new_status :
			print('status chenged: ' , new_status)
			time.sleep(60 * IGNOERE_MIN)
			if new_status == is_pressed() :
				return new_status
		time.sleep(0.5)
	
def send_request():
	if get_pressure() == 0:
		requests.get( SERVER_URL + '/api/stand_up' )
	else:
		requests.get( SERVER_URL + '/api/sit_down' )
	print('request sent')

if __name__ =='__main__':
	while True:
		current_status = is_pressed()
		wait_status_change(current_status)
		send_request()

