### xsp.py

import pandas
import numpy as np
from sas7bdat import SAS7BDAT
from baseline_functions import *
from datetime import timedelta
import csv
from statistics import mean
import global_vars
global_vars.init()

if False:
	DR_events = {
				6549809230:["10/31/17","11/22/17","12/6/17","12/9/17","12/12/17","12/15/17","12/18/17","12/24/17","12/28/17",
				"12/30/17","1/3/18","1/6/18","1/8/18","1/11/18","1/14/18","1/18/18","1/27/18","1/30/18","2/17/18","2/20/18",
				"2/22/18","2/24/18","2/27/18","3/2/18","3/4/18","3/8/18","3/10/18","3/12/18","3/21/18","3/23/18","3/27/18",
				"4/2/18","4/7/18","4/10/18","4/13/18","4/15/18","4/18/18","4/24/18","4/26/18","5/4/18","5/8/18","5/12/18", 
				"5/14/18","5/16/18","5/20/18","5/22/18"],
				4696091913:["5/12/17","6/7/17","6/10/17","6/13/17","6/16/17","6/22/17","6/25/17","6/26/17","6/28/17","7/6/17",
				"7/8/17","7/12/17","7/16/17","7/17/17","7/25/17","7/28/17","7/31/17","8/4/17","8/7/17","8/10/17","8/13/17",
				"8/16/17","8/19/17","8/22/17","8/27/17","9/1/17","9/6/17","9/9/17","9/13/17","9/14/17","9/17/17","9/20/17",
				"9/25/17","9/30/17","10/8/17","10/10/17","10/13/17","10/15/17","10/19/17","10/25/17","10/29/17","10/30/17",
				"11/3/17","11/6/17","11/9/17","11/11/17","11/14/17","11/18/17","11/26/17","11/29/17","12/4/17","12/7/17",
				"12/10/17","12/15/17","12/20/17","12/23/17","12/27/17","12/30/17","1/5/18","1/10/18","1/13/18","1/16/18",
				"1/18/18","1/21/18","1/27/18","1/29/18","2/18/18","2/20/18","2/24/18","2/26/18","2/28/18","3/2/18","3/5/18",
				"3/6/18","3/14/18","3/17/18","3/23/18","3/25/18","3/27/18","4/3/18","4/6/18","4/11/18","4/14/18","4/16/18",
				"4/19/18","4/22/18","4/29/18","5/6/18","5/8/18","5/12/18","5/14/18","5/16/18","5/22/18","5/25/18","6/2/18",
				"6/5/18","6/9/18"],
				584266842:["5/12/17","6/7/17","6/10/17","6/13/17","6/16/17","6/22/17","6/25/17","6/26/17","6/28/17","7/6/17",
				"7/8/17","7/12/17","7/16/17","7/17/17","7/25/17","7/28/17","7/31/17","8/4/17","8/7/17","8/10/17","8/13/17",
				"8/16/17","8/19/17","8/22/17","8/27/17","9/1/17","9/6/17","9/9/17","9/13/17","9/14/17","9/17/17","9/20/17",
				"9/25/17","9/30/17","10/8/17","10/10/17","10/13/17","10/15/17","10/19/17","10/25/17","10/29/17","10/30/17",
				"11/3/17","11/6/17","11/9/17","11/11/17","11/14/17","11/18/17","11/26/17","11/29/17","12/4/17","12/7/17",
				"12/10/17","12/15/17","12/20/17","12/23/17","12/27/17","12/30/17","1/5/18","1/10/18","1/13/18","1/16/18",
				"1/18/18","1/21/18","1/27/18","1/29/18","2/18/18","2/20/18","2/24/18","2/26/18","2/28/18","3/2/18","3/5/18",
				"3/6/18","3/14/18","3/17/18","3/23/18","3/25/18","3/27/18","4/3/18","4/6/18","4/11/18","4/14/18","4/16/18",
				"4/19/18","4/22/18","4/29/18","5/6/18","5/8/18","5/12/18","5/14/18","5/16/18","5/22/18","5/25/18","6/2/18",
				"6/5/18","6/9/18"],
				2230915856:["6/28/17","7/7/17","8/7/17","8/11/17","8/13/17","8/19/17","8/23/17","8/24/17","8/27/17","8/29/17",
				"9/2/17","9/8/17","9/11/17","9/14/17","9/17/17","9/19/17","9/23/17","9/27/17","10/4/17","10/7/17","10/12/17",
				"10/15/17","10/24/17","10/27/17","10/29/17","10/30/17","11/4/17","11/8/17","11/10/17","11/14/17","11/19/17",
				"11/20/17","11/26/17","11/30/17","12/3/17","12/8/17","12/11/17","12/14/17","12/16/17","12/19/17","12/27/17",
				"12/30/17","1/6/18","1/12/18","1/15/18","1/18/18","1/21/18","1/23/18","1/27/18","1/31/18","2/17/18","2/18/18",
				"2/22/18","2/25/18","2/28/18","3/6/18","3/10/18","3/14/18","3/16/18","3/18/18","3/19/18","3/24/18","3/29/18",
				"4/4/18","4/7/18","4/9/18","4/12/18","4/15/18","4/17/18","4/23/18","4/27/18","5/3/18","5/8/18","5/12/18",
				"5/18/18","5/20/18","5/23/18","6/5/18","6/9/18"],
				2230915314:["6/28/17","7/7/17","8/7/17","8/11/17","8/13/17","8/19/17","8/23/17","8/24/17","8/27/17","8/29/17",
				"9/2/17","9/8/17","9/11/17","9/14/17","9/17/17","9/19/17","9/23/17","9/27/17","10/4/17","10/7/17","10/12/17",
				"10/15/17","10/24/17","10/27/17","10/29/17","10/30/17","11/4/17","11/8/17","11/10/17","11/14/17","11/19/17",
				"11/20/17","11/26/17","11/30/17","12/3/17","12/8/17","12/11/17","12/14/17","12/16/17","12/19/17","12/27/17",
				"12/30/17","1/6/18","1/12/18","1/15/18","1/18/18","1/21/18","1/23/18","1/27/18","1/31/18","2/17/18","2/18/18",
				"2/22/18","2/25/18","2/28/18","3/6/18","3/10/18","3/14/18","3/16/18","3/18/18","3/19/18","3/24/18","3/29/18",
				"4/4/18","4/7/18","4/9/18","4/12/18","4/15/18","4/17/18","4/23/18","4/27/18","5/3/18","5/8/18","5/12/18",
				"5/18/18","5/20/18","5/23/18","6/5/18","6/9/18"],
				1658016832:["3/8/16","3/9/16","3/14/16","3/17/16","3/21/16","3/22/16","3/26/16","3/27/16","4/8/16","4/9/16",
				"4/14/16","4/17/16","4/21/16","4/26/16","4/27/16","4/30/16","5/3/16","5/6/16","5/12/16","5/14/16","5/24/16",
				"5/28/16","5/31/16","6/3/16","6/7/16","6/15/16","6/18/16","6/19/16","6/23/16","6/27/16","6/30/16","7/2/16",
				"7/6/16","7/11/16","7/15/16","7/21/16","7/24/16","7/26/16","7/29/16","8/6/16","8/9/16","8/15/16","8/19/16",
				"8/21/16","8/24/16","8/25/16","8/27/16","9/2/16","9/6/16","9/10/16","9/12/16","9/21/16","9/25/16","9/29/16",
				"9/30/16","10/2/16","10/5/16","10/10/16","10/13/16","10/14/16","10/22/16","10/25/16","10/30/16","11/4/16",
				"11/7/16","11/12/16","11/15/16","11/20/16","11/22/16","11/27/16","11/30/16","12/5/16","12/7/16","12/11/16",
				"12/13/16","12/15/16","12/17/16","12/28/16","12/29/16","1/4/17","1/6/17","1/9/17","1/15/17","1/18/17",
				"1/19/17","1/28/17","1/30/17","2/3/17","2/4/17","2/9/17","2/12/17","2/13/17","2/21/17","2/22/17","2/25/17",
				"3/2/17","3/6/17","3/10/17","3/14/17","3/15/17","3/25/17","3/29/17","3/30/17","4/4/17","4/10/17","4/15/17",
				"4/19/17","4/20/17","4/22/17","4/24/17","4/28/17","5/2/17","5/6/17","5/10/17","5/14/17","5/22/17","5/25/17",
				"5/26/17","5/30/17","6/3/17","6/6/17","6/12/17","6/15/17","6/18/17","6/21/17","6/23/17","6/27/17","7/6/17",
				"7/11/17","7/15/17","7/17/17","7/21/17","7/26/17","7/27/17","7/30/17","8/3/17","8/6/17","8/11/17","8/14/17",
				"8/19/17","8/23/17","8/27/17","8/29/17","9/2/17","9/8/17","9/11/17","9/12/17","9/19/17","9/21/17","9/23/17",
				"9/24/17","9/27/17","10/3/17","10/7/17","10/11/17","10/12/17","10/15/17","10/19/17","10/21/17","10/23/17",
				"10/27/17","11/2/17","11/6/17","11/11/17","11/17/17","11/19/17","11/22/17","11/25/17","11/28/17","12/5/17",
				"12/8/17","12/11/17","12/14/17","12/20/17","12/22/17","12/27/17","12/28/17","1/4/18","1/8/18","1/12/18",
				"1/15/18","1/18/18","1/24/18","1/29/18","1/30/18","2/7/18","2/12/18","2/16/18","2/22/18","2/27/18","3/5/18",
				"3/13/18","3/21/18","3/23/18","3/27/18","4/5/18","4/9/18","4/18/18","4/24/18","4/27/18","5/4/18","5/8/18",
				"5/16/18","5/25/18"],
				6609644067:["1/16/18","1/23/18","1/26/18","1/30/18","1/31/18","2/7/18","2/9/18","2/14/18","2/14/18","2/16/18",
				"2/22/18","2/23/18","2/27/18","2/28/18"],
				2012155022:["1/16/18","1/23/18","1/26/18","1/30/18","1/31/18","2/7/18","2/9/18","2/14/18","2/14/18","2/16/18",
				"2/22/18","2/23/18","2/27/18","2/28/18"],
				6013474815:["1/16/18","1/23/18","1/26/18","1/30/18","1/31/18","2/7/18","2/9/18","2/14/18","2/14/18","2/16/18",
				"2/22/18","2/23/18","2/27/18","2/28/18"]
				}

	SAID_locations = {
				6549809230:"Stockton",
				4696091913:"Merced",
				584266842:"Merced",
				2230915856:"Santa Maria",
				2230915314:"Santa Maria",
				1658016832:"Santa Cruz",
				6609644067:"San Jose",
				2012155022:"San Jose",
				6013474815:"San Jose"
				}

	interval_data = pandas.read_csv("XSPdata/20180606_ExcessSypply_StanfordStudy_2_IntervalData.csv")

	SAID_array = interval_data['sa_id'].unique()

	characteristics_data = pandas.read_excel("XSPdata/20180606_ExcessSypply_StanfordStudy_1_Characteristics.xlsx")
	weather_data = pandas.read_csv('XSPdata/20180606_ExcessSypply_StanfordStudy_3_Weather.csv')

	temp_data = weather_data.loc[(weather_data['wea_data_typ_cd'] == 'Temperature')]

	temp_data['wea_dttm'] = pandas.to_datetime(temp_data['wea_dttm'])
	temp_data['wea_dt'] = pandas.to_datetime(temp_data['wea_dt'])
	temp_data = temp_data.drop(columns=['opr_area_cd', 'wea_data_typ_cd', 'uom', 'wea_stn_cd', 'dst_shft_amt'])
	temp_data = temp_data.sort_values(by='wea_dttm')
	temp_data = temp_data.reset_index(drop=True)

	all_data = []	

	for SAID in SAID_array:

		SAID = int(SAID)
		print("SAID:", SAID)

		# print(characteristics_data.loc(characteristics_data['sa_id'] == SAID))
		
		said_interval_data = interval_data.loc[(interval_data['sa_id'] == SAID)]
		print("Available days",len(said_interval_data))
		said_interval_data['usg_dt'] = pandas.to_datetime(said_interval_data['usg_dt'])
		said_interval_data = said_interval_data.sort_values(by='usg_dt')
		said_interval_data = said_interval_data.drop(columns=['channel6', 'divide_ind', 'sum_ind', 'res_ind', 'ener_dir_cd', 
														'kw_0015', 'kw_0030', 'kw_0045', 'kw_0100', 'kw_0115', 'kw_0130', 
														'kw_0145', 'kw_0200', 'kw_0215', 'kw_0230', 'kw_0245', 'kw_0300', 
														'kw_0315', 'kw_0330', 'kw_0345', 'kw_0400', 'kw_0415', 'kw_0430', 
														'kw_0445', 'kw_0500', 'kw_0515', 'kw_0530', 'kw_0545', 'kw_0600', 
														'kw_0615', 'kw_0630', 'kw_0645', 'kw_0700', 'kw_0715', 'kw_0730', 
														'kw_0745', 'kw_0800', 'kw_0815', 'kw_0830', 'kw_0845', 'kw_0900', 
														'kw_0915', 'kw_0930', 'kw_0945', 'kw_1000', 'kw_1015', 'kw_1030', 
														'kw_1045', 'kw_1100', 'kw_1115', 'kw_1130', 'kw_1145', 'kw_1200', 
														'kw_1215', 'kw_1230', 'kw_1245', 'kw_1300', 'kw_1315', 'kw_1330', 
														'kw_1345', 'kw_1400', 'kw_1415', 'kw_1430', 'kw_1445', 'kw_1500', 
														'kw_1515', 'kw_1530', 'kw_1545', 'kw_1600', 'kw_1615', 'kw_1630', 
														'kw_1645', 'kw_1700', 'kw_1715', 'kw_1730', 'kw_1745', 'kw_1800', 
														'kw_1815', 'kw_1830', 'kw_1845', 'kw_1900', 'kw_1915', 'kw_1930', 
														'kw_1945', 'kw_2000', 'kw_2015', 'kw_2030', 'kw_2045', 'kw_2100', 
														'kw_2115', 'kw_2130', 'kw_2145', 'kw_2200', 'kw_2215', 'kw_2230', 
														'kw_2245', 'kw_2300', 'kw_2315', 'kw_2330', 'kw_2345', 'kw_2400'])
		said_interval_data.insert(3,"DIR",np.nan)

		said_interval_data['usg_dt'] = (pandas.to_datetime(said_interval_data['usg_dt']).apply(lambda x: x.date()))
		said_interval_data.iloc[:,12:] = said_interval_data.iloc[:,12:].convert_objects(convert_numeric=True)
		print("Starting",said_interval_data['usg_dt'].min())
		print("Ending",said_interval_data['usg_dt'].max())
		
		naics = said_interval_data['sa_naics_cd'].unique()[0]

		print("NAICS:",naics)

		if (len(said_interval_data) != len(said_interval_data['usg_dt'].unique())):
			print("Multiple instances of same days found, cleaning dataframe.")
			dates = list(said_interval_data['usg_dt'].unique())
			for date in dates:
				date_interval_data = said_interval_data.loc[(said_interval_data['usg_dt'] == date)]

				if len(date_interval_data) > 1:
					index_max = int(date_interval_data.iloc[:,12:18].sum(axis=1).idxmax())
					all_index = list(date_interval_data.index)
					all_index.remove(index_max)
					for index in all_index:
						said_interval_data.drop(index, inplace=True)
						
			print("Unique days:",len(said_interval_data))

		DR_days = DR_events[SAID]
		DR_days = [datetime.strptime(date, "%m/%d/%y").date() for date in DR_days]

		print("Number of DR days:",len(DR_days))

		weather_df = temp_data.loc[(temp_data["wea_stn_nm"]==SAID_locations[SAID])]
		weather_df = weather_df.reset_index(drop=True)

		print("Weather recieved with shape", weather_df.shape)
		print("running baseline...")
		
		interval = 15
		storage_list = []
		date = said_interval_data['usg_dt'].max()

		min_date = said_interval_data['usg_dt'].min()
		min_date = min_date + timedelta(days=30)

		print("min_date is",min_date)

		said_interval_data.columns = ['SPID', 'SA', 'UOM', 'DIR', 'DATE', 'RS', 'NAICS', 'APCT', 'time0015', 'time0030', 'time0045', 
								'time0100', 'time0115', 'time0130', 'time0145', 'time0200', 'time0215', 'time0230', 'time0245', 
								'time0300', 'time0315', 'time0330', 'time0345', 'time0400', 'time0415', 'time0430', 'time0445', 
								'time0500', 'time0515', 'time0530', 'time0545', 'time0600', 'time0615', 'time0630', 'time0645', 
								'time0700', 'time0715', 'time0730', 'time0745', 'time0800', 'time0815', 'time0830', 'time0845', 
								'time0900', 'time0915', 'time0930', 'time0945', 'time1000', 'time1015', 'time1030', 'time1045', 
								'time1100', 'time1115', 'time1130', 'time1145', 'time1200', 'time1215', 'time1230', 'time1245', 
								'time1300', 'time1315', 'time1330', 'time1345', 'time1400', 'time1415', 'time1430', 'time1445', 
								'time1500', 'time1515', 'time1530', 'time1545', 'time1600', 'time1615', 'time1630', 'time1645', 
								'time1700', 'time1715', 'time1730', 'time1745', 'time1800', 'time1815', 'time1830', 'time1845', 
								'time1900', 'time1915', 'time1930', 'time1945', 'time2000', 'time2015', 'time2030', 'time2045', 
								'time2100', 'time2115', 'time2130', 'time2145', 'time2200', 'time2215', 'time2230', 'time2245', 
								'time2300', 'time2315', 'time2330', 'time2345', 'time2400']	

		weather_df = weather_df[['wea_dt', 'wea_stn_nm', 'wea_dttm',  'meas_val', 'intvl_lgth']]
		weather_df.columns = ['wea_stn_cd', 'wea_stn_nm', 'wea_dttm', 'TempFahr', 'RHumidity']

		while (date.year > 2015) & (date>min_date):
			try:
				row_data = runXSPBaseline(said_interval_data, DR_days, weather_df, interval, date, storage_list)
			except:
				row_data = ['NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA','NA']
				print("skipped")
			row_data.append(date)
			row_data.append(SAID)
			all_data.append(row_data)
			date = date - timedelta(days=1)
			print(date)

		print('\n')


	all_data_array = np.array([np.array(xi) for xi in all_data])

	np.save('xsp_all_days.npy', all_data_array)    # .npy extension is added if not given

	print("Complete")

