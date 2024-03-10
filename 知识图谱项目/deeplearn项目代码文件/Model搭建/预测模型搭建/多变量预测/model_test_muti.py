import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from math import sqrt
from keras.models import load_model
import matplotlib.pyplot as plt


def time_series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    """
    :param data:作为列表或2D NumPy数组的观察序列。需要。
    :param n_in:作为输入的滞后观察数（X）。值可以在[1..len（数据）]之间可选。默认为1。
    :param n_out:作为输出的观测数量（y）。值可以在[0..len（数据）]之间。可选的。默认为1。
    :param dropnan:Boolean是否删除具有NaN值的行。可选的。默认为True。
    :return:
    """
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    origNames = df.columns
    cols, names = list(), list()
    cols.append(df.shift(0))
    names += [('%s' % origNames[j]) for j in range(n_vars)]
    n_in = max(0, n_in)
    for i in range(n_in, 0, -1):
        time = '(t-%d)' % i
        cols.append(df.shift(i))
        names += [('%s%s' % (origNames[j], time)) for j in range(n_vars)]
    n_out = max(n_out, 0)
    for i in range(1, n_out + 1):
        time = '(t+%d)' % i
        cols.append(df.shift(-i))
        names += [('%s%s' % (origNames[j], time)) for j in range(n_vars)]
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    if dropnan:
        agg.dropna(inplace=True)
    return agg


"""
"""

path = "/Users/ctb/Downloads/PyProject/project/csv/codcr_tp.csv"
model_path = '/Users/ctb/Downloads/PyProject/project/deeplearn/Model/codcr_tp.h5'
# predict 指的是预测第几行
pre = 1
"""
"""
n_step_in = 9  # 历史时间长度
n_step_out = 1  # 预测时间长度
x_data_l = '0(t-9)'
x_data_r = '1(t-1)'
y_data_l = '0'
y_data_r = '1'
"""
"""

# mac解决matplotlib中文显示问题
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
# 第一行当索引，不会被使用
dataset = pd.DataFrame(pd.read_csv(path, index_col=[0]))
# print(dataset)

# 将空值形式的缺失值删除
dataset = dataset.dropna()
dataset = dataset.interpolate()
value = dataset.values
# print(dataset.head())
# print(dataset.shape)
'''
# 数据预处理:填充列中缺失对象(nan)。strategy：均值（mean）、中位数（median）、最频繁值(most_frequent）
imp = SimpleImpute(missing_values=np.nan, strategy='median')
fill = imp.fit_transform(dataset)
pd.DataFrame(fill)
'''
# 设置训练集的长度


# 数据归一化
sc = MinMaxScaler(feature_range=(0, 1))
dataset_scaled = sc.fit_transform(dataset)

progress_set = time_series_to_supervised(dataset_scaled, n_step_in, n_step_out)
# print(progress_set.head())

x_data = progress_set.loc[:, x_data_l:x_data_r]
y_data = progress_set.loc[:, y_data_l:y_data_r]

x_train, x_test, y_train, y_test = train_test_split(x_data.values, y_data.values, test_size=0.2, random_state=343)
# 进行训练集特征和标签的制作,水质数据一天2小时一测，一天测12次，读取连续12次作为标签


# LSTM训练的特征格式：[样本数，循环的时间步，特征个数]
x_train = x_train.reshape(x_train.shape[0], n_step_in, dataset_scaled.shape[1])
x_test = x_test.reshape(x_test.shape[0], n_step_in, dataset_scaled.shape[1])

model = load_model(model_path)
# 预测
predicted = model.predict(x_test)
# 反归一化
inv_forecast_y = sc.inverse_transform(predicted)
inv_test_y = sc.inverse_transform(y_test)

# 计算均方根误差:predicted代表只对第4列的预测值进行画图观察和误差分析

title = dataset.columns[pre]
rmse = sqrt(mean_squared_error(inv_test_y[:, pre], inv_forecast_y[:, pre]))
mape = np.mean(np.abs(inv_forecast_y[:, pre] - inv_test_y[:, pre]) / inv_test_y[:, pre])
print('rmse:', rmse)
print('mape:', mape)
# 画图
# 画图区域为（16，8）
# plt.figure(figsize=(16, 8))
plt.plot(inv_test_y[:, pre], label='真实值')
plt.plot(inv_forecast_y[:, pre], label='预测值')
plt.title(title)
plt.legend()
plt.show()
