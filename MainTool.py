#!/usr/bin/env Python
# coding=utf-8
import upload,api_up,demo
import sys, os,time
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread
from Mainwin import Ui_MainWindow
from PyQt5.QtGui import QIcon
from PyQt5 import sip
class MainCode(QMainWindow,Ui_MainWindow):

    def __init__(self):
        super(MainCode,self).__init__()
        self.setupUi(self)
        self.initUI()
        self.lineEdit_2.setReadOnly(True)
        #self.pushButton.clicked.connect(self.local_file)
        self.pushButton_2.clicked.connect(self.up_file)
        self.pushButton.clicked.connect(self.accept_file)
        sys.stdout = EmittingStr(textWritten=self.output_log)
        sys.stderr = EmittingStr(textWritten=self.output_log)
    def initUI(self):
        self.setWindowTitle("上传工具")
        self.setWindowIcon(QIcon('./image/title.png'))  # 设置窗体图标
    # def thread_file(self):
    #     t = threading.Thread(target=self.up_file, name='thread_1')
    #     t.setDaemon(True)
    #     t.start()
    def r_files(self):
        file_path = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'test'
        for root, dirs, files in os.walk(file_path):
            yield dirs
    def up_file(self):
        self.pushButton_2.setDisabled(True)
        self.lineEdit.setText('https://ota.sprocomm.com/api/file/8011/uploadDownload/v2/')
        self.textBrowser_2.append('---------------------------------开始上传--------------------------------')
        QApplication.processEvents()
        time.sleep(0.1)
        #c.get_url(self.re_sn(),self.re_file())上传地址路径
        #c.main()
        try:
            count = 1
            for sn in next(self.r_files()):
                print('SN ：' + sn)
                m_path= os.path.dirname(os.path.abspath(__file__)) + '\\' + 'test'+ '\\' + sn  # 上传为路径
                upload.Upfile().upfile(m_path, sn)
                #self.up_api('上传文件pass:%d次' % count)
                log=api_up.UpApi(sn).up_post()
                if log.status_code==400:
                    self.up_api('请求SN：'+sn)
                    self.up_api('请求Url：'+log.url)
                    self.up_api('Api请求fail:%d次'%count)
                if log.status_code==200:
                    self.up_api('上传文件地址:')
                    for file in next(self.re_file(sn)):
                        self.up_api(upload.Upfile().get_url(sn,file))
                        self.up_api('请求SN：' + sn)
                        self.up_api('请求Url：' + log.url)
                        self.up_api(log.text)
                        self.up_api('Api请求pass:%d次'%count)
                        self.up_api()
                count = count + 1
        except Exception as e:
            print(e)
        self.textBrowser_2.append('---------------------------------上传结束--------------------------------')

    def up_api(self,log):
        self.textBrowser_2.append(log)# 在指定的区域显示提示信息
        self.cursot = self.textBrowser_2.textCursor()
        self.textBrowser_2.moveCursor(self.cursot.End)
        QApplication.processEvents()
        time.sleep(0.2)
    def re_file(self,sn):
        path = os.path.dirname(os.path.abspath(__file__)) + '\\' + 'test'+'\\'+sn
        for root, dirs, files in os.walk(path):
            yield files
    def local_file(self):
        path = os.path.dirname(os.path.realpath(sys.argv[0]))+'\\'+'test'
        print(path)
        self.lineEdit_2.setText(path)
        print('打开服务接收数据')
        QApplication.processEvents()
        time.sleep(0.1)
        # self.textBrowser.append('上传文件列表：')
        # while 1:
        #     QApplication.processEvents()
        #     time.sleep(0.2)
        #     for root, dirs, files in os.walk(path):
        #         print(dirs)# dirs返回文件夹名字# files返回文件名字
        #         if dirs:
        #             # return array
        #             self.textBrowser.append(str(dirs))  # 在指定的区域显示提示信息
        #             self.cursot = self.textBrowser.textCursor()
        #             self.textBrowser.moveCursor(self.cursot.End)
        #             QApplication.processEvents()
        #             time.sleep(0.1)
            #else:
                #break
    def accept_file(self):

        ip=self.lineEdit_3.text()
        if len(ip)!=0:
            self.local_file()
            try:
                self.myThread=MyQThread(ip,6001)
                self.myThread2 = MyQThread(ip, 7001)
                self.myThread3 = MyQThread(ip, 8001)
                self.pushButton.setDisabled(True)
                self.myThread.start()
                self.myThread2.start()
                self.myThread3.start()
            except:
                print(traceback.format_exe())
        else:
            print('请输入ip地址')
    def output_log(self, text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()
        if 'ZIPHASH is OK' in text:
            self.textEdit.clear()#接收成功，清理log
            QApplication.processEvents()
            time.sleep(0.1)
class MyQThread(QThread):
    def __init__(self, ip,port):
        super().__init__()  ## 继承QThread
        self.ip = ip
        self.port=port
    def run(self):
        demo.Accept(self.ip,self.port).main()

class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str) #定义一个发送str的信号
    def write(self, text):
        try:
            self.textWritten.emit(str(text))
            time.sleep(0.01)#加个延时
        except:
            print(traceback.format_exe())
if __name__=='__main__':
    import sys,os
    app=QApplication(sys.argv)
    md=MainCode()
    md.show()
    sys.exit(app.exec_())

