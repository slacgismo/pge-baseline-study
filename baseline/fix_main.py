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
			interval = 15
			dbnm = 'MIN15'
		elif global_vars.INTERVALFLAG == 1:
			query = "SELECT * FROM SAID_TABLE_DR_60 LIMIT %i OFFSET %i" %(global_vars.SAID_LIMIT, global_vars.SAID_OFFSET)
			interval = 60
			dbnm = 'MIN60'
		elif global_vars.INTERVALFLAG == 2:
			query = "SELECT * FROM SAID_TABLE_NONDR_15 LIMIT %i OFFSET %i" %(global_vars.SAID_LIMIT, global_vars.SAID_OFFSET)
		elif global_vars.INTERVALFLAG == 3:
			query = "SELECT * FROM SAID_TABLE_NONDR_60 LIMIT %i OFFSET %i" %(global_vars.SAID_LIMIT, global_vars.SAID_OFFSET)
		
		cursor.execute(query)

		said_counter = 0

		tic = time.time()

		said_packet = []
		said_pack_count = 0
		PACK_SIZE = 25
		storage_df_columns = global_vars.storage_df_columns

		pack_bank = []

		# Go through each SAID
		for row in cursor:

			SAID = str(row[0]).zfill(10)
			said_packet.append(SAID)

			said_pack_count += 1

			if said_pack_count%PACK_SIZE != 0:
				continue

			pack_bank.append(said_packet)
			said_packet = []

			if len(pack_bank)*PACK_SIZE > 1000:
				# print(pack_bank)
				break
			else:
				continue

		said_pack_count = 0

		for said_packet in pack_bank:

			said_pack_count += PACK_SIZE

			tic_packet = time.time()

			print("packet",said_packet)

			packet_string = '('+str(said_packet)[1:-1]+')'


			try:
				cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
																		  host=global_vars.DATABASE_IP_RO,
																		  database=global_vars.DATABASE_NAME)
				tic_query = time.time()
				query = "SELECT * FROM %s WHERE SA in %s" %(dbnm, packet_string)
				all_interval_df = pd.read_sql_query(query,cnx)
				all_interval_df['DATE'] =  pd.to_datetime(all_interval_df['DATE'])
				toc_query = time.time()
				print("All interval df shape:", all_interval_df.shape, "- time:", toc_query-tic_query)
			except:
				print("Interval_df error")
				said_packet = []
				continue

			# storage_df = pd.DataFrame(columns=storage_df_columns)
			nonres_storage_df = pd.DataFrame(columns=storage_df_columns)
			pdp_storage_df = pd.DataFrame(columns=storage_df_columns)
			cbp_storage_df = pd.DataFrame(columns=storage_df_columns)
			bip_storage_df = pd.DataFrame(columns=storage_df_columns)
			amp_storage_df = pd.DataFrame(columns=storage_df_columns)
			res_storage_df = pd.DataFrame(columns=storage_df_columns)
			smartrate_storage_df = pd.DataFrame(columns=storage_df_columns)
			smartac_storage_df = pd.DataFrame(columns=storage_df_columns)

			for SAID in said_packet:

				tic_said = time.time()
				try:
					(program, NAICS, weather) = getInfo(SAID)
				except Exception as e:
					print("getInfo error")
					continue 

				print(SAID, program)

				try:
					# Find DR days of SAID
					DRDays = getDR(SAID, program)
				except:
					print("DRDays error")
					continue

				try:
					# Find temperature for SAID
					temp_df = getTemp(weather)
				except:
					print("temp_df error")
					continue

           
				# storage_list is used to have all relevant information for a single SAID in a single Date
				# storage_list = [SAID, program, NAICS, date, max_temp...]
				storage_list = [int(SAID), program, NAICS]

				# will contain all storage lists for 1 said, so approx 731 rows
				said_all_data = []

				interval_df = all_interval_df.loc[all_interval_df['SA'] == SAID]
				print(interval_df.shape)

				# date is initialized to last day and will backtrack through every day
				date = (interval_df['DATE'].max()).date()

				while date.year > 2015:

					# row_data = runFrequentBaseline(interval_df, DRDays, temp_df, interval, date, storage_list)

					try:
						row_data = runBaseline2(interval_df, DRDays, temp_df, interval, date, storage_list)
					except Exception as e:
						print("row_data error")
						continue

					if row_data != 'NA':
							said_all_data.append(row_data)
					
					date = date - datetime.timedelta(days=1)

				said_df = pd.DataFrame(said_all_data, columns=storage_df_columns)
				print("said_df shape:", said_df.shape)
				# frames = [storage_df, said_df]
				# storage_df = pd.concat(frames)

				if program == 'PDP':
					frames = [pdp_storage_df, said_df]
					pdp_storage_df = pd.concat(frames)

					frames = [nonres_storage_df, said_df]
					nonres_storage_df = pd.concat(frames)

					print("Nonres Shape", nonres_storage_df.shape)

				elif program == 'AMP':
					frames = [amp_storage_df, said_df]
					amp_storage_df = pd.concat(frames)

					frames = [nonres_storage_df, said_df]
					nonres_storage_df = pd.concat(frames)

				elif program == 'BIP':
					frames = [bip_storage_df, said_df]
					bip_storage_df = pd.concat(frames)

					frames = [nonres_storage_df, said_df]
					nonres_storage_df = pd.concat(frames)

					print("Nonres Shape", nonres_storage_df.shape)

				elif program == 'CBP':
					frames = [cbp_storage_df, said_df]
					cbp_storage_df = pd.concat(frames)

					frames = [nonres_storage_df, said_df]
					nonres_storage_df = pd.concat(frames)

				elif program == 'SmartAC':
					frames = [smartac_storage_df, said_df]
					smartac_storage_df = pd.concat(frames)

					frames = [res_storage_df, said_df]
					res_storage_df = pd.concat(frames)

				elif program == 'SmartRate':
					frames = [smartrate_storage_df, said_df]
					smartrate_storage_df = pd.concat(frames)

					frames = [res_storage_df, said_df]
					res_storage_df = pd.concat(frames)

				toc_said = time.time()

				# print("SAID took", toc_said-tic_said)

			# storage_df.to_csv('new_tests/%s_saids.csv'%said_pack_count)

			if nonres_storage_df.shape[0]>0:
				nonres_storage_df.to_csv('new_tests/nonres_%s_%s_%s_saids.csv'%(str(global_vars.INTERVALFLAG),str(global_vars.SAID_OFFSET),said_pack_count))
				print("NonRes stored")
			if pdp_storage_df.shape[0]>0:
				pdp_storage_df.to_csv('new_tests/pdp_%s_%s_%s_saids.csv'%(str(global_vars.INTERVALFLAG),str(global_vars.SAID_OFFSET),said_pack_count))
				print("pdp stored")
			if cbp_storage_df.shape[0]>0:
				cbp_storage_df.to_csv('new_tests/cbp_%s_%s_%s_saids.csv'%(str(global_vars.INTERVALFLAG),str(global_vars.SAID_OFFSET),said_pack_count))
				print("cbp stored")	
			if bip_storage_df.shape[0]>0:
				bip_storage_df.to_csv('new_tests/bip_%s_%s_%s_saids.csv'%(str(global_vars.INTERVALFLAG),str(global_vars.SAID_OFFSET),said_pack_count))
				print("bip stored")
			if amp_storage_df.shape[0]>0:
				amp_storage_df.to_csv('new_tests/amp_%s_%s_%s_saids.csv'%(str(global_vars.INTERVALFLAG),str(global_vars.SAID_OFFSET),said_pack_count))
				print("amp stored")
			if res_storage_df.shape[0]>0:
				res_storage_df.to_csv('new_tests/res_%s_%s_%s_saids.csv'%(str(global_vars.INTERVALFLAG),str(global_vars.SAID_OFFSET),said_pack_count))
				print("res stored")
			if smartac_storage_df.shape[0]>0:
				smartac_storage_df.to_csv('new_tests/smartac_%s_%s_%s_saids.csv'%(str(global_vars.INTERVALFLAG),str(global_vars.SAID_OFFSET),said_pack_count))
				print("smartac stored")
			if smartrate_storage_df.shape[0]>0:
				smartrate_storage_df.to_csv('new_tests/smartrate_%s_%s_%s_saids.csv'%(str(global_vars.INTERVALFLAG),str(global_vars.SAID_OFFSET),said_pack_count))	
				print("smartrate stored")	

			toc_packet = time.time()
			said_packet = []

			print("Packet took:", toc_packet-tic_packet)


main()

