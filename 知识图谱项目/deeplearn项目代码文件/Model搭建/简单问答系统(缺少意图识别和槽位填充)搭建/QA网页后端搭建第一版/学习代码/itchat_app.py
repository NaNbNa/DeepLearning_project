import json
import sys

import requests
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

# 表示从PyQt5的QtWidgets中引用全部函数（*表示全部）
# 1.应答核心--in判断成员是否在list中
# 2. 百度unitAPI接进来

# 常量
AK = 'LNsYReyUKb9idkO9OHHnanm0'
SK = '28iTb65vBPmSR05vyNU6pnYjIa739KP7'

key_word = ('你要找', '你要查')
weather = ('晴', '雾', '雨', '阴')
connect_flag = False
connect_word = '初始化'
word_flag = 0
bg_flag = 0


# 继承
class ChatBox(QWidget):
    def __init__(self):
        # 初始化父类构造函数
        # super会找到ChatBox继承的父类QWindegt， 去实例化父类的构造函数
        super(ChatBox, self).__init__()
        # 绘制界面方法
        # 初始化界面
        self.submit = None
        self.char_input = None
        self.chatBox = None
        self.AI = None
        self.icon = None
        self.left_box = None
        self.AI_robot = Chat_robot()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("快来聊天啊！")
        self.setGeometry(500, 100, 800, 700)
        # 美化窗口+添加控件
        # 窗口图标
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("/Users/ctb/Downloads/photo_图片/1.png"),  # 图标路径
                            QtGui.QIcon.Normal,
                            QtGui.QIcon.Off)
        self.setWindowIcon(self.icon)
        # 左侧栏
        self.left_box = QWidget(self)
        self.left_box.setGeometry(10, 10, 200, 680)
        self.left_box.setStyleSheet("background-color: rgb(200, 200, 169)")  # 设置背景色
        self.AI = QLabel("专属机器人在线中", self)
        self.AI.setGeometry(11, 11, 200, 120)
        self.AI.setStyleSheet("background-color: rgb(0, 245, 255); color: black; font-size:22px")
        # 右上方聊天区
        self.chatBox = QListWidget(self)
        # 设置位置
        self.chatBox.setGeometry(210, 10, 590, 600)
        # 设置样式
        self.chatBox.setStyleSheet("background-image: url(background.png);border:2px solid #c4c4c4; font-size:30px")
        # 设置图标大小
        self.chatBox.setIconSize(QSize(40, 40))

        # 右下方内容准备
        self.char_input = QLineEdit(self)
        self.char_input.setGeometry(210, 615, 480, 80)
        self.char_input.setStyleSheet("color:black; font-size:30px; border: 10px solid #f4f4f4; "
                                      "background-color: rgb(255, 255, 255);")
        # 发送按钮
        self.submit = QPushButton('发送', self)
        self.submit.setToolTip('点击发送')  # 当鼠标放上去后显示的内容
        self.submit.setGeometry(695, 615, 100, 80)
        self.submit.setStyleSheet("color:black; font-size:20px; font-weight:bold; border-radius:2;"
                                  "background-color: rgb(131, 175, 155);")
        # 点击发送按钮，发送消息
        item = QListWidgetItem(QIcon("/Users/ctb/Downloads/photo_图片/2.png"), "你好！有什么可以为你服务的？", self.chatBox)
        self.submit.clicked.connect(self.send_message)  # 信号与槽的连接

    def send_message(self):
        # 用户输出什么信息
        content = self.char_input.text()
        if len(content) == 0:
            return  # 函数终结
        # 把输入的信息显示在聊天区
        item = QListWidgetItem(QIcon("/Users/ctb/Downloads/photo_图片/3.png"), content, self.chatBox)
        # 清空输入框
        self.char_input.clear()
        robot_reply = self.AI_robot.get_reply(content)
        # 当询问天气等缺少地点元素的时候
        global connect_flag, word_flag
        if connect_flag:
            content = content + connect_word
            robot_reply = self.AI_robot.get_reply(content)
            connect_flag = False
        self.deal_message(robot_reply, content)
        #
        # 下面这个是处理重复输入多次函数
        robot_reply = self.deal_reprtion(robot_reply)
        # 改变背景
        self.change_background()
        self.reply(robot_reply)

    # 消息回复
    def reply(self, robot_reply):
        if robot_reply is None:
            return
        if len(robot_reply) >= 16:
            count = int(len(robot_reply) / 16)
            for i in range(0, count):
                if i == 0:
                    res = robot_reply[16 * i:(16 * (i + 1) - 1)]
                    item = QListWidgetItem(QIcon("AI_robot.png"), res, self.chatBox)
                else:
                    res = robot_reply[16 * i - 1:(16 * (i + 1) - 1)]
                    item = QListWidgetItem(res, self.chatBox)
            if len(robot_reply) / 16 > count:
                res = robot_reply[16 * count - 1:]
                item = QListWidgetItem(res, self.chatBox)
            return
        item = QListWidgetItem(QIcon("AI_robot.png"), robot_reply, self.chatBox)

    def deal_message(self, robot_reply, content):
        # 处理句子的连接
        for index, item in enumerate(key_word):
            if item in robot_reply:
                global connect_flag
                connect_flag = True
        # 处理重复输入
        global word_flag, connect_word
        if word_flag == 0:
            connect_word = content
        if connect_word == content:
            word_flag = word_flag + 1
        else:
            word_flag = 0
        # 处理背景的改变
        global bg_flag
        for index, item in enumerate(weather):
            if item in robot_reply:
                bg_flag = index + 1
                break
            else:
                bg_flag = 0

    def deal_reprtion(self, robot_reply):
        global word_flag
        if word_flag == 2:
            robot_reply = '这个问题我已经回答过了'
        elif word_flag == 3:
            robot_reply = '你是憨憨嘛？都说了回答了你还问，再问就不理你了。'
        elif word_flag == 4:
            robot_reply = '不理你了'
        elif word_flag >= 5:
            robot_reply = None
        return robot_reply

    def change_background(self):
        global bg_flag
        if bg_flag == 1:
            self.chatBox.setStyleSheet("background-image: url(sunny.png);border:2px solid #c4c4c4; font-size:30px")
        elif bg_flag == 2:
            self.chatBox.setStyleSheet("background-image: url(foggy.png);border:2px solid #c4c4c4; font-size:30px")
        elif bg_flag == 3:
            self.chatBox.setStyleSheet("background-image: url(rainy.png);border:2px solid #c4c4c4; font-size:30px")
        elif bg_flag == 4:
            self.chatBox.setStyleSheet("background-image: url(cloudy.png);border:2px solid #c4c4c4; font-size:30px")
        else:
            self.chatBox.setStyleSheet("background-image: url(background.png);border:2px solid #c4c4c4; font-size:30px")


