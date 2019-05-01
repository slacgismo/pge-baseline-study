import global_vars
import numpy as np 
import warnings

# mpe(prediction, actual) 
# input
#	prediction, nparray, prediction for interval data for day
#	actual, nparray, actual interval data
# output
#	returns the Mean Percentage Error between two Numpy Arrays. The two lists must be of the same size and greater than 0.
def mpe(prediction, actual):
	
	np.seterr(all='raise')
	try:
		return np.mean((actual - prediction) / actual) * 100
	except:
		return 'NA'

# cv(prediction, actual) 
# input
#	prediction, nparray, prediction for interval data for day
#	actual, nparray, actual interval data
# output
#	returns the Coefficient of Variation between two Numpy Arrays. The two lists must be of the same size and greater than 0.
def cv(prediction, actual): 
	return rmse(prediction, actual)/np.mean(actual)

# cv(prediction, actual) 
# input
#	prediction, nparray, prediction for interval data for day
#	actual, nparray, actual interval data
# output
#   returns the Root-Mean-Square Error between two Numpy Arrays. The two lists must be of the same size and greater than 0.
def rmse(prediction, actual):
	return np.sqrt(((prediction - actual) ** 2).mean()) 

# cv(prediction, actual) 
# input
#	prediction, nparray, prediction for interval data for day
#	actual, nparray, actual interval data
# output
#   returns the Mean Absolute Percentage Error between two Numpy Arrays. The two lists must be of the same size and no values of 0 in Actual list.
def mape(prediction, actual):
	np.seterr(all='raise')
	try:
		return np.mean(np.abs((actual - prediction) / actual)) * 100
	except:
		return 'NA'

# cv(prediction, actual) 
# input
#	prediction, nparray, prediction for interval data for day
#	actual, nparray, actual interval data
# output
#	triple, (cv,rmse,mape)
def getErrors(prediction, actual):

	# rmse_err = rmse(prediction,actual)

	mpe_err = mpe(prediction, actual)
	mape_err = mape(prediction,actual)
	cv_err = cv(prediction,actual)
	
	if(global_vars.PRINTFLAG >= 2):
		print("MPE is",mpe_err)
		print("MAPE is",mape_err)
		print("CV is",cv_err)
		# print("RMSE is",rmse_err)
	
	mpe_err = str(mpe_err)[0:10]
	mape_err = str(mape_err)[0:10]
	cv_err = str(cv_err)[0:10]

	# print(mpe_err, type(mpe_err))

	return [mpe_err,mape_err,cv_err]
