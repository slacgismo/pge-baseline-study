import global_vars
import mysql.connector
import pandas as pd 
import sqlalchemy
from datetime import datetime

# getInfo(SAID)
# get program, NAICS code and weather station identifiers of SAID from a SQL table
#	SAID, string, contains 10 digit SAID
# output
#	return_data, triple, for SAID (program, NAICS, weather identifier)
def getInfo(SAID):
	
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

		if(global_vars.PRINTFLAG >= 1):
			print("Program is", program)

		NAICS = row[12]

		if(global_vars.PRINTFLAG >= 1):
			print("NAICS is", NAICS)

		weather = (row[21],row[22])

		if(global_vars.PRINTFLAG >= 1):
			print("Weather identifiers are", weather) 

		return_data = (program, NAICS, weather)
		return return_data

# getDR(SAID, interval)
# This function takes an SAID and returns all DR events related to that SAID
# input
#	SAID, string, contains 10 digit SAID
#	program, string, which program it is part of
# output
#	DRdays, list, contains list of DR event dates in datetime form
def getDR(SAID, program):

	if(program == 'AMP') | (program == 'BIP') | (program == 'CBP') | (program == 'PDP'):
		#get Agg_ID and Location based on SAID from first sheet
		excel_file='DR2564_SLAC_20180216_AggregatorData.xlsx'
		df = pd.read_excel(io=excel_file, sheet_name='AggNominations')

		SAID = int(SAID)

		try:
			a = df.loc[df['SA_ID'] == SAID]

			name =  a.iat[0, 1]
			location = a.iat[0, 9]

		except:
			if(global_vars.PRINTFLAG >= 2):
				print("No DR days found")
			return []

		try:
			#get Date of event based on SA_ID
			excel_file='DR2564_SLAC_20180216_AggregatorData.xlsx'
			df = pd.read_excel(io=excel_file, sheet_name='AggEvents')
			a = df.loc[(df['LOCATION'] == location) & (df['AGGREGATOR_ID'] == name)]

			#if DR hours wanted, can be done here

			DRdays = a['EVENT_DATE'].tolist() 

			# print("b",DRdays,type(DRdays[0]))

			if(global_vars.PRINTFLAG >= 2):
				print(DRdays)
		except:
			#get Date of event based on SA_ID
			excel_file='DR2564_SLAC_20180216_AggregatorData.xlsx'
			df = pd.read_excel(io=excel_file, sheetname='AggEvents')
			a = df.loc[(df['LOCATION'] == location) & (df['AGGREGATOR_ID'] == name)]

			#if DR hours wanted, can be done here

			DRdays = a['EVENT_DATE'].tolist() 

			# print("b",DRdays,type(DRdays[0]))

			if(global_vars.PRINTFLAG >= 2):
				print(DRdays)

	elif (program == 'SmartAC'):

		DRdays = []
		
		# Connect to table that connects SAIDs
		cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
																  host=global_vars.DATABASE_IP_RO,
																  database=global_vars.DATABASE_NAME)
		# Get 2017
		query = "SELECT EventDt FROM SMARTAC_DR_2017 Where SAID = %s;" %str(SAID)
		# print(query)

		DR_df = pd.read_sql_query(query, cnx)

		# print(DR_df)

		DR_2017 = DR_df['EventDt'].tolist()

		# print(DR_2017)

		for day in DR_2017:
			dt = datetime.strptime(day, '%d-%b-%y')
			DRdays.append(dt)

		# DRdays = [datetime.striptime(date,"'%d-%m-%Y'").date() for date in DR_2017]
		# print("DRdays",DRdays)

		# Get 2016
		query = "SELECT * FROM SMARTAC_DR_2016_CUST WHERE SAID = %s;" %str(SAID).zfill(10)

		SAID_df = pd.read_sql_query(query, cnx)

		try:
			Group = SAID_df["Group"].tolist()
		except:
			Group = "no group"

		if len(SAID_df["Group"].iloc[0]) != 1:
			Group = list(Group[0])

		if ("1" or "2" or "3" or "6" or "9") in Group:
			DRdays.append(pd.to_datetime(20160714, format='%Y%m%d', errors='ignore'))

		if ("2" or "3") in Group:
			DRdays.append(pd.to_datetime(20160725, format='%Y%m%d', errors='ignore'))

		if ("1" or "2" or "3") in Group:
			DRdays.append(pd.to_datetime(20160727, format='%Y%m%d', errors='ignore'))

		if ("4" or "5" or "7") in Group:
			DRdays.append(pd.to_datetime(20160728, format='%Y%m%d', errors='ignore'))

		if ('6' or '7' or '8') in Group:
			DRdays.append(pd.to_datetime(20160729, format='%Y%m%d', errors='ignore'))

		if ("2" or "3") in Group:
			DRdays.append(pd.to_datetime(20160907, format='%Y%m%d', errors='ignore'))

		if ("0" or "1" or "2" or "3" or "4" or "9") in Group:
			DRdays.append(pd.to_datetime(20160627, format='%Y%m%d', errors='ignore'))

		if ("5" or "0" or "1" or "2" or "3" or "6") in Group:
			DRdays.append(pd.to_datetime(20160919, format='%Y%m%d', errors='ignore'))


		try:
			Sublap = SAID_df["SublapID"].tolist()[0][5:9]
		except:
			Sublap = "no sublap id"

		if Sublap == "PGNV":
			DRdays.append(pd.to_datetime(20160815, format='%Y%m%d', errors='ignore'))

		if Sublap == ("PGNC" or "PGSA"):
			DRdays.append(pd.to_datetime(20160816, format='%Y%m%d', errors='ignore'))

		if Sublap == ("PGEB" or "PGSI"):
			DRdays.append(pd.to_datetime(20160817, format='%Y%m%d', errors='ignore'))

		if Sublap == ("PGLP" or "PGF1"):
			DRdays.append(pd.to_datetime(20160620, format='%Y%m%d', errors='ignore'))

		if Sublap == ("PGF1" or "PGLP" or "PGNV" or "PGSA" or "PGSI" or "PGST"):
			DRdays.append(pd.to_datetime(20160628, format='%Y%m%d', errors='ignore'))

		if Sublap != ("PGCC" or "PGSF" or "PGHB" or "PGSN"):
			DRdays.append(pd.to_datetime(20160926, format='%Y%m%d', errors='ignore'))

		print("DRdays", DRdays)

		return DRdays

	elif (program == 'SmartRate'):
		try:
			excel_file='DR2564_SLAC_20180216_AggregatorData.xlsx'
			df = pd.read_excel(open(excel_file, 'rb'), sheet_name="AllDREvents")

			a = df.loc[df['Program'] == 'SmartRate']
			a_days = list(a.ix[:,'EventDate'])
			
			b = df.loc[df['Program'] == 'SmartRate ']
			b_days = list(b.ix[:,'EventDate'])
			
			DRdays = a_days+b_days
			print("_", DRdays)

		except:
			excel_file='DR2564_SLAC_20180216_AggregatorData.xlsx'
			df = pd.read_excel(open(excel_file, 'rb'), sheetname="AllDREvents")

			a = df.loc[df['Program'] == 'SmartRate']
			a_days = list(a.ix[:,'EventDate'])
			
			b = df.loc[df['Program'] == 'SmartRate ']
			b_days = list(b.ix[:,'EventDate'])
			
			DRdays = a_days+b_days
			print(DRdays)

		return DRdays			

	else:
		if(global_vars.PRINTFLAG >= 2):
			print("No DR days found")
		return []
	return DRdays

