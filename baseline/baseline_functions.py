from helper_functions import *
from error_functions import *
from data_get import *
from calendar_date import *
import global_vars
from datetime import datetime

# runBaseline(interval_df, DRDays, temp_df, interval, date, storage_list)
# runs baseline functions for an SAID for given day using passed in data
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       temp_df, pandas.Dataframe, contains all temperature data
#       interval, int, 15 or 60, data collection interval used to find correct sql table
#       date, pandas.datetime, date to run baselines on 
#       storage_list, list, starter list for new row
# output
#       row_data, list, all data including baseline for specific SAID 
def runBaseline(interval_df, DRDays, temp_df, interval, date, storage_list):

		try:
			maxTemp = getMaxTemp(temp_df, date)
			if(global_vars.PRINTFLAG >= 2):
				print("Max Temp is",maxTemp,"F")
		except:
			# print("Failed MaxTemp")
			return 'NA'

		maxTemp = str(maxTemp)

		# used for time inputs
		twoPM = pd.to_datetime(('14:00').strip(),format='%H:%M').time()
		eightPM = pd.to_datetime(('20:00').strip(),format='%H:%M').time()
				
		try:
				errorsTTN = getTenTenNonAdjustment(interval_df, DRDays, date)
		except:
				return 'NA'

		if errorsTTN == 'NA':
				return 'NA'

		try:
				errorsTTA, cappedAdjustmentsErrorsTTA = getTenTenWithAdjustment(interval_df, DRDays, date, twoPM, interval)
		except:
				return 'NA'

		if errorsTTA == 'NA':
				return 'NA'

		errorsThTN =  getThreeTenNonAdjustment(interval_df, DRDays, date, twoPM, eightPM)

		if errorsThTN == 'NA':
				return 'NA'

		try:
				errorsThTA, cappedAdjustmentsErrorsThTA = getThreeTenWithAdjustment(interval_df, DRDays, date, twoPM, eightPM, interval)
		except:
				return 'NA'

		if errorsThTA == 'NA':
				return 'NA'

		try:
				errorsFN, cappedAdjustmentsErrorsFN = getFourNintyWeather(interval_df, DRDays, temp_df, date)
		except:
				return 'NA'

		if errorsFN == 'NA':
				return 'NA'

		if isHoliday(date):
				try:
						errorsF, cappedAdjustmentsErrorsF = getThreeFiveWeather(interval_df, DRDays, temp_df, date)
				except:
						return 'NA'

				if errorsF == 'NA':
						return 'NA'

				if(global_vars.PRINTFLAG >= 2):
						print("errors", errorsF)
						print("cappedAdjustmentsErrors", cappedAdjustmentsErrorsF)

				try:
						errorsT, cappedAdjustmentsErrorsT = getFourFourWeather(interval_df, DRDays, temp_df, date)
				except:
						return 'NA'

				if errorsT == 'NA':
						return 'NA'
		
		#bussinessday
		else:
				try:
						errorsF, cappedAdjustmentsErrorsF = getFiveTenWeather(interval_df, DRDays, temp_df, date)
				except:
						return 'NA'

				if errorsF == 'NA':
						return 'NA'

				try:            
						errorsT, cappedAdjustmentsErrorsT = getTenTenWeather(interval_df, DRDays, temp_df, date)
				except:
						return 'NA'

				if errorsT == 'NA':
						return 'NA'

		today = str(datetime.now().date())

		row_data = [errorsTTN[0], errorsTTN[1], errorsTTN[2], errorsTTA[0], errorsTTA[1], errorsTTA[2], cappedAdjustmentsErrorsTTA[0][0], cappedAdjustmentsErrorsTTA[0][1], cappedAdjustmentsErrorsTTA[0][2], cappedAdjustmentsErrorsTTA[1][0], cappedAdjustmentsErrorsTTA[1][1], cappedAdjustmentsErrorsTTA[1][2], cappedAdjustmentsErrorsTTA[2][0], cappedAdjustmentsErrorsTTA[2][1], cappedAdjustmentsErrorsTTA[2][2], cappedAdjustmentsErrorsTTA[3][0], cappedAdjustmentsErrorsTTA[3][1], cappedAdjustmentsErrorsTTA[3][2], cappedAdjustmentsErrorsTTA[4][0], cappedAdjustmentsErrorsTTA[4][1], cappedAdjustmentsErrorsTTA[4][2], cappedAdjustmentsErrorsTTA[5][0], cappedAdjustmentsErrorsTTA[5][1], cappedAdjustmentsErrorsTTA[5][2], cappedAdjustmentsErrorsTTA[6][0], cappedAdjustmentsErrorsTTA[6][1], cappedAdjustmentsErrorsTTA[6][2], cappedAdjustmentsErrorsTTA[7][0], cappedAdjustmentsErrorsTTA[7][1], cappedAdjustmentsErrorsTTA[7][2],  cappedAdjustmentsErrorsTTA[8][0], cappedAdjustmentsErrorsTTA[8][1], cappedAdjustmentsErrorsTTA[8][2], cappedAdjustmentsErrorsTTA[9][0], cappedAdjustmentsErrorsTTA[9][1], cappedAdjustmentsErrorsTTA[9][2], cappedAdjustmentsErrorsTTA[10][0], cappedAdjustmentsErrorsTTA[10][1], cappedAdjustmentsErrorsTTA[10][2], errorsThTN[0], errorsThTN[1], errorsThTN[2], errorsThTA[0], errorsThTA[1], errorsThTA[2], cappedAdjustmentsErrorsThTA[0][0], cappedAdjustmentsErrorsThTA[0][1], cappedAdjustmentsErrorsThTA[0][2], cappedAdjustmentsErrorsThTA[1][0], cappedAdjustmentsErrorsThTA[1][1], cappedAdjustmentsErrorsThTA[1][2], cappedAdjustmentsErrorsThTA[2][0], cappedAdjustmentsErrorsThTA[2][1], cappedAdjustmentsErrorsThTA[2][2], cappedAdjustmentsErrorsThTA[3][0], cappedAdjustmentsErrorsThTA[3][1], cappedAdjustmentsErrorsThTA[3][2], cappedAdjustmentsErrorsThTA[4][0], cappedAdjustmentsErrorsThTA[4][1], cappedAdjustmentsErrorsThTA[4][2], cappedAdjustmentsErrorsThTA[5][0], cappedAdjustmentsErrorsThTA[5][1], cappedAdjustmentsErrorsThTA[5][2], cappedAdjustmentsErrorsThTA[6][0], cappedAdjustmentsErrorsThTA[6][1], cappedAdjustmentsErrorsThTA[6][2], cappedAdjustmentsErrorsThTA[7][0], cappedAdjustmentsErrorsThTA[7][1], cappedAdjustmentsErrorsThTA[7][2],  cappedAdjustmentsErrorsThTA[8][0], cappedAdjustmentsErrorsThTA[8][1], cappedAdjustmentsErrorsThTA[8][2], cappedAdjustmentsErrorsThTA[9][0], cappedAdjustmentsErrorsThTA[9][1], cappedAdjustmentsErrorsThTA[9][2], cappedAdjustmentsErrorsThTA[10][0], cappedAdjustmentsErrorsThTA[10][1], cappedAdjustmentsErrorsThTA[10][2], errorsFN[0], errorsFN[1], errorsFN[2], cappedAdjustmentsErrorsFN[0][0], cappedAdjustmentsErrorsFN[0][1], cappedAdjustmentsErrorsFN[0][2], cappedAdjustmentsErrorsFN[1][0], cappedAdjustmentsErrorsFN[1][1], cappedAdjustmentsErrorsFN[1][2], cappedAdjustmentsErrorsFN[2][0], cappedAdjustmentsErrorsFN[2][1], cappedAdjustmentsErrorsFN[2][2], cappedAdjustmentsErrorsFN[3][0], cappedAdjustmentsErrorsFN[3][1], cappedAdjustmentsErrorsFN[3][2], cappedAdjustmentsErrorsFN[4][0], cappedAdjustmentsErrorsFN[4][1], cappedAdjustmentsErrorsFN[4][2], cappedAdjustmentsErrorsFN[5][0], cappedAdjustmentsErrorsFN[5][1], cappedAdjustmentsErrorsFN[5][2], cappedAdjustmentsErrorsFN[6][0], cappedAdjustmentsErrorsFN[6][1], cappedAdjustmentsErrorsFN[6][2], cappedAdjustmentsErrorsFN[7][0], cappedAdjustmentsErrorsFN[7][1], cappedAdjustmentsErrorsFN[7][2],  cappedAdjustmentsErrorsFN[8][0], cappedAdjustmentsErrorsFN[8][1], cappedAdjustmentsErrorsFN[8][2], cappedAdjustmentsErrorsFN[9][0], cappedAdjustmentsErrorsFN[9][1], cappedAdjustmentsErrorsFN[9][2], cappedAdjustmentsErrorsFN[10][0], cappedAdjustmentsErrorsFN[10][1], cappedAdjustmentsErrorsFN[10][2], errorsF[0], errorsF[1], errorsF[2], cappedAdjustmentsErrorsF[0][0], cappedAdjustmentsErrorsF[0][1], cappedAdjustmentsErrorsF[0][2], cappedAdjustmentsErrorsF[1][0], cappedAdjustmentsErrorsF[1][1], cappedAdjustmentsErrorsF[1][2], cappedAdjustmentsErrorsF[2][0], cappedAdjustmentsErrorsF[2][1], cappedAdjustmentsErrorsF[2][2], cappedAdjustmentsErrorsF[3][0], cappedAdjustmentsErrorsF[3][1], cappedAdjustmentsErrorsF[3][2], cappedAdjustmentsErrorsF[4][0], cappedAdjustmentsErrorsF[4][1], cappedAdjustmentsErrorsF[4][2], cappedAdjustmentsErrorsF[5][0], cappedAdjustmentsErrorsF[5][1], cappedAdjustmentsErrorsF[5][2], cappedAdjustmentsErrorsF[6][0], cappedAdjustmentsErrorsF[6][1], cappedAdjustmentsErrorsF[6][2], cappedAdjustmentsErrorsF[7][0], cappedAdjustmentsErrorsF[7][1], cappedAdjustmentsErrorsF[7][2],  cappedAdjustmentsErrorsF[8][0], cappedAdjustmentsErrorsF[8][1], cappedAdjustmentsErrorsF[8][2], cappedAdjustmentsErrorsF[9][0], cappedAdjustmentsErrorsF[9][1], cappedAdjustmentsErrorsF[9][2], cappedAdjustmentsErrorsF[10][0], cappedAdjustmentsErrorsF[10][1], cappedAdjustmentsErrorsF[10][2], errorsT[0], errorsT[1], errorsT[2], cappedAdjustmentsErrorsT[0][0], cappedAdjustmentsErrorsT[0][1], cappedAdjustmentsErrorsT[0][2], cappedAdjustmentsErrorsT[1][0], cappedAdjustmentsErrorsT[1][1], cappedAdjustmentsErrorsT[1][2], cappedAdjustmentsErrorsT[2][0], cappedAdjustmentsErrorsT[2][1], cappedAdjustmentsErrorsT[2][2], cappedAdjustmentsErrorsT[3][0], cappedAdjustmentsErrorsT[3][1], cappedAdjustmentsErrorsT[3][2], cappedAdjustmentsErrorsT[4][0], cappedAdjustmentsErrorsT[4][1], cappedAdjustmentsErrorsT[4][2], cappedAdjustmentsErrorsT[5][0], cappedAdjustmentsErrorsT[5][1], cappedAdjustmentsErrorsT[5][2], cappedAdjustmentsErrorsT[6][0], cappedAdjustmentsErrorsT[6][1], cappedAdjustmentsErrorsT[6][2], cappedAdjustmentsErrorsT[7][0], cappedAdjustmentsErrorsT[7][1], cappedAdjustmentsErrorsT[7][2],  cappedAdjustmentsErrorsT[8][0], cappedAdjustmentsErrorsT[8][1], cappedAdjustmentsErrorsT[8][2], cappedAdjustmentsErrorsT[9][0], cappedAdjustmentsErrorsT[9][1], cappedAdjustmentsErrorsT[9][2], cappedAdjustmentsErrorsT[10][0], cappedAdjustmentsErrorsT[10][1], cappedAdjustmentsErrorsT[10][2]]
		row_data.append(today)

		row_data.insert(0, maxTemp)
		 # Holiday is H, Bussiness is B
		if isHoliday(date):
				row_data.insert(0, 'H')
		else:
				row_data.insert(0, 'B')
		row_data.insert(0, date)
		row_data.insert(0, storage_list[2])
		row_data.insert(0, storage_list[1])
		row_data.insert(0, storage_list[0])


		if(global_vars.PRINTFLAG >= 2):
				print("returning row")
		return row_data




