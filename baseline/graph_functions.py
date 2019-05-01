import global_vars
import datetime
import pandas as pd

import matplotlib.pyplot as plt

from helper_functions import *
from error_functions import *
from data_get import *
from calendar_date import *

def getBaselineGraphs(interval_df, DRDays, temp_df, interval):


	startDay = global_vars.GRAPHSTART
	endDay = global_vars.GRAPHEND

	date = startDay

	shift = startDay.day

	allPredictTenTenN = []
	allPredictTenTenA = []
	allPredictThreeTenN = []
	allPredictThreeTenA = []
	allPredictFourNintyW = []
	allPredictFiveTenW = []
	allPredictTenTenW = []
	allPredictThreeFiveW = []
	allPredictFourFourW = []

	allAct = []

	maxtemps = []

	dateCount = 0

	while date < endDay:

		# used for time inputs
		twoPM = pd.to_datetime(('14:00').strip(),format='%H:%M').time()
		eightPM = pd.to_datetime(('20:00').strip(),format='%H:%M').time()

		eventTime = twoPM
		eventStart = twoPM
		eventEnd = eightPM


		predictionTenTen, actualTenTen = getTenTenNonAdjustmentGraph(interval_df, DRDays, date)
		predictionTenTenA, actualTenTenA = getTenTenWithAdjustmentGraph(interval_df, DRDays, date, eventTime, interval)
		predictionThreeTen, actualThreeTen = getThreeTenNonAdjustmentGraph(interval_df, DRDays, date, eventStart, eventEnd)
		predictionThreeTenA, actualThreeTenA = getThreeTenWithAdjustmentGraph(interval_df, DRDays, date, eventTime, eventEnd, interval)
		predictionFourNintyW, actualFourNintyW = getFourNintyWeatherGraph(interval_df, DRDays, temp_df, date)
		predictionFiveTenW, actualFiveTenW = getFiveTenWeatherGraph(interval_df, DRDays, temp_df, date)
		predictionTenTenW, actualTenTenW = getTenTenWeatherGraph(interval_df, DRDays, temp_df, date)
		predictionThreeFiveW, actualThreeFiveW = getThreeFiveWeatherGraph(interval_df, DRDays, temp_df, date)
		predictionFourFourW, actualFourFourW = getFourFourWeatherGraph(interval_df, DRDays, temp_df, date)

		allPredictTenTenN.extend(predictionTenTen.tolist())
		allPredictTenTenA.extend(predictionTenTenA)
		allPredictThreeTenN.extend(predictionThreeTen.tolist())
		allPredictThreeTenA.extend(predictionThreeTenA)
		allPredictFourNintyW.extend(predictionFourNintyW.tolist())
		allPredictFiveTenW.extend(predictionFiveTenW.tolist())
		allPredictTenTenW.extend(predictionTenTenW)
		allPredictThreeFiveW.extend(predictionThreeFiveW)
		allPredictFourFourW.extend(predictionFourFourW.tolist())

		allAct.extend(actualTenTen)
	
		a_day = []

		x = range(96)
		for num in x:
			a_day.append(float(num/4))	

		# only uncomment if a plot for each day is needed

		# plt.plot(a_day,actualTenTen, color='r', label='Actual')

		# plt.xlabel('Hours')
		# plt.ylabel('kWh')
		# plt.title('Daily Plot')
		# plt.legend()
		# plt.savefig('actual_%s.png' %date.strftime("%B%d,%Y"))
		# plt.clf()

		maxTemp = getMaxTemp(temp_df, date)

		maxtemps.append(maxTemp)

		dateCount = dateCount + 1
		date = date + datetime.timedelta(days=1)
	
	a = []

	x = range(dateCount*96)
	for num in x:
		a.append(float(num/96) + shift)

	xt = []
	xtr = range(dateCount)
	for num in xtr:
		xt.append(num + shift)
	
	plt.plot(xt, maxtemps, color='r', marker='o',label='Max temperatures')
	plt.title('Maximum Temperature Plot')
	plt.xlabel('Days')
	plt.ylabel('F')
	plt.tight_layout()	
	plt.savefig('maxtemps.png')
	plt.clf()


	plt.plot(a, allPredictTenTenN, color='b', label = 'Ten Ten no adjustment')
	plt.plot(a, allPredictTenTenA, color='g', label = 'Ten Ten with adjustment')
	plt.plot(a, allAct, color='r', label='Actual')

	plt.xlabel('Days')
	plt.ylabel('kWh')
	plt.title('Ten Ten Baseline Plot')
	plt.legend()
	plt.tight_layout()
	plt.savefig('tentenplot.png')
	plt.clf()



	plt.plot(a, allPredictThreeTenN, color='b', label = 'Three Ten no adjustment')
	plt.plot(a, allPredictThreeTenA, color='g', label = 'Three Ten with adjustment')
	plt.plot(a, allAct, color='r', label='Actual')

	plt.xlabel('Days')
	plt.ylabel('kWh')
	plt.title('Three Ten Baseline Plot')
	plt.legend()
	plt.tight_layout()
	plt.savefig('threetenplot.png')
	plt.clf()



	plt.plot(a, allPredictFourNintyW, color='b', label = 'Four Ninety Weather')
	plt.plot(a, allPredictFiveTenW, color='g', label = 'Five Ten Weather')
	plt.plot(a, allPredictTenTenW, color='m', label = 'Ten Ten Weather')
	plt.plot(a, allAct, color='r', label='Actual')

	plt.xlabel('Days')
	plt.ylabel('kWh')
	plt.title('Four Ninety, Five Ten, and Ten Ten Weather')
	plt.legend()
	plt.tight_layout()
	plt.savefig('fivetententenplot.png')
	plt.clf()



	plt.plot(a, allPredictFourNintyW, color='b', label = 'Four Ninety Weather')
	plt.plot(a, allPredictThreeFiveW, color='g', label = 'Three Five Weather')
	plt.plot(a, allPredictFourFourW, color='m', label = 'Four Four Weather')
	plt.plot(a, allAct, color='r', label='Actual')

	plt.xlabel('Days')
	plt.ylabel('kWh')
	plt.title('Four Ninety, Three Five, and Four Four Weather')
	plt.legend()
	plt.tight_layout()
	plt.savefig('threefivefourfourplot.png')
	plt.clf()



	plt.plot(a, allPredictFourNintyW, color='b', label = 'Four Ninety Weather')
	plt.plot(a, allAct, color='r', label='Actual')

	plt.xlabel('Days')
	plt.ylabel('kWh')
	plt.title('Four Ninety Weather')
	plt.legend()
	plt.tight_layout()
	plt.savefig('fourninty.png')
	plt.clf()


	plt.plot(a, allPredictTenTenN, color='b', label = 'Ten Ten Non')
	plt.plot(a, allPredictTenTenW, color='r', label = 'Ten Ten Weather')
	plt.plot(a, allAct, color = 'g', label = 'Actual')

	plt.xlabel('Days')
	plt.ylabel('kWh')
	plt.title('Ten Ten Non/Weather')
	plt.legend()
	plt.tight_layout()
	plt.savefig('tens.png')
	plt.clf()

	# plt.plot(a, allAct, color='r', label='Actual')

	# plt.xlabel('Days')
	# plt.ylabel('kWh')
	# plt.title('actual')
	# plt.legend()
	# plt.savefig('actualdaily.png')
	# plt.clf()

