import sqlite3
# import pandas as pd

class SQLHandler:
	"""
	Class that communicates with sqlite database
	Able to write to database from a dict
	TODO : inteface with Pandas for easy extraction (?)
	"""
	ref_dict = {'timestamp_data':0.0,
			'active_powerA':0.0,
			'active_powerB':0.0,
			'active_powerC':0.0, 
			'active_powerT':0.0, 
			'reactive_powerA':0.0,
			'reactive_powerB':0.0,
			'reactive_powerC':0.0,
			'reactive_powerT':0.0
			}

	def __init__(self, filename):
		"""
		String filename of the database file (eg: 'datalog.sqlite')
		"""
		self.con = sqlite3.connect(filename)
		self.cur = self.con.cursor()

	def create_database(self, database = 'smart_meter'):
		"""
		function to create sql database
		! very hardcoded so far
		need to define more general way to specify columns (from a dict)
		"""
		sql = '''CREATE TABLE IF NOT EXISTS {} (
			timestamp_data    TEXT UNIQUE,
			active_powerA 	REAL,
		    active_powerB 	REAL,
		    active_powerC 	REAL,
		    active_powerT 	REAL,
		    reactive_powerA REAL,
		    reactive_powerB REAL,
		    reactive_powerC REAL,
		    reactive_powerT REAL);
		    '''.format(database)

		self.cur.execute(sql)
		self.con.commit()
		print("Database {} has been created from default setting".format(database))

	def create_db_from_dict(self, ref_dict, database = 'smart_meter'):
		"""
		Function t create a database from the keys of a dictionary 
		Made to make the code more general
		The shape of the database can then be directly chosen in the main script
		"""



		print("Database {} has been created from the dictionary".format(database))

	def swipe_clean_database(self, database = 'smart_meter'):
		"""
		function to delete existing database
		mainly for dev
		"""
		sql = 'DROP TABLE IF EXISTS {} ;'.format(database)
		self.cur.execute(sql)
		print("database has been deleted")

	def _insert_value(self, column, value = 0.0, database = 'smart_meter'):
		"""
		tool function used to insert a value in a particular column of the database
		"""
		sql =  'INSERT OR REPLACE INTO {}{} VALUES {}'.format(database, column, value)
		self.cur.execute(sql)
		self.con.commit()

	def insert_measurement(self, data_dict, database = 'smart_meter'):
		"""
		Function that only works with a precise type of dict, matching the data
		Stores a whole row into the database
		Returns a bool to know if input dict matched requirements or not
		"""
		if (data_dict.keys() == SQLHandler.ref_dict.keys()):
			columns = ()
			values = ()
			for key, value in data_dict.items():
				columns += (key,)
				values += (value,)
			self._insert_value(columns, values)
			return(True)
		else:
			return(False)

	# def show_database(self, database = 'smart_meter'):
		# df = pd.read_sql_query("SELECT * FROM {}".format(database), self.con)
		# print(df.head(10))


#function for tests
import random
def generate_measurements(sql_handler, n = 10):
	for i in range(n):
		a = random.randint(1, 2)
		b = random.randint(5, 15)
		dict0 = {'timestamp_data':i,
			'active_powerA':0.0,
			'active_powerB':a,
			'active_powerC':0.0, 
			'active_powerT':0.0, 
			'reactive_powerA':0.0,
			'reactive_powerB':b,
			'reactive_powerC':0.0,
			'reactive_powerT':0.0
			}
		sql_handler.insert_measurement(dict0)

##############
### SCRIPT ###
##############
print('SQLHandler imported')
# sql_handler = SQLHandler('datalog.sqlite')
# sql_handler.swipe_clean_database()
# sql_handler.create_database()

# generate_measurements(sql_handler, 10)

# import pandas as pd
# df = pd.read_sql_query("SELECT * FROM smart_meter", sql_handler.con)
# print(df.head(10))
