# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 21:43:37 2021

@author: Runner
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd
import sqlite3

TR_REQ_TIME_INTERVAL = 0.2

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
            
        else:
            self.remained_data = False
            

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")

            self.ohlcv['dates'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))



con1 = sqlite3.connect("c://Users//Runner//Data//Stock//Dayprice_kospi_filtered.db")
cursor = con1.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
table_list = cursor.fetchall()

table_list_str = []
for j in table_list:
    string_j = str(j[0])
    table_list_str.append(string_j)
    
print(table_list_str)
print(type(table_list_str))
print(len(table_list_str))

stock_filtered = pd.read_excel('C://Users//Runner//Data//Stock//Kospi_List_Filtered4.xlsx')
stock_list1 = stock_filtered['종목코드']
stock_list = stock_list1.tolist()
print(len(stock_list))

#when excel data is imported, the stock code of the list could be integer in which case leading zeroes are automatically removed
#so we have to create a new list of strings with leading zeroes attached
stock_list_str = []
for k in stock_list:
    k = str(k)
    if len(k) == 1:
        k = "00000"+k
    elif len(k) == 2:
        k = "0000"+k
    elif len(k) == 3:
        k = "000"+k
    elif len(k) == 4:
        k = "00"+k
    elif len(k) == 5:
        k = "0"+k
    stock_list_str.append(k)
        

stock_list = stock_list_str    
print(type(stock_list[3]))

for i in table_list_str:
    if i in stock_list:
        stock_list.remove(i)
    
print(len(stock_list))
print(stock_list)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()
    kiwoom.ohlcv = {'dates': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

    # opt10081 TR 요청
    for stock_code in stock_list:
        for key in kiwoom.ohlcv:
            kiwoom.ohlcv[key].clear()
        kiwoom.set_input_value("종목코드", stock_code)
        kiwoom.set_input_value("기준일자", "20210101")
        kiwoom.set_input_value("수정주가구분", 1)
        kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
    
        while kiwoom.remained_data == True:
            time.sleep(1)
            kiwoom.set_input_value("종목코드", stock_code)
            kiwoom.set_input_value("기준일자", "20210101")
            kiwoom.set_input_value("수정주가구분", 1)
            kiwoom.comm_rq_data("opt10081_req", "opt10081", 2, "0101")
    
        df = pd.DataFrame(kiwoom.ohlcv, columns=['dates','open', 'high', 'low', 'close', 'volume'])
    
        con = sqlite3.connect("c:/Users/Runner/Data/Stock/Dayprice_kospi_filtered.db")
        df.to_sql(stock_code, con, if_exists='replace')
        time.sleep(1)