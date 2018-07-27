#coding:utf-8
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import hashlib
import sqlite3
import area
import time
import datetime
#import qdarkstyle

class SignInWidget(QWidget):
#    is_admin_signal = pyqtSignal()

    def __init__(self):
        super(SignInWidget, self).__init__()
        self.setFixedSize(250, 300)
        self.setWindowTitle("NCD")
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
                self.a = ListWindow()
                self.a.show()

            else:
                print(QMessageBox.information(self,'提示','密码错误',QMessageBox.Yes,QMessageBox.Yes))
        db.close()
        return

class ListWindow(QWidget):

    def __init__(self):
        super(ListWindow,self).__init__()
        self.setWindowTitle('main')
        self.setFixedSize(600, 400)
        self.set_ui()

    def set_ui(self):

        self.bnt1 = QPushButton()
        self.bnt2 = QPushButton()
        self.bnt3 = QPushButton()
        self.bnt1.clicked.connect(self.user_change)
        self.bnt2.clicked.connect(self.back_click)
        self.bnt3.clicked.connect(self.query_click)

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

    def back_click(self):
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



class UserInfoWindow(QWidget):

    def __init__(self):
        super(UserInfoWindow,self).__init__()
        self.setWindowTitle('user infomation')
        self.setFixedSize(300,400)
        self.set_ui()

    def set_ui(self):

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
        self.bnt1.clicked.connect(self.ok_click)
        self.bnt2 = QPushButton('取消(ESC)')
        self.bnt2.clicked.connect(self.back_click)

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

        self.f2box.setLayout(self.fbox)
        self.tool2box.setLayout(self.toolbox)

        self.vbox.addWidget(self.f2box)
        self.vbox.addWidget(self.message)
        self.vbox.addWidget(self.tool2box)

        self.setLayout(self.vbox)

    def ok_click(self):
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
                self.a = ListWindow()
                self.a.show()
            else:
                pass
        else:
            self.message.setText('两次输入密码不一致')


    def back_click(self):
        self.close()
        self.a = ListWindow()
        self.a.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.back_click()

