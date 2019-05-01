import datetime
import pandas as pd
import sys

def init():
	global DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_IP, DATABASE_IP_RO, DATABASE_NAME,INTERVALFLAG, PRINTFLAG, GRAPHFLAG, NEWTESTS, GRAPHSTART, GRAPHEND, SAID_LIMIT, SAID_OFFSET, storage_df_columns

	try:
		file = open("config.txt", "r")
	except:
		print("Error: config.txt file does not exist")
		sys.exit()

	sql_id = file.readlines() 

	DATABASE_USERNAME = sql_id[0].rstrip()
	DATABASE_PASSWORD = sql_id[1].rstrip()
	DATABASE_IP       = sql_id[2].rstrip()
	DATABASE_IP_RO    = sql_id[3].rstrip()	
	DATABASE_NAME     = sql_id[4].rstrip()

	INTERVALFLAG = 0
	# 0 = 15 minute intervals
	# 1 = 60 minute intervals
	# 2 = 15 minute intervals (NONDR)
	# 3 = 60 minute intervals (NONDR)
	# 4 = CAISE Baselines

	PRINTFLAG = 0
	# 0 = Print only amount of SAIDs completed
	# 1 = Print SAID name, program
	# 2 = Print individual dates and all error rates

	GRAPHFLAG = 0
	# 0 = No graph
	# 1 = All graphs for given time interval

	NEWTESTS = True
	# True = run more baselines
	# False = run original baselines

