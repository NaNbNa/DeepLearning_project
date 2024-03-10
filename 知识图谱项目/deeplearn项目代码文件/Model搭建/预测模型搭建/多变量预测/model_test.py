import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from math import sqrt
from keras.models import load_model
import matplotlib.pyplot as plt

# mac解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

dataset = pd.read_csv("/Users/ctb/Downloads/PyProject/project/csv/water_quantity.csv", index_col=[0])
# print(dataset)

# 设置训练集的长度
training_len = 1483 - 200

# 获取测试集
test_set = dataset.iloc[training_len:, [1]]

# 数据归一化
sc = MinMaxScaler(feature_range=(0, 1))
test_set = sc.fit_transform(test_set)

# 设置测试集特征和标签
x_test = []
y_test = []
"""
分界限
"""
# 进行测试集特征和标签的制作

for i in range(12, len(test_set)):
    x_test.append(test_set[i-12:i, 0])
    y_test.append(test_set[i, 0])

# 将训练集用list转化为array格式
x_test, y_test = np.array(x_test), np.array(y_test)

# LSTM训练的特征格式：[样本数，循环的时间步，特征个数]
x_test = np.reshape(x_test, (x_test.shape[0], 12, 1))
# print(x_test.shape)

# 导入模型,并利用模型预测
model = load_model('model.h5')


# 利用模型进行测试,predicted是所预测的值
predicted = model.predict(x_test)
# print(predicted)
# print(predicted.shape)

# 预测值的反归一化
predicted = sc.inverse_transform(predicted)
# print(predicted)

# 对测试集的标签进行反归一化
real = sc.inverse_transform(test_set[12:])
# print(real)

# 打印模型的评价指标
rsme = sqrt(mean_squared_error(predicted, real))
mape = np.mean(np.abs(real-predicted)/predicted)
#  RSME 代表均方根误差，RSME 衡量预测值与真实值之间的离散程度
print('rsme', rsme)
# MAPE 代表平均绝对百分比误差，MAPE 衡量预测值偏差的大小，越小表示模型预测效果越好
print('mape', mape)

# 真实值和预测值的对比
plt.plot(real, label='真实值')
plt.plot(predicted, label='预测值')
plt.title("基于LSTM神经网络的水文数据预测")
plt.legend()
plt.show()