def getTenTenNonAdjustmentGraph(interval_df, DRDays, date):

	# get numpy array interval data for past 10 days and current date (11 rows)
	numberData, time_indexes = getNeededDates(interval_df, DRDays, date, 10, True)

	if numberData.shape[0] <= 10:
		if(global_vars.PRINTFLAG >= 2):
			print("Dataframe has only",numberData.shape[0], "days")
		return 'NA'

	predictionTenTen = np.mean(numberData[0:numberData.shape[0]-1], axis=0)
	actualTenTen = numberData[numberData.shape[0]-1,:]

	return predictionTenTen, actualTenTen



def getTenTenWithAdjustmentGraph(interval_df, DRDays, date, eventTime, interval):

	# get numpy array interval data for past 10 days and current date (11 rows)
	numberData, time_indexes = getNeededDates(interval_df, DRDays, date, 10, True)

	if numberData.shape[0] <= 10:
		if(global_vars.PRINTFLAG >= 2):
			print("Dataframe has only",numberData.shape[0], "days")
		return 'NA','NA'

	prediction = np.mean(numberData[0:numberData.shape[0]-1], axis=0)
	actualTenTenA = numberData[numberData.shape[0]-1,:]

	adjustment = getAdjustment(numberData, time_indexes, eventTime, interval)

	predictionTenTenA = [data * adjustment for data in prediction]
	
	return predictionTenTenA, actualTenTenA



