from data_get import *
from baseline_functions import *
from calendar_date import *

import global_vars
global_vars.init()
if global_vars.GRAPHFLAG > 0:
		from graph_functions import *
		from error_graphs import *

import mysql.connector
import pandas as pd 
import datetime

import time
# main()
# This function goes through each SAID in the SAID_TABLE sql table, retrieves its data and runs baselinining methods on them
def main():

		# Connect to table that connects SAIDs
		cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
																  host=global_vars.DATABASE_IP_RO,
																  database=global_vars.DATABASE_NAME)
		cursor = cnx.cursor()

		# return
		if global_vars.INTERVALFLAG == 0:
			query = "SELECT * FROM SAID_TABLE_DR_15 LIMIT %i OFFSET %i" %(global_vars.SAID_LIMIT, global_vars.SAID_OFFSET)
		elif global_vars.INTERVALFLAG == 1:
			query = "SELECT * FROM SAID_TABLE_DR_60 LIMIT %i OFFSET %i" %(global_vars.SAID_LIMIT, global_vars.SAID_OFFSET)
		elif global_vars.INTERVALFLAG == 2:
			query = "SELECT * FROM SAID_TABLE_NONDR_15 LIMIT %i OFFSET %i" %(global_vars.SAID_LIMIT, global_vars.SAID_OFFSET)
		elif global_vars.INTERVALFLAG == 3:
			query = "SELECT * FROM SAID_TABLE_NONDR_60 LIMIT %i OFFSET %i" %(global_vars.SAID_LIMIT, global_vars.SAID_OFFSET)
		
		cursor.execute(query)

		said_counter = 0

		tic = time.time()

		# Go through each SAID
		for row in cursor:
			SAID = str(row[0]).zfill(10)

			if(not global_vars.NEWTESTS):
				if (row[1] == 'T') | (row[1] == 'F'):
					if(global_vars.PRINTFLAG >= 1):
						print("SAID", SAID, "done with completion",row[1])
					continue
				
			if(global_vars.PRINTFLAG >= 1):
					print("SAID =", SAID)

			# Find program, NAICS and weather identifiers of SAID
			try:
					(program, NAICS, weather) = getInfo(SAID)
			except Exception as e:
					print(e)
					with open('log.txt', 'a+') as logfile:
						logfile.write("getInfo exception %s \n" %e )
					# if info not found skip

					if(not global_vars.NEWTESTS):
						update_said_table(SAID, False)
					continue 

			# Find interval data of SAID
			if (program == 'AMP') | (program == 'BIP') | (program == 'CBP') | (program == 'PDP'):
					interval = 15

			elif (program == 'SmartAC') | (program == 'SmartRate'):
					interval = 60
					if(global_vars.INTERVALFLAG == 0):
						continue


			if global_vars.INTERVALFLAG < 2:
				DR_tries = 0
				try:
					# Find DR days of SAID
					DRDays = getDR(SAID, program)
				except:
					flag = False
					with open('log.txt', 'a+') as logfile:
						logfile.write("Main error: DRDays\n")
					while DR_tries < 10 and flag == False:
						time.sleep(10-DR_tries)
						# Find DR days of SAID
						try:
							DRDays = getDR(SAID, program)
							print("DRDays",DRDays)
							flag = True
						except:
							DR_tries = DR_tries + 1

			temp_tries = 0
			try:
				# Find temperature for SAID
				temp_df = getTemp(weather)
				# print("temp_df",temp_df["wea_dttm"])
			except:
				flag = False
				with open('log.txt', 'a+') as logfile:
					logfile.write("Main error: getTemp\n")
				# Find temperature for SAID
				while temp_tries < 10 and flag == False:
					time.sleep(10-temp_tries)
					# Find temperature for SAID
					try:
						temp_df = getTemp(weather)
						flag = True
					except:
						temp_tries = temp_tries + 1

			interval_tries = 0
			try:
				# interval_df will contain all interval data for an SAID
				interval_df = getIntervalData(SAID, interval)
				# print("interval_df",interval_df.shape, list(interval_df))

			except:
				flag = False
				with open('log.txt', 'a+') as logfile:
					logfile.write("Main error: getIntervalData\n")
				while interval_tries < 10 and flag == False:
					time.sleep(10-interval_tries)
					# Find temperature for SAID
					try:
						interval_df = getIntervalData(SAID, interval)
						flag = True
					except:
						interval_tries = interval_tries + 1                

			if(global_vars.PRINTFLAG >= 1):
				print("interval data recieved with shape", interval_df.shape)

			# storage_list is used to have all relevant information for a single SAID in a single Date
			# storage_list = [SAID, program, NAICS, date, max_temp...]
			storage_list = [int(SAID), program, NAICS]

			# will contain all storage lists for 1 said, so approx 731 rows
			said_all_data = []

			try:
				if(global_vars.GRAPHFLAG >= 1):
					getBaselineGraphs(interval_df, DRDays, temp_df, interval)
					getErrorGraphs(interval_df, DRDays, temp_df, interval)
					print("graphs done")
					continue
			except:
				if(global_vars.GRAPHFLAG >= 1):
					print("error occured skipping to next SAID")
					continue

			# date is initialized to last day and will backtrack through every day
			date = (interval_df['DATE'].max()).date()

			if(global_vars.PRINTFLAG >= 2):
				print(date)

			while date.year > 2015:

				# row_data = runFrequentBaseline(interval_df, DRDays, temp_df, interval, date, storage_list)

				try:
					# if(not global_vars.NEWTESTS):
					# 	print(date)
					row_data = runBaseline(interval_df, DRDays, temp_df, interval, date, storage_list)
					# else:
					# 	row_data = runFrequentBaseline(interval_df, DRDays, temp_df, interval, date, storage_list)
				except Exception as e:
					with open('log.txt', 'a+') as logfile:
						logfile.write("runBaseline exception %s \n" %e )

				if row_data != 'NA':
						said_all_data.append(row_data)
				# baseline

				if(global_vars.PRINTFLAG >= 2):
						print(date)
				date = date - datetime.timedelta(days=1)

			if(global_vars.PRINTFLAG >= 1):
				print("SAID done")
				try:
						print("With",len(said_all_data),"days/rows")
						print("and",len(said_all_data[0]),"columns")
				except:
						print("With no data")
						if(not global_vars.NEWTESTS):
							update_said_table(SAID, False)
						continue

			said_df = pd.DataFrame(said_all_data)


			update_tries = 0
			try:
				if(not global_vars.NEWTESTS):
					update_said_table(SAID, True)
			except:
				flag = False
				with open('log.txt', 'a+') as logfile:
					logfile.write("Main-update_said_table error\n")
				while update_tries < 10 and flag == False:
					time.sleep(10-update_tries)
					try:
						if(not global_vars.NEWTESTS):
							update_said_table(SAID, True)
						flag = True
					except:
						update_tries = update_tries + 1

			if(not global_vars.NEWTESTS):
				store_tries = 0
				try:
					store(said_df, interval)
				except:
					flag = False
					with open('log.txt', 'a+') as logfile:
						logfile.write("Main-store error\n")
					while store_tries < 10 and flag == False:
						time.sleep(10-store_tries)
						try:
							store(said_df, interval)
							flag = True
						except:
							store_tries = store_tries + 1
			else:
				# print("Here is where to store")
				
				if said_counter == 0:
					tic_store = time.time()
					columns = list(said_df.columns.values)
					# print("columns",columns)
					storage_df = pd.DataFrame(columns=columns)

				storage_df = pd.concat([storage_df,said_df])	

				if (said_counter%25 == 0) & (said_counter!=0):
					print("storage_df",storage_df)
					storage_df.columns = ['SAID', 'Program', 'NAICS', 'Date', 'DayType', 'MaxTemp', 'TenTenNoMPE', 'TenTenNoMAPE', 'TenTenNoCV', 'TenTenAdMPE', 'TenTenAdMAPE', 'TenTenAdCV', 'TenTenAd-50MPE', 'TenTenAd-50MAPE', 'TenTenAd-50CV', 'TenTenAd-40MPE', 'TenTenAd-40MAPE', 'TenTenAd-40CV', 'TenTenAd-30MPE', 'TenTenAd-30MAPE', 'TenTenAd-30CV', 'TenTenAd-20MPE', 'TenTenAd-20MAPE', 'TenTenAd-20CV', 'TenTenAd-10MPE', 'TenTenAd-10MAPE', 'TenTenAd-10CV', 'TenTenAd0MPE', 'TenTenAd0MAPE', 'TenTenAd0CV', 'TenTenAd10MPE', 'TenTenAd10MAPE', 'TenTenAd10CV', 'TenTenAd20MPE', 'TenTenAd20MAPE', 'TenTenAd20CV', 'TenTenAd30MPE', 'TenTenAd30MAPE', 'TenTenAd30CV', 'TenTenAd40MPE', 'TenTenAd40MAPE', 'TenTenAd40CV', 'TenTenAd50MPE', 'TenTenAd50MAPE', 'TenTenAd50CV', 'ThreeTenNoMPE', 'ThreeTenNoMAPE', 'ThreeTenNoCV', 'ThreeTenAdMPE', 'ThreeTenAdMAPE', 'ThreeTenAdCV', 'ThreeTenAd-50MPE', 'ThreeTenAd-50MAPE', 'ThreeTenAd-50CV', 'ThreeTenAd-40MPE', 'ThreeTenAd-40MAPE', 'ThreeTenAd-40CV', 'ThreeTenAd-30MPE', 'ThreeTenAd-30MAPE', 'ThreeTenAd-30CV', 'ThreeTenAd-20MPE', 'ThreeTenAd-20MAPE', 'ThreeTenAd-20CV', 'ThreeTenAd-10MPE', 'ThreeTenAd-10MAPE', 'ThreeTenAd-10CV', 'ThreeTenAd0MPE', 'ThreeTenAd0MAPE', 'ThreeTenAd0CV', 'ThreeTenAd10MPE', 'ThreeTenAd10MAPE', 'ThreeTenAd10CV', 'ThreeTenAd20MPE', 'ThreeTenAd20MAPE', 'ThreeTenAd20CV', 'ThreeTenAd30MPE', 'ThreeTenAd30MAPE', 'ThreeTenAd30CV', 'ThreeTenAd40MPE', 'ThreeTenAd40MAPE', 'ThreeTenAd40CV', 'ThreeTenAd50MPE', 'ThreeTenAd50MAPE', 'ThreeTenAd50CV', 'FourNintyAdMPE', 'FourNintyAdMAPE', 'FourNintyAdCV', 'FourNintyAd-50MPE', 'FourNintyAd-50MAPE', 'FourNintyAd-50CV', 'FourNintyAd-40MPE', 'FourNintyAd-40MAPE', 'FourNintyAd-40CV', 'FourNintyAd-30MPE', 'FourNintyAd-30MAPE', 'FourNintyAd-30CV', 'FourNintyAd-20MPE', 'FourNintyAd-20MAPE', 'FourNintyAd-20CV', 'FourNintyAd-10MPE', 'FourNintyAd-10MAPE', 'FourNintyAd-10CV', 'FourNintyAd0MPE', 'FourNintyAd0MAPE', 'FourNintyAd0CV', 'FourNintyAd10MPE', 'FourNintyAd10MAPE', 'FourNintyAd10CV', 'FourNintyAd20MPE', 'FourNintyAd20MAPE', 'FourNintyAd20CV', 'FourNintyAd30MPE', 'FourNintyAd30MAPE', 'FourNintyAd30CV', 'FourNintyAd40MPE', 'FourNintyAd40MAPE', 'FourNintyAd40CV', 'FourNintyAd50MPE', 'FourNintyAd50MAPE', 'FourNintyAd50CV', 'TF-FTAdMPE', 'TF-FTAdMAPE', 'TF-FTAdCV', 'TF-FTAd-50MPE', 'TF-FTAd-50MAPE', 'TF-FTAd-50CV', 'TF-FTAd-40MPE', 'TF-FTAd-40MAPE', 'TF-FTAd-40CV', 'TF-FTAd-30MPE', 'TF-FTAd-30MAPE', 'TF-FTAd-30CV', 'TF-FTAd-20MPE', 'TF-FTAd-20MAPE', 'TF-FTAd-20CV', 'TF-FTAd-10MPE', 'TF-FTAd-10MAPE', 'TF-FTAd-10CV', 'TF-FTAd0MPE', 'TF-FTAd0MAPE', 'TF-FTAd0CV', 'TF-FTAd10MPE', 'TF-FTAd10MAPE', 'TF-FTAd10CV', 'TF-FTAd20MPE', 'TF-FTAd20MAPE', 'TF-FTAd20CV', 'TF-FTAd30MPE', 'TF-FTAd30MAPE', 'TF-FTAd30CV', 'TF-FTAd40MPE', 'TF-FTAd40MAPE', 'TF-FTAd40CV', 'TF-FTAd50MPE', 'TF-FTAd50MAPE', 'TF-FTAd50CV', 'FF-TTAdMPE', 'FF-TTAdMAPE', 'FF-TTAdCV', 'FF-TTAd-50MPE', 'FF-TTAd-50MAPE', 'FF-TTAd-50CV', 'FF-TTAd-40MPE', 'FF-TTAd-40MAPE', 'FF-TTAd-40CV', 'FF-TTAd-30MPE', 'FF-TTAd-30MAPE', 'FF-TTAd-30CV', 'FF-TTAd-20MPE', 'FF-TTAd-20MAPE', 'FF-TTAd-20CV', 'FF-TTAd-10MPE', 'FF-TTAd-10MAPE', 'FF-TTAd-10CV', 'FF-TTAd0MPE', 'FF-TTAd0MAPE', 'FF-TTAd0CV', 'FF-TTAd10MPE', 'FF-TTAd10MAPE', 'FF-TTAd10CV', 'FF-TTAd20MPE', 'FF-TTAd20MAPE', 'FF-TTAd20CV', 'FF-TTAd30MPE', 'FF-TTAd30MAPE', 'FF-TTAd30CV', 'FF-TTAd40MPE', 'FF-TTAd40MAPE', 'FF-TTAd40CV', 'FF-TTAd50MPE', 'FF-TTAd50MAPE', 'FF-TTAd50CV', 'DateModified']
					storage_df.to_pickle("new_tests/%s_saids.pkl"%said_counter)
					storage_df.to_csv('new_tests/%s_saids.csv'%said_counter)
					columns = list(said_df)
					storage_df = pd.DataFrame(columns=columns)
				
				if(said_counter%10==0):
					print("completing 10 took", str(time.time()-tic_store), "seconds, said_counter:",said_counter)
					tic_store = time.time()

			said_counter = said_counter + 1

			with open('log.txt', 'a+') as logfile:
					logfile.write("SAID: %s \n" %SAID )

			if(said_counter%10 == 0):
					if(global_vars.PRINTFLAG >= 0):
							with open('log.txt', 'a+') as logfile:
									logfile.write("%s SAID's complete.\n" %said_counter )
							
			if(said_counter%10 == 0):
				toc = time.time()
				time_elapsed =  (toc - tic)/60
				print("it has taken", time_elapsed, "minutes to do 10 SAIDs")
				tic = time.time()

			print("\n")
			# break
main()