# getIntervalData(SAID, interval)
# gets all interval data for SAID from an SQL table
# input
#	SAID, string, contains 10 digit SAID
#	interval, int, 15 or 60, data collection interval used to find correct sql table
# output
#	interval_df, pandas.Dataframe, contains all interval data relevant to SAID
def getIntervalData(SAID, interval):
	cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
															  host=global_vars.DATABASE_IP_RO,
															  database=global_vars.DATABASE_NAME)
	
	if interval == 15:

		query = "SELECT * FROM MIN15 WHERE SA = '%s' LIMIT 731" %(SAID)
		interval_df = pd.read_sql_query(query,cnx)

	elif interval == 60:

		query = "SELECT * FROM MIN60 WHERE SA = '%s' LIMIT 731" %(SAID)
		interval_df = pd.read_sql_query(query,cnx)

	interval_df['DATE'] =  pd.to_datetime(interval_df['DATE'])

	return interval_df

# getTemp(weather)
# gets weather from sql table based on location
# input
#	weather, tuple, contains (wea_stn_cd, wea_stn_nm)
# output
#	temp_df, pandas.Dataframe, contains all temperature data for weather location
def getTemp(weather):

	cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
															  host=global_vars.DATABASE_IP_RO,
															  database=global_vars.DATABASE_NAME)
	query = "SELECT * FROM WEATHER_copy WHERE wea_stn_cd = '%s' AND wea_stn_nm = '%s'" %(weather[0],weather[1])
	temp_df = pd.read_sql_query(query,cnx)
	temp_df['wea_dttm'] =  pd.to_datetime(temp_df['wea_dttm'])

	return temp_df