#######################

	# BERK - MBP
	SAID_LIMIT = 60000
	SAID_OFFSET = 0

	storage_df_columns = ['SAID', 'Program', 'NAICS', 'Date', 'DayType', 'MaxTemp', 'TenTenNoMPE', 'TenTenNoMAPE', 'TenTenNoCV', 'TenTenAdMPE', 'TenTenAdMAPE', 'TenTenAdCV', 'TenTenAd-50MPE', 'TenTenAd-50MAPE', 'TenTenAd-50CV', 'TenTenAd-40MPE', 'TenTenAd-40MAPE', 'TenTenAd-40CV', 'TenTenAd-30MPE', 'TenTenAd-30MAPE', 'TenTenAd-30CV', 'TenTenAd-20MPE', 'TenTenAd-20MAPE', 'TenTenAd-20CV', 'TenTenAd-10MPE', 'TenTenAd-10MAPE', 'TenTenAd-10CV', 'TenTenAd0MPE', 'TenTenAd0MAPE', 'TenTenAd0CV', 'TenTenAd10MPE', 'TenTenAd10MAPE', 'TenTenAd10CV', 'TenTenAd20MPE', 'TenTenAd20MAPE', 'TenTenAd20CV', 'TenTenAd30MPE', 'TenTenAd30MAPE', 'TenTenAd30CV', 'TenTenAd40MPE', 'TenTenAd40MAPE', 'TenTenAd40CV', 'TenTenAd50MPE', 'TenTenAd50MAPE', 'TenTenAd50CV', 
	'ThreeTenNoMPE', 'ThreeTenNoMAPE', 'ThreeTenNoCV', 'ThreeTenAdMPE', 'ThreeTenAdMAPE', 'ThreeTenAdCV', 'ThreeTenAd-50MPE', 'ThreeTenAd-50MAPE', 'ThreeTenAd-50CV', 'ThreeTenAd-40MPE', 'ThreeTenAd-40MAPE', 'ThreeTenAd-40CV', 'ThreeTenAd-30MPE', 'ThreeTenAd-30MAPE', 'ThreeTenAd-30CV', 'ThreeTenAd-20MPE', 'ThreeTenAd-20MAPE', 'ThreeTenAd-20CV', 'ThreeTenAd-10MPE', 'ThreeTenAd-10MAPE', 'ThreeTenAd-10CV', 'ThreeTenAd0MPE', 'ThreeTenAd0MAPE', 'ThreeTenAd0CV', 'ThreeTenAd10MPE', 'ThreeTenAd10MAPE', 'ThreeTenAd10CV', 'ThreeTenAd20MPE', 'ThreeTenAd20MAPE', 'ThreeTenAd20CV', 'ThreeTenAd30MPE', 'ThreeTenAd30MAPE', 'ThreeTenAd30CV', 'ThreeTenAd40MPE', 'ThreeTenAd40MAPE', 'ThreeTenAd40CV', 'ThreeTenAd50MPE', 'ThreeTenAd50MAPE', 'ThreeTenAd50CV', 
	'FiveTenNoMPE', 'FiveTenNoMAPE', 'FiveTenNoCV', 'FiveTenAdMPE', 'FiveTenAdMAPE', 'FiveTenAdCV', 'FiveTenAd-50MPE', 'FiveTenAd-50MAPE', 'FiveTenAd-50CV', 'FiveTenAd-40MPE', 'FiveTenAd-40MAPE', 'FiveTenAd-40CV', 'FiveTenAd-30MPE', 'FiveTenAd-30MAPE', 'FiveTenAd-30CV', 'FiveTenAd-20MPE', 'FiveTenAd-20MAPE', 'FiveTenAd-20CV', 'FiveTenAd-10MPE', 'FiveTenAd-10MAPE', 'FiveTenAd-10CV', 'FiveTenAd0MPE', 'FiveTenAd0MAPE', 'FiveTenAd0CV', 'FiveTenAd10MPE', 'FiveTenAd10MAPE', 'FiveTenAd10CV', 'FiveTenAd20MPE', 'FiveTenAd20MAPE', 'FiveTenAd20CV', 'FiveTenAd30MPE', 'FiveTenAd30MAPE', 'FiveTenAd30CV', 'FiveTenAd40MPE', 'FiveTenAd40MAPE', 'FiveTenAd40CV', 'FiveTenAd50MPE', 'FiveTenAd50MAPE', 'FiveTenAd50CV', 
	'FourNintyAdMPE', 'FourNintyAdMAPE', 'FourNintyAdCV', 'FourNintyAd-50MPE', 'FourNintyAd-50MAPE', 'FourNintyAd-50CV', 'FourNintyAd-40MPE', 'FourNintyAd-40MAPE', 'FourNintyAd-40CV', 'FourNintyAd-30MPE', 'FourNintyAd-30MAPE', 'FourNintyAd-30CV', 'FourNintyAd-20MPE', 'FourNintyAd-20MAPE', 'FourNintyAd-20CV', 'FourNintyAd-10MPE', 'FourNintyAd-10MAPE', 'FourNintyAd-10CV', 'FourNintyAd0MPE', 'FourNintyAd0MAPE', 'FourNintyAd0CV', 'FourNintyAd10MPE', 'FourNintyAd10MAPE', 'FourNintyAd10CV', 'FourNintyAd20MPE', 'FourNintyAd20MAPE', 'FourNintyAd20CV', 'FourNintyAd30MPE', 'FourNintyAd30MAPE', 'FourNintyAd30CV', 'FourNintyAd40MPE', 'FourNintyAd40MAPE', 'FourNintyAd40CV', 'FourNintyAd50MPE', 'FourNintyAd50MAPE', 'FourNintyAd50CV', 'TF-FTAdMPE', 'TF-FTAdMAPE', 'TF-FTAdCV', 'TF-FTAd-50MPE', 'TF-FTAd-50MAPE', 'TF-FTAd-50CV', 'TF-FTAd-40MPE', 'TF-FTAd-40MAPE', 'TF-FTAd-40CV', 'TF-FTAd-30MPE', 'TF-FTAd-30MAPE', 'TF-FTAd-30CV', 'TF-FTAd-20MPE', 'TF-FTAd-20MAPE', 'TF-FTAd-20CV', 'TF-FTAd-10MPE', 'TF-FTAd-10MAPE', 'TF-FTAd-10CV', 'TF-FTAd0MPE', 'TF-FTAd0MAPE', 'TF-FTAd0CV', 'TF-FTAd10MPE', 'TF-FTAd10MAPE', 'TF-FTAd10CV', 'TF-FTAd20MPE', 'TF-FTAd20MAPE', 'TF-FTAd20CV', 'TF-FTAd30MPE', 'TF-FTAd30MAPE', 'TF-FTAd30CV', 'TF-FTAd40MPE', 'TF-FTAd40MAPE', 'TF-FTAd40CV', 'TF-FTAd50MPE', 'TF-FTAd50MAPE', 'TF-FTAd50CV', 'FF-TTAdMPE', 'FF-TTAdMAPE', 'FF-TTAdCV', 'FF-TTAd-50MPE', 'FF-TTAd-50MAPE', 'FF-TTAd-50CV', 'FF-TTAd-40MPE', 'FF-TTAd-40MAPE', 'FF-TTAd-40CV', 'FF-TTAd-30MPE', 'FF-TTAd-30MAPE', 'FF-TTAd-30CV', 'FF-TTAd-20MPE', 'FF-TTAd-20MAPE', 'FF-TTAd-20CV', 'FF-TTAd-10MPE', 'FF-TTAd-10MAPE', 'FF-TTAd-10CV', 'FF-TTAd0MPE', 'FF-TTAd0MAPE', 'FF-TTAd0CV', 'FF-TTAd10MPE', 'FF-TTAd10MAPE', 'FF-TTAd10CV', 'FF-TTAd20MPE', 'FF-TTAd20MAPE', 'FF-TTAd20CV', 'FF-TTAd30MPE', 'FF-TTAd30MAPE', 'FF-TTAd30CV', 'FF-TTAd40MPE', 'FF-TTAd40MAPE', 'FF-TTAd40CV', 'FF-TTAd50MPE', 'FF-TTAd50MAPE', 'FF-TTAd50CV', 'DateModified']


	# 15 MIN

	# BENNET - SC1
	# SAID_LIMIT = 30000
	# SAID_OFFSET = 60000

	# MARK - VM
	# SAID_LIMIT = 30000
	# SAID_OFFSET = 140000 

	# MAYANK - DT2
	# SAID_LIMIT = 30000
	# SAID_OFFSET = 210000

	# SILA - DT3
	# SAID_LIMIT = 30000
	# SAID_OFFSET = 290000

