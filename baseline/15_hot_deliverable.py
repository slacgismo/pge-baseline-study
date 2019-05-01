import global_vars
global_vars.init()
if global_vars.GRAPHFLAG > 0:
        from graph_functions import *
        from error_graphs import *

import mysql.connector
from deliverable_functions import *
from data_get import *
import pandas as pd 
import sqlalchemy
import numpy as np
import time
from random_data import *
import os

def calculateSpecificErrors(input_program, random_seed, number):

	if not os.path.exists('Errors'):
		os.makedirs('Errors')

	tic = time.time()
	# Since we don't know how many skewed customers there are, these try/excepts will get extra SAIDs
	# so that skipping doesn't leave us with fewer SAIDs that we want

	try:
		said_list = get_random_data(input_program, random_seed, number*2)
	except:
		said_list = get_random_data(input_program, random_seed, number)

	toc = time.time()
	print("Initial SAID query plus randomizer took", toc-tic)

	# initialize arrays
	counter = np.zeros(186)
	spring_counter = np.zeros(186)
	summer_counter = np.zeros(186)
	fall_counter = np.zeros(186)
	winter_counter = np.zeros(186)
	existingAverageList = np.zeros(186)
	springAvgList = np.zeros(186)
	summerAvgList = np.zeros(186)
	fallAvgList = np.zeros(186)
	winterAvgList = np.zeros(186)
	
	milpitas_counter = np.zeros(186)
	stockton_counter = np.zeros(186)
	concord_counter = np.zeros(186)
	potrero_counter = np.zeros(186)
	sacramento_counter = np.zeros(186)
	cupertino_counter = np.zeros(186)
	eureka_counter = np.zeros(186)
	marysville_counter = np.zeros(186)
	fresno_counter = np.zeros(186)
	colma_counter = np.zeros(186)
	santacruz_counter = np.zeros(186)

	eurekaAvgList = np.zeros(186)
	milpitasAvgList = np.zeros(186)
	stocktonAvgList = np.zeros(186)
	concordAvgList = np.zeros(186)
	potreroAvgList = np.zeros(186)
	sacramentoAvgList = np.zeros(186)
	cupertinoAvgList = np.zeros(186)
	marysvilleAvgList = np.zeros(186)
	fresnoAvgList = np.zeros(186)
	colmaAvgList = np.zeros(186)
	santacruzAvgList = np.zeros(186)
	
	# NAICS CODES
	# 110000, 221310, 531113, 452319, 813110, 713990, 722211, 621000
	AvgList11 = np.zeros(186)
	AvgList22 = np.zeros(186)
	AvgList53 = np.zeros(186)
	AvgList45 = np.zeros(186)
	AvgList81 = np.zeros(186)
	AvgList71 = np.zeros(186)
	AvgList72 = np.zeros(186)
	AvgList62 = np.zeros(186)		
	counter_11 = np.zeros(186)
	counter_22 = np.zeros(186)
	counter_53 = np.zeros(186)
	counter_45 = np.zeros(186)
	counter_81 = np.zeros(186)
	counter_71 = np.zeros(186)
	counter_72 = np.zeros(186)
	counter_62 = np.zeros(186)

	index_size = 100

	main_tic = time.time()

	for index in range(int(len(said_list)/index_size)+1):

		if counter[0] >= number:
			print("done with", number, "SAIDs")
			break


		try:
			os.system('say "Done with %s"' %str(index*index_size))

			print("audio played")
		except:
			print("audio not available")

		try:
			current_SAIDs = said_list[index*index_size:index*index_size+index_size]
		except: 
			current_SAIDs = said_list[index*index_size:]

		sql_said_str = str(current_SAIDs)[1:-1]

		tic = time.time()

		cnx = mysql.connector.connect(user=global_vars.DATABASE_USERNAME, password=global_vars.DATABASE_PASSWORD,
														  host=global_vars.DATABASE_IP_RO,
														  database=global_vars.DATABASE_NAME)

		if(input_program[:3] == 'NON'):
			query = "SELECT * FROM ERROR15DR where SAID IN (%s) LIMIT %s;" %((sql_said_str),str(index_size*731))
		elif(input_program[:3] == 'RES'):
			query = "SELECT * FROM ERROR60DR where SAID IN (%s) LIMIT %s;" %((sql_said_str),str(index_size*731))
		else:
			print("Input program error")
			return "ERR"

		print(query)

		# error_df = pd.read_pickle("dummy.pkl")
		
		error_df = pd.read_sql_query(query,cnx)

		error_df.to_pickle("dummy.pkl")

		print("error_df shape", error_df.shape)

		error_df['Date'] =  pd.to_datetime(error_df['Date'])

		toc = time.time()

		print("Getting all data from databases took", toc-tic)

		for SAID in list(current_SAIDs):

			said_error_df = error_df.loc[error_df['SAID'] == SAID]
			print("said_error_df shape", said_error_df.shape)
			
			corrupt_flag = verify_error_df(said_error_df)

			if corrupt_flag:
				print("SAID skewed, skipping \n")

			if(said_error_df.shape[0] < 60):
				print("Skipping SAID")
				continue
			
			(program, NAICS, weather) = getInformation(SAID.zfill(10))

			if (input_program == 'NONRES_WEEKDAY') | (input_program == 'RES_WEEKDAY') | (input_program == 'NONRES_WEEKDAY_15_HOT') | (input_program == 'RES_WEEKDAY_15_HOT'):
				said_error_df = said_error_df[(said_error_df['Date'].dt.dayofweek<5)]
			elif (input_program == 'NONRES_WEEKEND') | (input_program == 'RES_WEEKEND') | (input_program == 'NONRES_WEEKEND_15_HOT') | (input_program == 'RES_WEEKEND_15_HOT'):
				said_error_df = said_error_df[(said_error_df['Date'].dt.dayofweek>4)]

			said_error_df = said_error_df[(said_error_df['Date'].dt.month>=4)]
			said_error_df = said_error_df[(said_error_df['Date'].dt.month<=8)]

			print("After getting rid of unneeded dates said_error_df.shape:",said_error_df.shape)

			if said_error_df.shape[0] < 15:
				print("said_error_df too small")
				continue

			tempCol = 'MaxTemp'

			try:
				said_error_df[tempCol] = said_error_df[tempCol].astype('int')
			except:	
				print("Can't make tempCol into ints")
				continue

			print("Picking 15 max temp days")
			templist = (said_error_df['MaxTemp'].tolist())
			
			print("Len templist:",len(templist), type(templist[2]))
			print("15th max temps is", sorted(templist)[-15], type(sorted(templist)[-15]))

			minVals = list(sorted(templist)[-15:])
			print("MinVals", minVals)

			try:
				print("old error_df shape:", said_error_df.shape)
				said_error_df = said_error_df.loc[said_error_df[tempCol].isin(minVals)]
				print("new error_df shape:", said_error_df.shape)
			except:
				print("Getting 15 days error")
				continue
		
			# increments counters
			tic = time.time()
			counter = [x + 1 for x in counter]
			spring_counter = [x + 1 for x in spring_counter]
			summer_counter = [x + 1 for x in summer_counter]
			fall_counter = [x + 1 for x in fall_counter]
			winter_counter = [x + 1 for x in winter_counter]

			columnAverageList, counter = calcColumnAverage(said_error_df, counter)
			print("said_error_df",said_error_df)

			# backup skip if skewed; decrements counters
			if columnAverageList[2]>5:
				print("Skipping this SAID", SAID)
				counter = [x - 1 for x in counter]
				spring_counter = [x - 1 for x in spring_counter]
				summer_counter = [x - 1 for x in summer_counter]
				fall_counter = [x - 1 for x in fall_counter]
				winter_counter = [x - 1 for x in winter_counter]
				continue

			# adds this SAID's averages to the total
			tempAverageList = np.add(columnAverageList, existingAverageList)
			existingAverageList = tempAverageList

			spring_df, summer_df, fall_df, winter_df = getSeasonalErrors(said_error_df)


			# if the season doesn't have any data, decrements season counter; otherwise adds seasonal average
			if spring_df.shape[0] == 0:
				spring_counter = [x - 1 for x in spring_counter] 
			else:
				springColAvgList, spring_counter = calcColumnAverage(spring_df, spring_counter)
				springAvgList = np.add(springColAvgList, springAvgList)

			if summer_df.shape[0] == 0:
				summer_counter = [x - 1 for x in summer_counter] 
			else:
				summerColAvgList, summer_counter = calcColumnAverage(summer_df, summer_counter)
				summerAvgList = np.add(summerColAvgList, summerAvgList)

			if fall_df.shape[0] == 0:
				fall_counter = [x - 1 for x in fall_counter] 
			else:
				fallColAvgList, fall_counter = calcColumnAverage(fall_df, fall_counter)
				fallAvgList = np.add(fallColAvgList, fallAvgList)

			if winter_df.shape[0] == 0:
				winter_counter = [x - 1 for x in winter_counter] 
			else:
				winterColAvgList, winter_counter = calcColumnAverage(winter_df, winter_counter)
				winterAvgList = np.add(winterColAvgList, winterAvgList)

			# Eureka, Marysville, Fresno, Colma, Santa Cruz
			# If the city is one of the watched cities, calculates the column averages and adds it to the
			# city's average list
			if(weather[1] == 'Eureka'):
				eureka_counter = [x + 1 for x in eureka_counter]
				columnAverageList, eureka_counter = calcColumnAverage(said_error_df, eureka_counter)
				eurekaAvgList = np.add(columnAverageList,eurekaAvgList)
				print("Eureka")

			elif(weather[1] == 'Marysville'):
				marysville_counter = [x + 1 for x in marysville_counter]
				columnAverageList, marysville_counter = calcColumnAverage(said_error_df, marysville_counter)
				marysvilleAvgList = np.add(columnAverageList,marysvilleAvgList)
				print("Marysville")

			elif(weather[1] == 'Fresno'):
				fresno_counter = [x + 1 for x in fresno_counter]
				columnAverageList, fresno_counter = calcColumnAverage(said_error_df, fresno_counter)
				fresnoAvgList = np.add(columnAverageList,fresnoAvgList)
				print("Fresno")

			elif(weather[1] == 'Colma'):
				colma_counter = [x + 1 for x in colma_counter]
				columnAverageList, colma_counter = calcColumnAverage(said_error_df, colma_counter)
				colmaAvgList = np.add(columnAverageList,colmaAvgList)
				print("Colma")

			elif(weather[1] == 'Santa Cruz'):
				santacruz_counter = [x + 1 for x in santacruz_counter]
				columnAverageList, santacruz_counter = calcColumnAverage(said_error_df, santacruz_counter)
				santacruzAvgList = np.add(columnAverageList,santacruzAvgList)
				print("Santa Cruz")	

			elif(weather[1] == 'Milpitas'):
				milpitas_counter = [x + 1 for x in milpitas_counter]
				columnAverageList, milpitas_counter = calcColumnAverage(said_error_df, milpitas_counter)
				milpitasAvgList = np.add(columnAverageList,milpitasAvgList)
				print("Milpitas")

			elif(weather[1] == 'Stockton'):
				stockton_counter = [x + 1 for x in stockton_counter]
				columnAverageList, stockton_counter = calcColumnAverage(said_error_df, stockton_counter)
				stocktonAvgList = np.add(columnAverageList,stocktonAvgList)
				print("Stockton")

			elif(weather[1] == 'Concord'):
				concord_counter = [x + 1 for x in concord_counter]
				columnAverageList, concord_counter = calcColumnAverage(said_error_df, concord_counter)
				concordAvgList = np.add(columnAverageList,concordAvgList)
				print("Concord")

			elif(weather[1] == 'Potrero'):
				potrero_counter = [x + 1 for x in potrero_counter]
				columnAverageList, potrero_counter = calcColumnAverage(said_error_df, potrero_counter)
				potreroAvgList = np.add(columnAverageList,potreroAvgList)
				print("Potrero")

			elif(weather[1] == 'Sacramento'):
				sacramento_counter = [x + 1 for x in sacramento_counter]
				columnAverageList, sacramento_counter = calcColumnAverage(said_error_df, sacramento_counter)
				sacramentoAvgList = np.add(columnAverageList,sacramentoAvgList)
				print("Sacramento")

			elif(weather[1] == 'Cupertino'):
				cupertino_counter = [x + 1 for x in cupertino_counter]
				columnAverageList, cupertino_counter = calcColumnAverage(said_error_df, cupertino_counter)
				cupertinoAvgList = np.add(columnAverageList,cupertinoAvgList)
				print("Cupertino")

			# If the SAID is one of the watched NAICS codes, calculates the column averages and adds it to
			# the NAICS-specific average list
			if NAICS == '110000':
				counter_11 = [x + 1 for x in counter_11]
				print(NAICS)
				columnAverageList, counter_11 = calcColumnAverage(said_error_df, counter_11)
				AvgList11 = np.add(columnAverageList, AvgList11)
			elif NAICS == '221310':
				counter_22 = [x + 1 for x in counter_22]
				print(NAICS)
				columnAverageList, counter_22 = calcColumnAverage(said_error_df, counter_22)
				AvgList22 = np.add(columnAverageList, AvgList22)
			elif NAICS == '531123':
				counter_53 = [x + 1 for x in counter_53]
				print(NAICS)
				columnAverageList, counter_53 = calcColumnAverage(said_error_df, counter_53)
				AvgList53 = np.add(columnAverageList, AvgList53)
			elif NAICS == '452319':
				counter_45 = [x + 1 for x in counter_45]
				print(NAICS)
				columnAverageList, counter_45 = calcColumnAverage(said_error_df, counter_45)
				AvgList45 = np.add(columnAverageList, AvgList45)
			elif NAICS == '813110':
				counter_81 = [x + 1 for x in counter_81]
				print(NAICS)
				columnAverageList, counter_81 = calcColumnAverage(said_error_df, counter_81)
				AvgList81 = np.add(columnAverageList, AvgList81)
			elif NAICS == '111998':
				counter_71 = [x + 1 for x in counter_71]
				print(NAICS)
				columnAverageList, counter_71 = calcColumnAverage(said_error_df, counter_71)
				AvgList71 = np.add(columnAverageList, AvgList71)
			elif NAICS == '722000':
				counter_72 = [x + 1 for x in counter_72]
				print(NAICS)
				columnAverageList, counter_72 = calcColumnAverage(said_error_df, counter_72)
				AvgList72 = np.add(columnAverageList, AvgList72)
			elif NAICS == '621210':
				counter_62 = [x + 1 for x in counter_62]
				print(NAICS)
				columnAverageList, counter_62 = calcColumnAverage(said_error_df, counter_62)
				AvgList62 = np.add(columnAverageList, AvgList62)
		
			toc = time.time()
			print("Completing SAID calculations took", toc-tic)
			print(int(counter[0]), "/", number, '\n')
			# Ends the loop if the number of averages completed is the number requested
			# if there are not enough non-skewed SAIDs to complete the number requested, this will not print

		# Divides the "average" lists (really the sum lists) by their respective counters to find each average
		existingAverageList_temp = [x/y for x, y in zip(existingAverageList, counter)]
		springAvgList_temp = [x/y for x, y in zip(springAvgList, spring_counter)]
		summerAvgList_temp = [x/y for x, y in zip(summerAvgList, summer_counter)]
		fallAvgList_temp = [x/y for x, y in zip(fallAvgList, fall_counter)]
		winterAvgList_temp = [x/y for x, y in zip(winterAvgList, winter_counter)]
		eurekaAvgList_temp = [x/y for x, y in zip(eurekaAvgList, eureka_counter)]
		stocktonAvgList_temp = [x/y for x, y in zip(stocktonAvgList, stockton_counter)]
		concordAvgList_temp = [x/y for x, y in zip(concordAvgList, concord_counter)]
		potreroAvgList_temp = [x/y for x, y in zip(potreroAvgList, potrero_counter)]
		sacramentoAvgList_temp = [x/y for x, y in zip(sacramentoAvgList, sacramento_counter)]
		cupertinoAvgList_temp = [x/y for x, y in zip(cupertinoAvgList, cupertino_counter)]
		milpitasAvgList_temp = [x/y for x, y in zip(milpitasAvgList, milpitas_counter)]
		marysvilleAvgList_temp = [x/y for x, y in zip(marysvilleAvgList, marysville_counter)]
		fresnoAvgList_temp = [x/y for x, y in zip(fresnoAvgList, fresno_counter)]
		colmaAvgList_temp = [x/y for x, y in zip(colmaAvgList, colma_counter)]
		santacruzAvgList_temp = [x/y for x, y in zip(santacruzAvgList, santacruz_counter)]
		AvgList11_temp = [x/y for x, y in zip(AvgList11, counter_11)]
		AvgList22_temp = [x/y for x, y in zip(AvgList22, counter_22)]
		AvgList53_temp = [x/y for x, y in zip(AvgList53, counter_53)]
		AvgList45_temp = [x/y for x, y in zip(AvgList45, counter_45)]
		AvgList81_temp = [x/y for x, y in zip(AvgList81, counter_81)]
		AvgList71_temp = [x/y for x, y in zip(AvgList71, counter_71)]
		AvgList72_temp = [x/y for x, y in zip(AvgList72, counter_72)]
		AvgList62_temp = [x/y for x, y in zip(AvgList62, counter_62)]

		# inserts row names and appends the final counter to the end of each list, for display purposes
		existingAverageList_temp.append(counter[0])
		existingAverageList_temp.insert(0, "Overall")
		springAvgList_temp.append(spring_counter[0])
		springAvgList_temp.insert(0, "Spring")
		summerAvgList_temp.append(summer_counter[0])
		summerAvgList_temp.insert(0, "Summer")
		fallAvgList_temp.append(fall_counter[0])
		fallAvgList_temp.insert(0, "Fall")
		winterAvgList_temp.append(winter_counter[0])
		winterAvgList_temp.insert(0, "Winter")
		milpitasAvgList_temp.append(milpitas_counter[0])
		milpitasAvgList_temp.insert(0, "Milpitas")
		fresnoAvgList_temp.append(fresno_counter[0])
		fresnoAvgList_temp.insert(0, "Fresno")
		stocktonAvgList_temp.append(stockton_counter[0])
		stocktonAvgList_temp.insert(0, "Stockton")
		concordAvgList_temp.append(concord_counter[0])
		concordAvgList_temp.insert(0, "Concord")
		potreroAvgList_temp.append(potrero_counter[0])
		potreroAvgList_temp.insert(0, "Potrero")
		sacramentoAvgList_temp.append(sacramento_counter[0])
		sacramentoAvgList_temp.insert(0, "Sacramento")
		cupertinoAvgList_temp.append(cupertino_counter[0])
		cupertinoAvgList_temp.insert(0, "Cupertino")
		santacruzAvgList_temp.append(santacruz_counter[0])
		santacruzAvgList_temp.insert(0, "Santa Cruz")
		marysvilleAvgList_temp.append(marysville_counter[0])
		marysvilleAvgList_temp.insert(0, "Marysville")
		colmaAvgList_temp.append(colma_counter[0])
		colmaAvgList_temp.insert(0, "Colma")
		eurekaAvgList_temp.append(eureka_counter[0])
		eurekaAvgList_temp.insert(0, "Eureka")
		AvgList11_temp.append(counter_11[0])
		AvgList11_temp.insert(0, "110000")
		AvgList22_temp.append(counter_22[0])
		AvgList22_temp.insert(0, "221310")
		AvgList53_temp.append(counter_53[0])
		AvgList53_temp.insert(0, "531123")
		AvgList45_temp.append(counter_45[0])
		AvgList45_temp.insert(0, "452319")
		AvgList81_temp.append(counter_81[0])
		AvgList81_temp.insert(0, "813110")
		AvgList71_temp.append(counter_71[0])
		AvgList71_temp.insert(0, "111998")
		AvgList72_temp.append(counter_72[0])
		AvgList72_temp.insert(0, "722000")
		AvgList62_temp.append(counter_62[0])
		AvgList62_temp.insert(0, "621210")

		headers = ['{}_{}'.format(input_program, number), 'TenTenNoMPE', 'TenTenNoMAPE', 'TenTenNoCV', 'TenTenAdMPE', 'TenTenAdMAPE', 'TenTenAdCV', 'TenTenAd-50MPE', 'TenTenAd-50MAPE', 'TenTenAd-50CV', 'TenTenAd-40MPE', 'TenTenAd-40MAPE', 'TenTenAd-40CV', 'TenTenAd-30MPE', 'TenTenAd-30MAPE', 'TenTenAd-30CV', 'TenTenAd-20MPE', 'TenTenAd-20MAPE', 'TenTenAd-20CV', 'TenTenAd-10MPE', 'TenTenAd-10MAPE', 'TenTenAd-10CV', 'TenTenAd0MPE', 'TenTenAd0MAPE', 'TenTenAd0CV', 'TenTenAd10MPE', 'TenTenAd10MAPE', 'TenTenAd10CV', 'TenTenAd20MPE', 'TenTenAd20MAPE', 'TenTenAd20CV', 'TenTenAd30MPE', 'TenTenAd30MAPE', 'TenTenAd30CV', 'TenTenAd40MPE', 'TenTenAd40MAPE', 'TenTenAd40CV', 'TenTenAd50MPE', 'TenTenAd50MAPE', 'TenTenAd50CV', 'ThreeTenNoMPE', 'ThreeTenNoMAPE', 'ThreeTenNoCV', 'ThreeTenAdMPE', 'ThreeTenAdMAPE', 'ThreeTenAdCV', 'ThreeTenAd-50MPE', 'ThreeTenAd-50MAPE', 'ThreeTenAd-50CV', 'ThreeTenAd-40MPE', 'ThreeTenAd-40MAPE', 'ThreeTenAd-40CV', 'ThreeTenAd-30MPE', 'ThreeTenAd-30MAPE', 'ThreeTenAd-30CV', 'ThreeTenAd-20MPE', 'ThreeTenAd-20MAPE', 'ThreeTenAd-20CV', 'ThreeTenAd-10MPE', 'ThreeTenAd-10MAPE', 'ThreeTenAd-10CV', 'ThreeTenAd0MPE', 'ThreeTenAd0MAPE', 'ThreeTenAd0CV', 'ThreeTenAd10MPE', 'ThreeTenAd10MAPE', 'ThreeTenAd10CV', 'ThreeTenAd20MPE', 'ThreeTenAd20MAPE', 'ThreeTenAd20CV', 'ThreeTenAd30MPE', 'ThreeTenAd30MAPE', 'ThreeTenAd30CV', 'ThreeTenAd40MPE', 'ThreeTenAd40MAPE', 'ThreeTenAd40CV', 'ThreeTenAd50MPE', 'ThreeTenAd50MAPE', 'ThreeTenAd50CV', 'FourNintyAdMPE', 'FourNintyAdMAPE', 'FourNintyAdCV', 'FourNintyAd-50MPE', 'FourNintyAd-50MAPE', 'FourNintyAd-50CV', 'FourNintyAd-40MPE', 'FourNintyAd-40MAPE', 'FourNintyAd-40CV', 'FourNintyAd-30MPE', 'FourNintyAd-30MAPE', 'FourNintyAd-30CV', 'FourNintyAd-20MPE', 'FourNintyAd-20MAPE', 'FourNintyAd-20CV', 'FourNintyAd-10MPE', 'FourNintyAd-10MAPE', 'FourNintyAd-10CV', 'FourNintyAd0MPE', 'FourNintyAd0MAPE', 'FourNintyAd0CV', 'FourNintyAd10MPE', 'FourNintyAd10MAPE', 'FourNintyAd10CV', 'FourNintyAd20MPE', 'FourNintyAd20MAPE', 'FourNintyAd20CV', 'FourNintyAd30MPE', 'FourNintyAd30MAPE', 'FourNintyAd30CV', 'FourNintyAd40MPE', 'FourNintyAd40MAPE', 'FourNintyAd40CV', 'FourNintyAd50MPE', 'FourNintyAd50MAPE', 'FourNintyAd50CV', 'TF-FTAdMPE', 'TF-FTAdMAPE', 'TF-FTAdCV', 'TF-FTAd-50MPE', 'TF-FTAd-50MAPE', 'TF-FTAd-50CV', 'TF-FTAd-40MPE', 'TF-FTAd-40MAPE', 'TF-FTAd-40CV', 'TF-FTAd-30MPE', 'TF-FTAd-30MAPE', 'TF-FTAd-30CV', 'TF-FTAd-20MPE', 'TF-FTAd-20MAPE', 'TF-FTAd-20CV', 'TF-FTAd-10MPE', 'TF-FTAd-10MAPE', 'TF-FTAd-10CV', 'TF-FTAd0MPE', 'TF-FTAd0MAPE', 'TF-FTAd0CV', 'TF-FTAd10MPE', 'TF-FTAd10MAPE', 'TF-FTAd10CV', 'TF-FTAd20MPE', 'TF-FTAd20MAPE', 'TF-FTAd20CV', 'TF-FTAd30MPE', 'TF-FTAd30MAPE', 'TF-FTAd30CV', 'TF-FTAd40MPE', 'TF-FTAd40MAPE', 'TF-FTAd40CV', 'TF-FTAd50MPE', 'TF-FTAd50MAPE', 'TF-FTAd50CV', 'FF-TTAdMPE', 'FF-TTAdMAPE', 'FF-TTAdCV', 'FF-TTAd-50MPE', 'FF-TTAd-50MAPE', 'FF-TTAd-50CV', 'FF-TTAd-40MPE', 'FF-TTAd-40MAPE', 'FF-TTAd-40CV', 'FF-TTAd-30MPE', 'FF-TTAd-30MAPE', 'FF-TTAd-30CV', 'FF-TTAd-20MPE', 'FF-TTAd-20MAPE', 'FF-TTAd-20CV', 'FF-TTAd-10MPE', 'FF-TTAd-10MAPE', 'FF-TTAd-10CV', 'FF-TTAd0MPE', 'FF-TTAd0MAPE', 'FF-TTAd0CV', 'FF-TTAd10MPE', 'FF-TTAd10MAPE', 'FF-TTAd10CV', 'FF-TTAd20MPE', 'FF-TTAd20MAPE', 'FF-TTAd20CV', 'FF-TTAd30MPE', 'FF-TTAd30MAPE', 'FF-TTAd30CV', 'FF-TTAd40MPE', 'FF-TTAd40MAPE', 'FF-TTAd40CV', 'FF-TTAd50MPE', 'FF-TTAd50MAPE', 'FF-TTAd50CV']

		final_data = np.array([headers, existingAverageList_temp, springAvgList_temp, summerAvgList_temp, fallAvgList_temp, winterAvgList_temp, 
								milpitasAvgList_temp, fresnoAvgList_temp, stocktonAvgList_temp, concordAvgList_temp, potreroAvgList_temp, 
								sacramentoAvgList_temp, cupertinoAvgList_temp, santacruzAvgList_temp, marysvilleAvgList_temp, colmaAvgList_temp, 
								eurekaAvgList_temp, 
								AvgList11_temp, AvgList22_temp, AvgList53_temp, AvgList45_temp, AvgList81_temp, AvgList71_temp, AvgList72_temp, AvgList62_temp])

		# formatting this as a string allows us to include headers and NaNs, but means that the first and last
		# entries will have a '[' or a ']' included
		# np.savetxt('Errors/all_error_results_{}_{}.csv'.format(input_program, number), final_data, fmt='%s') 
		np.savetxt('Errors/all_error_results_{}_{}_of_{}.csv'.format(input_program, int(counter[0]), number), final_data, fmt='%s') 
		print("Complete", int(counter[0]), "in", main_tic-(time.time()), "seconds")

