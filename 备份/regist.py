# coding:utf-8
import sys, os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import hashlib
import sqlite3
import time
import datetime
from math import ceil
import xlwt

'''
VERSION:0.1.1000
'''

class DataBase():
    def __init__(self):
        file_name = os.path.join(os.getcwd(),'basetable.db')
        self.con = sqlite3.connect(file_name,check_same_thread=False)
        self.cur = self.con.cursor()


class SignInWidget(QWidget):
#    is_admin_signal = pyqtSignal()

    def __init__(self):
        super(SignInWidget, self).__init__()
        self.setFixedSize(250, 300)
        self.setWindowTitle("死亡证明")
        self.set_up_ui()
#        self.setWindowFlags(Qt.FramelessWindowHint)  #设置标题栏透明

    def set_up_ui(self):
        self.create_regist()
        self.create_title()
        mainlayout = QVBoxLayout()
        mainlayout.addWidget(self.blankbox)
        mainlayout.addWidget(self.registbox)
        self.setLayout(mainlayout)

    def create_regist(self):

        self.label1 = QLineEdit()
        self.label1.setPlaceholderText("请输入用户名")
        self.label1.setClearButtonEnabled(True)
        self.label1.setFixedHeight(30)

        reg = QRegExp('[a-z]{2}[0-9]{3}')
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

        self.bnt1.clicked.connect(self.sign_in_check)
        self.label2.returnPressed.connect(self.sign_in_check)
        self.label1.returnPressed.connect(self.sign_in_check)

        self.registbox = QGroupBox()
        vbox = QVBoxLayout()
        vbox.addWidget(self.label1)
        vbox.addWidget(self.label2)
        vbox.addWidget(self.bnt1)

        self.registbox.setStyleSheet('QGroupBox{background-color:#f0f0f0; }')
        self.registbox.setLayout(vbox)

    def create_title(self):
        self.blankbox = QGroupBox()
        vbox = QVBoxLayout()
        self.title = QLabel('死亡证明登记系统')
        self.title.setFont(QFont('Roman Times', 16,QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)

        vbox.addWidget(self.title)
        self.blankbox.setStyleSheet('QGroupBox{background-color:#f0f0f0;border:hide}')

        self.blankbox.setLayout(vbox)

    def sign_in_check(self):
        username = self.label1.text()
        password = self.label2.text()
        if (username == '' or password == ''):
            QMessageBox.warning(self,'提示','用户名或密码为空', QMessageBox.Yes, QMessageBox.Yes)
            return
        self.db = DataBase()
        sql = 'SELECT password FROM user WHERE name = "%s"'%(username)
        a = self.db.cur.execute(sql)
        b = 0
        for i in a:
            b = i[0]

        h1 = hashlib.md5()
        h1.update(password.encode(encoding='utf-8'))
        if ( not b):
            QMessageBox.information(self,'提示','帐号不存在',QMessageBox.Yes,QMessageBox.Yes)
        else:
            if h1.hexdigest() == b :
                #print(QMessageBox.information(self,'提示','帐号存在',QMessageBox.Yes,QMessageBox.Yes))
                mainWindow.close()
                self.a = ListWindow()
                self.a.show()

            else:
                QMessageBox.information(self,'提示','密码错误',QMessageBox.Yes,QMessageBox.Yes)
        self.con.close()
        return

class ListWindow(QWidget):

    def __init__(self):
        super(ListWindow,self).__init__()
        self.setWindowTitle('主页')
        self.setFixedSize(800, 600)
        self.set_ui()

    def set_ui(self):

        self.regist_bnt = QPushButton()
        self.query_bnt = QPushButton()
        self.setting_bnt = QPushButton()
        self.regist_bnt.clicked.connect(self.regist_click)
        self.query_bnt.clicked.connect(self.query_click)
        self.setting_bnt.clicked.connect(self.user_change)

        self.mainlayout = QVBoxLayout()
        self.icon_layout = QHBoxLayout()

        self.icon_layout.addWidget(self.regist_bnt)
        self.icon_layout.addWidget(self.query_bnt)
        self.icon_layout.addWidget(self.setting_bnt)
        self.regist_bnt.setFixedSize(200,200)
        self.query_bnt.setFixedSize(200,200)
        self.setting_bnt.setFixedSize(200,200)
        self.regist_bnt.setStyleSheet('background-image:url(./img/regist.png);border:hide;')
        self.query_bnt.setStyleSheet('background-image:url(./img/query.png);border:hide;')
        self.setting_bnt.setStyleSheet('background-image:url(./img/setting.png);border:hide;')


        self.v1box = QWidget()
        self.v1box.setLayout(self.icon_layout)
        self.mainlayout.addWidget(self.v1box)
        self.setLayout(self.mainlayout)

    def regist_click(self):
        self.close()
        self.a = RegistWindow()
        self.a.show()

    def user_change(self):
        self.close()
        self.a = UserInfoWindow()
        self.a.show()

    def query_click(self):
        self.close()
        self.a = QueryWindow()
        self.a.show()
        # self.a.showFullScreen()


class UserInfoWindow(QWidget):

    def __init__(self):
        super(UserInfoWindow,self).__init__()
        self.setWindowTitle('账号信息')
        self.setFixedSize(300, 400)
        self.db = DataBase()
        self.set_ui()

    def set_ui(self):

        info = self.db.cur.execute('select * from user')
        infolist = []
        for i in info:
            for j in range(4):
                infolist.append(i[j])


        self.name = QLineEdit()
        self.name.setText(infolist[0])
        self.name.setReadOnly(True)
        self.name.setStyleSheet('background-color:#f0f0f0;')

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

        self.confirm_bnt = QPushButton('确定(ENT)')
        self.confirm_bnt.clicked.connect(self.ok_click)
        self.cancel_bnt = QPushButton('取消(ESC)')
        self.cancel_bnt.clicked.connect(self.back_click)

        self.message = QLabel()
        self.message.setStyleSheet('QLabel{color:red;font-size:20px;}')
        self.message.setAlignment(Qt.AlignCenter)

        self.vbox = QVBoxLayout()
        self.fbox = QFormLayout()
        self.toolbox = QHBoxLayout()

        self.fbox.addRow('姓名',self.name)
        self.fbox.addRow('密码',self.password)
        self.fbox.addRow('确认密码',self.password2)
        self.fbox.addRow('单位名称',self.department)

        self.toolbox.addWidget(self.cancel_bnt)
        self.toolbox.addWidget(self.confirm_bnt)

        self.f2box = QWidget()
        self.tool2box = QWidget()

        self.f2box.setLayout(self.fbox)
        self.tool2box.setLayout(self.toolbox)

        self.vbox.addWidget(self.f2box)
        self.vbox.addWidget(self.message)
        self.vbox.addWidget(self.tool2box)

        self.setLayout(self.vbox)

    def ok_click(self):
        if self.password.text() == self.password2.text():
            a = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
            if a == QMessageBox.Yes:
                h5 = hashlib.md5()
                h5.update(self.password.text().encode(encoding='utf-8'))
                query = self.cur
                if self.password.text() == '':
                    query.execute('update user set  department="%s"'%(self.department.text()))
                else:
                    query.execute('update user set password = "%s", department="%s"'%(h5.hexdigest(), self.department.text()))
                self.con.commit()
                self.message.setText(self.password.text())
                self.close()
                self.a = ListWindow()
                self.a.show()
            else:
                pass
        else:
            self.message.setText('两次输入密码不一致')


    def back_click(self):
        self.db.con.close()
        self.close()
        self.a = ListWindow()
        self.a.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.back_click()
        if e.key() == Qt.Key_Return:
            self.ok_click()

class RegistWindow(QWidget):

    def __init__(self):
        super(RegistWindow,self).__init__()
        self.setWindowTitle('登记')
        self.setFixedSize(400, 600)
        self.set_ui()

    def set_ui(self):

        self.back_bnt = QPushButton('返回(ESC)')
        self.back_bnt.clicked.connect(self.back_click)

        self.print_bnt = QPushButton('打印(F5)')
        self.print_bnt.clicked.connect(self.print_record)

        self.save_bnt = QPushButton('保存(F2)')
        self.save_bnt.clicked.connect(self.save_record)

        self.add_bnt = QPushButton('添加(F1)')
        self.add_bnt.clicked.connect(self.add_record)

        self.seriallabel = QLabel('编号')
        self.serialnumber = QLineEdit()
        self.serialnumber2 = str(QDateTime.currentDateTime().toPyDateTime()).replace('/',
                            '').replace(' ','').replace(':','').replace('.','').replace('-','')[:-3]
        self.serialnumber.setPlaceholderText(self.serialnumber2)
        self.serialnumber.setReadOnly(True)
        self.namelabel = QLabel('姓名')
        self.name = QLineEdit()

        self.genderlabel = QLabel('性别')
        self.gender = QLineEdit()
        self.male = QCheckBox('男')
        self.male.stateChanged.connect(self.tomale)
        self.female = QCheckBox('女')
        self.female.stateChanged.connect(self.tofemale)

        self.racelabel = QLabel('民族')
        self.race = QComboBox()
        self.race.setEditable(True)
        self.race.addItem('汉族')
        self.race.addItem('回族')
        self.race.addItem('壮族')
        self.race.addItem('藏族')
        self.race.addItem('维吾尔族')

        self.idlabel = QLabel('证件号码')
        self.id = QLineEdit()
        self.id_bnt = QLabel('请按回车ENTER')
        self.id.returnPressed.connect(self.id_to_date)

        self.birthlable = QLabel('出生日期')
        self.birthday = QDateEdit()
        self.birthchoice = QPushButton('>')
        self.birthchoice.clicked.connect(self.show_cal)

        self.addresslabel = QLabel('住址')
        self.address = QLineEdit()
        # self.provincelabel = QLabel('省份')
        # self.province = QComboBox()
        # self.citylable = QLabel('市')
        # self.city = QComboBox()
        # self.countrylabel = QLabel('区/县')
        # self.country = QComboBox()
        # self.townlabel = QLabel('乡镇')
        # self.town = QComboBox()
        # self.town.setEditable(True)

        # self.dictProvince = area.dictProvince
        # self.dictCity = area.dictCity
        # self.dictTown = area.dictTown
        # for (keys, val) in self.dictProvince.items():
        #     self.province.addItem(val, QVariant(keys))


        self.deathlabel = QLabel('死亡日期')
        self.deathdate = QDateEdit()
        self.deathchoice = QPushButton('>')
        self.deathchoice.clicked.connect(self.show_death_cal)

        self.diseaselabel = QLabel('死因')
        self.disease = QLineEdit()

        self.regist_date_lable = QLabel('登记日期')
        self.regist_date = QDateEdit(QDate.currentDate())
        self.regist_date_choice = QPushButton('>')
        self.regist_date_choice.clicked.connect(self.regist_date_cal)

        self.familylabel = QLabel('家属姓名')
        self.family = QLineEdit()

        self.tellabel= QLabel('联系方式')
        self.tel = QLineEdit()

        self.genderbox = QHBoxLayout()
        self.genderbox.addWidget(self.male)
        self.genderbox.addWidget(self.female)
        self.gender2box = QWidget()
        self.gender2box.setLayout(self.genderbox)

        self.mainbox = QVBoxLayout()
        self.gridbox = QGridLayout()
        self.hbox = QHBoxLayout()

        self.gridbox.addWidget(self.seriallabel,1,0)
        self.gridbox.addWidget(self.serialnumber,1,1,1,2)
        self.gridbox.addWidget(self.namelabel,2,0)
        self.gridbox.addWidget(self.name,2,1,1,2)
        self.gridbox.addWidget(self.idlabel,3,0)
        self.gridbox.addWidget(self.id,3,1,1,2)
        self.gridbox.addWidget(self.id_bnt,3,3)
        self.gridbox.addWidget(self.genderlabel,4,0)
        self.gridbox.addWidget(self.gender2box,4,1)
        self.gridbox.addWidget(self.racelabel,5,0)
        self.gridbox.addWidget(self.race,5,1,1,2)
        self.gridbox.addWidget(self.birthlable,6,0)
        self.gridbox.addWidget(self.birthday,6,1,1,2)
        self.gridbox.addWidget(self.birthchoice,6,3)
        # self.gridbox.addWidget(self.provincelabel,6,0)
        # self.gridbox.addWidget(self.province,6,1)
        # self.gridbox.addWidget(self.citylable,6,2)
        # self.gridbox.addWidget(self.city,6,3)
        # self.gridbox.addWidget(self.countrylabel,7,0)
        # self.gridbox.addWidget(self.country,7,1)
        # self.gridbox.addWidget(self.townlabel,7,2)
        # self.gridbox.addWidget(self.town,7,3)
        self.gridbox.addWidget(self.addresslabel,8,0)
        self.gridbox.addWidget(self.address,8,1,1,2)
        self.gridbox.addWidget(self.deathlabel,9,0)
        self.gridbox.addWidget(self.deathdate,9,1,1,2)
        self.gridbox.addWidget(self.deathchoice,9,3)
        self.gridbox.addWidget(self.diseaselabel,10,0)
        self.gridbox.addWidget(self.disease,10,1,1,2)
        self.gridbox.addWidget(self.familylabel,11,0)
        self.gridbox.addWidget(self.family,11,1,1,2)
        self.gridbox.addWidget(self.tellabel,12,0)
        self.gridbox.addWidget(self.tel,12,1,1,2)
        self.gridbox.addWidget(self.regist_date_lable,13,0)
        self.gridbox.addWidget(self.regist_date,13,1,1,2)

        self.hbox.addWidget(self.add_bnt)
        self.hbox.addWidget(self.save_bnt)
        self.hbox.addWidget(self.print_bnt)
        self.hbox.addWidget(self.back_bnt)

        self.formbox = QWidget()
        self.h2box = QWidget()
        self.formbox.setLayout(self.gridbox)
        self.h2box.setLayout(self.hbox)

        self.blank = QLabel('==========登  记==========')
        self.blank.setFont(QFont('Roman Times', 16,QFont.Bold))
        self.blank.setAlignment(Qt.AlignCenter)
        self.mainbox.addWidget(self.blank)
        self.mainbox.addWidget(self.formbox)
        self.mainbox.addWidget(self.blank)
        self.mainbox.addWidget(self.h2box)
        self.setLayout(self.mainbox)


    def back_click(self):
        self.close()
        if self.back_bnt.text() == "返回(ESC)":
            self.a = ListWindow()
            self.a.show()
        else:
            pass



    def save_record(self):
        sql = '''insert into base (serialnumber,name,id,gender,race,birthday,address,deathdate,disease,
                family,tel,regist_date,is_deleted) values ("{0}","{1}","{2}","{3}","{4}",{5},"{6}",{7},
                "{8}","{9}","{10}",{11},0)'''.format(self.serialnumber2,self.name.text(),self.id.text(),
                self.gender.text(),self.race.currentText(),self.change_date(self.birthday),self.address.text(),
                self.change_date(self.deathdate),self.disease.text(),self.family.text(),self.tel.text(),
                self.change_date(self.regist_date))
        self.db = DataBase()
        if self.name.text() != "":
            self.db.cur.execute(sql)
            self.db.con.commit()
            self.db.con.close()
            QMessageBox.information(self,'提示','保存成功！',QMessageBox.Yes,QMessageBox.Yes)
            self.save_bnt.clicked.disconnect(self.save_record)
            self.save_bnt.setText("更新(F2)")
            self.save_bnt.clicked.connect(self.update_record)
        else:
            pass

    def update_record(self):
        sql = '''update base set name = "{0}", id = "{1}",gender = "{2}",race = "{3}",birthday = {4},address = "{5}",
                deathdate = {6},disease = "{7}",family = "{8}",tel = "{9}",regist_date = {10} where serialnumber = "{11}"
            '''.format(self.name.text(),self.id.text(),self.gender.text(),self.race.currentText(),
            self.change_date(self.birthday),self.address.text(),self.change_date(self.deathdate),
            self.disease.text(),self.family.text(),self.tel.text(),self.change_date(self.regist_date),
            self.serialnumber2)
        self.db = DataBase()
        self.db.cur.execute(sql)
        self.db.con.commit()
        self.db.con.close()
        QMessageBox.information(self,'提示','修改成功！',QMessageBox.Yes,QMessageBox.Yes)

    def print_record(self):
        if self.save_bnt.text() == '保存(F2)':
            self.save_record()
        else:
            self.update_record()
        # self.close()
        self.b = PrintWindow(self.serialnumber2)
        self.b.show()

    def add_record(self):
        if self.save_bnt.text == '保存(F2)':
            self.save_record()
        else:
            self.update_record()
        self.close()
        self.a = RegistWindow()
        self.a.show()

    def show_cal(self):
        self.d = Calendar()
        self.d.show()
        self.d.date_signal.connect(self.change_birthday)

    def change_birthday(self, date):
        self.birthday.setDate(date)

    def show_death_cal(self):
        self.d = Calendar()
        self.d.show()
        self.d.date_signal.connect(self.change_death_date)

    def change_death_date(self, date):
        self.deathdate.setDate(date)

    def regist_date_cal(self):
        pass

    def id_to_date(self):
        id_upper = self.id.text().upper()
        if len(id_upper) == 18:
            self.id.setText(id_upper)
            year = int(id_upper[6:10])
            month =int(id_upper[10:12])
            day = int(id_upper[12:14])
            self.birthday.setDate(QDate(year,month,day))
            gender = int(id_upper[-2])
            if gender%2==0:
                self.female.setChecked(True)
                self.male.setChecked(False)
            else:
                self.female.setChecked(False)
                self.male.setChecked(True)

            certify_number = ['1','0','X','9','8','7','6','5','4','3','2','1']
            std_number = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
            sum = 0
            for i in range(17):
                sum += int(id_upper[i])*std_number[i]
            certify_rslt = certify_number[sum%11]
            if certify_rslt != id_upper[-1]:
                self.id_bnt.setText('身份证号码不正确')
                self.id_bnt.setStyleSheet('QLabel{color:red}')
            else:
                self.id_bnt.setText('请按回车ENTER')
        else:
            self.id_bnt.setText('请按回车ENTER')

    def tomale(self,state):
        if state == Qt.Checked:
            self.gender.setText('男')
            self.female.setChecked(False)

    def tofemale(self,state):
        if state == Qt.Checked:
            self.gender.setText('女')
            self.male.setChecked(False)

    def change_date(self,a):   # yyyymmdd to time stamp
        pydate = a.date().toPyDate()
        base_date = datetime.date(1970,1,1)
        day_delta = pydate - base_date
        days = day_delta.days
        seconds = days*24*3600
        return seconds



    def keyPressEvent(self,e):
        if e.key() == Qt.Key_F2 and self.save_bnt.text == '保存(F2)':
            self.save_record()
        if e.key() == Qt.Key_F2 and self.save_bnt.text == '更新(F2)':
            self.update_record()
        if e.key() == Qt.Key_Escape:
            self.back_click()
        if e.key() == Qt.Key_F1:
            self.add_record()
        if e.key() == Qt.Key_F5:
            self.print_record()


class Calendar(QWidget):

    date_signal = pyqtSignal(QDate)
    def __init__(self):
        super(Calendar,self).__init__()


#        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('日历')
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.clicked.connect(self.show_date)
        vbox = QVBoxLayout()
        vbox.addWidget(self.cal)
        self.setLayout(vbox)


    def show_date(self):
        date = self.cal.selectedDate()
        self.date_signal.emit(date)
        self.close()


class PrintWindow(QWidget):
    def __init__(self,serialnumber):
        super(PrintWindow,self).__init__()
        self.printer = QPrinter()
        self.printer.setPageSize(QPrinter.A4)
        self.db = DataBase()
        self.setWindowTitle('打印')
        self.setFixedSize(680,960)
        self.serialnumber = serialnumber
        self.set_ui()

    def set_ui(self):
        self.db.cur.execute('select * from base where serialnumber = %s'%self.serialnumber)
        rslt = self.db.cur.fetchone()
        self.db.cur.execute('select department from user')
        rslt2 = self.db.cur.fetchone()
        text = '''<style>#normal {text-indent:40px;font:24px;line-height:40px;}</style>
                 <p style="text-align:center;white-space:pre;font:40px">证     明</p><br>'''
        self.db.con.close()
        try:
            if rslt:
                text += '''<p id='normal'>{0}，{1}，{2}，{3}出生，身份证号码：
                            {4}，常住地址：{5}，{6}因{7}去世。</p>
                            <p id='normal'>特此证明！</p><br><br><br><br><br><br>
                            <p id='normal'>申请人：{8}</p>
                            <p id='normal'>联系方式：{9}</p>
                            <br>
                            <br>
                            <br>
                            <br>
                            <br>
                            <br>
                            <p id = 'normal' style="text-align:right;margin-right:40px">{10}</p>
                            <p id = 'normal' style="text-align:right;margin-right:40px;">{11}</p>
                            '''.format(rslt[1],rslt[3],rslt[4],self.change_date(rslt[5]),rslt[2],rslt[6],
                                self.change_date(rslt[7]),rslt[8],rslt[9],rslt[10],rslt2[0],self.change_date(rslt[11]))
        except:
            text = '姓名未填写！！！！'


        self.bnt1 = QPushButton('关闭(ESC)')
        self.bnt1.clicked.connect(self.back_click)
        self.bnt2 = QPushButton('打印(ENT)')
        self.bnt2.clicked.connect(lambda:self.print_record(text))
        # self.bnt2.clicked.connect(lambda:self.print_record(self.content.toPlainText()))

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(2)
        self.hbox.addWidget(self.bnt1)
        self.hbox.addWidget(self.bnt2)

        self.hbox_layout = QWidget()
        self.hbox_layout.setLayout(self.hbox)

        self.content = QTextEdit()
        self.content.setStyleSheet('border:hide;background-color:#f0f0f0;')
        self.content.insertHtml(text)
        self.content.setReadOnly(True)
        self.vbox.addWidget(self.hbox_layout)
        self.vbox.addWidget(self.content)
        self.setLayout(self.vbox)


    def back_click(self):
        self.close()
        # self.a = ListWindow()
        # self.a.show()

    def print_record(self,htmltxt):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            document = QTextDocument()
            document.setHtml(htmltxt)
            document.print_(self.printer)
        self.close()

    def change_date(self,a):  #time stamp to yyyymmdd
        date = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=a)
        return str(date.year)+'年'+ str(date.month) +'月'+str(date.day)+'日'

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.back_click()
        # if e.key() == Qt.Key_Return:  #print_record function need a parameter; waiting for reparing.
            # self.print_record()

