import csv
import json
# 该py文件将json转化为csv ，将json中所有元素（键值对）写入csv中
# 编写此文件所需要注意的点
"""
 1。出现ValueError:too many values to unpack (expected 2)错误，因为字典循环，出现部分键值对不相同
    一部分键和值都是string，但另一部分是键string，值类型是int，导致for k，v in dict 无法使用。第二次写
    入csv使用的是是解决办法
"""
if __name__ == '__main__':
    # 文件路径
    json_file = "/Users/ctb/Downloads/PyProject/project/water/水质数据.json.json"

    # 打开json文件
    with open(json_file, 'r') as json_obj:
        json_data = json.load(json_obj)
    # 创建并打开csv文件
    f = open('/Users/ctb/Downloads/PyProject/project/csv/codcr_tp.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)

    json_list = json_data['data']  # json_list是字典类型
    # 储存 json文件 的 键
    json_title = []
    for k in json_list["data"][0]:     # 第二层嵌套的"键"
        if k == "codcr":
            json_title.append(k)
        if k == "tp":
            json_title.append(k)
    # 将时间标题插入json_title
    time = ['Time']
    json_title = time + json_title
    # 写入河流总体概况：比如名称，总体检测时间                              第一次写入

    # 写入河流各个检测的键
    csv_writer.writerow(json_title)
    # 储存json 的"值"
    json_value1 = []
    # 储存时间
    json_time = []
    # num是键值对的个数，假设1w个
    num = len(json_list["data"])
    print("     ", num)
    for i in range(num-1, -1, -1):                            # 第二次写入
        for k in json_list["data"][i]:
            if k != "t":
                if k == "tp":
                    v = json_list["data"][i][k]                             # 获取 键=k 的值
                    json_value1.append(v)
                if k == "codcr":
                    v = json_list["data"][i][k]        # 获取 键=k 的值
                    json_value1.append(v)
            else:
                v = json_list["data"][i][k]
                json_time.append(v)
        json_value1 = json_time + json_value1
        csv_writer.writerow(json_value1)
        # 清空
        json_value1.clear()
        json_time.clear()
    # 关闭文件
    f.close()
    print("ok")
