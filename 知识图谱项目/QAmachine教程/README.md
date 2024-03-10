@[TOC](文章目录)

# 1 项目简介
## 1.1项目概述
问答机器人是人工智能和自然语言处理领域中一个倍受关注并且具有广泛应用前景的研究方向。本项目聚焦于特定领域的智能问答应用研究。在此基础上研究基于语义解析的问答匹配，通过对领域知识进行知识图谱表示、构建问答模型，综合应用了文本映射，SPARQL查询等技术实现智能问答机器人系统。项目中问答算法的设计与知识图谱的构建参考了GitHub中的开源项目。
## 1.2项目使用环境及工具

 - jdk 8（本项目使用java 1.8.0版本）
 - neo4j 3.5.X （本项目使用3.5.18版本，是基于java的nosql图形数据库）
 - Python 3.6 （本项目使用3.6.8版本）
 - py2neo 3.1.2（项目中调用neo4j数据库的必要包）
 - Django 3.1.5（项目的web应用框架）
 - jieba  0.42.1（项目中对问题进行分词时使用的包）

其余基础的包不在此处做特别说明，项目使用pycharm作为Python的集成开发环境进行开发和调试。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210125113713451.gif#pic_center )
## 1.3项目部署
1.首先运行neo4j数据库，切换到数据库bin目录下，使用命令 ==neo4j console==。
2.将Django项目导入pycharm中，并设置项目settings.py的路径。
2.将build_kg.py中第10行的neo4j密码修改为自己的，然后python build_kg.py，构建知识图谱。    
3.观察database中是否成功导入节点及关系：浏览器打开 http://localhost:7474/即可查看构建好的知识图谱。
4.修改answer_question.py中第8行的neo4j密码。
5.选择Django作为项目的解释器，并运行项目。
# 2 代码目录结构及原理
## 2.1核心代码目录结构
|——**Django**
|————**_init\_.py**	
|————**settings.py**	是 Django 项目的配置文件. 包含很多重要的配置项。
|————**urls.py**	存放着路由表， 声明了前端发过来的各种http请求分别由哪些函数处理。
|————**wsgi.py** 	提供给wsgi web server调用的接口文件，变量application对应对象实现了wsgi入口。
|——**QAManagement**
|————**migrations**
|——————**views.py** Django的视图层，写有前端发来请求后调用的处理函数
|——**QASystem**
|————**poetryData** 用于存放从csv文件中抽取的各个实体之间联系文件的文件夹
|————**answer_question.py** 设置问题分类查询的CQL模板，并输出查询到的答案。
 |————**build_kg.py** 读入csv文件并构建知识图谱
 |————**main.py** 调用知识图谱问答算法
 |————**question_classifier.py** 问题分词、问题分类
 |——**staic** 存放前端依赖的css和img和js资源的文件夹
 |——**templates**
  |————**test.html** 项目的前端页面
|——**manage.py** 是一个工具脚本，用作项目管理。使用它来执行管理操作。



详细的介绍文章请参考csdn博客 https://blog.csdn.net/qq_45647925/article/details/113102301