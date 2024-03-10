# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
import requests
import json
from easyQA.q_classifier import *
from easyQA.q_parser import *
from easyQA.a_search import *

app = Flask(__name__)

# 从配置文件中settings加载配置
app.config.from_pyfile('settings.py')
classifier = QuestionClassifier()
# 问题处理
parser = QuestionPaser()
# 答案搜索
searcher = AnswerSearcher()



@app.route("/", methods=["GET"])
def index():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    # 此时message即为传递的字符串--data["prompt"]
    message = request.form.get("prompt")

    final_answers = '您好，我是小勇智能助理'

    res_classify = classifier.classify(message)
    if not res_classify:
        return final_answers
    else:
        res_sql = parser.parser_main(res_classify)
        final_answers = searcher.search_main(res_sql)
        return final_answers


if __name__ == '__main__':
    app.run(port=5000)
