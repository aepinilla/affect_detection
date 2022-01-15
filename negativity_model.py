import pandas as pd


df = pd.read_csv('50_Startups.csv')

#separate the other attributes from the predicting attribute
x = df.drop('Profit',axis=1)
#separte the predicting attribute into Y for model training
y = ['profit']

# importing train_test_split from sklearn
from sklearn.model_selection import train_test_split
# splitting the data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

# importing module
from sklearn.linear_model import LinearRegression
# creating an object of LinearRegression class
LR = LinearRegression()
# fitting the training data
LR.fit(x_train,y_train)

y_prediction =  LR.predict(x_test)
y_prediction