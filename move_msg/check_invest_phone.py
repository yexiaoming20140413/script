# _*_ coding: utf-8
#输出投资用户手机号
import os

import dbConn
from phone import Phone
p  = Phone()
home_type={}

def get_invest_user_phone():
    conn = dbConn.get_db_conn()
    cursor = conn.cursor()
    cursor.execute("select a.userid,b.mobilePhone from (select distinct userid from t_fundrecord where operatetype in (653,726,901 ) and userid is not null) a,t_user b where a.userid=b.id")
    rows = cursor.fetchall()
    result=''
    for item in rows:
        phone = item['mobilePhone']
        if phone is None:
            continue
        if len(phone) != 11:
            continue
        result += str(phone)
        result += "\r\n"
    cursor.close()
    conn.close()
    return result



def check_user_by_page():
    result =''
    result+=get_invest_user_phone()
    print "result:" + result
    filename ='/home/xxxx/state_invest_phone.txt'
    file = open(filename,'w')
    try:
        file.write(result)
    finally:
        file.close()
    print "check invest user end!"

check_user_by_page()
