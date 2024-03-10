import csv
import json
import os

# 该py文件将json转化为csv ，将json中所有元素（键值对）写入csv中
# 编写此文件所需要注意的点
"""
 1。出现ValueError:too many values to unpack (expected 2)错误，因为字典循环，出现部分键值对不相同
    一部分键和值都是string，但另一部分是键string，值类型是int，导致for k，v in dict 无法使用。第二次写
    入csv使用的是是解决办法
"""


def json2csv(data_path, output_path):
    files = os.listdir(data_path)
    out_path = output_path + "\\" + "water_quantity.csv"
    f = open(out_path, 'w', encoding='utf-8', newline='')
    for file in files:  # 遍历文件夹内文件
        position = data_path + "\\" + file
        # 打开json文件
        with open(position, 'r') as json_obj:
            json_data = json.load(json_obj)
            # 创建并打开csv文件
            csv_writer = csv.writer(f)
            json_list = json_data['data']  # json_list是字典类型
            # 储存 json文件 的 键
            json_title0 = []
            json_value0 = []
            json_title = []
            for k in json_list:
                json_title0.append(k)  # 第一层嵌套的"键"
                v = json_list[k]
                json_value0.append(v)
            for k in json_list["data"][0]:  # 第二层嵌套的"键"
                json_title.append(k)
            # 删除多余重复json的键值对
            json_title0.pop(1)
            json_value0.pop(1)
            # 写入河流总体概况：比如名称，总体检测时间                              第一次写入,
            csv_writer.writerow(json_title0)
            csv_writer.writerow(json_value0)

            # 写入河流各个检测的键
            csv_writer.writerow(json_title)
            # 储存json 的"值"
            json_value1 = []
            # num是键值对的个数，假设1w个
            num = len(json_list["data"])
            for i in range(num):  # 第二次写入
                for k in json_list["data"][i]:
                    v = json_list["data"][i][k]  # 获取 键=k 的值
                    json_value1.append(v)
                csv_writer.writerow(json_value1)
                # 清空
                json_value1.clear()

            # 关闭文件
            f.close()


if __name__ == '__main__':
    # 保存json的文件夹
    path = "/Users/ctb/Downloads/PyProject/project/projectFile"
    # 保存csv的文件夹
    output = "/Users/ctb/Downloads/PyProject/project/csv"
    json2csv(path, output)
