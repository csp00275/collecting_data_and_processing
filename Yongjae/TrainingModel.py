import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers
import matplotlib.pyplot as plt

tf.random.set_seed(1)  # 난수표에서 가지고온 데이터 셋 (일정한 난수)
temp_data = pd.read_csv('C:/Users/Lab/Desktop/forLearing_final.csv')  #

x_data = temp_data.iloc[:,:10] # 10번까지의 데이터 Sx0-Sx9
y_data = temp_data.iloc[:,11:] # 10번이후의 데이터 r theta z

model = tf.keras.Sequential()
model.add(layers.Dense(8, activation = 'relu', input_shape = [x_data.shape[1]]))
model.add(layers.Dense(4,  activation = 'relu'))
model.add(layers.Dense(2))

model.compile(loss = 'mse', optimizer=tf.keras.optimizers.Adam(0.00001), metrics=['mae', 'mse'])

hist = model.fit(x_data, y_data, epochs=10000, verbose=1)

plt.plot(hist.history['loss'])
plt.ylabel('mse')
plt.xlabel('epochs')
plt.show()


model.save('E100_h128_NoR.h5')