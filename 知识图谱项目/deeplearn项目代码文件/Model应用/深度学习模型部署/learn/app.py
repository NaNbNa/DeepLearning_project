import json
import io
import base64
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask import render_template
from keras import Sequential
import matplotlib.pyplot as plt
from keras.models import load_model
import pandas as pd
from math import sqrt
import numpy as np
from keras.callbacks import Callback
import plotly.graph_objs as go
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from keras.layers import LSTM, Dropout, Dense
from sklearn.model_selection import train_test_split
import plotly
from sklearn.metrics import mean_squared_error
import plotly.offline as pyo

# 存储进度数据 ，全局变量
progress_data = {'progress': 0.00}

"""
path = "/Users/ctb/Downloads/PyProject/project/csv/codcr_tp.csv"
model_path = '/Users/ctb/Downloads/PyProject/project/deeplearn/Model/codcr_tp.h5'
# n_step_in 个数据训练后预测 n_step_out 个数据
n_step_in = 1  # 历史时间长度
n_step_out = 1  # 预测时间长度
# x_data_r - x_data_l = n_step_in * 特征数
x_data_l = '0(t-9)'  # 随着n_step_in变化
x_data_r = '1(t-1)'
y_data_l = '0'
y_data_r = '1'
column --csv列数
predicted --预测的数据所在的列
# model
batch_size = 32
epochs = 100
"""
"""
分割线
分割线
"""

n_step_in = 1
n_step_out = 1
column = 5
predict = 2
batch_size = 32
epochs = 100
path = '/Users/ctb/Downloads/项目/csv/json.csv'
model_path = '/Users/ctb/Downloads/项目/model.h5'


# 回调函数
class CustomCallback(Callback):
    # 在每个epoch开始前调用该函数，记录训练进度
    def on_epoch_begin(self, epoch, logs=None):
        global progress_data
        progress_data['progress'] = epoch / epochs * 100

    def on_epoch_end(self, epoch, logs=None):
        print()


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


app = Flask(__name__)


# 主界面
@app.route('/')
def index():
    return render_template('main.html')


# 切换网页
@app.route('/build')
def to_build():
    return render_template('build.html')


@app.route('/test')
def to_test():
    return render_template('test.html')


@app.route('/use')
def to_use():
    return render_template('use.html')


# 超参数修改
@app.route('/train_para', methods=['POST'])
def train_para():
    # data是dict类型
    data = request.get_json()  # 获取请求中的 JSON 数据
    # 注意强制转换
    global path, model_path, n_step_in, n_step_out, predict, column, batch_size, epochs
    if data['path']:
        path = data['path']
    if data['model_path']:
        model_path = data['model_path']
    if data['n_step_in']:
        n_step_in = int(data['n_step_in'])
    if data['n_step_out']:
        n_step_out = int(data['n_step_out'])
    if data['column']:
        column = int(data['column'])
    if data['predict']:
        predict = int(data['predict'])
    if data['batch_size']:
        batch_size = int(data['batch_size'])
    if data['epochs']:
        epochs = int(data['epochs'])
    return '传输超参数完成'


@app.route('/train_run', methods=['GET'])
def train_run():
    x_data_l = '0(t-' + str(n_step_in) + ')'
    x_data_r = str(column - 1) + '(t-1)'
    y_data_l = '0'
    y_data_r = str(column - 1)

    # mac解决matplotlib中文显示问题
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    # 第一行当索引，不会被使用
    dataset = pd.DataFrame(pd.read_csv(path, index_col=[0], nrows=70))
    # print(dataset)

    # 将空值形式的缺失值删除
    dataset = dataset.dropna()
    dataset = dataset.interpolate()
    # value = dataset.values
    # print(dataset.head())sg
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

    x_train, x_test, y_train, y_test = train_test_split(x_data.values, y_data.values, test_size=0.2,
                                                        random_state=343)
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
    model.add(Dense(y_train.shape[predict - 1]))
    model.compile(loss='mse', optimizer='adam')

    # print(model.summary())
    global progress_data
    history = model.fit(x_train, y_train, batch_size=batch_size,
                        epochs=epochs, validation_data=(x_test, y_test), callbacks=[CustomCallback()])

    # 保存模型
    model.save(model_path)
    # 不实用matplotlib画图是因为训练模型的线程不在主线程
    # 创建训练和测试损失的数据
    train_loss = history.history['loss']
    test_loss = history.history['val_loss']
    train_loss_data = go.Scatter(x=list(range(len(train_loss))),
                                 y=train_loss,
                                 mode='lines',
                                 name='训练集损失值')
    test_loss_data = go.Scatter(x=list(range(len(test_loss))),
                                y=test_loss,
                                mode='lines',
                                name='测试集损失值')
    # 将数据添加到一个列表中
    data = [train_loss_data, test_loss_data]

    # 设置布局
    layout = go.Layout(title='Train vs Test Loss',
                       xaxis=dict(title='Epoch'),
                       yaxis=dict(title='Loss'))

    # 创建图表
    fig = go.Figure(data=data, layout=layout)

    # 将图表转换为HTML代码
    plot_html = plotly.offline.plot(fig, output_type='div')
    plot_data = {"plot_html": plot_html}  # 将 plot_html 存储到一个字典中

    # 返回序列化后的 plot_data
    return json.dumps(plot_data)