def runBaseline2(interval_df, DRDays, temp_df, interval, date, storage_list):

		try:
			maxTemp = getMaxTemp(temp_df, date)
			if(global_vars.PRINTFLAG >= 2):
				print("Max Temp is",maxTemp,"F")
		except:
			# print("Failed MaxTemp")
			return 'NA'

		maxTemp = str(maxTemp)

		# used for time inputs
		twoPM = pd.to_datetime(('14:00').strip(),format='%H:%M').time()
		eightPM = pd.to_datetime(('20:00').strip(),format='%H:%M').time()
				
		try:
				errorsTTN = getTenTenNonAdjustment(interval_df, DRDays, date)
		except:
				return 'NA'

		if errorsTTN == 'NA':
				return 'NA'

		try:
				errorsTTA, cappedAdjustmentsErrorsTTA = getTenTenWithAdjustment(interval_df, DRDays, date, twoPM, interval)
		except:
				return 'NA'

		if errorsTTA == 'NA':
				return 'NA'

		errorsThTN =  getThreeTenNonAdjustment(interval_df, DRDays, date, twoPM, eightPM)

		if errorsThTN == 'NA':
				return 'NA'

		try:
				errorsThTA, cappedAdjustmentsErrorsThTA = getThreeTenWithAdjustment(interval_df, DRDays, date, twoPM, eightPM, interval)
		except:
				return 'NA'

		if errorsThTA == 'NA':
				return 'NA'

		errorsFiveTN =  getFiveTenNonAdjustment(interval_df, DRDays, date, twoPM, eightPM)

		if errorsThTN == 'NA':
				return 'NA'

		try:
				errorsFiveTA, cappedAdjustmentsErrorsFiveTA = getFiveTenWithAdjustment(interval_df, DRDays, date, twoPM, eightPM, interval)
		except:
				return 'NA'

		if errorsThTA == 'NA':
				return 'NA'

		try:
				errorsFN, cappedAdjustmentsErrorsFN = getFourNintyWeather(interval_df, DRDays, temp_df, date)
		except:
				return 'NA'

		if errorsFN == 'NA':
				return 'NA'

		if isHoliday(date):
				try:
						errorsF, cappedAdjustmentsErrorsF = getThreeFiveWeather(interval_df, DRDays, temp_df, date)
				except:
						return 'NA'

				if errorsF == 'NA':
						return 'NA'

				if(global_vars.PRINTFLAG >= 2):
						print("errors", errorsF)
						print("cappedAdjustmentsErrors", cappedAdjustmentsErrorsF)

				try:
						errorsT, cappedAdjustmentsErrorsT = getFourFourWeather(interval_df, DRDays, temp_df, date)
				except:
						return 'NA'

				if errorsT == 'NA':
						return 'NA'
		
		#bussinessday
		else:
				try:
						errorsF, cappedAdjustmentsErrorsF = getFiveTenWeather(interval_df, DRDays, temp_df, date)
				except:
						return 'NA'

				if errorsF == 'NA':
						return 'NA'

				try:            
						errorsT, cappedAdjustmentsErrorsT = getTenTenWeather(interval_df, DRDays, temp_df, date)
				except:
						return 'NA'

				if errorsT == 'NA':
						return 'NA'

		today = str(datetime.now().date())

		row_data = [errorsTTN[0], errorsTTN[1], errorsTTN[2], errorsTTA[0], errorsTTA[1], errorsTTA[2], cappedAdjustmentsErrorsTTA[0][0], cappedAdjustmentsErrorsTTA[0][1], cappedAdjustmentsErrorsTTA[0][2], cappedAdjustmentsErrorsTTA[1][0], cappedAdjustmentsErrorsTTA[1][1], cappedAdjustmentsErrorsTTA[1][2], cappedAdjustmentsErrorsTTA[2][0], cappedAdjustmentsErrorsTTA[2][1], cappedAdjustmentsErrorsTTA[2][2], cappedAdjustmentsErrorsTTA[3][0], cappedAdjustmentsErrorsTTA[3][1], cappedAdjustmentsErrorsTTA[3][2], cappedAdjustmentsErrorsTTA[4][0], cappedAdjustmentsErrorsTTA[4][1], cappedAdjustmentsErrorsTTA[4][2], cappedAdjustmentsErrorsTTA[5][0], cappedAdjustmentsErrorsTTA[5][1], cappedAdjustmentsErrorsTTA[5][2], cappedAdjustmentsErrorsTTA[6][0], cappedAdjustmentsErrorsTTA[6][1], cappedAdjustmentsErrorsTTA[6][2], cappedAdjustmentsErrorsTTA[7][0], cappedAdjustmentsErrorsTTA[7][1], cappedAdjustmentsErrorsTTA[7][2],  cappedAdjustmentsErrorsTTA[8][0], cappedAdjustmentsErrorsTTA[8][1], cappedAdjustmentsErrorsTTA[8][2], cappedAdjustmentsErrorsTTA[9][0], cappedAdjustmentsErrorsTTA[9][1], cappedAdjustmentsErrorsTTA[9][2], cappedAdjustmentsErrorsTTA[10][0], cappedAdjustmentsErrorsTTA[10][1], cappedAdjustmentsErrorsTTA[10][2], errorsThTN[0], errorsThTN[1], errorsThTN[2], errorsThTA[0], errorsThTA[1], errorsThTA[2], cappedAdjustmentsErrorsThTA[0][0], cappedAdjustmentsErrorsThTA[0][1], cappedAdjustmentsErrorsThTA[0][2], cappedAdjustmentsErrorsThTA[1][0], cappedAdjustmentsErrorsThTA[1][1], cappedAdjustmentsErrorsThTA[1][2], cappedAdjustmentsErrorsThTA[2][0], cappedAdjustmentsErrorsThTA[2][1], cappedAdjustmentsErrorsThTA[2][2], cappedAdjustmentsErrorsThTA[3][0], cappedAdjustmentsErrorsThTA[3][1], cappedAdjustmentsErrorsThTA[3][2], cappedAdjustmentsErrorsThTA[4][0], cappedAdjustmentsErrorsThTA[4][1], cappedAdjustmentsErrorsThTA[4][2], cappedAdjustmentsErrorsThTA[5][0], cappedAdjustmentsErrorsThTA[5][1], cappedAdjustmentsErrorsThTA[5][2], cappedAdjustmentsErrorsThTA[6][0], cappedAdjustmentsErrorsThTA[6][1], cappedAdjustmentsErrorsThTA[6][2], cappedAdjustmentsErrorsThTA[7][0], cappedAdjustmentsErrorsThTA[7][1], cappedAdjustmentsErrorsThTA[7][2],  cappedAdjustmentsErrorsThTA[8][0], cappedAdjustmentsErrorsThTA[8][1], cappedAdjustmentsErrorsThTA[8][2], cappedAdjustmentsErrorsThTA[9][0], cappedAdjustmentsErrorsThTA[9][1], cappedAdjustmentsErrorsThTA[9][2], cappedAdjustmentsErrorsThTA[10][0], cappedAdjustmentsErrorsThTA[10][1], cappedAdjustmentsErrorsThTA[10][2],	errorsFiveTN[0], errorsFiveTN[1], errorsFiveTN[2], errorsFiveTA[0], errorsFiveTA[1], errorsFiveTA[2], cappedAdjustmentsErrorsFiveTA[0][0], cappedAdjustmentsErrorsFiveTA[0][1], cappedAdjustmentsErrorsFiveTA[0][2], cappedAdjustmentsErrorsFiveTA[1][0], cappedAdjustmentsErrorsFiveTA[1][1], cappedAdjustmentsErrorsFiveTA[1][2], cappedAdjustmentsErrorsFiveTA[2][0], cappedAdjustmentsErrorsFiveTA[2][1], cappedAdjustmentsErrorsFiveTA[2][2], cappedAdjustmentsErrorsFiveTA[3][0], cappedAdjustmentsErrorsFiveTA[3][1], cappedAdjustmentsErrorsFiveTA[3][2], cappedAdjustmentsErrorsFiveTA[4][0], cappedAdjustmentsErrorsFiveTA[4][1], cappedAdjustmentsErrorsFiveTA[4][2], cappedAdjustmentsErrorsFiveTA[5][0], cappedAdjustmentsErrorsFiveTA[5][1], cappedAdjustmentsErrorsFiveTA[5][2], cappedAdjustmentsErrorsFiveTA[6][0], cappedAdjustmentsErrorsFiveTA[6][1], cappedAdjustmentsErrorsFiveTA[6][2], cappedAdjustmentsErrorsFiveTA[7][0], cappedAdjustmentsErrorsFiveTA[7][1], cappedAdjustmentsErrorsFiveTA[7][2],  cappedAdjustmentsErrorsFiveTA[8][0], cappedAdjustmentsErrorsFiveTA[8][1], cappedAdjustmentsErrorsFiveTA[8][2], cappedAdjustmentsErrorsFiveTA[9][0], cappedAdjustmentsErrorsFiveTA[9][1], cappedAdjustmentsErrorsFiveTA[9][2], cappedAdjustmentsErrorsFiveTA[10][0], cappedAdjustmentsErrorsFiveTA[10][1], cappedAdjustmentsErrorsFiveTA[10][2], errorsFN[0], errorsFN[1], errorsFN[2], cappedAdjustmentsErrorsFN[0][0], cappedAdjustmentsErrorsFN[0][1], cappedAdjustmentsErrorsFN[0][2], cappedAdjustmentsErrorsFN[1][0], cappedAdjustmentsErrorsFN[1][1], cappedAdjustmentsErrorsFN[1][2], cappedAdjustmentsErrorsFN[2][0], cappedAdjustmentsErrorsFN[2][1], cappedAdjustmentsErrorsFN[2][2], cappedAdjustmentsErrorsFN[3][0], cappedAdjustmentsErrorsFN[3][1], cappedAdjustmentsErrorsFN[3][2], cappedAdjustmentsErrorsFN[4][0], cappedAdjustmentsErrorsFN[4][1], cappedAdjustmentsErrorsFN[4][2], cappedAdjustmentsErrorsFN[5][0], cappedAdjustmentsErrorsFN[5][1], cappedAdjustmentsErrorsFN[5][2], cappedAdjustmentsErrorsFN[6][0], cappedAdjustmentsErrorsFN[6][1], cappedAdjustmentsErrorsFN[6][2], cappedAdjustmentsErrorsFN[7][0], cappedAdjustmentsErrorsFN[7][1], cappedAdjustmentsErrorsFN[7][2],  cappedAdjustmentsErrorsFN[8][0], cappedAdjustmentsErrorsFN[8][1], cappedAdjustmentsErrorsFN[8][2], cappedAdjustmentsErrorsFN[9][0], cappedAdjustmentsErrorsFN[9][1], cappedAdjustmentsErrorsFN[9][2], cappedAdjustmentsErrorsFN[10][0], cappedAdjustmentsErrorsFN[10][1], cappedAdjustmentsErrorsFN[10][2], errorsF[0], errorsF[1], errorsF[2], cappedAdjustmentsErrorsF[0][0], cappedAdjustmentsErrorsF[0][1], cappedAdjustmentsErrorsF[0][2], cappedAdjustmentsErrorsF[1][0], cappedAdjustmentsErrorsF[1][1], cappedAdjustmentsErrorsF[1][2], cappedAdjustmentsErrorsF[2][0], cappedAdjustmentsErrorsF[2][1], cappedAdjustmentsErrorsF[2][2], cappedAdjustmentsErrorsF[3][0], cappedAdjustmentsErrorsF[3][1], cappedAdjustmentsErrorsF[3][2], cappedAdjustmentsErrorsF[4][0], cappedAdjustmentsErrorsF[4][1], cappedAdjustmentsErrorsF[4][2], cappedAdjustmentsErrorsF[5][0], cappedAdjustmentsErrorsF[5][1], cappedAdjustmentsErrorsF[5][2], cappedAdjustmentsErrorsF[6][0], cappedAdjustmentsErrorsF[6][1], cappedAdjustmentsErrorsF[6][2], cappedAdjustmentsErrorsF[7][0], cappedAdjustmentsErrorsF[7][1], cappedAdjustmentsErrorsF[7][2],  cappedAdjustmentsErrorsF[8][0], cappedAdjustmentsErrorsF[8][1], cappedAdjustmentsErrorsF[8][2], cappedAdjustmentsErrorsF[9][0], cappedAdjustmentsErrorsF[9][1], cappedAdjustmentsErrorsF[9][2], cappedAdjustmentsErrorsF[10][0], cappedAdjustmentsErrorsF[10][1], cappedAdjustmentsErrorsF[10][2], errorsT[0], errorsT[1], errorsT[2], cappedAdjustmentsErrorsT[0][0], cappedAdjustmentsErrorsT[0][1], cappedAdjustmentsErrorsT[0][2], cappedAdjustmentsErrorsT[1][0], cappedAdjustmentsErrorsT[1][1], cappedAdjustmentsErrorsT[1][2], cappedAdjustmentsErrorsT[2][0], cappedAdjustmentsErrorsT[2][1], cappedAdjustmentsErrorsT[2][2], cappedAdjustmentsErrorsT[3][0], cappedAdjustmentsErrorsT[3][1], cappedAdjustmentsErrorsT[3][2], cappedAdjustmentsErrorsT[4][0], cappedAdjustmentsErrorsT[4][1], cappedAdjustmentsErrorsT[4][2], cappedAdjustmentsErrorsT[5][0], cappedAdjustmentsErrorsT[5][1], cappedAdjustmentsErrorsT[5][2], cappedAdjustmentsErrorsT[6][0], cappedAdjustmentsErrorsT[6][1], cappedAdjustmentsErrorsT[6][2], cappedAdjustmentsErrorsT[7][0], cappedAdjustmentsErrorsT[7][1], cappedAdjustmentsErrorsT[7][2],  cappedAdjustmentsErrorsT[8][0], cappedAdjustmentsErrorsT[8][1], cappedAdjustmentsErrorsT[8][2], cappedAdjustmentsErrorsT[9][0], cappedAdjustmentsErrorsT[9][1], cappedAdjustmentsErrorsT[9][2], cappedAdjustmentsErrorsT[10][0], cappedAdjustmentsErrorsT[10][1], cappedAdjustmentsErrorsT[10][2]]
		# errorsFiveTN[0], errorsFiveTN[1], errorsFiveTN[2], errorsFiveTA[0], errorsFiveTA[1], errorsFiveTA[2], cappedAdjustmentsErrorsFiveTA[0][0], cappedAdjustmentsErrorsFiveTA[0][1], cappedAdjustmentsErrorsFiveTA[0][2], cappedAdjustmentsErrorsFiveTA[1][0], cappedAdjustmentsErrorsFiveTA[1][1], cappedAdjustmentsErrorsFiveTA[1][2], cappedAdjustmentsErrorsFiveTA[2][0], cappedAdjustmentsErrorsFiveTA[2][1], cappedAdjustmentsErrorsFiveTA[2][2], cappedAdjustmentsErrorsFiveTA[3][0], cappedAdjustmentsErrorsFiveTA[3][1], cappedAdjustmentsErrorsFiveTA[3][2], cappedAdjustmentsErrorsFiveTA[4][0], cappedAdjustmentsErrorsFiveTA[4][1], cappedAdjustmentsErrorsFiveTA[4][2], cappedAdjustmentsErrorsFiveTA[5][0], cappedAdjustmentsErrorsFiveTA[5][1], cappedAdjustmentsErrorsFiveTA[5][2], cappedAdjustmentsErrorsFiveTA[6][0], cappedAdjustmentsErrorsFiveTA[6][1], cappedAdjustmentsErrorsFiveTA[6][2], cappedAdjustmentsErrorsFiveTA[7][0], cappedAdjustmentsErrorsFiveTA[7][1], cappedAdjustmentsErrorsFiveTA[7][2],  cappedAdjustmentsErrorsFiveTA[8][0], cappedAdjustmentsErrorsFiveTA[8][1], cappedAdjustmentsErrorsFiveTA[8][2], cappedAdjustmentsErrorsFiveTA[9][0], cappedAdjustmentsErrorsFiveTA[9][1], cappedAdjustmentsErrorsFiveTA[9][2], cappedAdjustmentsErrorsFiveTA[10][0], cappedAdjustmentsErrorsFiveTA[10][1], cappedAdjustmentsErrorsFiveTA[10][2],

		row_data.append(today)

		row_data.insert(0, maxTemp)
		 # Holiday is H, Bussiness is B
		if isHoliday(date):
				row_data.insert(0, 'H')
		else:
				row_data.insert(0, 'B')
		row_data.insert(0, date)
		row_data.insert(0, storage_list[2])
		row_data.insert(0, storage_list[1])
		row_data.insert(0, storage_list[0])


		if(global_vars.PRINTFLAG >= 2):
				print("returning row")
		return row_data