#######################

	# 60 MIN

	# ALYONA - MBP
	# SAID_LIMIT = 50000
	# SAID_OFFSET = 0 

	# SUPRIYA - SC2
	# SAID_LIMIT = 30000
	# SAID_OFFSET = 300000
	
	# DAVE - DT1
	# SAID_LIMIT = 50000
	# SAID_OFFSET = 200000

	# DERIN - IMAC
	# SAID_LIMIT = 50000
	# SAID_OFFSET = 100000

	jun10_2017 = pd.to_datetime(20170610, format='%Y%m%d', errors='ignore').date()
	jun20_2017 = pd.to_datetime(20170620, format='%Y%m%d', errors='ignore').date()


	jul10_2017 = pd.to_datetime(20170710, format='%Y%m%d', errors='ignore').date()
	jul20_2017 = pd.to_datetime(20170720, format='%Y%m%d', errors='ignore').date()

	aug05_2017 = pd.to_datetime(20170805, format='%Y%m%d', errors='ignore').date()
	aug11_2017 = pd.to_datetime(20170811, format='%Y%m%d', errors='ignore').date()

	jan01_2017 = pd.to_datetime(20170101, format='%Y%m%d', errors='ignore').date()
	dec31_2017 = pd.to_datetime(20171231, format='%Y%m%d', errors='ignore').date()


	GRAPHSTART = jun10_2017
	GRAPHEND = jun20_2017
