
import os

import ahocorasick


class QuestionClassifier:
    def __init__(self):
        cur_dir = '../static/txt/'

        # 读取节点
        # 区
        self.quName_path = cur_dir + 'quName.txt'
        # 街道
        self.jdName_path = cur_dir + 'jdName.txt'
        # 区域
        self.beregion_path = cur_dir + 'beregion.txt'
        # 社区
        self.sqName_path = cur_dir + 'sqName.txt'
        # 楼宇
        self.name_path = cur_dir + 'name.txt'

        # 读取特征词
        self.quName_wds = [i.strip() for i in open(self.quName_path) if i.strip()]
        self.jdName_wds = [i.strip() for i in open(self.jdName_path) if i.strip()]
        self.beregion_wds = [i.strip() for i in open(self.beregion_path) if i.strip()]
        self.sqName_wds = [i.strip() for i in open(self.sqName_path) if i.strip()]
        self.name_wds = [i.strip() for i in open(self.name_path) if i.strip()]
        # 合并，去掉重复部分

        self.region_words = set(
            self.quName_wds + self.jdName_wds + self.beregion_wds + self.sqName_wds + self.name_wds)

        # actree：加速过滤
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()

        # 问句疑问词
        self.quName_all = ['多少区', '区的个数', '一共有多少区']
        self.jdName_all = ['多少街道', '街道个数']
        self.beregion_all = ['多少区域', '区域个数']
        self.sqName_all = ['多少社区', '社区个数']

        self.quName_qwds = ['区', '有什么区', '哪些区']
        self.jdName_qwds = ['街道', '有什么街道', '哪些街道']
        self.beregion_qwds = ['区域', '有什么区域', '哪些区域']
        self.sqName_qwds = ['社区', '有什么社区', '哪些社区']
        self.name_qwds = ['楼宇', '有什么楼宇', '哪些楼宇']
        # 楼宇信息,属性
        self.info_all_qwds = ['属性', '信息']
        # 详细地址
        self.bldaddr_qwds = ['哪里', '在哪里', '详细', '地址', '位置', '地理']
        # 经纬度
        self.location_qwds = ['经度', '纬度', '经纬度']
        # 占地面积
        self.bldgLdArea_qwds = ['占地', '面积', '多大', '多小']
        # 可能污染物
        self.possiblePollution_qwds = ['污染', '源头']

        print('模型初始化结束 ......')

        return

    '''
    分类主函数 ： 进行分类操作，分类各个结点和关系
    '''

    def classify(self, question):
        data = {}
        # 实体字典
        apartment_dict = self.check_medical(question)
        if not apartment_dict:
            return {}
        data['args'] = apartment_dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in apartment_dict.values():
            types += type_

        #  question_types是问题类型，这个类型可以是已存在的关系（用于关系打印），也可以是自定义关系，返回节点特定属性
        question_types = []

        # 以下8个if（已存在的节点关系）--用处：知道节点关系和知道一个节点， 推出另一个节点
        # 一级
        if self.check_words(self.jdName_qwds, question) and ('quName' in types):
            question_type = 'One_level_composition'
            question_types.append(question_type)

        # 二级
        if self.check_words(self.beregion_qwds, question) and ('jdName' in types):
            question_type = 'Two_level_composition'
            question_types.append(question_type)

        # 三级
        if self.check_words(self.sqName_qwds, question) and ('beregion' in types):
            question_type = 'Three_level_composition'
            question_types.append(question_type)

        # 四级
        if self.check_words(self.name_qwds, question) and ('sqName' in types):
            question_type = 'Four_level_composition'
            question_types.append(question_type)

        # 以下是自定义关系--节点属性

        # 楼宇详细地址
        if self.check_words(self.bldaddr_qwds, question) and 'name' in types:
            question_type = 'name_bldaddr'
            question_types.append(question_type)
        # 经纬度
        if self.check_words(self.location_qwds, question) and 'name' in types:
            question_type = 'name_location'
            question_types.append(question_type)
        # 占地面积
        if self.check_words(self.bldgLdArea_qwds, question) and 'name' in types:
            question_type = 'name_bldgLdArea'
            question_types.append(question_type)
        # 可能污染物
        if self.check_words(self.possiblePollution_qwds, question) and 'name' in types:
            question_type = 'name_possiblePollution'
            question_types.append(question_type)
        # 楼宇全部属性
        if self.check_words(self.info_all_qwds, question) and 'name' in types:
            question_type = 'name_all'
            question_types.append(question_type)
        # 若没有查到相关的外部查询信息，那么则将其的描述信息返回
        # 若没有查到相关的外部查询信息，那么则将其的描述信息返回
        # 若没有查到相关的外部查询信息，那么则将其的描述信息返回
        if self.check_words(self.quName_all, question):
            question_type = 'quName_desc'
            question_types.append(question_type)
        if self.check_words(self.jdName_all, question):
            question_type = 'jdName_desc'
            question_types.append(question_type)
        if self.check_words(self.beregion_all, question):
            question_type = 'beregion_desc'
            question_types.append(question_type)
        if self.check_words(self.sqName_all, question):
            question_type = 'sqName_desc'
            question_types.append(question_type)
        if question_types == [] and 'name' in types:
            question_type = 'name_desc'
            question_types.append(question_type)



        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''

    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.quName_wds:
                wd_dict[wd].append('quName')
            if wd in self.jdName_wds:
                wd_dict[wd].append('jdName')
            if wd in self.beregion_wds:
                wd_dict[wd].append('beregion')
            if wd in self.sqName_wds:
                wd_dict[wd].append('sqName')
            if wd in self.name_wds:
                wd_dict[wd].append('name')
        return wd_dict

    '''构造actree，加速过滤'''

    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''

    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''

    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)