# runFrequentBaseline(interval_df, DRDays, temp_df, interval, date, storage_list)
# runs baseline functions for an SAID for given day using passed in data
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       temp_df, pandas.Dataframe, contains all temperature data
#       interval, int, 15 or 60, data collection interval used to find correct sql table
#       date, pandas.datetime, date to run baselines on 
#       storage_list, list, starter list for new row
# output
#       row_data, list, all data including baseline for specific SAID 
def runFrequentBaseline(interval_df, DRDays, temp_df, interval, date, storage_list):

	try:
		maxTemp = getMaxTemp(temp_df, date)
		if(global_vars.PRINTFLAG >= 2):
			print("Max Temp is",maxTemp,"F")
	except:
		print("Might be error with python version if this prints many times, try Python 3.5.5")
		return 'NA'

	maxTemp = str(maxTemp)

	# used for time inputs
	twoAM = pd.to_datetime(('02:00').strip(),format='%H:%M').time() 
	fourAM = pd.to_datetime(('04:00').strip(),format='%H:%M').time() 
	eightAM = pd.to_datetime(('08:00').strip(),format='%H:%M').time()
	tenAM = pd.to_datetime(('10:00').strip(),format='%H:%M').time()
	twoPM = pd.to_datetime(('14:00').strip(),format='%H:%M').time()
	fourPM = pd.to_datetime(('16:00').strip(),format='%H:%M').time() 
	eightPM = pd.to_datetime(('20:00').strip(),format='%H:%M').time()
	tenPM = pd.to_datetime(('22:00').strip(),format='%H:%M').time()		

	event_times = [fourAM, eightAM, tenAM, twoPM, fourPM, eightPM, tenPM]
	event_tuples = [(eightAM, tenAM), (twoPM, fourPM), (eightPM, tenPM), 
					(fourAM, eightAM), (tenAM, twoPM), (fourPM, eightPM),
					(fourAM, tenAM), (tenAM, fourPM), (fourPM, tenPM), 
					(eightAM, fourPM), (twoPM, tenPM)]

	# all data that will be returned for that date
	row_data = []

	try:
		for start_time in event_times:
			errorsTTA, cappedAdjustmentsErrorsTTA = getTenTenWithAdjustment(interval_df, DRDays, date, start_time, interval)
			if errorsTTA == 'NA':
				return 'NA'
			row_data.append(errorsTTA[0])
			row_data.append(errorsTTA[1])
			row_data.append(errorsTTA[2])			
	except:
		return 'NA'

	try:
		for (start_time, end_time) in event_tuples:
			errorsThTN =  getThreeTenNonAdjustment(interval_df, DRDays, date, start_time, end_time)
			if errorsThTN == 'NA':
				return 'NA'
			row_data.append(errorsThTN[0])
			row_data.append(errorsThTN[1])
			row_data.append(errorsThTN[2])				
	except:
		return 'NA'

	try:
		for (start_time, end_time) in event_tuples:
			errorsThTA, cappedAdjustmentsErrorsThTA = getThreeTenWithAdjustment(interval_df, DRDays, date, start_time, end_time, interval)
			if errorsTTA == 'NA':
				return 'NA'
			row_data.append(errorsThTA[0])
			row_data.append(errorsThTA[1])
			row_data.append(errorsThTA[2])				
	except:
		return 'NA'

	today = str(datetime.now().date())

	row_data.append(today)

	row_data.insert(0, maxTemp)
	 # Holiday is H, Bussiness is B
	if isHoliday(date):
		row_data.insert(0, 'H')
	else:
		row_data.insert(0, 'B')
	row_data.insert(0, date)
	row_data.insert(0, storage_list[2])
	row_data.insert(0, storage_list[1])
	row_data.insert(0, storage_list[0])

	if(global_vars.PRINTFLAG >= 2):
			print("returning row")

	return row_data