print("Calculating averages")
all_data_array = np.load('xsp_all_days.npy')

winter  = [[],[],[],[],[],[],[],[],[],[],[],[]]
summer = [[],[],[],[],[],[],[],[],[],[],[],[]]
fall = [[],[],[],[],[],[],[],[],[],[],[],[]]
spring = [[],[],[],[],[],[],[],[],[],[],[],[]]

total = [[],[],[],[],[],[],[],[],[],[],[],[]]

for row in all_data_array:
	for i in range(12):
		if (row[i] != 'NA') & (row[i] != 'nan'):
			total[i].append(float(row[i]))

	date = row[12]
	m = date.month * 100
	d = date.day
	md = m + d

	if ((md >= 301) and (md <= 531)):
		for i in range(12):
			if (row[i] != 'NA') & (row[i] != 'nan'):
				spring[i].append(float(row[i]))
	elif ((md > 531) and (md < 901)):
		for i in range(12):
			if (row[i] != 'NA') & (row[i] != 'nan'):
				summer[i].append(float(row[i]))
	elif ((md >= 901) and (md <= 1130)):
		for i in range(12):
			if (row[i] != 'NA') & (row[i] != 'nan'):
				fall[i].append(float(row[i]))
	else:
		for i in range(12):
			if (row[i] != 'NA') & (row[i] != 'nan'):
				winter[i].append(float(row[i]))

