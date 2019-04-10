import paho.mqtt.client as mqtt
import json
import time

class CloudHandler:
	"""
	Class that enables sending data to Thingsboard for live visualization
	Could be used to store data in the cloud as well
	"""
	def __init__(self, tb_host = 'demo.thingsboard.io', access_token = 'Xn7d8oJvxSpkPpBv30N0'):
		self._THINGSBOARD_HOST = tb_host
		self._ACCESS_TOKEN = access_token
		
		self._client = mqtt.Client()
		self._client.username_pw_set(self._ACCESS_TOKEN)

	def connect(self, port = 1883, keep_alive = 60):
		# Connect to ThingsBoard using by default MQTT port and 60 seconds keepalive interval
		print('Initiating connection to Thingsboard')
		try:
		    self._client.connect(self._THINGSBOARD_HOST, port, keep_alive)
		    print('Connected to Thingsboard')
		except AssertionError as e:
		    print("No connection")
		    print(e)

		self._client.loop_start() #not sure this goes here

	def shutdown(self):
		"""
		Meant to be called at the end of the program
		"""
		print('Shutting down connection to Thingsboard')
		self._client.loop_stop()
		self._client.disconnect()

	def send_data(self, message):
		"""
		Function to send data to Thingsboard
		! message attribute must be a dict 
		"""
		try:
			self._client.publish('v1/devices/me/telemetry', json.dumps(message), 1)
		except AssertionError as e:
			print("Couldn't send message")
			print(e)


import random
def generate_data(cloud_hdlr):
	while(True):
		a = random.randint(1, 2000)
		data = {'power': 30 + (1000 - a) / 100}
		# print(type(data['power']))
		cloud_hdlr.send_data(data)
		time.sleep(0.5)

##############
### SCRIPT ###
##############
print('CloudHandler imported')

# #tb_host = 'https://demo.thingsboard.io'
# tb_host = 'demo.thingsboard.io'

# access_token = 'Xn7d8oJvxSpkPpBv30N0'
# cloud_hdlr = CloudHandler(tb_host, access_token)
# cloud_hdlr.connect()

# generate_data(cloud_hdlr)

# cloud_hdlr.shutdown()
