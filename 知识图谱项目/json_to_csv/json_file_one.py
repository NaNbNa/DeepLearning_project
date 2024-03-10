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
    json_file = "/Users/ctb/Downloads/PyProject/project/projectFile/01_南湖街道_1167条数据.json"

    # 打开json文件
    with open(json_file, 'r') as json_obj:
        json_data = json.load(json_obj)
    # 创建并打开csv文件
    f = open('/Users/ctb/Downloads/PyProject/project/projectFile/json_csv2.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)

    json_list = json_data['dataList']    # json_list是列表类型
    # 储存 json文件 的 键
    json_title = []
    for k in json_list[0]:      # 第一层嵌套的"键"
        json_title.append(k)
    for k in json_list[0]["attributes"]["xtBusinessType"]:     # 第二层嵌套的"键"
        json_title.append(k)
    # 删除多余重复json的键
    json_title.remove("attributes")
    # 写入json的 键                                   第一次写入
    csv_writer.writerow(json_title)

    # 以下两个变量储存json 的"值"
    json_value0 = []
    json_value1 = []
    # num是键值对的个数
    num = json_data["total"]
    for i in range(num):                            # 第二次写入
        for k in json_list[i]["attributes"]["xtBusinessType"]:
            v = json_list[i]["attributes"]["xtBusinessType"][k]      # 获取 键=k 的值
            json_value1.append(v)
        del json_list[i]["attributes"]              # 删除多余重复的键值对
        for k in json_list[i]:
            v = json_list[i][k]                             # 获取 键=k 的值
            json_value0.append(v)
        csv_writer.writerow(json_value0+json_value1)
        json_value0.clear()                   # 清空
        json_value1.clear()

    # 关闭文件
    f.close()
    print("ok")
