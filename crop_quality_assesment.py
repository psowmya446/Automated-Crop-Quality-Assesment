# -*- coding: utf-8 -*-
"""Crop quality assesment

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GuUtLBfM21zvXeqUv0dBOa6R_vELh4gq
"""

!pip install keras

import numpy as np
import pandas as pd
pesticides=pd.read_csv("/content/pesticides (1).csv")
rainfall=pd.read_csv("/content/rainfall (1).csv")
temperature=pd.read_csv("/content/temp.csv")
yield_data=pd.read_csv("/content/yield.csv")
yield_df=pd.read_csv("/content/yield_df.csv")
yield_df.rename({'Area':'Country','hg/ha_yield':'Yield (hg/ha)','average_rain_fall_mm_per_year':'Rainfall (mm)'},axis=1,inplace=True)
yield_df.drop('Unnamed: 0',axis=1,inplace=True)
yield_df.isnull().sum()
from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
yield_df['Country_encoded']=le.fit_transform(yield_df['Country'])
yield_df['Item_encoded']=le.fit_transform(yield_df['Item'])
yield_df.drop(['Country','Item'],axis=1,inplace=True)
for i in yield_df.columns:
    q75, q25 = np.percentile(yield_df[i], [75 ,25])
    iqr = q75 - q25
    min_val = q25 - (iqr*1.5)
    max_val = q75 + (iqr*1.5)
    yield_df=yield_df[(yield_df[i]<max_val)]
    yield_df=yield_df[(yield_df[i]>min_val)]
    Y=yield_df['Yield (hg/ha)']
X=yield_df.drop('Yield (hg/ha)',axis=1)

from sklearn.preprocessing import MinMaxScaler
min_max_scaler=MinMaxScaler()
X_scaled=pd.DataFrame(min_max_scaler.fit_transform(X))
from sklearn. model_selection import train_test_split
from sklearn. datasets import load_iris
x_train,x_test,y_train,y_test=train_test_split(X_scaled,Y,test_size=0.2,random_state=42)
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, GRU, Flatten, Dropout, Lambda
from keras.layers import Embedding
import tensorflow as tf
neural_regressor = tf.keras.models.Sequential()
neural_regressor.add(tf.keras.layers.Dense(units=12, activation='selu',))
neural_regressor.add(tf.keras.layers.Dense(units=12, activation='selu'))
neural_regressor.add(tf.keras.layers.Dense(units=1, activation='linear'))
neural_regressor.compile(optimizer=tf.keras.optimizers.Adam(0.1), loss='mse',metrics=['mean_absolute_error'])
plot_data = neural_regressor.fit(x_train,y_train, epochs=600,)
loss_train = plot_data.history['mean_absolute_error']
epochs = range(1,601)
import matplotlib.pyplot as plt
plt.plot(epochs, loss_train, 'g', label='Training loss')
plt.title('Training loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()
y_pred = neural_regressor.predict(x_test)
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_pred)
print("R2 score: ", r2)
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
print("MSE: ",mean_squared_error(y_test, y_pred))
print("MAE: ",mean_absolute_error(y_test, y_pred))
ry=range(0,len(x_test))
plt.plot(ry, y_test,color='g')
plt.plot(ry, y_pred,color='k')
plt.show()