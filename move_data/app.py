#!/usr/bin/env python
# _*_ coding: utf-8

import sys
import datetime
import MySQLdb
import MySQLdb.cursors
import os
import config


def get_mail_data(page, pages):
    '''
    获取老的mail信息
    '''
    conn = MySQLdb.connect(host = config.mysql_host,user = config.mysql_user, \
                           passwd = config.mysql_passwd, \
                           port = config.mysql_port,db = config.mysql_db,
                           cursorclass = MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute("select * from t_mail limit %s, %s", [(page - 1) * pages ,pages])
    rows = cursor.fetchall()

    for item in rows:
        print item

    cursor.close()
    conn.close()


get_mail_data(1, 200)
