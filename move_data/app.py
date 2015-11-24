#!/usr/bin/env python
# _*_ coding: utf-8

import sys
import datetime
import MySQLdb
import MySQLdb.cursors
import os
import config


#userMessageType = {
#    '平台公告': 1,
#    '系统通知': 2,
#    '还款通知': 4,
#    '转让通知': 4,
#    '龙聚宝通知': 5,
#    '红包返利中奖通知': 6,
#    '投标通知': 7,
#    '借款通知': 8
#}

mailType = {
    u'信用额度审核通知': 2,
    u'基本信息审核通知': 2,
    u'龙聚宝退出通知': 5,
    u'龙聚宝收益月报': 5,
    u'还款提前还清通知': 4,
    u'返利余额已经清零': 6,
    u'返利余额即将清零': 7,
    u'转让债权购买成功通知': 4,
    u'转让中的债权已撤销': 4,
    u'投标满标审核成功通知': 7,
    u'借款发布报告': 2,
    u'用户还款资金收入报告': 4,
    u'用户还款资金收入报告': 4,
    u'投标满标审核成功通知': 2,
    u'投标成功通知': 7,

    #such as ...
}


def get_type(title):
    return mailType[title]
    

def get_mail_data(page, pages):
    '''
    获取老的mail信息
    '''
    conn = MySQLdb.connect(host = config.mysql_host,user = config.mysql_user, 
                           passwd = config.mysql_passwd,
                           port = config.mysql_port,db = config.mysql_db,
                           cursorclass = MySQLdb.cursors.DictCursor, charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select * from t_mail limit %s, %s", [(page - 1) * pages ,pages])
    rows = cursor.fetchall()

    #print mailType.has_key('投标成功通知')

    for item in rows:
        title = item['mailTitle'].strip()

        if mailType.has_key(title):
            print get_type(title)

    cursor.close()
    conn.close()


get_mail_data(1, 2000)