# 模型测试
@app.route('/test_run')
def test_run():
    x_data_l = '0(t-' + str(n_step_in) + ')'
    x_data_r = str(column - 1) + '(t-1)'
    y_data_l = '0'
    y_data_r = str(column - 1)

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

    x_train, x_test, y_train, y_test = train_test_split(x_data.values, y_data.values, test_size=0.2,
                                                        random_state=343)
    # 进行训练集特征和标签的制作,水质数据一天2小时一测，一天测12次，读取连续12次作为标签

    # LSTM训练的特征格式：[样本数，循环的时间步，特征个数]
    x_test = x_test.reshape(x_test.shape[0], n_step_in, dataset_scaled.shape[1])

    model = load_model(model_path)
    # 预测
    predicted = model.predict(x_test)
    # 反归一化
    inv_forecast_y = sc.inverse_transform(predicted)
    inv_test_y = sc.inverse_transform(y_test)

    # 计算均方根误差:predict-1代表只对第predict列的预测值进行画图观察和误差分析
    # 创建折线图来绘制预测值和测试值
    trace1 = go.Scatter(
        x=list(range(len(inv_test_y[:, predict - 1]))),
        y=inv_test_y[:, predict - 1].flatten(),
        mode='lines',
        name='真实值'
    )

    trace2 = go.Scatter(
        x=list(range(len(inv_forecast_y[:, predict - 1]))),
        y=inv_forecast_y[:, predict - 1].flatten(),
        mode='lines',
        name='预测值'
    )

    data = [trace1, trace2]

    # 创建布局对象
    layout = go.Layout(
        title='Predicted vs Actual',
        xaxis=dict(title='Index'),
        yaxis=dict(title='Value')
    )

    # 创建图形对象
    fig = go.Figure(data=data, layout=layout)

    # 将图形转换为HTML代码
    plot_html = plotly.offline.plot(fig, output_type='div')
    # 评测模型数据
    # 计算均方根误差:predict-1代表只对第predict列的预测值进行画图观察和误差分析
    rmse = sqrt(mean_squared_error(inv_test_y[:, predict - 1], inv_forecast_y[:, predict - 1]))
    if inv_test_y[:, predict - 1].all():
        mape = np.mean(np.abs(inv_forecast_y[:, predict - 1] - inv_test_y[:, predict - 1]) / inv_test_y[:, predict - 1])
    else:
        mape = "false"
    # 将 plot_html 存储到一个字典中
    plot_data = {"plot_html": plot_html, "rmse": rmse, "mape": mape}

    return json.dumps(plot_data)


# 深度学习模型单组预测应用
@app.route('/use_run', methods=['POST'])
def model_use():
    model = load_model(model_path)
    # 读取CSV文件并获取第一行元素
    csv_data = pd.read_csv(path, nrows=1)
    # 获取第二列开始的元素作为键
    column_names = csv_data.columns[1:].tolist()

    # 将表单数据转换为字典
    form_data = request.form.to_dict()

    # 创建新的字典，以第一行第二列开始元素作为键，表单数据作为值
    # f'input_{i}' 是一个 f-string，用于在字符串中插入变量 i 的值。
    # 它会生成类似 "input_0"、"input_1"、"input_2" 这样的字符串
    # 使用f'input_{i}'是因为表单字段的 name 属性被设置为 input_0、input_1、input_2 等形式
    data = {column_names[i]: form_data[f'input_{i}'] for i in range(len(column_names))}

    # 将字典转换为DataFrame
    df = pd.DataFrame.from_dict(data, orient='index').T

    # 归一化
    sc = MinMaxScaler(feature_range=(0, 1))
    X_data = sc.fit_transform(df)

    # 将 DataFrame 转换为 Numpy 数组并进行形状调整
    X_array = np.array(X_data)
    X_reshaped = np.reshape(X_array, (X_array.shape[0], 1, column))
    # 获取预测值
    predicted = model.predict(X_reshaped)

    # 反归一化
    prediction = sc.inverse_transform(predicted)

    # 预测值和键对应
    dict = {column_names[i]: float(prediction[0][i]) for i in range(len(column_names))}

    # json.dumps() 是 Python 中的一个函数
    # Python 对象转换为 JSON 字符串
    return json.dumps(dict)


# 多线程之一，实时请求训练进度
@app.route('/train_progress')
def get_progress():
    return jsonify({'res': progress_data['progress']})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