def runXSPBaseline(interval_df, DRDays, temp_df, interval, date, storage_list):

	# used for time inputs
	twoPM = pd.to_datetime(('14:00').strip(),format='%H:%M').time()
	eightPM = pd.to_datetime(('20:00').strip(),format='%H:%M').time()
			
	try:
		errorsTTN = getTenTenNonAdjustment(interval_df, DRDays, date)
	except:
		errorsTTN = ['NA','NA','NA']

	try:
		errorsTTA, cappedAdjustmentsErrorsTTA = getTenTenWithAdjustment(interval_df, DRDays, date, twoPM, interval)
	except:
		errorsTTA = ['NA','NA','NA']

	try:
		errorsThTN =  getThreeTenNonAdjustment(interval_df, DRDays, date, twoPM, eightPM)
	except:
		errorsThTN = ['NA','NA','NA']

	try:
		errorsThTA, cappedAdjustmentsErrorsThTA = getThreeTenWithAdjustment(interval_df, DRDays, date, twoPM, eightPM, interval)
	except:
		errorsThTA = ['NA','NA','NA'] 

	row_data = [errorsTTN[0], errorsTTN[1], errorsTTN[2], errorsTTA[0], errorsTTA[1], errorsTTA[2], errorsThTN[0], errorsThTN[1], errorsThTN[2], errorsThTA[0], errorsThTA[1], errorsThTA[2]]

	return row_data


