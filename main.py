from cloudhandler import CloudHandler
from sqlhandler import SQLHandler
from sensorhandler import SensorHandler

from datetime import datetime


#dictionary to store data
data_dict = {'timestamp_data':0.0,
			'active_powerA':0.0,
			'active_powerB':0.0,
			'active_powerC':0.0, 
			'active_powerT':0.0, 
			'reactive_powerA':0.0,
			'reactive_powerB':0.0,
			'reactive_powerC':0.0,
			'reactive_powerT':0.0
			}

#instanciating 3 types of handlers

#sensor handler
sensor_hdlr = SensorHandler(dev_test = True)
# sensor_hdlr = SensorHandler(dev_test = False)

#sql handler
sql_hdlr = SQLHandler('datalog.sqlite')
sql_hdlr.swipe_clean_database()
sql_hdlr.create_database()

#cloud handler
cloud_hdlr = CloudHandler()
cloud_hdlr.connect()

def do_things():
	#collecting data from sensor
	sensor_data = sensor_hdlr.request_power()

	#asigning new values to dict
	data_dict['timestamp_data'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	data_dict['active_powerA'] = sensor_data['getPowerA']
	data_dict['active_powerB'] = sensor_data['getPowerB']
	data_dict['active_powerC'] = sensor_data['getPowerC']
	data_dict['active_powerT'] = sensor_data['getPowerT']
	data_dict['reactive_powerA'] = sensor_data['getQPowerA']
	data_dict['reactive_powerB'] = sensor_data['getQPowerB']
	data_dict['reactive_powerC'] = sensor_data['getQPowerC']
	data_dict['reactive_powerT'] = sensor_data['getQPowerT']

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
