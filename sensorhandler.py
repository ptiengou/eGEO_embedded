""" Docstring
	Module to actually communicate with eGEO sensor
	Able to extract easurements from sensor to store them in dict

	A "dev_test" attribute is used for development purposes
	It enables testing the complete workflow without an actual serial connection
	Makes it easier to test and correct code before importing it on Omega chips
"""
import serial
import json
import time
import random

class SensorHandler:

	operations = [
		'getTemp',
		'getFrequency',
		'getPowerA',
		'getPowerB',
		'getPowerC',
		'getPowerT',
		'getQPowerA',
		'getQPowerB',
		'getQPowerC',
		'getQPowerT',
		'getPmeanAH',
		'getPmeanBH',
		'getPmeanCH',
		'getPmeanTH',
		'getADAE',
		'getBDAE',
		'getCDAE',
		'getAIRE',
		'getBIRE',
		'getCIRE']

	def __init__(self, dev_test = False):
		""" Docstring
			ser will be the handle on the serial connection with the eGEO meter
			dev_test is a boolean used for dev to be able to test as many things before trying on the actual Omega card
		"""
		self.dev_test = dev_test
		if not(self.dev_test):
			self.ser = serial.Serial('/dev/ttyS1', 230400, timeout = 0.2)
		
	def _send_request(self, operation):
		"""
		operation is a string
		it corresponds to one of the commands for eGEO sensor
		https://www.egeo.co/docs/metering/operations-glossary/
		! Note: one of the operations won't work (Get Current Harmonic Ratio)

		A test_dev version has been written as well
		"""
		if not(self.dev_test):
			self.ser.flush()
			message0 ='"chip":"1","operation":"{op}"'.format(op =operation)
			message1 = '{' + message0 + '}'
			self.ser.write(message1.encode())
		print('Operation requested : {}'.format(operation))
	
	def _read_value(self, operation):
		""" Docstring
			operation is a string
			it corresponds to one of the commands for eGEO sensor
			https://www.egeo.co/docs/metering/operations-glossary/
			The desired value is returned by the function but not stored anywhere yet
			
			A test_dev version has been written as well
		"""
		if not (self.dev_test):
			while not self.ser.inWaiting():
	                    time.sleep(0.1) #wait until value is ready to be read
			message = self.ser.readline()
			data = json.loads(message)
			desired_value = data['value']

		else:
			time.sleep(0.1)
			a = random.randint(1, 2000)
			desired_value = 30 + (1000 - a) / 100

		return(desired_value)

	def request_operation(self, operation):
		""" Docstring
			operation is a string
			it corresponds to one of the commands for eGEO sensor
			https://www.egeo.co/docs/metering/operations-glossary/
		"""
		if (self._op_in_list(operation)):
			self._send_request(operation)
			value = self._read_value(operation)
			print('Answer received: {}'.format(value))
			return(value)
		else:
			print('Requested operation is incorrect')
			return(False)

	def _op_in_list(self, operation):
		""" Docstring
			tool function to check if an operation is in operations list
		"""
		for op in SensorHandler.operations:
			if operation == op:
				return(True)
		return(False)

	def request_power(self):
		""" Docstring
			function to return a dict containing active and reactive power measurements
		"""
		data = {'getPowerA':0.0,
				'getPowerB':0.0,
				'getPowerC':0.0, 
				'getPowerT':0.0, 
				'getQPowerA':0.0,
				'getQPowerB':0.0,
				'getQPowerC':0.0,
				'getQPowerT':0.0
				}

		for key in data.keys():
			data[key] = self.request_operation(key)
		return(data)

#{"chip": "1","operation": "getTemp"}
##############
### SCRIPT ###
##############
print('SensorHandler imported')

# sensor_hdlr = SensorHandler(True)
# # begin_time = time.time()
# #for operation in sensor_hdlr.operations:
# 	#sensor_hdlr.request_operation(operation)

# sensor_hdlr.request_power()

# # final_time = time.time()
# # print('Total time: {}'.format(final_time - begin_time))