# getTenTenNonAdjustment(interval_df, DRdays, date)
# gets error rates for 10-in-10 Baseline with no adjustment
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       date, pandas.datetime, date to run baselines on 
# output
#       error, triple, (cv, rmse, mape)
def getTenTenNonAdjustment(interval_df, DRDays, date):

		# get numpy array interval data for past 10 days and current date (11 rows)
		numberData, time_indexes = getNeededDates(interval_df, DRDays, date, 10, True)

		if numberData.shape[0] <= 10:
			if(global_vars.PRINTFLAG >= 2):
				print("Dataframe has only",numberData.shape[0], "days")

			return 'NA'

		prediction = np.mean(numberData[0:numberData.shape[0]-1], axis=0)
		actual = numberData[numberData.shape[0]-1,:]

		if(global_vars.PRINTFLAG >= 2):
			print("10-in-10 With No Adjustment:")

		errors = getErrors(prediction, actual)

		return errors

# getTenTenWithAdjustment(interval_df, DRdays, date, timeInitial, timeFinal)
# gets error rates for 10-in-10 Baseline with adjustment based on the start and end time
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       date, pandas.datetime, date to run baselines on 
#       eventTime, datetime.time, time of start of event
#       interval, int, period between each interval measurement
# output
#       error, triple, (cv, rmse, mape)
#       cappedAdjustmentsErrors,list of triples, error rates for each capped adjustment in list form
def getTenTenWithAdjustment(interval_df, DRDays, date, eventTime, interval):

		# get numpy array interval data for past 10 days and current date (11 rows)
		numberData, time_indexes = getNeededDates(interval_df, DRDays, date, 10, True)

		if numberData.shape[0] <= 10:
				if(global_vars.PRINTFLAG >= 2):
						print("Dataframe has only",numberData.shape[0], "days")
				return 'NA','NA'

		prediction = np.mean(numberData[0:numberData.shape[0]-1], axis=0)
		actual = numberData[numberData.shape[0]-1,:]

		adjustment = getAdjustment(numberData, time_indexes, eventTime, interval)

		if(global_vars.PRINTFLAG >= 2):
				print("10-10 With Adjustment Capped:")
		# -50,-40,-30,-20,-10,0 ,10,20,30,40,50 adjustment list (no)
		cappedAdjustmentsErrors = getCappedAdjustments(prediction, actual, adjustment)

		prediction = [data * adjustment for data in prediction]

		# print("10pred", prediction)

		if(global_vars.PRINTFLAG >= 2):
				print("10-in-10 With Adjustment:")
		errors = getErrors(prediction, actual)
		return errors, cappedAdjustmentsErrors