class Chat_robot:
    def __init__(self):
        self.AK = AK
        self.SK = SK
        self.access_token = self.get_access_token()

    def get_access_token(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + \
               self.AK + '&client_secret=' + self.SK
        response = requests.get(host).json()
        return response['access_token']

    def get_reply(self, user_input):
        post_data = json.dumps({
            "log_id": "UNITTEST_10000",
            "version": "2.0",
            "service_id": "S29968",
            "session_id": "",
            "request": {
                "query": user_input,
                "user_id": "8888",
            },
            "dialog_state": {
                "contexts": {
                    "SYS_REMEMBERED_SKILLS": ["1028652"]
                }
            }
        })
        # json.dumps() 用于将dict类型的数据转成str，因为如果直接将dict类型的数据写入json文件中会发生报错，因此在将数据写入时需要用到该函数

        url = 'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=' + self.access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(url, data=post_data, headers=headers).json()
        if response:
            return response['result']['response_list'][0]['action_list'][0]['say']


# 控件  位置  样式
# 程序的主入口会有main函数
# python把每一个py脚本看成模块，可以单独运行
if __name__ == "__main__":
    # 实例化一个应用对象
    app = QtWidgets.QApplication(sys.argv)
    # 实例化聊天窗
    win = ChatBox()
    win.show()
    sys.exit(app.exec_())
