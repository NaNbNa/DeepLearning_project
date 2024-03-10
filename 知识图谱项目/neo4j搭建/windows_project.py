# encoding:utf8
import os
import re
import json
import codecs
import threading
from py2neo import Graph
import pandas as pd
import numpy as np
from tqdm import tqdm


def print_data_info(data_path):
    triples = []
    i = 0
    with open(data_path, 'r', encoding='utf8') as f:  # with as 语句执行完毕后自动关闭已经打开的文件
        for line in f.readlines():
            # loads：针对内存对象，将string转换为dict (将string转换为dict)
            data = json.loads(line)
            print(json.dumps(data, sort_keys=True, indent=4,
                             separators=(', ', ': '), ensure_ascii=False))
            i += 1
            if i >= 5:
                break
    return triples


class BuildExtractor(object):
    def __init__(self):
        super(BuildExtractor, self).__init__()  # ????
        self.graph = Graph('http://localhost:7474/', user='neo4j', password='15878509077z', name='neo4j')

        # 节点----均用列表存储1
        self.success = []
        self.failureCode = []
        self.failureInfo = []

        # 共5类节点
        self.quNames = []  # 区
        self.jdNames = []  # 街道
        self.beregions = []  # 区域
        self.sqNames = []  # 社区
        self.names = []  # 楼宇

        self.department_infos = []  # 楼宇信息,属性

        # 构建节点实体关系
        self.rels_na_sq = []  # 楼宇—社区关系
        self.rels_sq_be = []  # 社区－区域关系
        self.rels_be_jd = []  # 区域－街道关系
        self.rels_jd_qu = []  # 街道－区关系

    # 该函数处理json文件的每一行数据，得到实体，关系，并存储在变量。变量再存在neo4j
    def extract_triples(self, data_path):

        # files是list类型
        files = os.listdir(data_path)

        for file in files:  # 遍历文件夹内文件
            print("从json文件中转换抽取三元组")
            position = data_path + "/" + file
            with open(position, 'r', encoding='utf8') as f:
                # ncols:输出整个信息的宽度
                line = f.read()
                # loads：针对内存对象，将string转换为dict (将string转换为dict)。data_json 为dict类型
                data_json = json.loads(line)

                department_list = data_json['dataList']
                for list_dict in department_list:

                    # department_dict储存一个楼宇
                    department_dict = {}
                    name = list_dict['name']
                    department_dict['name'] = name
                    self.names.append(name)

                    #     以下变量均属于department_dict
                    # 节点信息截取
                    department_dict['sqName'] = ''  # 所属社区名称
                    department_dict['beregion'] = ''  # 所属区域名称
                    department_dict['jdName'] = ''  # 所属街道名称
                    department_dict['quName'] = ''  # 所属区名称

                    # 节点属性截取
                    department_dict['bldaddr'] = ''  # 详细地址
                    department_dict['location'] = ''  # 经纬度
                    department_dict['bldgLdArea'] = ''  # 占地面积
                    department_dict['possiblePollution'] = ''  # 可能污染物

                    sqName = 'null'
                    beregion = 'null'
                    jdName = 'null'

                    # 属性——经纬度
                    if 'location' in list_dict:
                        department_dict['location'] = list_dict['location']

                    attribution = list_dict["attributes"]['xtBusinessType']
                    # 3个属性
                    if 'bldaddr' in attribution:
                        department_dict['bldaddr'] = attribution['bldaddr']

                    if 'bldgLdArea' in attribution:
                        department_dict['bldgLdArea'] = attribution['bldgLdArea']

                    if 'possiblePollution' in attribution:
                        department_dict['possiblePollution'] = attribution['possiblePollution']

                    # 关系
                    if 'sqName' in attribution:
                        sqName = attribution['sqName']
                        self.sqNames.append(sqName)
                        department_dict['sqName'] = attribution['sqName']
                        self.rels_na_sq.append(
                            [name, 'Four_level_composition', attribution['sqName']])

                    if 'beregion' in attribution:
                        beregion = attribution['beregion']
                        if 'sqName' in attribution:
                            sqName = attribution['sqName']
                        self.beregions.append(beregion)
                        department_dict['beregion'] = attribution['beregion']
                        self.rels_sq_be.append(
                            [sqName, 'Three_level_composition', attribution['beregion']])

                    if 'jdName' in attribution:
                        jdName = attribution['jdName']
                        if 'beregion' in attribution:
                            beregion = attribution['beregion']
                        self.jdNames.append(jdName)
                        department_dict['jdName'] = attribution['sqName']
                        self.rels_be_jd.append(
                            [beregion, 'Two_level_composition', attribution['jdName']])

                    if 'quName' in attribution:
                        if 'jdName' in attribution:
                            jdName = attribution['jdName']
                        self.quNames.append(attribution['quName'])
                        department_dict['quName'] = attribution['quName']
                        self.rels_jd_qu.append(
                            [jdName, 'One_level_composition', attribution['quName']])

                    self.department_infos.append(department_dict)

    def write_nodes(self, entitys, entity_type):  # 往neo4j里写节点
        # 实体——entitys类型为列表，set(entitys)去掉里面重复的数据，避免重复工作
        print("写入 {0} 实体".format(entity_type))
        # tqdm库：希望循环能够显示进度，那么只需要将循环中的可迭代对象用 tqdm 封装，就可以实现进度条的显示
        for node in tqdm(set(entitys), ncols=80):
            # MERGE ：可以根据一个或多个键将不同的DataFrame链接起来（DataFrame：数据框架）
            # MERGE ：典型应用场景是，针对同一个主键存在两张不同字段的表，根据主键整合到一张表里面。
            # """ """用法：构造str：cql，cql为str
            cql = """MERGE(n:{label}{{name:'{entity_name}'}})""".format(
                label=entity_type, entity_name=node)  # replace("'", "")，以免报错
            try:  # 防止程序报错而终止
                # cql虽然作为str，但通过run（）可以执行MERGE语句
                # graph.run：neo4j在Pycharm的运行指令
                self.graph.run(cql)
            except Exception as e:
                print(e)
                print(cql)

    def write_edges(self, triples, head_type, tail_type):  # 往neo4j里写入节点与节点的边
        print("写入{0}-->{1}关系".format(head_type, tail_type))
        for head, relation, tail in tqdm(triples, ncols=80):
            # MATCH：（动作）match（匹配）两个节点p，q，WHERE指定p，q名称。MERGE在p，q之间建立一个关系
            # 该cql的作用：建立p和q的关系。（MATCH用来寻找（匹配），WHERE用来指定）
            cql = """MATCH(p:{head_type}),(q:{tail_type})
                    WHERE p.name='{head}' AND q.name='{tail}'
                    MERGE (p)-[r:{relation}]->(q)""".format(
                head_type=head_type, tail_type=tail_type, head=head,
                tail=tail, relation=relation)  # head.replace("'", "")  replace("'", "")
            try:
                self.graph.run(cql)
            except Exception as e:
                print(e)
                print(cql)

    # 针对实体来写入实体属性，写入节点属性
    # entity_infos：实体属性
    def set_attributes(self, entity_infos, etype):
        print("写入 {0} 实体的属性".format(etype))
        for e_dict in tqdm(entity_infos, ncols=80):
            if 'name' in e_dict:
                name = e_dict['name']
                del e_dict['name']
                for k, v in e_dict.items():
                    cql = """MATCH (n:{label})
                        WHERE n.name='{name}'
                        set n.{k}='{v}'""".format(label=etype, name=name, k=k,
                                                  v=v)
                    # v=v.replace("'", "").replace("\n", "")
                    # .replace("'", "")
                    try:
                        self.graph.run(cql)
                    except Exception as e:
                        print(e)
                        print(cql)

    # 以下三个方法（函数）作用：将节点，边，属性写入neo4j
    def create_entitys(self):
        self.write_nodes(self.names, '楼宇')
        self.write_nodes(self.sqNames, '社区')
        self.write_nodes(self.beregions, '区域')
        self.write_nodes(self.jdNames, '街道')
        self.write_nodes(self.quNames, '区')

    def create_relations(self):
        self.write_edges(self.rels_na_sq, '楼宇', '社区')
        self.write_edges(self.rels_sq_be, '社区', '区域')
        self.write_edges(self.rels_be_jd, '区域', '街道')
        self.write_edges(self.rels_jd_qu, '街道', '区')

    def set_department_attributes(self):
        self.set_attributes(self.department_infos, "楼宇")
        t = threading.Thread(target=self.set_attributes, args=(self.department_infos, "楼宇"))
        t.daemon = False
        t.start()


if __name__ == '__main__':
    # 文件夹目录
    path = "/Users/ctb/Downloads/PyProject/project/projectFile"
    extractor = BuildExtractor()
    extractor.extract_triples(path)
    extractor.create_entitys()
    extractor.create_relations()
    extractor.set_department_attributes()
