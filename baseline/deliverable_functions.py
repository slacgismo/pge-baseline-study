import numpy as np
import global_vars
import mysql.connector
import pandas as pd 
import sqlalchemy
import os.path
from datetime import datetime
from copy import deepcopy
import time

# Gets the errors calculated for the specified SAID
# inputs: SAID (string), program (string)
# outputs: error_df (pandas dataframe containing error data)
def getCalculatedErrors(SAID,program):
	cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
															  host=global_vars.DATABASE_IP_RO,
															  database=global_vars.DATABASE_NAME)
	
	# print("special query")
	# tic = time.time()

	# query = "SELECT * FROM ERROR15DR where SAID IN ('55985','284590808','284751452','284758046','2942754414','2942754078','2957386406','2957520806','2956641175','2972272301','3841292747','3029232424','3249931115','6551936842','3029296617','3029296803','7168027907','3841340002','3250067502','3029304902');"

	# error_df = pd.read_sql_query(query,cnx)

	# print("error_df shape", error_df.shape)

	# error_df['Date'] =  pd.to_datetime(error_df['Date'])

	# toc = time.time()

	# print("Getting all data from databases took", toc-tic)

	if (program == 'AMP') | (program == 'BIP') | (program == 'CBP') | (program == 'PDP') | (program == 'NONRES') | (program == 'QUICK_NONRES') | (program == 'NONRES_WEEKDAY') | (program == 'NONRES_WEEKEND') | (program == 'NONRES_WEEKDAY_15_HOT') | (program == 'NONRES_WEEKEND_15_HOT'):
		query = "SELECT * FROM ERROR15DR WHERE SAID = '%s' LIMIT 731" %(SAID)

	elif (program == 'SmartAC') | (program == 'SmartRate') | (program == 'RES') | (program == 'QUICK_RES') | (program == 'RES_WEEKDAY') | (program == 'RES_WEEKEND') | (program == 'RES_WEEKDAY_15_HOT') | (program == 'RES_WEEKEND_15_HOT'):
		query = "SELECT * FROM ERROR60DR WHERE SAID = '%s' LIMIT 731" %(SAID)

	error_df = pd.read_sql_query(query,cnx)
	error_df['Date'] =  pd.to_datetime(error_df['Date'])

	return error_df

# Gets the program, NAICS, and location for a given SAID
# inputs: SAID (string)
# outputs: return_data (tuple of strings)
def getInformation(SAID):
	
	cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
															  host=global_vars.DATABASE_IP_RO,
															  database=global_vars.DATABASE_NAME)

	cursor = cnx.cursor()
	query = "SELECT * FROM DR_CUST_CHARACTERISTICS WHERE sa_id = '%s' LIMIT 1" %(SAID)
	cursor.execute(query)

	for row in cursor:

		# get program
		if(row[4] == '1.0'):
			program = 'AMP'
		elif(row[5] == '1.0'):
			program = 'BIP'
		elif(row[6] == '1.0'):
			program = 'CBP'
		elif(row[7] == '1.0'):
			program = 'PDP'
		elif(row[8] == '1.0'):
			program = 'SmartAC'	
		elif(row[9] == '1.0'):
			program = 'SmartRate'
		else:
			program = 'No Program Given'

		NAICS = row[12]

		weather = (row[21],row[22])

		return_data = (program, NAICS, weather)
		return return_data

# If 10% or more of the rows of error_df contain NA, returns 'true'
def verify_error_df(error_df):

	skew_row_limit = int(error_df.shape[0]/10)

	if (skew_row_limit == 0):
		skew_row_limit = 1

	print("skew row limit", skew_row_limit)

	NA_counting_df = error_df[error_df['TenTenNoMAPE']=='NA']

	print("Rows with NA", NA_counting_df.shape)
	if NA_counting_df.shape[0] >= skew_row_limit: 
		return True

	MPE_columns = ['TenTenNoMPE', 'TenTenAdMPE', 'ThreeTenNoMPE', 'ThreeTenAdMPE', 'FourNintyAdMPE', 'TF-FTAdMPE', 'FF-TTAdMPE']

	try:

		for column in MPE_columns:
			MPE_df = error_df[(error_df[column] != 'NA') & (error_df[column] != 'nan')]
			# print(MPE_df[column])
			MPE_df[column] = MPE_df[column].astype(float)
			# df_raw['PricePerSeat_Outdoor'] = pd.to_numeric(df_raw['PricePerSeat_Outdoor'], errors='coerce')
			MPE_counting_df = MPE_df[(MPE_df[column]<= (-2000)) | (MPE_df[column]>2000)]
			if MPE_counting_df.shape[0] > skew_row_limit: 
				print(MPE_df[column])
				print("MPE high rows",MPE_counting_df.shape[0],"skipping")
				return True

		MAPE_columns = ['TenTenNoMAPE', 'TenTenAdMAPE', 'ThreeTenNoMAPE', 'ThreeTenAdMAPE', 'FourNintyAdMAPE', 'TF-FTAdMAPE', 'FF-TTAdMAPE']

		for column in MAPE_columns:
			MAPE_df = error_df[(error_df[column] != 'NA') & (error_df[column] != 'nan')]
			MAPE_df[column] = MPE_df[column].astype(float)
			MAPE_counting_df = MAPE_df[(MAPE_df[column]<= (-2000)) | (MAPE_df[column]>2000)]
			if MAPE_counting_df.shape[0] > skew_row_limit: 
				print(MAPE_df[column])
				print("MAPE high rows",MAPE_counting_df.shape[0],"skipping")
				return True
	except:

		print("MPE verification failed")
		return False

	return False