# store(said_all_data, interval)
# stores data related to a SAID to related SQL table
# input
#	said_df, df, error data for 1 said for all available dates
#	interval, 15 or 60 based on customer
def store(said_df, interval):
	
	# cnx = mysql.connector.connect(user='pge', password='egpslac123',
	# 							  host='pgebaseline-cluster-identifier.cluster-ro-cpyvkv2lasim.us-west-1.rds.amazonaws.com',
	# 							  database='pgebaselinedb')
	said_df.columns = ['SAID', 'Program', 'NAICS', 'Date', 'DayType', 'MaxTemp', 'TenTenNoMPE', 'TenTenNoMAPE', 'TenTenNoCV', 'TenTenAdMPE', 'TenTenAdMAPE', 'TenTenAdCV', 'TenTenAd-50MPE', 'TenTenAd-50MAPE', 'TenTenAd-50CV', 'TenTenAd-40MPE', 'TenTenAd-40MAPE', 'TenTenAd-40CV', 'TenTenAd-30MPE', 'TenTenAd-30MAPE', 'TenTenAd-30CV', 'TenTenAd-20MPE', 'TenTenAd-20MAPE', 'TenTenAd-20CV', 'TenTenAd-10MPE', 'TenTenAd-10MAPE', 'TenTenAd-10CV', 'TenTenAd0MPE', 'TenTenAd0MAPE', 'TenTenAd0CV', 'TenTenAd10MPE', 'TenTenAd10MAPE', 'TenTenAd10CV', 'TenTenAd20MPE', 'TenTenAd20MAPE', 'TenTenAd20CV', 'TenTenAd30MPE', 'TenTenAd30MAPE', 'TenTenAd30CV', 'TenTenAd40MPE', 'TenTenAd40MAPE', 'TenTenAd40CV', 'TenTenAd50MPE', 'TenTenAd50MAPE', 'TenTenAd50CV', 'ThreeTenNoMPE', 'ThreeTenNoMAPE', 'ThreeTenNoCV', 'ThreeTenAdMPE', 'ThreeTenAdMAPE', 'ThreeTenAdCV', 'ThreeTenAd-50MPE', 'ThreeTenAd-50MAPE', 'ThreeTenAd-50CV', 'ThreeTenAd-40MPE', 'ThreeTenAd-40MAPE', 'ThreeTenAd-40CV', 'ThreeTenAd-30MPE', 'ThreeTenAd-30MAPE', 'ThreeTenAd-30CV', 'ThreeTenAd-20MPE', 'ThreeTenAd-20MAPE', 'ThreeTenAd-20CV', 'ThreeTenAd-10MPE', 'ThreeTenAd-10MAPE', 'ThreeTenAd-10CV', 'ThreeTenAd0MPE', 'ThreeTenAd0MAPE', 'ThreeTenAd0CV', 'ThreeTenAd10MPE', 'ThreeTenAd10MAPE', 'ThreeTenAd10CV', 'ThreeTenAd20MPE', 'ThreeTenAd20MAPE', 'ThreeTenAd20CV', 'ThreeTenAd30MPE', 'ThreeTenAd30MAPE', 'ThreeTenAd30CV', 'ThreeTenAd40MPE', 'ThreeTenAd40MAPE', 'ThreeTenAd40CV', 'ThreeTenAd50MPE', 'ThreeTenAd50MAPE', 'ThreeTenAd50CV', 'FourNintyAdMPE', 'FourNintyAdMAPE', 'FourNintyAdCV', 'FourNintyAd-50MPE', 'FourNintyAd-50MAPE', 'FourNintyAd-50CV', 'FourNintyAd-40MPE', 'FourNintyAd-40MAPE', 'FourNintyAd-40CV', 'FourNintyAd-30MPE', 'FourNintyAd-30MAPE', 'FourNintyAd-30CV', 'FourNintyAd-20MPE', 'FourNintyAd-20MAPE', 'FourNintyAd-20CV', 'FourNintyAd-10MPE', 'FourNintyAd-10MAPE', 'FourNintyAd-10CV', 'FourNintyAd0MPE', 'FourNintyAd0MAPE', 'FourNintyAd0CV', 'FourNintyAd10MPE', 'FourNintyAd10MAPE', 'FourNintyAd10CV', 'FourNintyAd20MPE', 'FourNintyAd20MAPE', 'FourNintyAd20CV', 'FourNintyAd30MPE', 'FourNintyAd30MAPE', 'FourNintyAd30CV', 'FourNintyAd40MPE', 'FourNintyAd40MAPE', 'FourNintyAd40CV', 'FourNintyAd50MPE', 'FourNintyAd50MAPE', 'FourNintyAd50CV', 'TF-FTAdMPE', 'TF-FTAdMAPE', 'TF-FTAdCV', 'TF-FTAd-50MPE', 'TF-FTAd-50MAPE', 'TF-FTAd-50CV', 'TF-FTAd-40MPE', 'TF-FTAd-40MAPE', 'TF-FTAd-40CV', 'TF-FTAd-30MPE', 'TF-FTAd-30MAPE', 'TF-FTAd-30CV', 'TF-FTAd-20MPE', 'TF-FTAd-20MAPE', 'TF-FTAd-20CV', 'TF-FTAd-10MPE', 'TF-FTAd-10MAPE', 'TF-FTAd-10CV', 'TF-FTAd0MPE', 'TF-FTAd0MAPE', 'TF-FTAd0CV', 'TF-FTAd10MPE', 'TF-FTAd10MAPE', 'TF-FTAd10CV', 'TF-FTAd20MPE', 'TF-FTAd20MAPE', 'TF-FTAd20CV', 'TF-FTAd30MPE', 'TF-FTAd30MAPE', 'TF-FTAd30CV', 'TF-FTAd40MPE', 'TF-FTAd40MAPE', 'TF-FTAd40CV', 'TF-FTAd50MPE', 'TF-FTAd50MAPE', 'TF-FTAd50CV', 'FF-TTAdMPE', 'FF-TTAdMAPE', 'FF-TTAdCV', 'FF-TTAd-50MPE', 'FF-TTAd-50MAPE', 'FF-TTAd-50CV', 'FF-TTAd-40MPE', 'FF-TTAd-40MAPE', 'FF-TTAd-40CV', 'FF-TTAd-30MPE', 'FF-TTAd-30MAPE', 'FF-TTAd-30CV', 'FF-TTAd-20MPE', 'FF-TTAd-20MAPE', 'FF-TTAd-20CV', 'FF-TTAd-10MPE', 'FF-TTAd-10MAPE', 'FF-TTAd-10CV', 'FF-TTAd0MPE', 'FF-TTAd0MAPE', 'FF-TTAd0CV', 'FF-TTAd10MPE', 'FF-TTAd10MAPE', 'FF-TTAd10CV', 'FF-TTAd20MPE', 'FF-TTAd20MAPE', 'FF-TTAd20CV', 'FF-TTAd30MPE', 'FF-TTAd30MAPE', 'FF-TTAd30CV', 'FF-TTAd40MPE', 'FF-TTAd40MAPE', 'FF-TTAd40CV', 'FF-TTAd50MPE', 'FF-TTAd50MAPE', 'FF-TTAd50CV', 'DateModified']

	database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
												   format(global_vars.DATABASE_USERNAME, global_vars.DATABASE_PASSWORD, 
														  global_vars.DATABASE_IP, global_vars.DATABASE_NAME))
	if global_vars.INTERVALFLAG == 0:
		said_df.to_sql(con=database_connection, name='ERROR15DR', if_exists='append')#, index='False')
	else:
		said_df.to_sql(con=database_connection, name='ERROR60DR', if_exists='append')#, index='False')

	# if interval == 15:
	# 	said_df.to_sql(name='ERROR15_DR',con=con,if_exists='append')

	# con.close()
	# if interval == 15:
	# 	said_df.to_sql(name = 'ERROR15_DR', if_exists = 'append', con = cnx)

