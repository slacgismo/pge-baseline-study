import time
import mysql.connector
import global_vars
import pandas as pd
import numpy as np
from random_data import *
import datetime
global_vars.init()

def checkCompletionStatus():

	check = True
	
	string_length = 18
	time_delay = 60*60

	completed15 = 0
	failed15 = 0
	completed60 = 0
	failed60 = 0

	while check == True:

		now = datetime.datetime.now()

		print(str(now)[:16])

		cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
	                                                                  host=global_vars.DATABASE_IP_RO,
	                                                                  database=global_vars.DATABASE_NAME)
		
		query = "SELECT * FROM SAID_TABLE_DR_15 WHERE CompletionStatus = 'T' LIMIT 100000"
	
		done_since_last15 = completed15

		completed15 = np.shape(pd.read_sql_query(query,cnx))[0]

		print("Complete DR NONRES".ljust(string_length), ":", completed15)

		query = "SELECT * FROM SAID_TABLE_DR_15 WHERE CompletionStatus = 'F' LIMIT 10000"
		
		done_since_last15 = done_since_last15 + failed15

		failed15 = np.shape(pd.read_sql_query(query,cnx))[0]

		print("Failed DR NONRES".ljust(string_length), ":", failed15)

		print("Total DR NONRES".ljust(string_length), ":", completed15+failed15)

		done_since_last15 = -(done_since_last15 - completed15 - failed15)

		for program in ['PDP','AMP','CBP']:

			query = "SELECT DISTINCT(SAID) FROM ERROR15DR WHERE Program = '%s'" %program
			program15 = np.shape(pd.read_sql_query(query,cnx))[0]

			print(str("Total "+ program).ljust(string_length), ":", program15)

		print("Total BIP".ljust(string_length), ":", len(get_bip_data()))

		# print("\n")

		query = "SELECT * FROM SAID_TABLE_DR_60 WHERE CompletionStatus = 'T' LIMIT 100000"
		
		done_since_last60 = completed60

		completed60 = np.shape(pd.read_sql_query(query,cnx))[0]

		print("Complete DR RES:".ljust(string_length), ":", completed60)

		query = "SELECT * FROM SAID_TABLE_DR_60 WHERE CompletionStatus = 'F' LIMIT 10000"
		
		done_since_last60 = done_since_last60 + failed60

		failed60 = np.shape(pd.read_sql_query(query,cnx))[0]
		
		print("Failed DR RES".ljust(string_length), ":", failed60)

		print("Total DR RES".ljust(string_length), ":", completed60+failed60)

		done_since_last60 = -(done_since_last60 - completed60 - failed60)

		for program in ['SmartRate','SmartAC']:

			query = "SELECT DISTINCT(SAID) FROM ERROR60DR WHERE Program = '%s'" %program
			program60 = np.shape(pd.read_sql_query(query,cnx))[0]

			print(str("Total "+ program).ljust(string_length), ":", program60)

		print(done_since_last15, "NONRES completed in last", time_delay/3600, "hours")
		print(done_since_last60, "RES completed in last", time_delay/3600, "hours")

		time.sleep(time_delay) # hourly
	
		print("\n")

checkCompletionStatus()
