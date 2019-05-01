import global_vars
import datetime
import pandas as pd 
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

# Set up Calendar
jan1_2016 = pd.to_datetime(20160101, format='%Y%m%d', errors='ignore')
dec31_2017 = pd.to_datetime(20171231, format='%Y%m%d', errors='ignore')
cal = USFederalHolidayCalendar()
holidays = cal.holidays(start=jan1_2016, end=dec31_2017).to_pydatetime()
bday_us = CustomBusinessDay(calendar=cal)
weekendmask = 'Sat Sun'
hday_us = CustomBusinessDay(weekmask=weekendmask)

# isHoliday(date)
# Function that returns if date is holiday
# input
#	date, pandas.datetime, date to check if is a holiday
# output
#	bool, True = holiday, False = not holiday
def isHoliday(date):
	if (date.weekday()>4 | (date in holidays)):
		# print(date.date(), "is a holiday")
		return True
	else:
		# print(date.date(), "is a business day")
		return False

# getPrevDays(DRdays,date,numDays,eligibility)
# gets previous numdays dates 
# input
#	DRDays, list, contains list of DR event dates in datetime form
#	date, pandas.datetime, date to run baselines on
#	numDays, int, previous days to get
#	elibility, bool, True = same type of day, False = all days 
# output
#	dateList, list, list of previous dates
def getPrevDays(DRDays,date,numDays,eligibility):

	dateList = [date] #add all date points 
	
	if(eligibility == True):

		# if holiday
		if(isHoliday(date)):
			for x in range(numDays):
				date = date - hday_us

				if date not in DRDays:
					dateList.append(date)
				else:
					x = x - 1

		# if not holiday
		else: 
			for x in range(numDays):
				date = date - bday_us

				if (date not in DRDays) & (not isHoliday(date)):
					dateList.append(date)
				else:
					x = x - 1
	
	# all days		
	else:
		for x in range(numDays):
			date = date - datetime.timedelta(days=1)

			if date not in DRDays:
				dateList.append(date)
			else:
				x = x - 1
	
	days = []
	for day in dateList:
		# print("day",day)
		if type(day) != datetime.date:
			days.append(day.date())
			# print("changed day",day)
		else:
			days.append(day)
			# print("unchanged")

	# print("Coming days are", days)

	return days