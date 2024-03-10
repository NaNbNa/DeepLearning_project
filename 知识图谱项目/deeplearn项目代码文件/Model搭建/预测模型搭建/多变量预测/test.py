import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from math import sqrt
from keras.models import load_model
import matplotlib.pyplot as plt
import joblib

# 调用已经训练好的模型
model = load_model("model.h5")

while True:
    p = float(input('降雨量:'))
    codcr = float(input('化学需氧量:'))
    nh3n = float(input('氨氮量:'))
    dox = float(input('溶解量:'))
    tp = float(input('总磷量:'))
    # 转变成DataFrame格式
    X = pd.DataFrame([[p, codcr, nh3n, dox, tp]], columns=["p", "codcr", "nh3n", "dox", "tp"])
    # 归一化
    sc = MinMaxScaler(feature_range=(0, 1))
    X_data = sc.fit_transform(X)

    # 将 DataFrame 转换为 Numpy 数组并进行形状调整
    X_array = np.array(X_data)
    X_reshaped = np.reshape(X_array, (X_array.shape[0], 1, 5))

    # 获取预测值
    predicted = model.predict(X_reshaped)

    # 返归一化
    prediction = sc.inverse_transform(predicted)
    # 分别打印预测值的各个值
    # 使用索引 [0] 访问了预测值数组的第一个元素（因为我们只有一个样本
    print("预测值如下：")
    print("p:", prediction[0][0])
    print("codcr:", prediction[0][1])
    print("nh3n:", prediction[0][2])
    print("dox:", prediction[0][3])
    print("tp:", prediction[0][4])
    Q = input("是否继续预测，如果要退出填写-quit' ")
    if Q == "quit":
        break
