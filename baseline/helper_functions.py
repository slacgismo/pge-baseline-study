from calendar_date import *
from error_functions import *
import numpy as np
import datetime
import global_vars

# getMaxTemp(interval_df, date)
# finds max temp for a date in a interval dataframe
# input
#	temp_df, pandas.Dataframe, contains all temperature data
#	date, pandas.datetime, date to run baselines on 
# output
#	maxTemp, int, max temperature for that day
def getMaxTemp(temp_df, date):

	# get that days rows
	day_rows = temp_df[(temp_df['wea_dttm'] > date + datetime.timedelta(days=1)) & (temp_df['wea_dttm'] < date + datetime.timedelta(days=2))]

	temps_day = day_rows.values[:,3]
	temps_day.astype(int)
	maxTemp = np.amax(temps_day)

	return maxTemp

# getNeededDates(interval_df, DRdays, date, numDays, eligibilty)
# gets past numDays and current days data from interval df
# input
#	interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#	DRdays, list, contains list of DR event dates in datetime form
#	date, pandas.datetime, date to run baselines on
#	numDays, int, previous days to get
#	elibility, bool, True = same type of day, False = all days 
# output
#	interval_array, nparray, interval_df data for those days
#	time_indexes, list, index of times
def getNeededDates(interval_df, DRdays, date, numDays, eligibilty):

	days = getPrevDays(DRdays,date,numDays,eligibilty)

	needed_days_df = interval_df.loc[interval_df['DATE'].isin(days)]

	time_indexes = getTimes(needed_days_df)

	needed_days_df = needed_days_df.sort_values(by='DATE')

	# numberData contains number part of interval_df in nparray form
	numberData = needed_days_df.iloc[:,8:]
	numberData = numberData.values

	# incase of empty entries
	try:
		numberData = numberData.astype(np.float)
	except:
		# print("numberData 1",numberData)
		for x in range(numberData.shape[0]):
			for y in range(numberData.shape[1]):
				if numberData[x,y] == '':
					try: 
						numberData[x,y] = (float(numberData[x,y-1]) + float(numberData[x,y+1]))/2
					except:
						if y != 0:
							numberData[x,y] = float(numberData[x,y-1])
						else:
							numberData[x,y] = 0
		numberData = numberData.astype(np.float)
		# print("numberData 2",numberData)
	return numberData, time_indexes

# getTimes(needed_days_df)
# Turn dataframe into indexable list times. It is indexed the came as columns of numberData, the 8's below is where time column starts. Return indexable times
# inputs
#      needed_days_df, pandas.dataframe, two dimensional array of interval data
# output
#      time_indexes, np.array, 1D array of the column index of times in pd.datetime.time format
def getTimes(needed_days_df):
	
	time_indexes = [None]*len(list(needed_days_df)[8:])

	for columns in range(len(list(needed_days_df)[8:])):
		data = (list(needed_days_df)[8+columns]).strip()
	
		if data == "time2400":
			data = "time0000"
	
		time_indexes[columns] = pd.to_datetime(data, format='time%H%M', errors='ignore').time()    
		
	return time_indexes

# getAdjustment(numberData, time_indexes, eventTime)
# returns the adjustment amount between the average of the energy data for a time period timeInitial, timeFinal between the last row and other rows.
# input
#	interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#	DRdays, list, contains list of DR event dates in datetime form
#	date, pandas.datetime, date to run baselines on 
#	timeInitial, datetime.time, time of start of event
#	interval, int, period between each interval measurement
# output
#	adjustment, float, rate of adjustment
def getAdjustment(numberData, time_indexes, eventTime, interval):
    
    # Identify column of event time
    eventTimeIndex = time_indexes.index(eventTime)
    
    # Identify periods 
    fourHourPriorTimeIndex = int(eventTimeIndex - 240/interval) + 1
    twoHourPriorTimeIndex = int(eventTimeIndex - 120/interval) + 1

   	# split into periods
    unusedDataPrev, splitData, unusedDataPost = np.hsplit(numberData, np.array([fourHourPriorTimeIndex, twoHourPriorTimeIndex]))

    # get both parts
    predictionForPeriod = np.mean(splitData[:splitData.shape[0]-1], axis=0).mean()
    actualForPeriod = splitData[numberData.shape[0]-1,:].mean()

    adjustmentRate = np.divide(actualForPeriod, predictionForPeriod)

    return adjustmentRate

