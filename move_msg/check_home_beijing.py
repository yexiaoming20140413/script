# _*_ coding: utf-8
import os

import dbConn
from phone import Phone
p  = Phone()
home_type={}

def get_user_count():
    conn = dbConn.get_db_conn()
    cursor = conn.cursor()
    cursor.execute("select count(*) as total from t_user")
    rows = cursor.fetchall()
    for item in rows:
        count = item['total']
    cursor.close()
    conn.close()
    return count

def check_user_home_by_page(page, pages):
    conn = dbConn.get_db_conn()
    cursor = conn.cursor()
    cursor.execute("select mobilePhone from t_user limit %s,%s",[(page - 1) * pages ,pages])
    rows = cursor.fetchall()
    result=''
    for item in rows:
        phone = item['mobilePhone']
        if phone is None:
            continue
        if len(phone) != 11:
            continue
        res = p.find(phone)
        if res is None:
            continue
        province = res['province']
        if province is None:
            continue
        if province != '北京':
            continue
        result += province+'-'+str(phone)
        result += "\r\n"
    cursor.close()
    conn.close()
    return result


def check_user_by_page():
    count = get_user_count()
    print "user count:"+str(count)
    pageSize = 2000
    pages = count/pageSize+2
    print "user pages:"+str(pages)
    result =''
    for page in range(1,pages):
        result += check_user_home_by_page(page,pageSize)

    print "result:" + result
    filename ='/home/xiaoming/longdai_stat_home_beijing.txt'
    file = open(filename,'w')
    try:
        file.write(result)
    finally:
        file.close()
    print "check home end!"

check_user_by_page()
