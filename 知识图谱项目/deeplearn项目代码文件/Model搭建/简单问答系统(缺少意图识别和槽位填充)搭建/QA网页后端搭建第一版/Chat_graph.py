#!/usr/bin/env python3
# coding: utf-8
# File: chatbot_graph.py
# Author: lhy<lhy_in_blcu@126.com, https://huangyong.github.io>
# Date: 18-10-4

from q_classifier import *
from q_parser import *
from a_search import *

'''问答类'''


class ChatBotGraph:
    def __init__(self):
        # 问题进行分类
        self.classifier = QuestionClassifier()
        # 问题处理
        self.parser = QuestionPaser()
        # 答案搜索
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '欢迎使用，如要退出，请输入quit'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)


if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        if question == 'quit':
            answer = "谢谢使用"
            print('小勇:', answer)
            break
        answer = handler.chat_main(question)
        print('小勇:', answer, flush=True)
