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
    cursor.execute("select id,mobilePhone,createTime from t_user where source like '%sm%' ")
    rows = cursor.fetchall()
    result=''
    for item in rows:
        phone = item['mobilePhone']
        createTime = item['createTime']
        userId = item['id']
        cursor.execute("select recordTime from t_fundrecord where userId=%s limit 1",[userId])
        rows1 = cursor.fetchall();
        for item1 in rows1:
            recordTime = item1['recordTime']
        if phone is None:
            continue
        if len(phone) != 11:
            continue
        result += "手机号："+str(phone)+"   注册时间："+str(createTime)+"   投资时间："+str(recordTime)
        result += "\r\n"
    cursor.close()
    conn.close()
    return result



def check_user_by_page():
    result =''
    result+=get_invest_user_phone()
    print "result:" + result
    filename ='/home/longdai_state_invest_register.txt'
    file = open(filename,'w')
    try:
        file.write(result)
    finally:
        file.close()
    print "check invest register end!"

check_user_by_page()
