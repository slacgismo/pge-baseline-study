import global_vars
import datetime
import pandas as pd

import matplotlib.pyplot as plt

from helper_functions import *
from error_functions import *
from data_get import *
from calendar_date import *
from baseline_functions import *


def getErrorGraphs(interval_df, DRDays, temp_df, interval):


	startDay = global_vars.GRAPHSTART
	endDay = global_vars.GRAPHEND

	date = startDay

	shift = startDay.day

	errorTenTenNmpe = []
	errorTenTenNmape = []
	errorTenTenNcv = []
	errorTenTenAmpe = []
	errorTenTenAmape = []
	errorTenTenAcv = []

	errorThreeTenNmpe = []
	errorThreeTenNmape = []
	errorThreeTenNcv = []
	errorThreeTenAmpe = []
	errorThreeTenAmape = []
	errorThreeTenAcv = []


	maxtemps = []

	dateCount = 0

	while date < endDay:

		# used for time inputs
		twoPM = pd.to_datetime(('14:00').strip(),format='%H:%M').time()
		eightPM = pd.to_datetime(('20:00').strip(),format='%H:%M').time()

		eventTime = twoPM
		eventStart = twoPM
		eventEnd = eightPM

		errorTenTenN = getTenTenNonAdjustment(interval_df, DRDays, date)
		errorTenTenA, eTTAcap = getTenTenWithAdjustment(interval_df, DRDays, date, twoPM, interval)
		errorThreeTenN = getThreeTenNonAdjustment(interval_df, DRDays, date, twoPM, eightPM)
		errorThreeTenA, eThTAcap = getThreeTenWithAdjustment(interval_df, DRDays, date, twoPM, eightPM, interval)
	
		errorTenTenN = [float(i) for i in errorTenTenN]
		errorTenTenA = [float(i) for i in errorTenTenA]
		errorThreeTenN = [float(i) for i in errorThreeTenN]
		errorThreeTenA = [float(i) for i in errorThreeTenA]

		errorTenTenNmpe.append(errorTenTenN[0])
		errorTenTenNmape.append(errorTenTenN[1])
		errorTenTenNcv.append(errorTenTenN[2])

		errorTenTenAmpe.append(errorTenTenA[0])
		errorTenTenAmape.append(errorTenTenA[1])
		errorTenTenAcv.append(errorTenTenA[2])

		errorThreeTenNmpe.append(errorThreeTenN[0])
		errorThreeTenNmape.append(errorThreeTenN[1])
		errorThreeTenNcv.append(errorThreeTenN[2])

		errorThreeTenAmpe.append(errorThreeTenA[0])
		errorThreeTenAmape.append(errorThreeTenA[1])
		errorThreeTenAcv.append(errorThreeTenA[2])



		maxTemp = getMaxTemp(temp_df, date)

		maxtemps.append(maxTemp)

		dateCount = dateCount + 1
		date = date + datetime.timedelta(days=1)

	x = []
	xr = range(dateCount)
	for num in xr:
		x.append(num + shift)


	plt.plot(x, errorTenTenNmpe, color = 'r', marker = 'o', label = 'Ten Ten non adjust MPE')
	plt.plot(x, errorTenTenAmpe, color = 'm', marker = 'o', label = 'Ten Ten with adjust MPE')

	plt.xlabel('date')
	plt.title('Ten Ten MPE')
	plt.legend()
	plt.tight_layout()
	plt.savefig('tentenmpe.png')
	plt.clf()


	plt.plot(x, errorTenTenNmape, color = 'g', marker = 'o', label = 'Ten Ten non adjust MAPE')
	plt.plot(x, errorTenTenAmape, color = 'y', marker = 'o', label = 'Ten Ten with adjust MAPE')

	plt.xlabel('date')
	plt.title('Ten Ten MAPE')
	plt.legend()
	plt.tight_layout()
	plt.savefig('tentenmape.png')
	plt.clf()


	plt.plot(x, errorTenTenNcv, color = 'b', marker = 'o', label = 'Ten Ten non adjust CV')
	plt.plot(x, errorTenTenAcv, color = 'c', marker = 'o', label = 'Ten Ten with adjust CV')

	plt.xlabel('date')
	plt.title('Ten Ten CV error')
	plt.legend()
	plt.tight_layout()
	plt.savefig('tentencv.png')
	plt.clf()


	plt.plot(x, errorThreeTenNmpe, color = 'r', marker = 'o', label = 'Three Ten non adjust MPE')
	plt.plot(x, errorThreeTenAmpe, color = 'm', marker = 'o', label = 'Three Ten with adjust MPE')

	plt.xlabel('date')
	plt.title('Three Ten error')
	plt.legend()
	plt.tight_layout()
	plt.savefig('threetenmpe.png')
	plt.clf()


	plt.plot(x, errorThreeTenNmape, color = 'g', marker = 'o', label = 'Three Ten non adjust MAPE')
	plt.plot(x, errorThreeTenAmape, color = 'y', marker = 'o', label = 'Three Ten with adjust MAPE')

	plt.xlabel('date')
	plt.title('Three Ten error')
	plt.legend()
	plt.tight_layout()
	plt.savefig('threetenmape.png')
	plt.clf()


	plt.plot(x, errorThreeTenNcv, color = 'b', marker = 'o', label = 'Three Ten non adjust CV')
	plt.plot(x, errorThreeTenAcv, color = 'c', marker = 'o', label = 'Three Ten with adjust CV')

	plt.xlabel('date')
	plt.title('Three Ten CV error')
	plt.legend()
	plt.tight_layout()
	plt.savefig('threetencv.png')
	plt.clf()
