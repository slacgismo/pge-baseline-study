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

def calculateSpecificErrors(input_program, random_seed, number):

	if not os.path.exists('Errors'):
		os.makedirs('Errors')

	tic = time.time()
	# Since we don't know how many skewed customers there are, these try/excepts will get extra SAIDs
	# so that skipping doesn't leave us with fewer SAIDs that we want

	try:
		said_list = get_random_data(input_program, random_seed, number*3)
	except:
		try:
			said_list = get_random_data(input_program, random_seed, number*2)
		except:
			try:
				said_list = get_random_data(input_program, random_seed, number*1.5)
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

	corrupt_count = 0

	for SAID in said_list:
		print(said_list[:10])

		tic = time.time()

		error_df = getCalculatedErrors(SAID, input_program)
		return 0
		try:
			tic = time.time()

			error_df = getCalculatedErrors(SAID, input_program)

			print("Got error_df")

			MPE_columns = ['TenTenNoMPE', 'TenTenAdMPE', 'TenTenAd-50MPE', 'TenTenAd-40MPE', 'TenTenAd-30MPE', 'TenTenAd-20MPE', 'TenTenAd-10MPE', 
				'TenTenAd0MPE', 'TenTenAd10MPE', 'TenTenAd20MPE', 'TenTenAd30MPE', 'TenTenAd40MPE', 'TenTenAd50MPE', 'ThreeTenNoMPE', 
				'ThreeTenAdMPE', 'ThreeTenAd-50MPE', 'ThreeTenAd-40MPE', 'ThreeTenAd-30MPE', 'ThreeTenAd-20MPE', 'ThreeTenAd-10MPE', 
				'ThreeTenAd0MPE', 'ThreeTenAd10MPE', 'ThreeTenAd20MPE', 'ThreeTenAd30MPE', 'ThreeTenAd40MPE', 'ThreeTenAd50MPE', 
				'FourNintyAdMPE', 'FourNintyAd-50MPE', 'FourNintyAd-40MPE', 'FourNintyAd-30MPE', 'FourNintyAd-20MPE', 'FourNintyAd-10MPE', 
				'FourNintyAd0MPE', 'FourNintyAd10MPE', 'FourNintyAd30MPE', 'FourNintyAd40MPE', 'FourNintyAd50MPE', 'TF-FTAdMPE', 'TF-FTAd-50MPE',  
				'TF-FTAd-40MPE', 'TF-FTAd-30MPE', 'TF-FTAd-20MPE', 'TF-FTAd-10MPE', 'TF-FTAd0MPE', 'TF-FTAd10MPE', 'TF-FTAd20MPE', 
				'TF-FTAd30MPE', 'TF-FTAd40MPE', 'TF-FTAd50MPE', 'FF-TTAdMPE', 'FF-TTAd-50MPE', 'FF-TTAd-40MPE', 'FF-TTAd-30MPE', 
				'FF-TTAd-20MPE', 'FF-TTAd-10MPE', 'FF-TTAd0MPE', 'FF-TTAd10MPE', 'FF-TTAd20MPE', 'FF-TTAd30MPE', 'FF-TTAd40MPE', 'FF-TTAd50MPE']


			# for col in MPE_columns:
			# 	print("pre",error_df[col])
			# 	error_df[col] = error_df[col].apply(lambda x: x*-1)
			# 	print("post",error_df[col])

			(program, NAICS, weather) = getInformation(SAID.zfill(10))
			print("Got program, NAICS, weather")

			toc = time.time()
			
			print("Getting SAID data from databases took", toc-tic)
			print("Said =", SAID)
			print("Location =", weather[1])
			print("NAICS =", NAICS)

		# skips if there's a problem with the information
		except: 
			print("ErrorZone1 error \n")
			continue
		
		corrupt_flag = verify_error_df(error_df)

		# for columns in negative_columns:
		# 	error_df[columns] = error_df[columns] * (-1)

		if (input_program == 'NONRES_WEEKDAY') | (input_program == 'RES_WEEKDAY') | (input_program == 'NONRES_WEEKDAY_15_HOT') | (input_program == 'RES_WEEKDAY_15_HOT'):
			error_df = error_df[(error_df['Date'].dt.dayofweek<5)]
			print(error_df.shape)

		if (input_program == 'NONRES_WEEKEND') | (input_program == 'RES_WEEKEND') | (input_program == 'NONRES_WEEKEND_15_HOT') | (input_program == 'RES_WEEKEND_15_HOT'):
			error_df = error_df[(error_df['Date'].dt.dayofweek>4)]
			print(error_df.shape)

		if (input_program == ('NONRES_WEEKDAY_15_HOT')) | (input_program == ('NONRES_WEEKEND_15_HOT')) | (input_program == ('RES_WEEKDAY_15_HOT')) | (input_program == ('RES_WEEKEND_15_HOT')):

			if error_df.shape[0] < 70:
				print("error_df too small")
				continue

			tempCol = 'MaxTemp'

			# error_df[tempCol] = error_df[tempCol].astype(int)
			# error_df[tempCol]=error_df.tempCol.astype('int64')

			try:
				error_df[tempCol] = error_df[tempCol].astype('int')
				print(error_df[tempCol].dtype)
			except:	
				continue

			print("Picking 15 max temp days")
			templist = (error_df['MaxTemp'].tolist())
			print(len(templist), type(templist[2]))
			print("15th max temps is", sorted(templist)[-15], type(sorted(templist)[-15]))

			minVal = int(sorted(templist)[-15])
			minVals = list(sorted(templist)[-15:])
			print("MinVals", minVals)

			try:
				print("old error_df shape:", error_df.shape)
				error_df = error_df.loc[error_df[tempCol].isin(minVals)]
				print("new error_df shape:", error_df.shape)
				print(error_df)
			except:
				continue
				print(error_df[tempCol].dtype)


		# skips if the SAID is skewed
		if corrupt_flag:
			print("SAID skewed, skipping \n")
			corrupt_count = corrupt_count + 1
			continue
		
		# increments counters
		tic = time.time()
		counter = [x + 1 for x in counter]
		spring_counter = [x + 1 for x in spring_counter]
		summer_counter = [x + 1 for x in summer_counter]
		fall_counter = [x + 1 for x in fall_counter]
		winter_counter = [x + 1 for x in winter_counter]

		columnAverageList, counter = calcColumnAverage(error_df, counter)
		print("error_df",error_df)
		print("columnAverageList",columnAverageList)

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

		spring_df, summer_df, fall_df, winter_df = getSeasonalErrors(error_df)



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
			columnAverageList, eureka_counter = calcColumnAverage(error_df, eureka_counter)
			eurekaAvgList = np.add(columnAverageList,eurekaAvgList)
			print("Eureka")

		elif(weather[1] == 'Marysville'):
			marysville_counter = [x + 1 for x in marysville_counter]
			columnAverageList, marysville_counter = calcColumnAverage(error_df, marysville_counter)
			marysvilleAvgList = np.add(columnAverageList,marysvilleAvgList)
			print("Marysville")

		elif(weather[1] == 'Fresno'):
			fresno_counter = [x + 1 for x in fresno_counter]
			columnAverageList, fresno_counter = calcColumnAverage(error_df, fresno_counter)
			fresnoAvgList = np.add(columnAverageList,fresnoAvgList)
			print("Fresno")

		elif(weather[1] == 'Colma'):
			colma_counter = [x + 1 for x in colma_counter]
			columnAverageList, colma_counter = calcColumnAverage(error_df, colma_counter)
			colmaAvgList = np.add(columnAverageList,colmaAvgList)
			print("Colma")

		elif(weather[1] == 'Santa Cruz'):
			santacruz_counter = [x + 1 for x in santacruz_counter]
			columnAverageList, santacruz_counter = calcColumnAverage(error_df, santacruz_counter)
			santacruzAvgList = np.add(columnAverageList,santacruzAvgList)
			print("Santa Cruz")	

		elif(weather[1] == 'Milpitas'):
			milpitas_counter = [x + 1 for x in milpitas_counter]
			columnAverageList, milpitas_counter = calcColumnAverage(error_df, milpitas_counter)
			milpitasAvgList = np.add(columnAverageList,milpitasAvgList)
			print("Milpitas")

		elif(weather[1] == 'Stockton'):
			stockton_counter = [x + 1 for x in stockton_counter]
			columnAverageList, stockton_counter = calcColumnAverage(error_df, stockton_counter)
			stocktonAvgList = np.add(columnAverageList,stocktonAvgList)
			print("Stockton")

		elif(weather[1] == 'Concord'):
			concord_counter = [x + 1 for x in concord_counter]
			columnAverageList, concord_counter = calcColumnAverage(error_df, concord_counter)
			concordAvgList = np.add(columnAverageList,concordAvgList)
			print("Concord")

		elif(weather[1] == 'Potrero'):
			potrero_counter = [x + 1 for x in potrero_counter]
			columnAverageList, potrero_counter = calcColumnAverage(error_df, potrero_counter)
			potreroAvgList = np.add(columnAverageList,potreroAvgList)
			print("Potrero")

		elif(weather[1] == 'Sacramento'):
			sacramento_counter = [x + 1 for x in sacramento_counter]
			columnAverageList, sacramento_counter = calcColumnAverage(error_df, sacramento_counter)
			sacramentoAvgList = np.add(columnAverageList,sacramentoAvgList)
			print("Sacramento")

		elif(weather[1] == 'Cupertino'):
			cupertino_counter = [x + 1 for x in cupertino_counter]
			columnAverageList, cupertino_counter = calcColumnAverage(error_df, cupertino_counter)
			cupertinoAvgList = np.add(columnAverageList,cupertinoAvgList)
			print("Cupertino")

		# If the SAID is one of the watched NAICS codes, calculates the column averages and adds it to
		# the NAICS-specific average list
		if NAICS == '110000':
			counter_11 = [x + 1 for x in counter_11]
			print(NAICS)
			columnAverageList, counter_11 = calcColumnAverage(error_df, counter_11)
			AvgList11 = np.add(columnAverageList, AvgList11)
		elif NAICS == '221310':
			counter_22 = [x + 1 for x in counter_22]
			print(NAICS)
			columnAverageList, counter_22 = calcColumnAverage(error_df, counter_22)
			AvgList22 = np.add(columnAverageList, AvgList22)
		elif NAICS == '531123':
			counter_53 = [x + 1 for x in counter_53]
			print(NAICS)
			columnAverageList, counter_53 = calcColumnAverage(error_df, counter_53)
			AvgList53 = np.add(columnAverageList, AvgList53)
		elif NAICS == '452319':
			counter_45 = [x + 1 for x in counter_45]
			print(NAICS)
			columnAverageList, counter_45 = calcColumnAverage(error_df, counter_45)
			AvgList45 = np.add(columnAverageList, AvgList45)
		elif NAICS == '813110':
			counter_81 = [x + 1 for x in counter_81]
			print(NAICS)
			columnAverageList, counter_81 = calcColumnAverage(error_df, counter_81)
			AvgList81 = np.add(columnAverageList, AvgList81)
		elif NAICS == '111998':
			counter_71 = [x + 1 for x in counter_71]
			print(NAICS)
			columnAverageList, counter_71 = calcColumnAverage(error_df, counter_71)
			AvgList71 = np.add(columnAverageList, AvgList71)
		elif NAICS == '722000':
			counter_72 = [x + 1 for x in counter_72]
			print(NAICS)
			columnAverageList, counter_72 = calcColumnAverage(error_df, counter_72)
			AvgList72 = np.add(columnAverageList, AvgList72)
		elif NAICS == '621210':
			counter_62 = [x + 1 for x in counter_62]
			print(NAICS)
			columnAverageList, counter_62 = calcColumnAverage(error_df, counter_62)
			AvgList62 = np.add(columnAverageList, AvgList62)
		
		toc = time.time()
		print("Completing SAID calculations took", toc-tic)
		print(int(counter[0]), "/", number, '\n')
		# Ends the loop if the number of averages completed is the number requested
		# if there are not enough non-skewed SAIDs to complete the number requested, this will not print
		if counter[0] == number:
			print("done with", number, "SAIDs")
			break

	# Divides the "average" lists (really the sum lists) by their respective counters to find each average
	existingAverageList = [x/y for x, y in zip(existingAverageList, counter)]
	springAvgList = [x/y for x, y in zip(springAvgList, spring_counter)]
	summerAvgList = [x/y for x, y in zip(summerAvgList, summer_counter)]
	fallAvgList = [x/y for x, y in zip(fallAvgList, fall_counter)]
	winterAvgList = [x/y for x, y in zip(winterAvgList, winter_counter)]
	eurekaAvgList = [x/y for x, y in zip(eurekaAvgList, eureka_counter)]
	stocktonAvgList = [x/y for x, y in zip(stocktonAvgList, stockton_counter)]
	concordAvgList = [x/y for x, y in zip(concordAvgList, concord_counter)]
	potreroAvgList = [x/y for x, y in zip(potreroAvgList, potrero_counter)]
	sacramentoAvgList = [x/y for x, y in zip(sacramentoAvgList, sacramento_counter)]
	cupertinoAvgList = [x/y for x, y in zip(cupertinoAvgList, cupertino_counter)]
	milpitasAvgList = [x/y for x, y in zip(milpitasAvgList, milpitas_counter)]
	marysvilleAvgList = [x/y for x, y in zip(marysvilleAvgList, marysville_counter)]
	fresnoAvgList = [x/y for x, y in zip(fresnoAvgList, fresno_counter)]
	colmaAvgList = [x/y for x, y in zip(colmaAvgList, colma_counter)]
	santacruzAvgList = [x/y for x, y in zip(santacruzAvgList, santacruz_counter)]
	AvgList11 = [x/y for x, y in zip(AvgList11, counter_11)]
	AvgList22 = [x/y for x, y in zip(AvgList22, counter_22)]
	AvgList53 = [x/y for x, y in zip(AvgList53, counter_53)]
	AvgList45 = [x/y for x, y in zip(AvgList45, counter_45)]
	AvgList81 = [x/y for x, y in zip(AvgList81, counter_81)]
	AvgList71 = [x/y for x, y in zip(AvgList71, counter_71)]
	AvgList72 = [x/y for x, y in zip(AvgList72, counter_72)]
	AvgList62 = [x/y for x, y in zip(AvgList62, counter_62)]

	# inserts row names and appends the final counter to the end of each list, for display purposes
	existingAverageList.append(counter[0])
	existingAverageList.insert(0, "Overall")
	springAvgList.append(spring_counter[0])
	springAvgList.insert(0, "Spring")
	summerAvgList.append(summer_counter[0])
	summerAvgList.insert(0, "Summer")
	fallAvgList.append(fall_counter[0])
	fallAvgList.insert(0, "Fall")
	winterAvgList.append(winter_counter[0])
	winterAvgList.insert(0, "Winter")
	milpitasAvgList.append(milpitas_counter[0])
	milpitasAvgList.insert(0, "Milpitas")
	fresnoAvgList.append(fresno_counter[0])
	fresnoAvgList.insert(0, "Fresno")
	stocktonAvgList.append(stockton_counter[0])
	stocktonAvgList.insert(0, "Stockton")
	concordAvgList.append(concord_counter[0])
	concordAvgList.insert(0, "Concord")
	potreroAvgList.append(potrero_counter[0])
	potreroAvgList.insert(0, "Potrero")
	sacramentoAvgList.append(sacramento_counter[0])
	sacramentoAvgList.insert(0, "Sacramento")
	cupertinoAvgList.append(cupertino_counter[0])
	cupertinoAvgList.insert(0, "Cupertino")
	santacruzAvgList.append(santacruz_counter[0])
	santacruzAvgList.insert(0, "Santa Cruz")
	marysvilleAvgList.append(marysville_counter[0])
	marysvilleAvgList.insert(0, "Marysville")
	colmaAvgList.append(colma_counter[0])
	colmaAvgList.insert(0, "Colma")
	eurekaAvgList.append(eureka_counter[0])
	eurekaAvgList.insert(0, "Eureka")
	AvgList11.append(counter_11[0])
	AvgList11.insert(0, "110000")
	AvgList22.append(counter_22[0])
	AvgList22.insert(0, "221310")
	AvgList53.append(counter_53[0])
	AvgList53.insert(0, "531123")
	AvgList45.append(counter_45[0])
	AvgList45.insert(0, "452319")
	AvgList81.append(counter_81[0])
	AvgList81.insert(0, "813110")
	AvgList71.append(counter_71[0])
	AvgList71.insert(0, "111998")
	AvgList72.append(counter_72[0])
	AvgList72.insert(0, "722000")
	AvgList62.append(counter_62[0])
	AvgList62.insert(0, "621210")

	headers = ['{}_{}'.format(input_program, number), 'TenTenNoMPE', 'TenTenNoMAPE', 'TenTenNoCV', 'TenTenAdMPE', 'TenTenAdMAPE', 'TenTenAdCV', 'TenTenAd-50MPE', 'TenTenAd-50MAPE', 'TenTenAd-50CV', 'TenTenAd-40MPE', 'TenTenAd-40MAPE', 'TenTenAd-40CV', 'TenTenAd-30MPE', 'TenTenAd-30MAPE', 'TenTenAd-30CV', 'TenTenAd-20MPE', 'TenTenAd-20MAPE', 'TenTenAd-20CV', 'TenTenAd-10MPE', 'TenTenAd-10MAPE', 'TenTenAd-10CV', 'TenTenAd0MPE', 'TenTenAd0MAPE', 'TenTenAd0CV', 'TenTenAd10MPE', 'TenTenAd10MAPE', 'TenTenAd10CV', 'TenTenAd20MPE', 'TenTenAd20MAPE', 'TenTenAd20CV', 'TenTenAd30MPE', 'TenTenAd30MAPE', 'TenTenAd30CV', 'TenTenAd40MPE', 'TenTenAd40MAPE', 'TenTenAd40CV', 'TenTenAd50MPE', 'TenTenAd50MAPE', 'TenTenAd50CV', 'ThreeTenNoMPE', 'ThreeTenNoMAPE', 'ThreeTenNoCV', 'ThreeTenAdMPE', 'ThreeTenAdMAPE', 'ThreeTenAdCV', 'ThreeTenAd-50MPE', 'ThreeTenAd-50MAPE', 'ThreeTenAd-50CV', 'ThreeTenAd-40MPE', 'ThreeTenAd-40MAPE', 'ThreeTenAd-40CV', 'ThreeTenAd-30MPE', 'ThreeTenAd-30MAPE', 'ThreeTenAd-30CV', 'ThreeTenAd-20MPE', 'ThreeTenAd-20MAPE', 'ThreeTenAd-20CV', 'ThreeTenAd-10MPE', 'ThreeTenAd-10MAPE', 'ThreeTenAd-10CV', 'ThreeTenAd0MPE', 'ThreeTenAd0MAPE', 'ThreeTenAd0CV', 'ThreeTenAd10MPE', 'ThreeTenAd10MAPE', 'ThreeTenAd10CV', 'ThreeTenAd20MPE', 'ThreeTenAd20MAPE', 'ThreeTenAd20CV', 'ThreeTenAd30MPE', 'ThreeTenAd30MAPE', 'ThreeTenAd30CV', 'ThreeTenAd40MPE', 'ThreeTenAd40MAPE', 'ThreeTenAd40CV', 'ThreeTenAd50MPE', 'ThreeTenAd50MAPE', 'ThreeTenAd50CV', 'FourNintyAdMPE', 'FourNintyAdMAPE', 'FourNintyAdCV', 'FourNintyAd-50MPE', 'FourNintyAd-50MAPE', 'FourNintyAd-50CV', 'FourNintyAd-40MPE', 'FourNintyAd-40MAPE', 'FourNintyAd-40CV', 'FourNintyAd-30MPE', 'FourNintyAd-30MAPE', 'FourNintyAd-30CV', 'FourNintyAd-20MPE', 'FourNintyAd-20MAPE', 'FourNintyAd-20CV', 'FourNintyAd-10MPE', 'FourNintyAd-10MAPE', 'FourNintyAd-10CV', 'FourNintyAd0MPE', 'FourNintyAd0MAPE', 'FourNintyAd0CV', 'FourNintyAd10MPE', 'FourNintyAd10MAPE', 'FourNintyAd10CV', 'FourNintyAd20MPE', 'FourNintyAd20MAPE', 'FourNintyAd20CV', 'FourNintyAd30MPE', 'FourNintyAd30MAPE', 'FourNintyAd30CV', 'FourNintyAd40MPE', 'FourNintyAd40MAPE', 'FourNintyAd40CV', 'FourNintyAd50MPE', 'FourNintyAd50MAPE', 'FourNintyAd50CV', 'TF-FTAdMPE', 'TF-FTAdMAPE', 'TF-FTAdCV', 'TF-FTAd-50MPE', 'TF-FTAd-50MAPE', 'TF-FTAd-50CV', 'TF-FTAd-40MPE', 'TF-FTAd-40MAPE', 'TF-FTAd-40CV', 'TF-FTAd-30MPE', 'TF-FTAd-30MAPE', 'TF-FTAd-30CV', 'TF-FTAd-20MPE', 'TF-FTAd-20MAPE', 'TF-FTAd-20CV', 'TF-FTAd-10MPE', 'TF-FTAd-10MAPE', 'TF-FTAd-10CV', 'TF-FTAd0MPE', 'TF-FTAd0MAPE', 'TF-FTAd0CV', 'TF-FTAd10MPE', 'TF-FTAd10MAPE', 'TF-FTAd10CV', 'TF-FTAd20MPE', 'TF-FTAd20MAPE', 'TF-FTAd20CV', 'TF-FTAd30MPE', 'TF-FTAd30MAPE', 'TF-FTAd30CV', 'TF-FTAd40MPE', 'TF-FTAd40MAPE', 'TF-FTAd40CV', 'TF-FTAd50MPE', 'TF-FTAd50MAPE', 'TF-FTAd50CV', 'FF-TTAdMPE', 'FF-TTAdMAPE', 'FF-TTAdCV', 'FF-TTAd-50MPE', 'FF-TTAd-50MAPE', 'FF-TTAd-50CV', 'FF-TTAd-40MPE', 'FF-TTAd-40MAPE', 'FF-TTAd-40CV', 'FF-TTAd-30MPE', 'FF-TTAd-30MAPE', 'FF-TTAd-30CV', 'FF-TTAd-20MPE', 'FF-TTAd-20MAPE', 'FF-TTAd-20CV', 'FF-TTAd-10MPE', 'FF-TTAd-10MAPE', 'FF-TTAd-10CV', 'FF-TTAd0MPE', 'FF-TTAd0MAPE', 'FF-TTAd0CV', 'FF-TTAd10MPE', 'FF-TTAd10MAPE', 'FF-TTAd10CV', 'FF-TTAd20MPE', 'FF-TTAd20MAPE', 'FF-TTAd20CV', 'FF-TTAd30MPE', 'FF-TTAd30MAPE', 'FF-TTAd30CV', 'FF-TTAd40MPE', 'FF-TTAd40MAPE', 'FF-TTAd40CV', 'FF-TTAd50MPE', 'FF-TTAd50MAPE', 'FF-TTAd50CV']

	final_data = np.array([headers, existingAverageList, springAvgList, summerAvgList, fallAvgList, winterAvgList, 
							milpitasAvgList, fresnoAvgList, stocktonAvgList, concordAvgList, potreroAvgList, 
							sacramentoAvgList, cupertinoAvgList, santacruzAvgList, marysvilleAvgList, colmaAvgList, 
							eurekaAvgList, 
							AvgList11, AvgList22, AvgList53, AvgList45, AvgList81, AvgList71, AvgList72, AvgList62])

	# formatting this as a string allows us to include headers and NaNs, but means that the first and last
	# entries will have a '[' or a ']' included
	# np.savetxt('Errors/all_error_results_{}_{}.csv'.format(input_program, number), final_data, fmt='%s') 
	np.savetxt('Errors/all_error_results_{}_{}.csv'.format(input_program, number), final_data, fmt='%s') 
	np.savetxt('../Dropbox/PGEerrors/all_error_results_{}_{}.csv'.format(input_program, number), final_data, fmt='%s') 
	print("Corrupt SAIDs:",corrupt_count)
	print("Complete")

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
calculateSpecificErrors('RES_WEEKEND_15_HOT', 13, 30)

calculateSpecificErrors('RES_WEEKDAY_15_HOT', 13, 500)

calculateSpecificErrors('NONRES_WEEKDAY_15_HOT', 13, 500)
calculateSpecificErrors('NONRES_WEEKEND_15_HOT', 13, 500)
