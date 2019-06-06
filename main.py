from cloudhandler import CloudHandler
from sqlhandler import SQLHandler
from sensorhandler import SensorHandler

from datetime import datetime, timedelta


#dictionary to store data
#note : for less hardcoded, those name could just be the commands we send to eGEO (like in sensorhandler)
#this would simplify a lot the do_things() function as well
data_dict = {'timestamp_data':0.0,
			'active_powerA':0.0,
			'active_powerB':0.0,
			'active_powerC':0.0, 
			'active_powerT':0.0, 
			'reactive_powerA':0.0,
			'reactive_powerB':0.0,
			'reactive_powerC':0.0,
			'reactive_powerT':0.0,
			'active_fundamental_powerA' : 0.0,
			'active_fundamental_powerB' : 0.0,
			'active_fundamental_powerC' : 0.0,
			'active_fundamental_powerT' : 0.0,
			'active_harmonic_powerA' : 0.0,
			'active_harmonic_powerB' : 0.0,
			'active_harmonic_powerC' : 0.0,
			'active_harmonic_powerT' : 0.0
			}

#instanciating 3 types of handlers

#sensor handler
# sensor_hdlr = SensorHandler(dev_test = True)
sensor_hdlr = SensorHandler(dev_test = False)

#sql handler
sql_hdlr = SQLHandler('datalog.sqlite')
sql_hdlr.swipe_clean_database()
sql_hdlr.create_database()

#cloud handler
cloud_hdlr = CloudHandler()
cloud_hdlr.connect()

def do_things():
	#collecting data from sensor
	# sensor_data = sensor_hdlr.request_power()
	sensor_data = sensor_hdlr.request_power2()

	#asigning new values to dict
	data_dict['timestamp_data'] = (datetime.now() - timedelta(hours = 5)).strftime('%Y-%m-%d %H:%M:%S') #offset in the clock of Omega for some reason...
	data_dict['active_powerA'] = sensor_data['getPowerA']
	data_dict['active_powerB'] = sensor_data['getPowerB']
	data_dict['active_powerC'] = sensor_data['getPowerC']
	data_dict['active_powerT'] = sensor_data['getPowerT']
	data_dict['reactive_powerA'] = sensor_data['getQPowerA']
	data_dict['reactive_powerB'] = sensor_data['getQPowerB']
	data_dict['reactive_powerC'] = sensor_data['getQPowerC']
	data_dict['reactive_powerT'] = sensor_data['getQPowerT']
	data_dict['active_fundamental_powerA'] = sensor_data['getPmeanAF']
	data_dict['active_fundamental_powerB'] = sensor_data['getPmeanBF']
	data_dict['active_fundamental_powerC'] = sensor_data['getPmeanCF']
	data_dict['active_fundamental_powerT'] = sensor_data['getPmeanTF']
	data_dict['active_harmonic_powerA'] = sensor_data['getPmeanAH']
	data_dict['active_harmonic_powerB'] = sensor_data['getPmeanBH']
	data_dict['active_harmonic_powerC'] = sensor_data['getPmeanCH']
	data_dict['active_harmonic_powerT'] = sensor_data['getPmeanTH']

	#sending dict to cloud
	cloud_hdlr.send_data(data_dict)

	#storing dict to sql database
	inserted = sql_hdlr.insert_measurement(data_dict)
	print (inserted)

#While loop to keep doing the things
try:
	while(True):
		do_things()
# except AssertionError as e:
# 	print(e)
# 	print('Program interrupted, you may want to check do_things function')
# 	pass
except :
	print('Program interrupted, you may want to check do_things function')
	pass


# import pandas as pd
# df = pd.read_sql_query("SELECT * FROM smart_meter", sql_hdlr.con)
# print(df.head(10))

#closing mqtt connection to cloud
cloud_hdlr.shutdown()
