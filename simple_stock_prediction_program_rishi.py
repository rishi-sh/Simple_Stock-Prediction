
pip install quandl

#This is a stock prediction program by using ML models
#Install the dependencies
import quandl
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

#Get the stock data
df = quandl.get("WIKI/FB")
#Look at the data
print(df.head())

#Get the adjusted close price 
df= df[['Adj. Close']]
#take a look at the new data
print(df.head())

# A variable for predicting 'n' days out into the future. 
forecast_out= 30
#Create another column(the target or dependent variable), it is going to be shifted 'n' units up
df['Prediction']= df[['Adj. Close']].shift(-forecast_out)
#print out the new data set
print(df.tail())
#df.head and tail indicate the start and the end of the data set respectively.

### Create the independent data set (X) #####
#convert the dataframe to a numpy array
X = np.array(df.drop(['Prediction'],1))
#Remove the last 'n' rows
X = X[:-forecast_out]
print(X)
#this is the a dataset which contains list of lists

### Create the dependent data set (y) ###
# Convert the dataframe to a numpy array (All of the values including the NaN's)
y = np.array(df['Prediction'])
#Get all of the y values except the last 'n' rows
y = y[:-forecast_out]
print(y)
#this is another data set which contains seperate list.

# Split the data into 80% training and 20% testing
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size= 0.2)

# Create and train the Support Vector Machine (Regressor)
svr_rbf = SVR(kernel='rbf' , C=1e3, gamma=0.1)
svr_rbf.fit(x_train,y_train)

#Check how good the model works
# Testing Model: Score returns the coefficient of determination R^2 of the prediction.
# The best possible score is 1.0
svm_cinfidence = svr_rbf.score(x_test,y_test)
print("svm confidence", svm_cinfidence)
#We get a nice confiedence score which is 0.98 which is really close to 1. This is good.

#Create and train a linear regression model
lr = LinearRegression()
#Train the model
lr.fit(x_train, y_train)

# Testing Model: Score returns the coefficient of determination R^2 of the prediction.
# The best possible score is 1.0
#Test the LinearRegression model
lr_cinfidence = lr.score(x_test,y_test)
print("lr confidence", lr_cinfidence)
#lr confidence is 0.982175. So our support vector regressor was better than LinearRegression model.

# Set x_forecast equal to the last 30 rows of the original data set from Adj. Close column 
x_forecast = np.array(df.drop(['Prediction'],1))[-forecast_out:]
print(x_forecast)

#Print LinearRegression model the predictions for the next 'n' days
lr_prediction = lr.predict(x_forecast)
print(lr_prediction)

#Print support vector regressor model the predictions for the next 'n' days
svm_prediction = svr_rbf.predict(x_forecast)
print(svm_prediction)
#Frist we print the LinerRegression model of what the price will be for next 30days. After that it will print the adjusted close price for the next 30 days from our support vector regressor.
