#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

class QuestionPaser:
    """构建实体节点"""

    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''

    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {'question_type': question_type}
            sql = []
            if question_type == 'One_level_composition':
                sql = self.sql_transfer(question_type, entity_dict.get('quName'))

            elif question_type == 'Two_level_composition':
                sql = self.sql_transfer(question_type, entity_dict.get('jdName'))

            elif question_type == 'Three_level_composition':
                sql = self.sql_transfer(question_type, entity_dict.get('beregion'))

            elif question_type == 'Four_level_composition':
                sql = self.sql_transfer(question_type, entity_dict.get('sqName'))

            elif question_type == 'name_bldaddr':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))

            elif question_type == 'name_location':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))

            elif question_type == 'name_bldgLdArea':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))

            elif question_type == 'name_possiblePollution':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))

            elif question_type == 'quName_desc':
                sql = self.sql_transfer(question_type, '')
            elif question_type == 'jdName_desc':
                sql = self.sql_transfer(question_type, '')
            elif question_type == 'beregion_desc':
                sql = self.sql_transfer(question_type, '')
            elif question_type == 'sqName_desc':
                sql = self.sql_transfer(question_type, '')
            elif question_type == 'name_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))
            elif question_type == 'name_all':
                sql = self.sql_transfer(question_type, entity_dict.get('name'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''

    def sql_transfer(self, question_type, entities):
        # 查询语句
        sql = []
        # 已知楼宇得到楼宇详细地址
        if question_type == 'name_bldaddr':
            sql = ["MATCH (m:楼宇) where m.name = '{0}' return m.name, m.bldaddr".format(i) for i in entities]

        # 经纬度
        elif question_type == 'name_location':
            sql = ["MATCH (m:楼宇) where m.name = '{0}' return m.name, m.location".format(i) for i in entities]

        # 占地面积
        elif question_type == 'name_bldgLdArea':
            sql = ["MATCH (m:楼宇) where m.name = '{0}' return m.name, m.bldgLdArea".format(i) for i in entities]

        # 可能污染物
        elif question_type == 'name_possiblePollution':
            sql = ["MATCH (m:楼宇) where m.name = '{0}' return m.name, m.possiblePollution".format(i) for i in entities]

        # 已知quName查jdName
        elif question_type == 'One_level_composition':
            sql1 = [
                "MATCH (m:街道)-[r:One_level_composition]->(n:区) where n.name = '{0}' return n.name, m.name".format(i)
                for i in entities]

            sql = sql1

        # 已知jdName查beregion
        elif question_type == 'Two_level_composition':
            sql1 = [
                "MATCH (m:区域)-[r:Two_level_composition]->(n:街道) where n.name = '{0}' return n.name, m.name".format(
                    i) for i in entities]

            sql = sql1
        # 已知beregion查sqName
        elif question_type == 'Three_level_composition':
            sql1 = [
                "MATCH (m:社区)-[r:Three_level_composition]->(n:区域) where n.name = '{0}' return n.name,  m.name".format(
                    i) for i in entities]
            sql = sql1
        # 已知sqName查name
        elif question_type == 'Four_level_composition':
            sql1 = [
                "MATCH (m:楼宇)-[r:Four_level_composition]->(n:社区) where n.name = '{0}' return n.name,  m.name".format(
                    i) for i in entities]
            sql = sql1
        elif question_type == 'quName_desc':
            sql1 = [
                "MATCH (m:区) return m.name LIMIT 25"]
            sql = sql1
        elif question_type == 'jdName_desc':
            sql1 = [
                "MATCH (m:街道) return m.name LIMIT 25"]
            sql = sql1
        elif question_type == 'beregion_desc':
            sql1 = [
                "MATCH (m:区域) return m.name LIMIT 25"]
            sql = sql1
        elif question_type == 'sqName_desc':
            sql1 = [
                "MATCH (m:社区) return m.name LIMIT 25"]
            sql = sql1
        elif question_type == 'name_desc':
            sql1 = [
                "MATCH (m:楼宇) where m.name = '{0}' return m.name, m.bldaddr, m.location, m.bldgLdArea, "
                "m.possiblePollution".format(i) for i in entities]
            sql = sql1
        elif question_type == 'name_all':
            sql1 = [
                "MATCH (m:楼宇) where m.name = '{0}' return m.name, m.bldaddr, m.location, m.bldgLdArea, m.quName,"
                "m.possiblePollution, m.jdName, m.sqName, m.beregion".format(i) for i in entities]
            sql = sql1
        return sql


if __name__ == '__main__':
    handler = QuestionPaser()
