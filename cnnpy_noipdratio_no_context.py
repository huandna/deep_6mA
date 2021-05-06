import keras
from keras.layers import *
import numpy as np
import  pandas as  pd
import argparse
import os
parser = argparse.ArgumentParser( description='Put a description of your script here')
parser.add_argument('-i', '--input_file', type=str, required=True, help='Path to an input file to be read' )
parser.add_argument('-o', '--output_file', type=str, required=True, help='Path to an output file to be read' )

args = parser.parse_args()

df= pd.read_csv(args.input_file,names=[i for i in range(106)])
df=df.drop([0],axis=1)
df=df.drop([i for i in range(21,105)],axis=1)
from sklearn.utils import shuffle
df = shuffle(df)
data = df.values
# 这里是一个频道
result=data
data.shape
train_size = int(0.8*len(result))
print(train_size)
#训练集切分
train = result[:train_size]
x_train = train[:,:-1]
y_train = train[:,-1]
x_test = result[train_size:,:-1]
y_test = result[train_size:,-1]
print("X_train", x_train.shape)
print("y_train", y_train.shape)
print("X_test", x_test.shape)
print("y_test", y_test.shape)
x_train = x_train.reshape(x_train.shape[0],x_train.shape[1],1)
x_test = x_test.reshape(x_test.shape[0],x_test.shape[1],1)
model = keras.models.Sequential()
model.add(Conv1D(80, kernel_size=4, activation='relu',input_shape = (20, 1)))
model.add(Conv1D(80, kernel_size=4, activation='relu',input_shape = (20, 1)))
model.add(BatchNormalization())
model.add(Dropout(0.5))#dropoutlayer with a dropout rate of 0.5
model.add(MaxPooling1D(pool_size=2, strides=None, padding='valid'))#A maximum pooling layer with a pool size of 2 was used
model.add(Flatten())
model.add(Dense(10, activation='relu', use_bias=True))#followed by a fully connected layer comprising 10 neurons with the use of the ReLU activation
model.add(Dense(1, activation='sigmoid', use_bias=True))
model.summary()
model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
from timeit import default_timer as timer
start = timer()
history = model.fit(x_train,y_train,batch_size=128,epochs=50,validation_split=0.2,verbose=2)
end = timer()
print(end - start)
score = model.evaluate(x_test, y_test, batch_size=20)
print(score)
import h5py
from keras.models import load_model
model.save(args.output_file)


