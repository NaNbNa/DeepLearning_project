import keras
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras import optimizers

# mac解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
# 第一行当索引，不会被使用
dataset = pd.read_csv("/Users/ctb/Downloads/PyProject/project/csv/water_quantity.csv", index_col=[0])
# print(dataset)

# 设置训练集的长度
training_len = 1483 - 200

# 获取训练量(切块函数)
training_set = dataset.iloc[:training_len, [0]]

# 获取测试集
test_set = dataset.iloc[training_len:, [0]]

# 数据归一化
sc = MinMaxScaler(feature_range=(0, 1))
train_set_scaled = sc.fit_transform(training_set)
test_set = sc.fit_transform(test_set)

# 设置训练集特征和训练集标签
x_train = []
y_train = []

# 设置测试集特征和标签
x_test = []
y_test = []

# 进行训练集特征和标签的制作,水质数据一天2小时一测，一天测12次，读取连续12次作为标签

for i in range(6, len(train_set_scaled)):
    x_train.append(train_set_scaled[i-6:i, 0])
    y_train.append(train_set_scaled[i, 0])

# 将训练集用list转化为array格式
x_train, y_train = np.array(x_train), np.array(y_train)

# LSTM训练的特征格式：[样本数，循环的时间步，特征个数]
x_train = np.reshape(x_train, (x_train.shape[0], 6, 1))
# print(x_train)
"""
分界限
"""
# 进行测试集特征和标签的制作

for i in range(6, len(test_set)):
    x_test.append(test_set[i-6:i, 0])
    y_test.append(test_set[i, 0])

# 将训练集用list转化为array格式
x_test, y_test = np.array(x_test), np.array(y_test)

# LSTM训练的特征格式：[样本数，循环的时间步，特征个数]
x_test = np.reshape(x_test, (x_test.shape[0], 6, 1))
# print(x_test)
# print(y_test)

# 利用keras搭建神经网络
model = keras.Sequential()
model.add(LSTM(80, return_sequences=True, activation='relu'))
model.add(LSTM(100, return_sequences=False, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(1))

# 对修建好的模型进行编译,0.01是学习深度(精度) 优化器SDG可以替换为更好的优化器Adam
model.compile(loss='mse', optimizer=optimizers.Adam(1e-5))

# 对数据进行训练:每批次送入的数据为bach_size个，一共训练epochs轮，将测试集样本放入神经网络中   测试起验证集的loss值
history = model.fit(x_train, y_train, batch_size=32, epochs=100, validation_data=(x_test, y_test))

# 保存训练好的模型
model.save('model_nh3n.h5')


# 绘制loss值
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='val')
plt.title('LSTM神经网络loss值')
plt.legend()
plt.show()


