#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket,openpyxl
import hashlib
import _thread
# from openpyxl import workbook  # 写入Excel表所用
# from openpyxl import load_workbook  # 读取Excel表所用
import os, time,sys
from pathlib import Path
import traceback
class Accept:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
    def CalcSha512(self,filepath):
        sha512obj = hashlib.sha512()
        with open(filepath, 'rb') as f:
            for line in f:
                sha512obj.update(line)
        hash = sha512obj.hexdigest()
        return hash


# 获取一个分配的SN号
    def get3DCSN(self):
        try:
            base_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
            #print(base_dir)
            #self.Txt_write("base_dir:%s"%base_dir)
            cc=os.path.join(base_dir,'3DCSN.xlsx')
            try:
                if os.path.exists(cc):
                    self.Txt_write('load_workbook')
                    wb = openpyxl.load_workbook(cc)  # 加载存在的Excel表
                    self.Txt_write("wb:%s" % str(wb))
                else:
                    self.Txt_write("error_exist")
                    return
            except:
                msg = traceback.format_exe()
                self.Txt_write("error_msg:%s"%(str(msg)))
            a_sheet = wb.get_sheet_by_name('Sheet1')  # 根据表名获取表对象

            now = time.strftime('%m%d', time.localtime(time.time()))
            count = a_sheet.max_row
            number = ("%06d" % count)
            sn = 'HMD3DC20' + now + number

            # 保存新的SN号
            ws = wb.active
            ws.append([sn])
            wb.save(cc)
            #self.Txt_write("now:%s" % now)
            print(a_sheet.cell(row=(a_sheet.max_row),column=1).value)
            self.Txt_write("a_sheet.cell(row=(a_sheet.max_row),column=1).value:%s" % a_sheet.cell(row=(a_sheet.max_row),column=1).value)
            return a_sheet.cell(row=(a_sheet.max_row),column=1).value
        except:
            print(traceback.format_exe())
            self.Txt_write(traceback.format_exe())

    def Txt_write(self,type):  # 写入函数
        filename =r'C:\Users\Administrator\Desktop\demo\log\test.txt' # 创建一个txt文件
        file = open(filename, 'a')
        file.write(type+"\r\n")  # 打开文件并且写入数据
        file.close()

    def Server(self):
        try:
            self.get3DCSN()
            print(self.port)
            ip_port = (self.ip, self.port)

            print(ip_port)
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(sk)
            sk.bind(ip_port)
            sk.listen(128)
            path = os.path.dirname(os.path.realpath(sys.argv[0]))
        except:
            print(traceback.format_exe())
        # 当前路径
        while True:
            print('server waiting...')
            self.Txt_write('server waiting...')
            conn, addr = sk.accept()  # 阻塞等待客户端连接
            print("来自%s的连接：" % addr[0])
            self.Txt_write("来自%s的连接：" % addr[0])

            while True:
                client_data = conn.recv(1024)

                print(len(client_data))
                # 判断长度
                if len(client_data) == 6:  # 判断数据的长度
                    aa = client_data.hex()
                    print(aa)
                    if aa == "7e800501097e":  # 反馈SN号
                        print(self.get3DCSN())
                        conn.send(self.get3DCSN().encode())

                    elif aa == "7e800101097e":  # 接收SN
                        conn.send('start rsv SN'.encode())
                        data = conn.recv(1024)  # 接收SN
                        # 创建文件
                        file_name = path + '\\' +'test'+'\\'+ bytes.decode(data)
                        print(file_name)
                        my_file = Path(file_name)
                        print(my_file)
                        if not my_file.exists():
                            os.mkdir(file_name)
                        conn.send('SN is OK'.encode())
                    elif aa == "7e800201097e":  # 接收ZIP包
                        conn.send('start rsv ZIP'.encode())
                        data = conn.recv(1024)  # 接收压缩包
                        f = open(file_name + "/data.zip", 'wb')
                        print('start rsv ZIPHASH')
                        while len(data) > 0:
                            f.write(data)
                            print(len(data))
                            if len(data) == 6 and data.hex() == "7e8002010a7e":
                                conn.send('start rsv ZIPHASH'.encode())
                                data = conn.recv(1024)  # 接收压缩包HASH指令
                                if bytes.decode(data) == self.CalcSha512(file_name + "/data.zip"):
                                    conn.send('ZIPHASH is OK'.encode())
                                    break
                                else:
                                    conn.send('ZIPHASH is ERROR'.encode())
                            elif len(data) != 1024:
                                conn.send('ZIP is OK'.encode())
                                self.Txt_write('ZIP is OK')
                                break
                                # ad1b6699ab5cd76c5edd0b31b61b1046b6efd02ea637277711f62931be1989561145b4fa3afc5dc207e42239c13039664818c417287903c1fa8c3629ebd5948a
                            data = conn.recv(1024)  # 接收压缩包
                        f.close()
                        print('ZIP is OK')
                    elif aa == "7e8002010a7e":  # 接收压缩包HASH指令
                        conn.send('start rsv ZIPHASH'.encode())
                        print(self.CalcSha512(file_name + "/data.zip"))
                        data = conn.recv(1024)
                        print(bytes.decode(data))
                        if bytes.decode(data) == self.CalcSha512(file_name + "/data.zip"):
                            conn.send('ZIPHASH is OK'.encode())
                            print('ZIPHASH is OK')
                            self.Txt_write('ZIPHASH is OK')
                        else:
                            conn.send('ZIPHASH is ERROR'.encode())
                            self.Txt_write('ZIPHASH is ERROR')
                    elif aa == "7e800601097e":  # 确认建立连接
                        conn.send('socket OK'.encode())
                        print('socket OK')
                    elif aa == "7e800401097e":  # 断开连接
                        conn.send('close OK'.encode())
                        print('close OK')
                        self.Txt_write('close OK')
                        break;
                    else:
                        print("等待连接....")
        #except:
            #print("SOCKET ERROR")
        sk.close()
#
    def main(self):    # 创建多个接收线程
        #self.get3DCSN()
        try:
            _thread.start_new_thread(self.Server())  # 6001 接收标定工位端口
            #_thread.start_new_thread(Server, (ip, port))  # 7001 接收深度工位端口
            #_thread.start_new_thread(Server, (ip, 8001))  # 8001 接收 AE 工位端口
            while 1:
                pass
        except :
            print (traceback.format_exe())
            #print("Error: 无法启动线程")
    
        
# c=Accept