class RegistWindow(QWidget):

    def __init__(self):
        super(RegistWindow,self).__init__()
        self.setWindowTitle('登记')
        self.setFixedSize(400, 600)
        self.set_ui()

    def set_ui(self):

        self.bnt1 = QPushButton('返回')
        self.bnt1.clicked.connect(self.back_click)

        self.bnt2 = QPushButton('打印')
        self.bnt2.clicked.connect(self.print_record)

        self.bnt3 = QPushButton('保存')
        self.bnt3.clicked.connect(self.save_record)

        self.seriallabel = QLabel('编号')
        self.serialnumber = QLineEdit()
        self.serialnumber2 = str(QDateTime.currentDateTime().toPyDateTime()).replace('/',
                            '').replace(' ','').replace(':','').replace('.','').replace('-','')
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
        self.idmsg = QLabel('请按回车ENTER')
        self.id.returnPressed.connect(self.id_to_date)

        self.birthlable = QLabel('出生日期')
        self.birthday = QDateEdit()
        self.birthchoice = QPushButton('>')
        self.birthchoice.clicked.connect(self.show_cal)

        self.addresslabel = QLabel('住址')
        self.address = QLineEdit()
        self.provincelabel = QLabel('省份')
        self.province = QComboBox()
        self.citylable = QLabel('市')
        self.city = QComboBox()
        self.countrylabel = QLabel('区/县')
        self.country = QComboBox()
        self.townlabel = QLabel('乡镇')
        self.town = QComboBox()
        self.town.setEditable(True)

        self.dictProvince = area.dictProvince
        self.dictCity = area.dictCity
        self.dictTown = area.dictTown
        for (keys, val) in self.dictProvince.items():
            self.province.addItem(val, QVariant(keys))


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
        self.gridbox.addWidget(self.idmsg,3,3)
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

        self.hbox.addWidget(self.bnt1)
        self.hbox.addWidget(self.bnt3)
        self.hbox.addWidget(self.bnt2)

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
        self.a = ListWindow()
        self.a.show()

    def print_record(self):
        self.save_record()
        self.close()
        self.b = PrintWindow(self.serialnumber2)
        self.b.show()

    def save_record(self):

        db = sqlite3.connect('basetable.db')
        cur = db.cursor()
        data = {'std_serial':self.serialnumber2,
                'std_name':self.name.text(),
                'std_id':self.id.text(),
                'std_gender':self.gender.text(),
                'std_race':self.race.currentText(),
                'std_birthday':self.change_date(self.birthday),
                'std_address':self.address.text(),
                'std_deathdate':self.change_date(self.deathdate),
                'std_disease':self.disease.text(),
                'std_family':self.family.text(),
                'std_tel':self.tel.text(),
                'std_regist_date':self.change_date(self.regist_date),
        }
        cur.execute('select * from base where serialnumber =%s' %(self.serialnumber2))
        res = cur.fetchone()
        try:
            if res[-1]:
                sql = '''update base set name = :std_name,gender = :std_gender, id = :std_id,
                                         race = :std_race, birthday = :std_birthday, address = :std_address,
                                         deathdate = :std_deathdate, disease = :std_disease, family = :std_family,
                                         tel = :std_tel, regist_date = :std_regist_date
                                         WHERE serialnumber = %s'''%(self.serialnumber2)
                cur.execute(sql,data)
        except:
             sql = '''insert into base (serialnumber,name,id,gender,race,birthday,address,deathdate,disease,
                            family,tel,regist_date,is_deleted) values (:std_serial,:std_name,:std_id,:std_gender,:std_race,
                            :std_birthday,:std_address,:std_deathdate,:std_disease,:std_family,
                            :std_tel,:std_regist_date,0)'''
             cur.execute(sql,data)
        if self.name.text() != '':
            db.commit()
        else:
            pass
        db.close()

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
                self.idmsg.setText('身份证号码不正确')
                self.idmsg.setStyleSheet('QLabel{color:red}')
            else:
                self.idmsg.setText('请按回车ENTER')
        else:
            self.idmsg.setText('请按回车ENTER')

    def tomale(self,state):
        if state == Qt.Checked:
            self.gender.setText('男')
            self.female.setChecked(False)

    def tofemale(self,state):
        if state == Qt.Checked:
            self.gender.setText('女')
            self.male.setChecked(False)

    def change_date(self,a):
        pydate = str(a.date().toPyDate())
        date2 = time.mktime(time.strptime(pydate,'%Y-%m-%d'))
        return date2



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
        self.setWindowTitle('打印')
        self.setFixedSize(400,600)
        self.serialnumber = serialnumber
        self.set_ui()

    def set_ui(self):
        con = sqlite3.connect('basetable.db')
        cur = con.cursor()
        cur.execute('select * from base where serialnumber = %s'%self.serialnumber)
        rslt = cur.fetchone()
        try:
            if rslt[0]:
                text = rslt[0] +','+ rslt[2] +','+ rslt[3] +',' + self.change_date(rslt[4])+'出生,身份证号：'+ rslt[1]+','+ rslt[5]+'人,' + self.change_date(rslt[6]) + '因' +rslt[7] + '去世，特此证明！'
        except:
            text = '姓名未填写！！！！'


        self.bnt1 = QPushButton('关闭')
        self.bnt1.clicked.connect(self.back_click)
        self.bnt2 = QPushButton('打印')
        self.bnt2.clicked.connect(self.print_record)

        self.vbox = QVBoxLayout()

        self.label = QLabel('证明')
        self.label.setFont(QFont('Roman Times',16,QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)

        self.content = QTextEdit(text)
        self.content.setStyleSheet('QTextEdit{font-size:15px;text-indent:30px;}')

        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.content)
        self.vbox.addWidget(self.bnt1)
        self.vbox.addWidget(self.bnt2)
        self.setLayout(self.vbox)


    def back_click(self):
        self.close()
        self.a = ListWindow()
        self.a.show()

    def print_record(self):
        pass

    def change_date(self,a):
        date = datetime.datetime.utcfromtimestamp(a)
        return str(date.year)+'年'+ str(date.month) +'月'+str(date.day)+'日'