# calculates the average for each column of error_df, decrementing each column's counter if it needs to be skipped
# inputs: error_df (pandas dataframe), counter (list)
# outputs: columnAverageList (list), counter (list)
def calcColumnAverage(error_df, counter):

	counterBackup = deepcopy(counter)
	columnAverageList = []

	count = 0
	for item in range(7,error_df.shape[1]-1):
		
		error_vals = error_df.iloc[:,item].values
		error_rates = []
		for rate in error_vals:
			try:
				if rate == 'NA':
					continue
				rate = float(rate)
				error_rates.append(rate)
			except: 

				# print(rate)
				continue

		# print("error_rates",error_rates)
			
		column_average = np.mean(error_rates)
		# print("column_average",column_average)
		if np.isnan(column_average):
			# print('nan')
			counter[count] = counter[count] - 1
			column_average = 0.0

		columnAverageList.append(column_average)

		count = count + 1

	# print("columnAverageList",columnAverageList)

	if (columnAverageList[0] == 0.0) | (columnAverageList[2] > 4.0):
		columnAverageList = np.zeros(186)
		return(columnAverageList, counterBackup)

	# print(columnAverageList)
	return(columnAverageList, counter)
	# print("column average list", columnAverageList, "length", len(columnAverageList))

# Spring
mar21_2016 = pd.Timestamp(2016, 3, 21)
# print(mar21_2016)
# Summer
jun21_2016 = pd.Timestamp(2016, 6, 21)
# print(jun21_2016)
# Fall
sep23_2016 = pd.Timestamp(2016, 9, 23)
# print(sep23_2016)
# Winter
dec21_2016 = pd.Timestamp(2016, 12, 21)
# print(dec21_2016)
# Spring
mar21_2017 = pd.Timestamp(2017, 3, 21)
# print(mar21_2017)
# Summer
jun21_2017 = pd.Timestamp(2017, 6, 21)
# print(jun21_2017)
# Fall
sep23_2017 = pd.Timestamp(2017, 9, 23)
# print(sep23_2017)
# Winter
dec21_2017 = pd.Timestamp(2017, 12, 21)
# print(dec21_2017)

# Splits up error_df into four different seasonal dataframes
def getSeasonalErrors(error_df):

	spring_start_2016 = mar21_2016 < error_df['Date']
	spring_end_2016 = error_df['Date'] < jun21_2016
	spring_start_2017 = mar21_2017 < error_df['Date']	
	spring_end_2017 = error_df['Date'] < jun21_2017

	spring_df = error_df[(spring_start_2016 & spring_end_2016) | (spring_start_2017 & spring_end_2017)]

	summer_start_2016 = jun21_2016 < error_df['Date']
	summer_end_2016 = error_df['Date'] < sep23_2016
	summer_start_2017 = jun21_2017 < error_df['Date']	
	summer_end_2017 = error_df['Date'] < sep23_2017

	summer_df = error_df[(summer_start_2016 & summer_end_2016) | (summer_start_2017 & summer_end_2017)]

	fall_start_2016 = sep23_2016 < error_df['Date']
	fall_end_2016 = error_df['Date'] < dec21_2016
	fall_start_2017 = sep23_2017 < error_df['Date']	
	fall_end_2017 = error_df['Date'] < dec21_2017

	fall_df = error_df[(fall_start_2016 & fall_end_2016) | (fall_start_2017 & fall_end_2017)]

	winter_end_2016 = error_df['Date'] < mar21_2016
	winter_start_2016 = dec21_2016 < error_df['Date']	
	winter_end_2017 = error_df['Date'] < mar21_2017
	winter_start_2017 = dec21_2017 < error_df['Date']

	winter_df = error_df[(winter_end_2016) | (winter_start_2016 & winter_end_2017) | (winter_start_2017)]

	return spring_df, summer_df, fall_df, winter_df