averages_total = []
winter_total = []
summer_total = []
fall_total = []
spring_total = []

for i in range(12):
	averages_total.append(mean(total[i]))
	winter_total.append(mean(winter[i]))
	summer_total.append(mean(summer[i]))
	fall_total.append(mean(fall[i]))
	spring_total.append(mean(spring[i]))	

final_list = [averages_total,spring_total,summer_total,fall_total,winter_total]

with open("xsp_results.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(final_list)

# characteristics_data = pandas.read_excel("XSPdata/DR2617_INTV_ID_XREF.xlsx")
# paticipant_data = pandas.read_excel("XSPdata/xsp_participant_information.xlsx")

# for SAID in SAID_array:
	
# 	print("\nSAID:",SAID)

# 	# participant_all_data = paticipant_data.loc[paticipant_data['SA'] == SAID]
# 	# print(participant_all_data)

# 	SAID_all_data = interval_data.loc[interval_data['sa_id'] == SAID]
	
# 	num_days = len(SAID_all_data)
# 	if num_days < 10:
# 		print("Days of data under 10, skipping SAID.")
# 		continue
# 	print("Days of data:", num_days)

# 	NAICS =  int(list(SAID_all_data['NAICS'])[0])
# 	print("NAICS code:", NAICS)
# 	break
	
# pandas.read_sas('XSPdata/dr2617_bill_y16.sas7bdat')