class QueryWindow(QWidget):


    def __init__(self):
        super(QueryWindow,self).__init__()
        self.setWindowTitle('查询')
        self.setFixedSize(800,600)
        self.set_ui()


    def set_ui(self):

        self.closebnt = QPushButton('close')
        self.closebnt.clicked.connect(self.back_click)
        self.querybnt = QPushButton('query')
        self.querybnt.clicked.connect(self.query_click)
        self.clearbnt = QPushButton('clear')
        self.clearbnt.clicked.connect(self.clear_click)
        self.exportbnt = QPushButton('export')
        self.exportbnt.clicked.connect(self.export_click)

        self.namelabel = QLabel('name')
        self.name = QLineEdit()
        self.idlabel = QLabel("id")
        self.id = QLineEdit()
        self.begin_date_label = QLabel('begin_date')
        self.begin_date = QDateEdit()
        self.begin_date_choice = QPushButton(">")
        self.begin_date_choice.clicked.connect(self.begin_date_input)
        self.end_date_label = QLabel('end_date')
        self.end_date = QDateEdit()
        self.end_date_choice = QPushButton(">")
        self.end_date_choice.clicked.connect(self.end_date_input)

        self.vbox = QVBoxLayout()

        self.head_box = QHBoxLayout()


        self.demand_box = QVBoxLayout()
        self.demand_box1 = QHBoxLayout()
        self.demand_box2 = QHBoxLayout()
        self.demand_box1.addWidget(self.namelabel)
        self.demand_box1.addWidget(self.name)
        self.demand_box1.addWidget(self.begin_date_label)
        self.demand_box1.addWidget(self.begin_date)
        self.demand_box1.addWidget(self.begin_date_choice)
        self.demand_box2.addWidget(self.idlabel)
        self.demand_box2.addWidget(self.id)
        self.demand_box2.addWidget(self.end_date_label)
        self.demand_box2.addWidget(self.end_date_choice)

        self.bnt_box = QVBoxLayout()
        self.bnt_box1 = QHBoxLayout()
        self.bnt_box2 = QHBoxLayout()
        self.bnt_box1.addWidget(self.querybnt)
        self.bnt_box1.addWidget(self.exportbnt)
        self.bnt_box2.addWidget(self.clearbnt)
        self.bnt_box2.addWidget(self.closebnt)

        self.demand_box_layout = QWidget()
        self.bnt_box_layout = QWidget()
        self.head_box_layout = QWidget()

        self.demand_box_layout.setLayout(self.demand_box1)
        self.demand_box_layout.setLayout(self.demand_box2)

        self.bnt_box_layout.setLayout(self.bnt_box1)
        self.bnt_box_layout.setLayout(self.bnt_box2)

        self.demand_box.addWidget(self.demand_box_layout)
        self.bnt_box.addWidget(self.bnt_box_layout)

        self.head_box_layout.setLayout(self.demand_box)
        self.head_box_layout.setLayout(self.bnt_box)

        self.head_box.addWidget(self.head_box_layout)
        self.vbox2 = QWidget()
        self.vbox2.setLayout(self.head_box)

        self.vbox.addWidget(self.vbox2)

        self.setLayout(self.vbox)

    def back_click(self):
        self.close()
        self.a = ListWindow()
        self.a.show()


    def query_click(self):
        pass

    def clear_click (self):
        pass

    def export_click(self):
        pass

    def begin_date_input(self):
        self.a = Calendar()
        self.a.show()

    def end_date_input(self):
        pass




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('octo.png'))
#    mainWindow = SignInWidget()
    mainWindow = ListWindow()
    mainWindow.show()
    sys.exit(app.exec_())
