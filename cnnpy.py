import keras
from keras.layers import *
import numpy as np
import  pandas as  pd

df= pd.read_csv("merge.csv",names=[i for i in range(43)])
data = df.values
result=[]
time_steps = 4 
for i in range(len(data)-time_steps):
	result.append(data[i:i+time_steps].T)
 result=np.array(result)
#训练集和测试集的数据量划分
train_size = int(0.8*len(result))
print(train_size)
#训练集切分
train = result[:train_size,:]
x_train = train[:,:-1]
y_train = train[:,-1][:,-1]
x_test = result[train_size:,:-1]
y_test = result[train_size:,-1][:,-1]

print("X_train", x_train.shape)
print("y_train", y_train.shape)
print("X_test", x_test.shape)
print("y_test", y_test.shape)

#数据重塑
x_train = x_train.reshape(x_train.shape[0],x_train.shape[1],x_train.shape[2])
x_test = x_test.reshape(x_test.shape[0],x_test.shape[1],x_test.shape[2])

#模型构建
model = keras.models.Sequential()
model.add(Conv1D(64, kernel_size=4, activation='relu',input_shape = (42, 4)))
model.add(Conv1D(64, kernel_size=4, activation='relu',input_shape = (42, 4)))
model.add(BatchNormalization())
model.add(Dropout(0.5))#dropoutlayer with a dropout rate of 0.5
model.add(MaxPooling1D(pool_size=2, strides=None, padding='valid'))#A maximum pooling layer with a pool size of 2 was used
model.add(Flatten())
model.add(Dense(10, activation='relu', use_bias=True))#followed by a fully connected layer comprising 10 neurons with the use of the ReLU activation
model.add(Dense(1, activation='sigmoid', use_bias=True))
model.summary()
#模型编译
model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['accuracy'])
#模型训练
from timeit import default_timer as timer
start = timer()
history = model.fit(x_train,y_train,batch_size=128,epochs=50,validation_split=0.2,verbose=2)
end = timer()
print(end - start)
#模型评估
score = model.evaluate(x_test, y_test, batch_size=20)