# getCompletedSaids()
# get all completed SAIDs
# output
#	SAIDs_done, list, all SAIDs that have been completed
def getCompletedSaids():
	cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
															  host=global_vars.DATABASE_IP_RO,
															  database=global_vars.DATABASE_NAME)

	if global_vars.INTERVALFLAG == 0:
		query = "SELECT DISTINCT(SAID) FROM ERROR15DR;"
	else:
		query = "SELECT DISTINCT(SAID) FROM ERROR60DR;"

		
	SAIDs_done = (said_df.values.T.tolist())[0]
	SAIDs_done = [str(int(n)).zfill(10) for n in SAIDs_done]

	return SAIDs_done

# update_said_table(SAID, completion)
# add weather an SAID has been completed to SAID_TABLE
# input
#	SAID, string, SAID of customer
#	completion, bool, true if fully complete, false if error found
def update_said_table(SAID, completion):

	cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
													  host=global_vars.DATABASE_IP,
													  database=global_vars.DATABASE_NAME)
	cursor2 = cnx.cursor()
	if global_vars.INTERVALFLAG == 0:
		if completion == True:
			query = """UPDATE SAID_TABLE_DR_15 SET CompletionStatus = 'T' WHERE SA = '%s' LIMIT 1;""" %SAID
		else:
			query = """UPDATE SAID_TABLE_DR_15 SET CompletionStatus = 'F' WHERE SA = '%s' LIMIT 1;""" %SAID
	else:
		if completion == True:
			query = """UPDATE SAID_TABLE_DR_60 SET CompletionStatus = 'T' WHERE SA = '%s' LIMIT 1;""" %SAID
		else:
			query = """UPDATE SAID_TABLE_DR_60 SET CompletionStatus = 'F' WHERE SA = '%s' LIMIT 1;""" %SAID

	cursor2.execute(query)

	cnx.commit()
	cnx.close()