# getThreeTenNonAdjustment(interval_df, DRdays, date)
# gets error rates for 3-in-10 Baseline (top three days of the last 10) with no adjustment
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       date, pandas.datetime, date to run baselines on 
#       eventStart, datetime.time, event start time
#       eventEnd, datetime.time, event end time
# output
#       error, triple, (cv, rmse, mape)
def getThreeTenNonAdjustment(interval_df, DRDays, date, eventStart, eventEnd):

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
				
		prediction = np.mean(numberData[max_rows], axis=0)
		actual = numberData[numberData.shape[0]-1,:]

		if(global_vars.PRINTFLAG >= 2):
				print("3-in-10 With No Adjustment:")
		errors = getErrors(prediction, actual)
		return errors

# getThreeTenWithAdjustment(interval_df, DRdays, date, eventTime, interval)
# gets error rates for 3-in-10 Baseline (top three days of the last 10) with adjustment
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       date, pandas.datetime, date to run baselines on 
#       eventTime, datetime.time, time of start of event
#       eventEnd, datetime.time, event end time
#       interval, int, period between each interval measurement
# output
#       error, triple, (cv, rmse, mape)
#       cappedAdjustmentsErrors,list of triples, error rates for each capped adjustment in list form
def getThreeTenWithAdjustment(interval_df, DRDays, date, eventTime, eventEnd, interval):

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
		actual = numberData[numberData.shape[0]-1,:]
 
		max_rows = max_rows.tolist()
		max_rows.append(numberData.shape[0]-1)

		# max_rows = np.vstack([max_rows, newrow])

		adjustment = getAdjustment(numberData[max_rows], time_indexes, eventTime, interval)
		
		# print("ey\n",numberData[max_rows])

		# print("adjustment",adjustment)

		if(global_vars.PRINTFLAG >= 2):
				print("3-10 With Adjustment Capped:")
		# -50,-40,-30,-20,-10,0 ,10,20,30,40,50 adjustment list (no)
		cappedAdjustmentsErrors = getCappedAdjustments(prediction, actual, adjustment)

		if(global_vars.PRINTFLAG >= 2):
				print("adjustment", adjustment)

		prediction = [data * adjustment for data in prediction]

		# print("3pred", prediction)

		if(global_vars.PRINTFLAG >= 2):
				print("3-in-10 With Adjustment:")

		errors = getErrors(prediction, actual)
		return errors, cappedAdjustmentsErrors