def getThreeTenNonAdjustmentGraph(interval_df, DRDays, date, eventStart, eventEnd):

	# get numpy array interval data for past 10 days and current date (11 rows)
	numberData, time_indexes = getNeededDates(interval_df, DRDays, date, 10, True)

	if numberData.shape[0] <=10:
		if(global_vars.PRINTFLAG >= 2):
			print("Dataframe has only",numberData.shape[0], "days")
		return 'NA','NA'

	numberData = np.asarray(numberData)

	eventStartTimeIndex = time_indexes.index(eventStart)
	eventEndTimeIndex = time_indexes.index(eventEnd)

	numberData_row_part_totals = np.sum(numberData[0:numberData.shape[0]-1, eventStartTimeIndex:eventEndTimeIndex], axis=1)
	max_rows = numberData_row_part_totals.argsort()[-3:][::-1]

	predictionThreeTen = np.mean(numberData[max_rows], axis=0)
	actualThreeTen = numberData[numberData.shape[0]-1,:]

	
	return predictionThreeTen, actualThreeTen



def getThreeTenWithAdjustmentGraph(interval_df, DRDays, date, eventTime, eventEnd, interval):

	# get numpy array interval data for past 10 days and current date (11 rows)
	numberData, time_indexes = getNeededDates(interval_df, DRDays, date, 10, True)

	if numberData.shape[0] <=10:
		if(global_vars.PRINTFLAG >= 2):
			print("Dataframe has only",numberData.shape[0], "days")
		return 'NA','NA'

	numberData = np.asarray(numberData)

	eventStartTimeIndex = time_indexes.index(eventTime)
	eventEndTimeIndex = time_indexes.index(eventEnd)

	numberData_row_part_totals = np.sum(numberData[0:numberData.shape[0]-1, eventStartTimeIndex:eventEndTimeIndex], axis=1)
	max_rows = numberData_row_part_totals.argsort()[-3:][::-1]

	prediction = np.mean(numberData[max_rows], axis=0)
	actualThreeTenA = numberData[numberData.shape[0]-1,:]

	max_rows = max_rows.tolist()
	max_rows.append(numberData.shape[0]-1)

	adjustment = getAdjustment(numberData[max_rows], time_indexes, eventTime, interval)

	predictionThreeTenA = [data * adjustment for data in prediction]

	return predictionThreeTenA, actualThreeTenA



def getFourNintyWeatherGraph(interval_df, DRDays, temp_df, date):

	tempHours, tempData = getPastDaysTemp(temp_df, DRDays, date, 90, False)
	# print("td",len(tempData))
	# print(tempData)

	# Make all tempDatas in the same hour the same
	tempData = adjustTimeTemp(tempHours, tempData)
	# print("td",len(tempData))
	# print(tempData)

	# Temp measurements per day
	chunksize = 48

	# to split days into seperate rows
	max_days_temp = []

	try:
		for i in range(90):
			newRow = max(tempData[(i*chunksize):(i+1)*chunksize])
			max_days_temp.append(newRow)
	except:
		return 'NA','NA'

	# get index of max temps from high to low
	max_days_temp = np.asarray(max_days_temp)
	indexList = list(max_days_temp.argsort())
	indexList.reverse()

	# get numpy array interval data for past 90 days and current date (91 rows)
	numberData, time_indexes = getNeededDates(interval_df, DRDays, date, 90, False)

	if numberData.shape[0] <= 90:
		if(global_vars.PRINTFLAG >= 2):
			print("Dataframe has only",numberData.shape[0], "days")
		return 'NA','NA'

	predictionFourNintyW = np.mean(numberData[indexList[:4]], axis=0)
	actualFourNintyW = numberData[numberData.shape[0]-1,:]

	return predictionFourNintyW, actualFourNintyW



def getFiveTenWeatherGraph(interval_df, DRDays, temp_df, date):

	tempHours, tempData = getPastDaysTemp(temp_df, DRDays, date, 10, True)

	# Make all tempDatas in the same hour the same
	tempData = adjustTimeTemp(tempHours, tempData)

	# Temp measurements per day
	chunksize = 48

	# to split days into seperate rows
	max_days_temp = []

	try:
		for i in range(10):
			newRow = max(tempData[(i*chunksize):(i+1)*chunksize])
			max_days_temp.append(newRow)
	except:
		return 'NA','NA'

	# get index of max temps from high to low
	max_days_temp = np.asarray(max_days_temp)
	indexList = list(max_days_temp.argsort())
	indexList.reverse()

	# get numpy array interval data for past 90 days and current date (91 rows)
	numberData, time_indexes = getNeededDates(interval_df, DRDays, date, 10, True)

	if numberData.shape[0] <= 10:
		if(global_vars.PRINTFLAG >= 2):
			print("Dataframe has only",numberData.shape[0], "days")
		return 'NA','NA'

	predictionFiveTenW = np.mean(numberData[indexList[:5]], axis=0)
	actualFiveTenW = numberData[numberData.shape[0]-1,:]

	return predictionFiveTenW, actualFiveTenW



