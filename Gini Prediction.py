
import pandas as pd
import numpy as np
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense,BatchNormalization
from keras.optimizers import Adam
from keras.layers import Dropout, Flatten
from sklearn.preprocessing import LabelEncoder
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import StandardScaler


dataset = pd.read_csv('gdrive/MyDrive/Deep Learning/Dataset 1.csv')

X = dataset.iloc[:,:8].values
Y = dataset.iloc[:, -1].values
print("Dataset used\n",dataset)
print(X)


label = LabelEncoder()
Y=label.fit_transform(Y)
Y=pd.get_dummies(Y).values


from sklearn.model_selection import train_test_split
X_main, X_test, Y_main, Y_test = train_test_split(X, Y, test_size=0.2) # splitting test data to 20%
X_train, X_val, Y_train, Y_val = train_test_split(X_main,Y_main,test_size=0.2) # splitting training and validation sets
print("Training data X(Attributes) - ",X_train.shape)
print("Training data Y(Gini values) - ",Y_train.shape)
print("Testing data X(Attributes) - ",X_test.shape)
print("Testing data Y(Gini values) - ",Y_test.shape)
print("Validation data X(Attributes) - ",X_val.shape)
print("Validation data Y(Gini values) - ",Y_val.shape)

gini_test = np.empty(50,dtype=int)
for i in range(50):
  gini_test[i]= np.argmax(Y_test[i])
gini_test = label.inverse_transform(gini_test)
print("Test data gini values\n",gini_test)


year = X_test[:,0]
quarter = X_test[:,1]

scaled = StandardScaler()
scaled.fit(X_train)
X_train = scaled.transform(X_train)
X_test = scaled.transform(X_test)
X_val = scaled.transform(X_val)
print("Training X attributes after Scaling\n",X_train)


def Model():
  nodes = 100

  model = Sequential()  # stacks sequential layers from i/p to o/p

  model.add(Dense(nodes, activation='relu'))  # fully connected layer where output from previous layers are fed to 
  model.add(Dense(nodes, activation='relu'))
  model.add(Dense(nodes, activation='relu'))
  model.add(Dropout(0.5))  # dropping random neurons during training(50 %)
  model.add(Dense(nodes, activation='relu'))  
  model.add(Dropout(0.5))
  model.add(Dense(9,activation='softmax'))  # output layer
  model.compile(Adam(0.001), loss='categorical_crossentropy',
                metrics=['accuracy'])  # configuring to train,adam opt algo,categ crossentr-softmax+cross-entropy loss
  return model


model = Model()
history = model.fit(X_train[:,2:],Y_train,epochs = 2000,validation_data=(X_val[:,2:], Y_val))
                                                                            # training the model with attributes - CPI-AllUrbanConsumers,GDP
modelEvaluation = model.evaluate(X_test[:,2:],Y_test,verbose=0)             # National_Debt,Long Term Interest Rate,Federal Minimum Wage Rates,
                                                                            # Government Expenditures
print('Error = ', modelEvaluation[0])    
print('Test Accuracy =', modelEvaluation[1]*100,"%")

classval = model.predict(X_test[:,2:])
Y_pred = np.empty(50,dtype=int)
for i in range(50):
  Y_pred[i]= np.argmax(classval[i])

Y_pred = label.inverse_transform(Y_pred)
print("Predicted Gini values\n ",Y_pred)

# Display data table

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd


fig, ax = plt.subplots()
      
data = {"year":year, "quarter":quarter, "actual gini":gini_test, "predicted gini":Y_pred}
data_set = pd.DataFrame(data)
data_set = data_set.sort_values(by=['year','quarter'])

fig = go.Figure(data=[go.Table(header=dict(values=['Year','Quarter', 'Actual Gini Index', 'Predicted Gini Index']),
                      cells=dict(values=[data_set['year'], data_set['quarter'], data_set['actual gini'], data_set['predicted gini']]))
                          ])
fig.show()

# Export data table to excel
import pandas
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

data = {"year":year, "quarter":quarter, "actual gini":gini_test, "predicted gini":Y_pred}
data_set = pandas.DataFrame(data)
data_set = data_set.sort_values(by=['year','quarter'])
 
# Save data as data_table.xlsx
data_set.to_excel("data_table.xlsx")

# Visualization of data

import pandas
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

data = {"year":year, "quarter":quarter, "actual gini":gini_test, "predicted gini":Y_pred}
data_set = pandas.DataFrame(data)
data_set = data_set.sort_values(by=['year','quarter'])


year = data_set['year']
actual_gini = data_set['actual gini']

predicted_gini = data_set['predicted gini']

fig, ax = plt.subplots()
ax.plot(year, actual_gini, 'g-')
ax.plot(year, predicted_gini, 'b-')
ax.set_xlabel('Year')
ax.set_ylabel('Gini', rotation='horizontal')
ax.legend(['Actual', 'Predicted'])
    

fig.show()
plt.title('actual vs predicted gini index')
plt.show()