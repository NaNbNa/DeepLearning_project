

from py2neo import Graph


class AnswerSearcher:
    def __init__(self):
        self.g = Graph('http://localhost:7474/', user='neo4j', password='15878509077z', name='neo4j')
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'One_level_composition':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}内有以下：\n{1}'.format(subject, '\n'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'Two_level_composition':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}内有以下区域：\n{1}'.format(subject, '\n'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'Three_level_composition':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}内有以下社区：\n{1}'.format(subject, '\n'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'Four_level_composition':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = '{0}内有以下楼宇：\n{1}'.format(subject, '\n'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'name_bldaddr':
            desc = [i['m.bldaddr'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的详细地址是：\n{1}'.format(subject, '\n'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'name_location':
            desc = [';'.join(i['m.location']) for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的经纬度是：\n{1}'.format(subject, '\n'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'name_bldgLdArea':
            desc = [i['m.bldgLdArea'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的占地面积是：\n{1}'.format(subject, '\n'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'name_possiblePollution':
            desc = [i['m.possiblePollution'] for i in answers]
            subject = answers[0]['m.name']

            final_answer = '{0}的可能污染物有：\n{1}'.format(subject, '\n'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'quName_desc':
            desc = [i['m.name'] for i in answers]
            final_answer = '全部区：{0}'.format('\n'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'jdName_desc':

            desc = [i['m.name'] for i in answers]
            final_answer = '全部街道：{0}'.format('\n'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'beregion_desc':

            desc = [i['m.name'] for i in answers]
            final_answer = '全部区域：{0}'.format('\n'.join(list(set(desc))[:self.num_limit]))


        elif question_type == 'sqName_desc':

            desc = [i['m.name'] for i in answers]
            final_answer = '全部社区：{0}'.format('\n'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'name_desc':
            subject = answers[0]['m.name']
            subject1 = answers[0]['m.bldaddr']
            subject2 = answers[0]['m.location']
            subject3 = answers[0]['m.bldgLdArea']
            subject4 = answers[0]['m.possiblePollution']
            final_answer = '{0}的有效属性：\n详细地占地面积址:{1}\n经纬度:{2}\n:{3}\n可能污染物{4}\n'.format(
                subject, subject1, subject2, subject3, subject4)
        elif question_type == 'name_all':
            subject = answers[0]['m.name']
            subject5 = answers[0]['m.bldaddr']
            subject6 = answers[0]['m.location']
            subject7 = answers[0]['m.bldgLdArea']
            subject8 = answers[0]['m.possiblePollution']
            subject1 = answers[0]['m.quName']
            subject2 = answers[0]['m.jdName']
            subject3 = answers[0]['m.beregion']
            subject4 = answers[0]['m.sqName']
            final_answer = '{0}的属性：\n所属区:{1}\n所属街道：{2}\n所属区域：{3}\n所属社区：{4}\n详细地址：{5}\n经纬度：{6}\n' \
                           ' 占地面积：{7}\n 可能污染物：{8}\n '.format(
                            subject, subject1, subject2, subject3, subject4, subject5, subject6, subject7, subject8)

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