class QueryWindow(QWidget):


    def __init__(self):
        super(QueryWindow,self).__init__()
        self.setWindowTitle('查询')
        # self.setFixedSize(1200,960)
        self.resize(960, 720)
        # self.move(50, 50)
        self.set_ui()


    def set_ui(self):

        self.closebnt = QPushButton('关闭(ESC)')
        self.closebnt.clicked.connect(self.back_click)
        self.querybnt = QPushButton('查询(ENT)')
        self.querybnt.clicked.connect(lambda:self.query_click())
        self.clearbnt = QPushButton('清空(F1)')
        self.clearbnt.clicked.connect(self.clear_click)
        self.exportbnt = QPushButton('导出(F5)')
        self.exportbnt.clicked.connect(self.export_click)
        self.table = QTableWidget(20,11)
        self.pre_bnt = QPushButton('<上一页')
        self.next_bnt = QPushButton('下一页>')
        self.page = QLabel()
        self.pre_bnt.clicked.connect(self.pre_page)
        self.next_bnt.clicked.connect(self.next_page)
        self.this_page = 1
        self.max_page = 1


        self.namelabel = QLabel('姓名')
        self.name = QLineEdit()
        self.idlabel = QLabel("身份证号码")
        self.id = QLineEdit()
        self.begin_date_label = QLabel('开始日期')
        self.begin_date = QDateEdit()
        self.begin_date_choice = QPushButton("↓")
        self.begin_date_choice.clicked.connect(self.begin_date_input)
        self.end_date_label = QLabel('截止日期')
        self.end_date = QDateEdit(QDate.currentDate())
        self.end_date_choice = QPushButton("↓")
        self.end_date_choice.clicked.connect(self.end_date_input)
        self.all_record = QRadioButton('所有个案')
        self.all_record.setChecked(True)
        self.no_del_record = QRadioButton("不含删除个案")
        self.no_del_record.setChecked(False)
        self.death_date = QRadioButton('按死亡日期')
        self.death_date.setChecked(False)
        self.report_date = QRadioButton('按登记日期')
        self.report_date.setChecked(True)
        self.tab_space = QLabel("------------------------")
        self.tab_space2 = QLabel("------------------")

        self.demand_box = QGridLayout()
        self.demand_box.addWidget(self.namelabel,0,0,1,1)
        self.demand_box.addWidget(self.name,0,1,1,1)
        self.demand_box.addWidget(self.idlabel,0,2,1,1)
        self.demand_box.addWidget(self.id,0,3,1,1)
        self.demand_box.addWidget(self.begin_date_label,0,4,1,1)
        self.demand_box.addWidget(self.begin_date,0,5,1,2)
        self.demand_box.addWidget(self.begin_date_choice,0,8,1,1)
        self.demand_box.addWidget(self.end_date_label,0,9,1,1)
        self.demand_box.addWidget(self.end_date,0,10,1,5)
        self.demand_box.addWidget(self.end_date_choice,0,16,1,1)

        self.choice_box = QGridLayout()
        self.record_choice_box = QHBoxLayout()
        self.date_choice_box = QHBoxLayout()
        self.record_choice_box.addWidget(self.all_record)
        self.record_choice_box.addWidget(self.no_del_record)
        self.date_choice_box.addWidget(self.report_date)
        self.date_choice_box.addWidget(self.death_date)

        self.record_choice_layout = QWidget()
        self.date_choice_layout = QWidget()
        self.record_choice_layout.setLayout(self.record_choice_box)
        self.date_choice_layout.setLayout(self.date_choice_box)

        self.choice_box.addWidget(self.record_choice_layout,1,0,1,3)
        self.choice_box.addWidget(self.tab_space,1,3,1,1)
        self.choice_box.addWidget(self.date_choice_layout,1,4,1,1)

        self.bnt_box = QGridLayout()
        self.bnt_box.addWidget(self.querybnt,0,1,1,1)
        self.bnt_box.addWidget(self.clearbnt,0,2,1,1)
        self.bnt_box.addWidget(self.exportbnt,0,3,1,1)
        self.bnt_box.addWidget(self.closebnt,0,4,1,1)

        self.page_box = QGridLayout()
        self.page_box.addWidget(self.tab_space2,0,0,1,1)
        self.page_box.addWidget(self.pre_bnt,0,1,1,1)
        self.page_box.addWidget(self.page,0,2,1,1)
        self.page_box.addWidget(self.next_bnt,0,3,1,1)

        self.demand_box_layout = QWidget()
        self.bnt_box_layout = QWidget()
        self.choice_box_layout = QWidget()
        self.page_box_layout = QWidget()

        self.demand_box_layout.setLayout(self.demand_box)
        self.bnt_box_layout.setLayout(self.bnt_box)
        self.choice_box_layout.setLayout(self.choice_box)
        self.page_box_layout.setLayout(self.page_box)

        self.table.verticalHeader().setVisible(True)
        self.table.setHorizontalHeaderLabels(['编号','姓名','身份证号码','性别','出生日期','常住地址','死亡日期','死亡原因','登记日期','是否报告','操作'])
        self.table.resizeColumnToContents(3)


        self.head_box = QGridLayout()
        self.head_box.addWidget(self.demand_box_layout,0,0,1,10)
        self.head_box.addWidget(self.bnt_box_layout,0,11,1,4)
        self.head_box.addWidget(self.choice_box_layout,1,0,1,5)
        self.head_box.addWidget(self.page_box_layout,1,12,1,3)
        self.head_box.addWidget(self.table,2,0,1,15)

        self.setLayout(self.head_box)


    def back_click(self):
        self.close()
        self.a = ListWindow()
        self.a.show()


    def query_click(self,start = 0, numbers = 20):
        self.db = DataBase()
        self.numbers =  numbers
        self.start = start
        if self.name.text() == '':
            name_sql = ' and name like "%"'
        else:
            name_text = '%' + self.name.text() + '%'
            name_sql = ' and name like "%s"'%(name_text)

        if self.all_record.isChecked():
            is_deleted_sql = ''
        else:
            is_deleted_sql = 'and is_deleted = 0 '
        if self.death_date.isChecked():
            date_sql = 'deathdate'
        else:
            date_sql = 'regist_date'
        a = RegistWindow()
        begin_date_interge = a.change_date(self.begin_date)
        end_date_interge = a.change_date(self.end_date)
        sql = '''
            select serialnumber,name,id,gender,birthday,address,deathdate,disease,regist_date,is_deleted from base where date2 between %d and %d
            '''%(begin_date_interge,end_date_interge)
        number_sql = 'select count(*) from base where date2 between %d and %d '%(begin_date_interge,end_date_interge)
        if self.id.text() != "":
            sql2 = 'select serialnumber,name,id,gender,birthday,address,deathdate,disease,regist_date,is_deleted from base where id = %s limit %d offset %d'%(self.id.text(),self.numbers, self.start)
            sql3 = 'select count(*) from base where id = %s '%(self.id.text())
        else:
            sql2 = sql.replace('date2',date_sql) + is_deleted_sql + name_sql + '  limit %d offset %d'%(self.numbers,self.start)
            sql3 = number_sql.replace('date2',date_sql) + is_deleted_sql + name_sql
        rlst_exec = self.db.cur.execute(sql2)
        rslt =  rlst_exec.fetchall()
        count = self.db.cur.execute(sql3).fetchone()[0]
        pages = ceil(count/self.numbers)
        pages_text = '共' + str(count) +'条 ' + str(pages) + '页，第' + str(self.this_page) +'页'
        self.page.setText(pages_text)
        self.max_page = pages
        k = 0
        self.table.clear()
        self.table.setHorizontalHeaderLabels(['编号','姓名','身份证号码','性别','出生日期','常住地址','死亡日期','死亡原因','登记日期','是否报告','操作'])
        for i in rslt:
            for j in range(9):
                if j in [4,6,8]:
                    self.table.setItem(k,j,QTableWidgetItem(self.to_date(i[j])))
                else:
                    self.table.setItem(k,j,QTableWidgetItem(i[j]))
                self.table.setCellWidget(k,10,self.button_row(i[0]))
            k += 1
        self.db.con.close()

    def button_row(self, id):
        self.db = DataBase()
        self.widget = QWidget()
        self.query_id = id
        self.view_bnt = QPushButton('查看')
        self.del_bnt = QPushButton('删除')
        self.regret_bnt = QPushButton('恢复')
        self.print_bnt = QPushButton('打印')

        self.view_bnt.setStyleSheet('''text-align:center;
                                       background-color:green;
                                       border-style:outset;
                                       height:20px;
                                       color:white;
                                    ''')
        self.del_bnt.setStyleSheet('''text-align:center;
                                       background-color: red;
                                       border-style:outset;
                                       height:20px;
                                       color:white;
                                    ''')
        self.regret_bnt.setStyleSheet('''text-align:center;
                                       background-color: grey;
                                       border-style:outset;
                                       height:20px;
                                       color:white;
                                    ''')
        self.print_bnt.setStyleSheet('''text-align:center;
                                       background-color: #660099;
                                       border-style:outset;
                                       height:20px;
                                       color:white;
                                    ''')

        self.hlayout = QHBoxLayout()
        self.db.cur.execute('select * from base where serialnumber = %s'%(self.query_id))
        rslt = self.db.cur.fetchone()
        self.db.con.close()
        if rslt[-1] == 1:
            self.hlayout.addWidget(self.regret_bnt)
        else:
            self.hlayout.addWidget(self.view_bnt)
            self.hlayout.addWidget(self.print_bnt)
            self.hlayout.addWidget(self.del_bnt)
        self.view_bnt.clicked.connect(lambda:self.view_record(rslt[0]))
        self.del_bnt.clicked.connect(lambda:self.del_record(rslt[0]))
        self.regret_bnt.clicked.connect(lambda:self.regret_record(rslt[0]))
        self.print_bnt.clicked.connect(lambda:self.print_record(rslt[0]))
        self.hlayout.setContentsMargins(5,2,5,2)
        self.widget.setLayout(self.hlayout)
        return self.widget

    def view_record(self,id):
        self.db = DataBase()
        self.db.cur.execute('select * from base where serialnumber = %s'%(id))
        b = self.db.cur.fetchone()
        self.db.con.close()
        self.a = RegistWindow()
        self.a.serialnumber.setText(b[0])
        self.a.serialnumber.setReadOnly(True)
        self.a.name.setText(b[1])
        self.a.id.setText(b[2])
        self.a.gender.setText(b[3])
        if b[3] == '男':
            self.a.male.setChecked(True)
        else:
            self.a.female.setChecked(True)
        self.a.race.setToolTip(b[4])
        birthday_list = self.to_pydate(b[5])
        self.a.birthday.setDate(QDate(birthday_list[0],birthday_list[1],birthday_list[2]))
        self.a.address.setText(b[6])
        deathdate_list = self.to_pydate(b[7])
        self.a.deathdate.setDate(QDate(deathdate_list[0],deathdate_list[1],deathdate_list[2]))
        self.a.disease.setText(b[8])
        self.a.family.setText(b[9])
        self.a.tel.setText(b[10])
        regist_list = self.to_pydate(b[11])
        self.a.regist_date.setDate(QDate(regist_list[0],regist_list[1],regist_list[2]))
        self.a.serialnumber2 = b[0]
        self.a.blank.setText("==========查  看==========")
        self.a.back_bnt.setText('关闭(ESC)')
        self.a.back_bnt.clicked.disconnect(self.a.back_click)
        self.a.back_bnt.clicked.connect(self.a.close)
        self.a.save_bnt.clicked.disconnect(self.a.save_record)
        self.a.save_bnt.clicked.connect(self.a.update_record)
        self.a.save_bnt.setText('更新(F2)')
        self.a.show()

    def del_record(self, id):
        self.db = DataBase()
        self.db.cur.execute('update base set is_deleted = 1 where serialnumber = %s'%(id))
        msg = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.db.con.commit()
        else:
            pass
        self.db.con.close()
        self.query_click()

    def regret_record(self, id):
        self.db = DataBase()
        self.db.cur.execute('update base set is_deleted = 0 where serialnumber = %s'%(id))
        msg = QMessageBox.information(self,'提示','是否更改信息？',QMessageBox.Yes,QMessageBox.No)
        if msg == QMessageBox.Yes:
            self.db.con.commit()
        else:
            pass
        self.db.con.close()
        self.query_click()

    def print_record(self, id):
        self.a = PrintWindow(id)
        self.a.show()

    def to_pydate(self,a):
        b = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=a)
        return [b.year, b.month, b.day]

    def to_date(self,a):
        b = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=a)
        c = b.strftime('%Y-%m-%d')
        return c

    def clear_click (self):
        self.name.clear()
        self.id.clear()
        self.begin_date.setDate(QDate(2000,1,1))
        self.end_date.setDate(QDate.currentDate())


    def export_click(self):
        self.db = DataBase()
        if self.name.text() == '':
            name_sql = ' and name like "%"'
        else:
            name_text = '%' + self.name.text() + '%'
            name_sql = ' and name like "%s"'%(name_text)

        if self.all_record.isChecked():
            is_deleted_sql = ''
        else:
            is_deleted_sql = 'and is_deleted = 0 '
        if self.death_date.isChecked():
            date_sql = 'deathdate'
        else:
            date_sql = 'regist_date'
        a = RegistWindow()
        begin_date_interge = a.change_date(self.begin_date)
        end_date_interge = a.change_date(self.end_date)
        sql = '''
            select serialnumber,name,id,gender,birthday,address,deathdate,disease,regist_date,is_deleted from base where date2 between %d and %d
            '''%(begin_date_interge,end_date_interge)
        number_sql = 'select * from base where date2 between %d and %d '%(begin_date_interge,end_date_interge)
        if self.id.text() != "":
            sql3 = 'select * from base where id = %s '%(self.id.text())
        else:
            sql3 = number_sql.replace('date2',date_sql) + is_deleted_sql + name_sql
        self.db.cur.execute(sql3)
        rslt = self.db.cur.fetchall()

        file, ok = QFileDialog.getSaveFileName(self,'文件保存','./','Excel Files (*.xls)')
        workbook = xlwt.Workbook(encoding='utf8')
        worksheet = workbook.add_sheet("sheet1")
        head = ['编号','姓名','身份证号码','性别','民族','出生日期','住址','死亡日期','死因','联系人','联系方式','登记日期','备注','是否删除']
        date_style = xlwt.XFStyle()
        date_style.num_format_str = 'yyyy/mm/dd'
        k = len(rslt)
        for i in range(k+1) :
            if i == 0:
                for j in range(14):
                    worksheet.write(i,j,head[j])
            else:
                for j in range(14):
                    if j in [5,7,11]:
                        worksheet.write(i,j,rslt[i-1][j]/3600/24+25570,date_style)
                    else:
                        worksheet.write(i,j,rslt[i-1][j])
        workbook.save(file)
        QMessageBox.warning(self,'success','保存成功')
        self.db.con.close()

    def begin_date_input(self):
        self.a = Calendar()
        self.a.show()
        self.a.date_signal.connect(self.begin_date_confirm)

    def begin_date_confirm(self, date):
        self.begin_date.setDate(date)

    def end_date_input(self):
        self.a = Calendar()
        self.a.show()
        self.a.date_signal.connect(self.end_date_confirm)

    def end_date_confirm(self, date):
        self.end_date.setDate(date)

    def next_page(self):
        self.this_page += 1
        if self.this_page < self.max_page:
            a =  (self.this_page-1) * 20
        else:
            a = (self.max_page-1)*20
            self.this_page = self.max_page
        self.query_click(start=a)

    def pre_page(self):
        self.this_page -= 1
        if self.this_page == 0:
            self.this_page = 1
        else:
            self.this_page = self.this_page
        a = (self.this_page-1)*20
        self.query_click(start=a)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.back_click()
        if e.key() == Qt.Key_Return:
            self.query_click()
        if e.key() == Qt.Key_F1:
            self.clear_click()
        if e.key() == Qt.Key_F5:
            self.export_click()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./img/octo.png'))
    mainWindow = SignInWidget()
    # mainWindow = ListWindow()
    mainWindow.show()
    sys.exit(app.exec_())
