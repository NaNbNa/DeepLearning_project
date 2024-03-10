from django.http import HttpResponse
from django.shortcuts import render
import json
from .models import QApair
from .models import Category
from .models import question_answer
from .models import question_type
from QASystem.main import end

def index(request):
    return render(request, "test.html");

def accurate_search_test(request):
    if request.method == 'POST':
        user_question = request.POST.get("accurate_Question")
        return HttpResponse("问题已收到");

def usermayask_test(request):
    if request.method=='POST':
        questions_dict = {'mayask'+ str(0):"问题一",
                          'count' + str(0): 10,
                          'mayask' + str(1): "sex",
                          'count' + str(1): 20
        }
        return HttpResponse(json.dumps(questions_dict))


def usermayask1(request):
    if request.method=='POST':
        questions_dict = {}
        categorys = Category.objects.all()
        i = 0
        for type in categorys:
            questions_dict['mayask'+ str(i)] = type.category
            '''
            questions_dict['count' + str(i)] = question.answer
            '''
            i = i + 1
        return HttpResponse(json.dumps(questions_dict))


def type_search1(request):
    if request.method == 'POST':
        question_type = request.POST.get("type_search")
        allquestions = QApair.objects.filter(category=question_type)
        questions_dict ={}
        questions_dict['questiontype' + str(0)] = question_type
        i = 1
        for q in allquestions:
            questions_dict['questiontype'+ str(i)] = q.question
            i = i + 1
        print(questions_dict)
        return HttpResponse(json.dumps(questions_dict))

def accurate_search1(request):
    if request.method == 'POST':
        question = request.POST.get("accurate_Question")
        answers = QApair.objects.get(question=question)
        answers_dict ={}
        answers_dict['answer' + str(0)] = question
        answers_dict['answer' + str(1)] = answers.answer
        return HttpResponse(json.dumps(answers_dict))
###########################################################################
#页面第一次刷新读取所有问题种类
def usermayask(request):
    if request.method=='POST':
        questions_dict = {}
        categorys = question_type.objects.all()
        i = 0
        # for type in categorys:
        #     questions_dict['mayask'+ str(i)] = type.question_type
        #     i = i + 1
        return HttpResponse(json.dumps(questions_dict))

#返回该种类的问题
def type_search(request):
    if request.method == 'POST':
        question_type = request.POST.get("type_search")
        allquestions = question_answer.objects.filter(question_type=question_type).order_by('-question_count')
        questions_dict ={}
        questions_dict['questiontype' + str(0)] = question_type
        i = 1
        for q in allquestions:
            if i == 6:
                break;
            questions_dict['questiontype'+ str(i)] = q.question_content
            i = i + 1
        print(questions_dict)
        return HttpResponse(json.dumps(questions_dict))

#返回选定问题的答案
def accurate_search(request):
    if request.method == 'POST':
        question = request.POST.get("accurate_Question")
        answers = question_answer.objects.get(question_content=question)
        answers_dict ={}
        answers_dict['answer' + str(0)] = question
        answers_dict['answer' + str(1)] = answers.answer_content

        #每次查询到某个问题，给问题count加1
        answers.question_count += 1
        answers.save()

        return HttpResponse(json.dumps(answers_dict))

def login(request):
    return render(request,'test.html')

question_content="null"
answer_content="null"
def gulu(request):
    question = request.POST.get('question')
    global question_content
    question_content=str(question)
    return HttpResponse(json.dumps(question))

def answer(request):
    global question_content
    global answer_content
    question=gulu(request)
    # print(question_content)

    answer_content=end(question_content)
    # print(answer_content)
    return HttpResponse(json.dumps(answer_content))

def jsons(request):
    global question_content
    global answer_content
    print(question_content)
    print(answer_content)
    if str(answer_content)=='-1':
        answer_content="不好意思鸭，没有找到关于\'"+question_content+"\'问题的答案。请您换个说法提问，知识图谱还在进一步的完善当中,敬请谅解~~"
    return HttpResponse(json.dumps(answer_content))