#coding:utf-8
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import hashlib
import sqlite3
#import qdarkstyle

class SignInWidget(QWidget):
#    is_admin_signal = pyqtSignal()

    def __init__(self):
        super(SignInWidget, self).__init__()
        self.setFixedSize(250, 300)
        self.setWindowTitle("NCD")
        self.setUpUI()
#        self.setWindowFlags(Qt.FramelessWindowHint)  #设置标题栏透明

    def setUpUI(self):
        self.createRegist()
        self.createtitle()
        mainlayout = QVBoxLayout()
        mainlayout.addWidget(self.blankbox)
        mainlayout.addWidget(self.registbox)
        self.setLayout(mainlayout)

    def createRegist(self):

        self.label1 = QLineEdit()
        self.label1.setPlaceholderText("请输入用户名")
        self.label1.setClearButtonEnabled(True)
    #    self.label1.setFixedWidth(190)
        self.label1.setFixedHeight(30)

        reg = QRegExp('hs[0-9]{3}')
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.label1.setValidator(pValidator)

        self.label2 = QLineEdit()
        self.label2.setPlaceholderText("请输入密码")
        self.label2.setClearButtonEnabled(True)
        self.label2.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.label2.setFixedHeight(30)
        self.label2.setFont(QFont())

        self.bnt1 = QPushButton("登    录")
        self.bnt1.setFixedHeight(30)
        self.bnt1.setStyleSheet('QPushButton{background-color:DodgerBlue;color:white;border:hide;}')

        self.bnt1.clicked.connect(self.signInCheck)
        self.label2.returnPressed.connect(self.signInCheck)
        self.label1.returnPressed.connect(self.signInCheck)

        self.registbox = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.label1)
        vbox.addWidget(self.label2)
        vbox.addWidget(self.bnt1)

        self.registbox.setStyleSheet('QGroupBox{background-color:#f0f0f0; }')
        self.registbox.setLayout(vbox)

    def createtitle(self):
        self.blankbox = QGroupBox()
        vbox = QVBoxLayout()
        self.title = QLabel('死亡证明登记系统')
        self.title.setFont(QFont('Roman Times', 16,QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)

        vbox.addWidget(self.title)
        self.blankbox.setStyleSheet('QGroupBox{background-color:#f0f0f0;border:hide}')

        self.blankbox.setLayout(vbox)

    def signInCheck(self):
        username = self.label1.text()
        password = self.label2.text()
        if (username == '' or password == ''):
            print(QMessageBox.warning(self,'alert','用户名或密码为空', QMessageBox.Yes, QMessageBox.Yes))
            return
#        db = QSqlDatabase.addDatabase("QSQLITE")
#        db.setDatabaseName('.basetable.db')
#        db.open()
#        query = QSqlQuery()
        db = sqlite3.connect('basetable.db')
        query = db.cursor()
        sql = 'SELECT password FROM user WHERE name = "%s"'%(username)
#        query.exec_(sql)
        a = query.execute(sql)
        b = 0
        for i in a:
            b = i[0]

        h1 = hashlib.md5()
        h1.update(password.encode(encoding='utf-8'))
        if ( not b):
            print(QMessageBox.information(self,'提示','帐号不存在',QMessageBox.Yes,QMessageBox.Yes))
        else:
            if h1.hexdigest() == b :
                #print(QMessageBox.information(self,'提示','帐号存在',QMessageBox.Yes,QMessageBox.Yes))
                mainWindow.close()
                self.a = listWindow()
                self.a.show()

            else:
                print(QMessageBox.information(self,'提示','密码错误',QMessageBox.Yes,QMessageBox.Yes))
        db.close()
        return

class listWindow(QWidget):

    def __init__(self):
        super(listWindow,self).__init__()
        self.setWindowTitle('main')
        self.setFixedSize(600, 400)
        self.setUI()

    def setUI(self):

        self.bnt1 = QPushButton()
        self.bnt2 = QPushButton()
        self.bnt3 = QPushButton()
        self.bnt1.clicked.connect(self.userChange)
        self.bnt2.clicked.connect(self.backClick)
        self.bnt3.clicked.connect(self.queryClick)

        self.mainlayout = QVBoxLayout()
        self.lvl1layout = QHBoxLayout()

        self.lvl1layout.addWidget(self.bnt2)
        self.lvl1layout.addWidget(self.bnt3)
        self.lvl1layout.addWidget(self.bnt1)
        self.bnt1.setFixedSize(200,200)
        self.bnt2.setFixedSize(200,200)
        self.bnt3.setFixedSize(200,200)
        self.bnt1.setStyleSheet('QPushButton{background-image:url(img/mobile.png);border:hide;}')
        self.bnt2.setStyleSheet('QPushButton{background-image:url(img/mdaudio.png);border:hide;}')
        self.bnt3.setStyleSheet('QPushButton{background-image:url(img/mic.png);border:hide;}')

        self.v2box = QWidget()
        self.v2box.setLayout(self.lvl1layout)
        self.mainlayout.addWidget(self.v2box)
        self.setLayout(self.mainlayout)

    def backClick(self):
        self.close()
        self.a = registWindow()
        self.a.show()

    def userChange(self):
        self.close()
        self.a = userInfoWindow()
        self.a.show()

    def queryClick(self):
        self.close()
        self.a = queryWindow()
        self.a.show()



class userInfoWindow(QWidget):

    def __init__(self):
        super(userInfoWindow,self).__init__()
        self.setWindowTitle('user infomation')
        self.setFixedSize(300,400)
        self.setUi()

    def setUi(self):

        db = sqlite3.connect('basetable.db')
        query = db.cursor()
        info = query.execute('select * from user')
        infolist = []
        for i in info:
            for j in range(4):
                infolist.append(i[j])
        db.close()

        self.namelabel = QLabel('用户名  ')
        self.passwordlabel1= QLabel('输入密码 ')
        self.passwordlabel2= QLabel('确认密码 ')
        self.departmentlabel = QLabel('单位名称 ')

        self.name = QLineEdit()
        self.name.setText(infolist[0])
        self.name.setReadOnly(True)
        self.name.setStyleSheet('QLineEdit{background-color:#f0f0f0}')

        self.password= QLineEdit()
        self.password.setPlaceholderText('请输入密码')
        self.password.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password.setClearButtonEnabled(True)


        self.password2= QLineEdit()
        self.password2.setPlaceholderText('请再次输入密码')
        self.password2.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.password.setClearButtonEnabled(True)

        self.department = QLineEdit()
        self.department.setText(infolist[3])
        self.department.setPlaceholderText('请输入单位名称')
        self.department.setClearButtonEnabled(True)

        self.bnt1 = QPushButton('确定')
        self.bnt1.clicked.connect(self.okClick)
        self.bnt2 = QPushButton('取消')
        self.bnt2.clicked.connect(self.backClick)

        self.message = QLabel()
        self.message.setStyleSheet('QLabel{color:red;font-size:20px;}')
        self.message.setAlignment(Qt.AlignCenter)

        self.vbox = QVBoxLayout()
        self.fbox = QFormLayout()
        self.toolbox = QHBoxLayout()

        self.fbox.addRow(self.namelabel,self.name)
        self.fbox.addRow(self.passwordlabel1,self.password)
        self.fbox.addRow(self.passwordlabel2, self.password2)
        self.fbox.addRow(self.departmentlabel,self.department)

        self.toolbox.addWidget(self.bnt2)
        self.toolbox.addWidget(self.bnt1)

        self.f2box = QWidget()
        self.tool2box = QWidget()

        self.vbox.addWidget(self.f2box)
        self.vbox.addWidget(self.message)
        self.vbox.addWidget(self.tool2box)

        self.f2box.setLayout(self.fbox)
        self.tool2box.setLayout(self.toolbox)
        self.setLayout(self.vbox)

    def okClick(self):
        if self.password.text() == self.password2.text():
            a = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
            #self.message.setText('ok')
            if a == QMessageBox.Yes:
                h5 = hashlib.md5()
                h5.update(self.password.text().encode(encoding='utf-8'))
                db = sqlite3.connect('basetable.db')
                query = db.cursor()
                if self.password.text() == '':
                    query.execute('update user set  department="%s"'%(self.department.text()))
                else:
                    query.execute('update user set password = "%s", department="%s"'%(h5.hexdigest(), self.department.text()))
                db.commit()
                db.close()
                self.message.setText(self.password.text())
                self.close()
                self.a = listWindow()
                self.a.show()
            else:
                pass
        else:
            self.message.setText('两次输入密码不一致')

    def info(self):
        db = sqlite3.connect('basetable.db')
        query = db.cursor()
        info = query.execute('select * from user')
        infolist = []
        for i in info:
            for j in range(4):
                infolist.append(i[j])
        db.close()
        return infolist

    def backClick(self):
        self.close()
        self.a = listWindow()
        self.a.show()

class registWindow(QWidget):
    def __init__(self):
        super(registWindow,self).__init__()
        self.setWindowTitle('登记')
        self.setFixedSize(300,600)
        self.setUi()

    def setUi(self):

        self.bnt1 = QPushButton('close')
        self.bnt1.clicked.connect(self.backClick)

        self.bnt2 = QPushButton('print')
        self.bnt2.clicked.connect(self.printwindow)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.bnt1)
        self.vbox.addWidget(self.bnt2)

        self.setLayout(self.vbox)


    def backClick(self):
        self.close()
        self.a = listWindow()
        self.a.show()

    def printwindow(self):
        self.close()
        self.b = printWindow()
        self.b.show()

class printWindow(QWidget):
    def __init__(self):
        super(printWindow,self).__init__()
        self.setWindowTitle('打印')
        self.setFixedSize(300,600)
        self.setUi()

    def setUi(self):

        self.bnt1 = QPushButton('close')
        self.bnt1.clicked.connect(self.backClick)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.bnt1)

        self.setLayout(self.vbox)


    def backClick(self):
        self.close()
        self.a = listWindow()
        self.a.show()

class queryWindow(QWidget):

    def __init__(self):
        super(queryWindow,self).__init__()
        self.setWindowTitle('查询')
        self.setFixedSize(600,400)
        self.setUi()

    def setUi(self):

        self.closebnt = QPushButton('close')
        self.closebnt.clicked.connect(self.backClick)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.closebnt)
        self.setLayout(self.vbox)

    def backClick(self):
        self.close()
        self.a = listWindow()
        self.a.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('octo.png'))
#    mainWindow = SignInWidget()
    mainWindow = listWindow()
    mainWindow.show()
    sys.exit(app.exec_())