def getTenTenWeatherGraph(interval_df, DRDays, temp_df, date):

	tempHours, tempData = getPastDaysTemp(temp_df, DRDays, date, 10, True)

	# Make all tempDatas in the same hour the same
	tempData = adjustTimeTemp(tempHours, tempData)

	# Temp measurements per day
	chunksize = 48

	# to split days into seperate rows
	max_days_temp = []

	try:
		for i in range(10):
			newRow = max(tempData[(i*chunksize):(i+1)*chunksize])
			max_days_temp.append(newRow)
	except:
		return 'NA','NA'

	# get index of max temps from high to low
	max_days_temp = np.asarray(max_days_temp)
	indexList = list(max_days_temp.argsort())
	indexList.reverse()

	# get numpy array interval data for past 90 days and current date (91 rows)
	numberData, time_indexes = getNeededDates(interval_df, DRDays, date, 10, True)

	if numberData.shape[0] <= 10:
		if(global_vars.PRINTFLAG >= 2):
			print("Dataframe has only",numberData.shape[0], "days")
		return 'NA','NA'

	predictionTenTenW = np.mean(numberData[indexList[:10]], axis=0)
	actualTenTenW = numberData[numberData.shape[0]-1,:]

	return predictionTenTenW, actualTenTenW



def getThreeFiveWeatherGraph(interval_df, DRDays, temp_df, date):

	tempHours, tempData = getPastDaysTemp(temp_df, DRDays, date, 5, True)
	# print("td",len(tempData))
	# print(tempData)

	# Make all tempDatas in the same hour the same
	tempData = adjustTimeTemp(tempHours, tempData)
	# print("td",len(tempData))
	# print(tempData)

	# Temp measurements per day
	chunksize = 48

	# to split days into seperate rows
	max_days_temp = []

	# try:
	# 	for i in range(5):
	# 		newRow = max(tempData[(i*chunksize):(i+1)*chunksize])
	# 		max_days_temp.append(newRow)
	# 		print(max_days_temp)
	# except:
	# 	print("Oh No")
	# 	return 'NA','NA'

	for i in range(5):
		newRow = max(tempData[(i*chunksize):(i+1)*chunksize])
		max_days_temp.append(newRow)
		# print(max_days_temp)

	# get index of max temps from high to low
	max_days_temp = np.asarray(max_days_temp)
	indexList = list(max_days_temp.argsort())
	indexList.reverse()

	# get numpy array interval data for past 90 days and current date (91 rows)
	numberData, time_indexes = getNeededDates(interval_df, DRDays, date, 5, True)

	# print(numberData)

	if numberData.shape[0] <= 5:
		if(global_vars.PRINTFLAG >= 2):
			print("Dataframe has only",numberData.shape[0], "days")
		return 'NA','NA'

	predictionThreeFiveW = (numberData[indexList[0]]*0.5)+(numberData[indexList[1]]*0.3)+(numberData[indexList[2]]*0.2)
	actualThreeFiveW = numberData[numberData.shape[0]-1,:]

	return predictionThreeFiveW, actualThreeFiveW



def getFourFourWeatherGraph(interval_df, DRDays, temp_df, date):

	tempHours, tempData = getPastDaysTemp(temp_df, DRDays, date, 4, True)

	# Make all tempDatas in the same hour the same
	tempData = adjustTimeTemp(tempHours, tempData)

	# Temp measurements per day
	chunksize = 48

	# to split days into seperate rows
	max_days_temp = []

	try:
		for i in range(4):
			newRow = max(tempData[(i*chunksize):(i+1)*chunksize])
			max_days_temp.append(newRow)
	except:
		return 'NA','NA'

	# get index of max temps from high to low
	max_days_temp = np.asarray(max_days_temp)
	indexList = list(max_days_temp.argsort())
	indexList.reverse()

	# get numpy array interval data for past 90 days and current date (91 rows)
	numberData, time_indexes = getNeededDates(interval_df, DRDays, date, 4, True)

	if numberData.shape[0] <= 4:
		return 'NA','NA'

	predictionFourFourW = np.mean(numberData[indexList[:4]], axis=0)
	actualFourFourW = numberData[numberData.shape[0]-1,:]

	return predictionFourFourW, actualFourFourW


