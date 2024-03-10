from keras import Sequential
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from keras.layers import LSTM, Dropout, Dense
from sklearn.model_selection import train_test_split


# 使用time_series_to_supervised函数生成适用于监督学习的 DataFrame
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
分割线
分割线
超参数
n_step_in = 9   ,    batch_size = 12   
"""
path = "/Users/ctb/Downloads/PyProject/project/csv/codcr_tp.csv"
model_path = '/Users/ctb/Downloads/PyProject/project/deeplearn/Model/codcr_tp.h5'
# n_step_in 个数据训练后预测 n_step_out 个数据
n_step_in = 9  # 历史时间长度
n_step_out = 1  # 预测时间长度
# x_data_r - x_data_l = n_step_in * 特征数
x_data_l = '0(t-9)'  # 随着n_step_in变化
x_data_r = '1(t-1)'
y_data_l = '0'
y_data_r = '1'
# model
batch_size = 32
epochs = 100
"""
分割线
分割线
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
# value = dataset.values
# print(dataset.head())
# print(dataset.shape)
'''
# 数据预处理:填充列中缺失对象(nan)。strategy：均值（mean）、中位数（median）、最频繁值(most_frequent）
imp = SimpleImpute(missing_values=np.nan, strategy='median')
fill = imp.fit_transform(dataset)
pd.DataFrame(fill)
'''

# 数据归一化
sc = MinMaxScaler(feature_range=(0, 1))
dataset_scaled = sc.fit_transform(dataset)



progress_set = time_series_to_supervised(dataset_scaled, n_step_in, n_step_out)
# print(progress_set.head)
# 划分特征和标签
x_data = progress_set.loc[:, x_data_l:x_data_r]
y_data = progress_set.loc[:, y_data_l:y_data_r]

x_train, x_test, y_train, y_test = train_test_split(x_data.values, y_data.values, test_size=0.2, random_state=343)
# 进行训练集特征和标签的制作,水质数据一天2小时一测，一天测12次，读取连续12次作为标签


# LSTM训练的特征格式：[样本数，循环的时间步，特征个数]
x_train = x_train.reshape(x_train.shape[0], n_step_in, dataset_scaled.shape[1])
x_test = x_test.reshape(x_test.shape[0], n_step_in, dataset_scaled.shape[1])
# print(x_train.shape, x_test.shape,  y_train.shape, y_test.shape)
""" 
分界限
"""
# 利用keras搭建神经网络
# design network
model = Sequential()
# input_shape千万不要写错！，第一个参数可以更改，x_train.shape[1:]是[步长， 列数（特征个数)]
model.add(LSTM(96, return_sequences=True, input_shape=(x_train.shape[1:])))
model.add(Dropout(0.2))
model.add(LSTM(64, return_sequences=False))  # returns a sequence of vectors of dimension 32
model.add(Dropout(0.2))
model.add(Dense(32))
model.add(Dropout(0.2))
# y_train.shape[1]是列数，也就是预测的特征数
model.add(Dense(y_train.shape[1]))
model.compile(loss='mse', optimizer='adam')

print(model.summary())
history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(x_test, y_test),
                    verbose=2,
                    shuffle=False)

model.save(model_path)
# 绘制loss值
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='val')
plt.title('LSTM神经网络loss值')
plt.legend()
plt.show()