# calculateSpecificErrors('RES', 13, 500)

# calculateSpecificErrors('SmartRate', 13, 500)

# calculateSpecificErrors('SmartAC', 13, 500)

# # calculateSpecificErrors('NONRES', 13, 500)

# calculateSpecificErrors('PDP', 13, 500)

# calculateSpecificErrors('AMP', 13, 500)

# calculateSpecificErrors('CBP', 13, 500)

# calculateSpecificErrors('BIP', 13, 500)

# calculateSpecificErrors('NONRES', 13, 500)
# # calculateSpecificErrors('RES', 13, 500)
# calculateSpecificErrors('RES_WEEKDAY', 13, 500)
# calculateSpecificErrors('RES_WEEKEND', 13, 500)
# calculateSpecificErrors('NONRES_WEEKDAY', 13, 500)
# calculateSpecificErrors('NONRES_WEEKEND', 13, 500)

# calculateSpecificErrors('NONRES_WEEKEND_15_HOT', 13, 7)
# calculateSpecificErrors('NONRES_WEEKDAY_15_HOT', 13, 500)
# calculateSpecificErrors('NONRES_WEEKEND_15_HOT', 13, 2500)
calculateSpecificErrors('RES_WEEKEND_15_HOT', 13, 2500)

# calculateSpecificErrors('RES_WEEKDAY_15_HOT', 13, 500)

# # calculateSpecificErrors('NONRES_WEEKDAY_15_HOT', 13, 500)
# calculateSpecificErrors('NONRES_WEEKEND_15_HOT', 13, 500)