# getThreeTenNonAdjustment(interval_df, DRdays, date)
# gets error rates for 3-in-10 Baseline (top three days of the last 10) with no adjustment
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       date, pandas.datetime, date to run baselines on 
#       eventStart, datetime.time, event start time
#       eventEnd, datetime.time, event end time
# output
#       error, triple, (cv, rmse, mape)
def getFiveTenNonAdjustment(interval_df, DRDays, date, eventStart, eventEnd):

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
		max_rows = numberData_row_part_totals.argsort()[-5:][::-1]
				
		prediction = np.mean(numberData[max_rows], axis=0)
		actual = numberData[numberData.shape[0]-1,:]

		if(global_vars.PRINTFLAG >= 2):
				print("3-in-10 With No Adjustment:")
		errors = getErrors(prediction, actual)
		return errors

# getThreeTenWithAdjustment(interval_df, DRdays, date, eventTime, interval)
# gets error rates for 3-in-10 Baseline (top three days of the last 10) with adjustment
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       date, pandas.datetime, date to run baselines on 
#       eventTime, datetime.time, time of start of event
#       eventEnd, datetime.time, event end time
#       interval, int, period between each interval measurement
# output
#       error, triple, (cv, rmse, mape)
#       cappedAdjustmentsErrors,list of triples, error rates for each capped adjustment in list form
def getFiveTenWithAdjustment(interval_df, DRDays, date, eventTime, eventEnd, interval):

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
		max_rows = numberData_row_part_totals.argsort()[-5:][::-1]

		prediction = np.mean(numberData[max_rows], axis=0)
		actual = numberData[numberData.shape[0]-1,:]
 
		max_rows = max_rows.tolist()
		max_rows.append(numberData.shape[0]-1)

		# max_rows = np.vstack([max_rows, newrow])

		adjustment = getAdjustment(numberData[max_rows], time_indexes, eventTime, interval)
		
		# print("ey\n",numberData[max_rows])

		# print("adjustment",adjustment)

		if(global_vars.PRINTFLAG >= 2):
				print("3-10 With Adjustment Capped:")
		# -50,-40,-30,-20,-10,0 ,10,20,30,40,50 adjustment list (no)
		cappedAdjustmentsErrors = getCappedAdjustments(prediction, actual, adjustment)

		if(global_vars.PRINTFLAG >= 2):
				print("adjustment", adjustment)

		prediction = [data * adjustment for data in prediction]

		# print("3pred", prediction)

		if(global_vars.PRINTFLAG >= 2):
				print("3-in-10 With Adjustment:")

		errors = getErrors(prediction, actual)
		return errors, cappedAdjustmentsErrors


# getFourNintyWeather(interval_df, DRDays, temp_df, date)
# runs 4-90 baseline function and return error. Top 4 weather days of any error
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       temp_df, pandas.Dataframe, contains all temperature data
#       date, pandas.datetime, date to run baselines on 
# output
#       error, triple, (cv, rmse, mape)
#       cappedAdjustmentsErrors,list of triples, error rates for each capped adjustment in list form
def getFourNintyWeather(interval_df, DRDays, temp_df, date):

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

		prediction = np.mean(numberData[indexList[:4]], axis=0)
		actual = numberData[numberData.shape[0]-1,:]

		if(global_vars.PRINTFLAG >= 2):
				print("4-90 Weather Capped:")
		# -50,-40,-30,-20,-10,0 ,10,20,30,40,50 adjustment list (no)
		cappedAdjustmentsErrors = getCappedAdjustments(prediction, actual, 1.51)

		if(global_vars.PRINTFLAG >= 2):
				print("4-90 Weather:")
		errors = getErrors(prediction, actual)
		return errors, cappedAdjustmentsErrors

