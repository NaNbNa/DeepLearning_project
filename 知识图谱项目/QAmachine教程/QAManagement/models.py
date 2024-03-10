from django.db import models

# Create your models here.

# 创建模型类
class QA(models.Model):
    id = models.AutoField(primary_key=True)  # 该字段可以不写，它会自动补全
    question = models.CharField(max_length=30)
    answer = models.CharField(max_length=8)

class QApair(models.Model):
    id = models.AutoField(primary_key=True)  # 该字段可以不写，它会自动补全
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=1000)
    category = models.CharField(max_length=8)

class Category(models.Model):
    id = models.AutoField(primary_key=True)  # 该字段可以不写，它会自动补全
    category = models.CharField(max_length=8)

class question_answer(models.Model):
    id = models.AutoField(primary_key=True)  # 该字段可以不写，它会自动补全
    question_number = models.CharField(max_length=10)
    question_content = models.CharField(max_length=500)
    answer_number = models.CharField(max_length=10)
    answer_content = models.CharField(max_length=8000)
    question_type = models.CharField(max_length=50)
    question_count = models.IntegerField()



class question_type(models.Model):
    id = models.AutoField(primary_key=True)
    question_type = models.CharField(max_length=50)