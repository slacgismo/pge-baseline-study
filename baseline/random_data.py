import numpy as np

import global_vars
global_vars.init()

import mysql.connector
import pandas as pd 

import time

# Gets a list of random SAIDs
# inputs: program (string), seed (int, seed for random number generator), num (int, number of SAIDs wanted)
# outputs: random_saids (list of num random SAIDs)
def get_random_data(program, seed, num):
	cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
                                                                  host=global_vars.DATABASE_IP_RO,
                                                                  database=global_vars.DATABASE_NAME)
	if program == 'RES':
		query = "SELECT DISTINCT(SAID) FROM ERROR60DR"
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()

	elif program == 'NONRES':
		query = "SELECT DISTINCT(SAID) FROM ERROR15DR"
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()


	elif program == "SmartRate" or program == "SmartAC":
		query = "SELECT DISTINCT(SAID) FROM ERROR60DR WHERE Program = '%s'" %program
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()


	elif program == "AMP" or program == "CBP" or program == "PDP":
		query = "SELECT DISTINCT(SAID) FROM ERROR15DR WHERE Program = '%s'" %program
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()

	elif program == "BIP":
		saids = get_bip_data()

	elif program == "NONRES_WEEKDAY_15_HOT":
		query = "SELECT DISTINCT(SAID) FROM ERROR15DR LIMIT 50000"
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()

	elif program == "NONRES_WEEKEND_15_HOT":
		query = "SELECT DISTINCT(SAID) FROM ERROR15DR LIMIT 50000"
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()

	elif program == "RES_WEEKDAY_15_HOT":
		query = "SELECT DISTINCT(SAID) FROM ERROR60DR LIMIT 50000"
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()

	elif program == "RES_WEEKEND_15_HOT":
		query = "SELECT DISTINCT(SAID) FROM ERROR60DR LIMIT 50000"
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()

	elif program == "QUICK_RES":
		query = "SELECT DISTINCT(SAID) FROM ERROR60DR LIMIT 50000"
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()

	elif program == "RES_WEEKEND":
		query = "SELECT DISTINCT(SAID) FROM ERROR60DR LIMIT 50000"
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()

	elif program == "RES_WEEKDAY":
		query = "SELECT DISTINCT(SAID) FROM ERROR60DR LIMIT 50000"
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()

	elif program == "QUICK_NONRES":
		query = "SELECT DISTINCT(SAID) FROM ERROR15DR LIMIT 50000"
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()

	elif program == "NONRES_WEEKEND":
		query = "SELECT DISTINCT(SAID) FROM ERROR15DR LIMIT 50000"
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()

	elif program == "NONRES_WEEKDAY":
		query = "SELECT DISTINCT(SAID) FROM ERROR15DR LIMIT 50000"
		print(query)
		saids_df = pd.read_sql_query(query, cnx)
		saids = saids_df['SAID'].tolist()

	# else:
	# 	print("Invalid program name")

	print("Found", len(saids), "SAIDs for program", program)

	test = range(len(saids))

	np.random.seed(seed) ; random_indices = np.random.choice(test, size=num, replace=False)

	random_saids = [saids[i] for i in random_indices]

	# print(random_saids)

	return random_saids

# gets all the BIP SAIDs, some of which are also AMP SAIDs
def get_bip_data():
	cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
                                                              host=global_vars.DATABASE_IP_RO,
                                                              database=global_vars.DATABASE_NAME)
	cursor = cnx.cursor()


	query1 = "SELECT DISTINCT(sa_id) FROM DR_CUST_CHARACTERISTICS WHERE BIP = '1.0' AND AMP = '1.0';"

	said_list = pd.read_sql_query(query1, cnx)
	said_list = said_list['sa_id'].tolist()
	said_string = "', '".join(said_list)
	# print(str(said_list[2:-2]))

	query2 = "SELECT SA FROM SAID_TABLE_DR_15 Where SA IN ('%s') AND CompletionStatus = 'T';" %said_string

	# print(query2)
	saids = pd.read_sql_query(query2, cnx)
	saids = saids['SA'].tolist()
	
	query = "SELECT DISTINCT(SAID) FROM ERROR15DR WHERE Program = 'BIP';"
	
	print(query)

	bips_df = pd.read_sql_query(query, cnx)
	bips = bips_df['SAID'].tolist()

	all_bips = saids + bips

	return all_bips

	# print(saids)