# getFiveTenWeather(interval_df, DRDays, temp_df, date)
# runs 5-10 baseline function and return error. Top 5 weather days of any error
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       temp_df, pandas.Dataframe, contains all temperature data
#       date, pandas.datetime, date to run baselines on 
# output
#       error, triple, (cv, rmse, mape)
#       cappedAdjustmentsErrors,list of triples, error rates for each capped adjustment in list form
def getFiveTenWeather(interval_df, DRDays, temp_df, date):

		tempHours, tempData = getPastDaysTemp(temp_df, DRDays, date, 10, True)

		# Make all tempDatas in the same hour the same
		tempData = adjustTimeTemp(tempHours, tempData)
		# print("td 5-10",len(tempData),date)
		# print(tempData)

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

		# print("5-10", numberData)

		if numberData.shape[0] <= 10:
				if(global_vars.PRINTFLAG >= 2):
						print("Dataframe has only",numberData.shape[0], "days")
				return 'NA','NA'

		prediction = np.mean(numberData[indexList[:5]], axis=0)
		actual = numberData[numberData.shape[0]-1,:]
		
		# print("5-10", prediction)

		if(global_vars.PRINTFLAG >= 2):
				print("5-10 Weather Capped:")
		# -50,-40,-30,-20,-10,0 ,10,20,30,40,50 adjustment list (no)
		cappedAdjustmentsErrors = getCappedAdjustments(prediction, actual, 1.51)

		if(global_vars.PRINTFLAG >= 2):
				print("5-10 Weather:")
		errors = getErrors(prediction, actual)
		return errors, cappedAdjustmentsErrors

# getTenTenWeather(interval_df, DRDays, temp_df, date)
# runs 10-10 baseline function and return error. Top 5 weather days of any error
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       temp_df, pandas.Dataframe, contains all temperature data
#       date, pandas.datetime, date to run baselines on 
# output
#       error, triple, (cv, rmse, mape)
#       cappedAdjustmentsErrors,list of triples, error rates for each capped adjustment in list form
def getTenTenWeather(interval_df, DRDays, temp_df, date):

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

		prediction = np.mean(numberData[indexList[:10]], axis=0)
		actual = numberData[numberData.shape[0]-1,:]

		if(global_vars.PRINTFLAG >= 2):
				print("10-10 Weather Capped:")
		# -50,-40,-30,-20,-10,0 ,10,20,30,40,50 adjustment list (no)
		cappedAdjustmentsErrors = getCappedAdjustments(prediction, actual, 1.51)

		if(global_vars.PRINTFLAG >= 2):
				print("10-10 Weather:")
		errors = getErrors(prediction, actual)
		return errors, cappedAdjustmentsErrors

# getThreeFiveWeather(interval_df, DRDays, temp_df, date)
# runs 3-5 baseline function and return error. Top 5 weather days of any error
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       temp_df, pandas.Dataframe, contains all temperature data
#       date, pandas.datetime, date to run baselines on 
# output
#       error, triple, (cv, rmse, mape)
#       cappedAdjustmentsErrors,list of triples, error rates for each capped adjustment in list form
def getThreeFiveWeather(interval_df, DRDays, temp_df, date):

		tempHours, tempData = getPastDaysTemp(temp_df, DRDays, date, 5, True)
		# print("td",len(tempData))
		# print(tempData)

		# Make all tempDatas in the same hour the same
		tempData = adjustTimeTemp(tempHours, tempData)
		# print("td 3-5",len(tempData), date)
		# print(tempData)

		# Temp measurements per day
		chunksize = 48

		# to split days into seperate rows
		max_days_temp = []

		# try:
		#       for i in range(5):
		#               newRow = max(tempData[(i*chunksize):(i+1)*chunksize])
		#               max_days_temp.append(newRow)
		#               print(max_days_temp)
		# except:
		#       print("Oh No")
		#       return 'NA','NA'

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

		# print("3-5", numberData)

		if numberData.shape[0] <= 5:
				if(global_vars.PRINTFLAG >= 2):
						print("Dataframe has only",numberData.shape[0], "days")
				return 'NA','NA'

		prediction = (numberData[indexList[0]]*0.5)+(numberData[indexList[1]]*0.3)+(numberData[indexList[2]]*0.2)
		actual = numberData[numberData.shape[0]-1,:]

		# print("3-5", prediction)
		# print("3-5 a", actual)

		if(global_vars.PRINTFLAG >= 2):
				print("3-5 Weather Capped:")
		# -50,-40,-30,-20,-10,0 ,10,20,30,40,50 adjustment list (no)
		cappedAdjustmentsErrors = getCappedAdjustments(prediction, actual, 1.51)

		if(global_vars.PRINTFLAG >= 2):
				print("3-5 Weather:")
		errors = getErrors(prediction, actual)

		return errors, cappedAdjustmentsErrors

# getFourFourWeather(interval_df, DRDays, temp_df, date)
# runs 4-4 baseline function and return error. Top 5 weather days of any error
# input
#       interval_df, pandas.Dataframe, contains all interval data relevant to SAID
#       DRdays, list, contains list of DR event dates in datetime form
#       temp_df, pandas.Dataframe, contains all temperature data
#       date, pandas.datetime, date to run baselines on 
# output
#       error, triple, (cv, rmse, mape)
#       cappedAdjustmentsErrors,list of triples, error rates for each capped adjustment in list form
def getFourFourWeather(interval_df, DRDays, temp_df, date):

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

		prediction = np.mean(numberData[indexList[:4]], axis=0)
		actual = numberData[numberData.shape[0]-1,:]

		if(global_vars.PRINTFLAG >= 2):
				print("4-4 Weather Capped:")
		# -50,-40,-30,-20,-10,0 ,10,20,30,40,50 adjustment list (no)
		cappedAdjustmentsErrors = getCappedAdjustments(prediction, actual, 1.51)

		if(global_vars.PRINTFLAG >= 2):
				print("4-4 Weather:")
		errors = getErrors(prediction, actual)
		return errors, cappedAdjustmentsErrors

							
										  
