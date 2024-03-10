import json
import csv
if __name__ == '__main__':
    json_file = "/Users/ctb/Downloads/PyProject/project/projectFile/01_南湖街道_1167条数据.json"
    with open(json_file, 'r') as json_obj:
        json_data = json.load(json_obj)
    f = open('/Users/ctb/Downloads/PyProject/project/projectFile/json2csvNew.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["id",  "name", "beregion", "jdName", "quName", "sqName"])
    json_values = json_data['dataList']
    num = json_data["total"]
    for i in range(num):
        csv_writer.writerow([json_values[i]['id'],
                             json_values[i]['name'],
                             json_values[i]['attributes']['xtBusinessType']['beregion'],
                             json_values[i]['attributes']['xtBusinessType']['jdName'],
                             json_values[i]['attributes']['xtBusinessType']['quName'],
                             json_values[i]['attributes']['xtBusinessType']['sqName']])
    f.close()
    print("ok")