# adjustTimeTemp(tempHours, tempData)
# adjusts the temperature data to fit a hourly format
# input
#	tempHours, pandas.datetime.index, one dimensional array of indexing times for tempData
#	tempData, np.ndarray(), 2d array where rows are days and columns are times (indexed by tempHours), value contains energy usage
# output
#	tempData,np.array, 1d array average energy consumption turned into a hourly format
def adjustTimeTemp(tempHours, tempData):
  
	#get datapoints per hour
	if(tempHours[1].minute-tempHours[0].minute == 0):
		perHour = 1
	else:    
		perHour = int(60/abs(tempHours[1].minute-tempHours[0].minute))

	items = 0
	while items < len(tempHours)-1:
		if tempHours[items].hour == tempHours[items+1].hour:
			tempAverage = 0
			
			#average data points within hour
			for times in range(perHour):
				tempAverage = tempAverage+tempData[items+times]
			tempAverage = tempAverage/perHour
			
			#set all datapoints to average
			for times in range(perHour):
				tempData[items+times] = int(tempAverage)
			items = items + perHour   
		else:
			items = items+1
	
	return tempData

# getNeededDates(interval_df, DRdays, date, numDays, eligibilty)
# gets past numDays and current days data from interval df
# input
#	temp_df, pandas.Dataframe, contains all temperature data
#	DRdays, list, contains list of DR event dates in datetime form
#	date, pandas.datetime, date to run baselines on
#	numDays, int, previous days to get
#	elibility, bool, True = same type of day, False = all days 
# output
#	tempData, nparray, array of temperatures indexed by tempHours
#	tempHours, nparray, array of times indexing tempData
def getPastDaysTemp(temp_df, DRDays, date, numDays, eligibility):

	# print("End date is", date)
	days = getPrevDays(DRDays,date,numDays,eligibility)

	# print("Days are", days, "length", len(days))
	# days = [day.date() for day in days]
	
	data_list = []

	# turn df to nparray, might be a better way
	temp_np = temp_df.values
	
	for row in temp_np:
		if row[2].date() in days:
			data_list.append(row)

	# print("Data list", data_list, "length", len(data_list), len(data_list[0]))

	# data_list = np.array(data_list)
	col_names =  ['wea_stn_cd', 'wea_stn_nm', 'wea_dttm', 'TempFahr', 'RHumidity']
	needed_temp_df = pd.DataFrame(data_list,columns=col_names)
	needed_temp_df = needed_temp_df.sort_values(by='wea_dttm')

	# print("Needed temp df", needed_temp_df, needed_temp_df.shape)

	tempHours = pd.to_datetime(needed_temp_df.iloc[:,2].values)
	tempData = needed_temp_df.iloc[:,3].values

	# print("tempHours", tempHours)
	# print("tempData", tempData)

	return tempHours, tempData

# getCappedAdjustments(prediction)
# returns -50,-40,-30,-20,-10,0,10,20,30,40,50 adjustment list (no 0)
# input
#	prediction, list, predicted baseline for a day
# 	actual, list, actual interval data 
#	adjustment, float, rate of adjustmentfor a day
# output
#	cappedAdjustmentsErrors,list of triples, error rates for each capped adjustment in list form
def getCappedAdjustments(prediction, actual, adjustment):

	if(global_vars.PRINTFLAG >= 2):
		print("adjustment is:", adjustment)

	cappedAdjustmentsErrors = []

	for adjustment_factor in range(-5,6):
		temp_prediction = list(prediction)
		adjustment_rate = float(adjustment_factor)/10+1
		temp_prediction = [data * adjustment_rate for data in temp_prediction]
		
		if (adjustment_factor < 0) & (adjustment_rate > adjustment) & (1 > adjustment):
			if(global_vars.PRINTFLAG >= 2):
				print(adjustment_rate,'adjustment:')
			errors = getErrors(temp_prediction, actual)
			cappedAdjustmentsErrors.append(errors)
		elif (adjustment_factor > 0) & (adjustment_rate < adjustment) & (1 < adjustment):
			if(global_vars.PRINTFLAG >= 2):
				print(adjustment_rate,'adjustment:')
			errors = getErrors(temp_prediction, actual)
			cappedAdjustmentsErrors.append(errors)
		else:
			cappedAdjustmentsErrors.append(['NA','NA','NA'])


	if(global_vars.PRINTFLAG >= 2):
		print("cappedAdjustmentsErrors:",cappedAdjustmentsErrors)

	return cappedAdjustmentsErrors
