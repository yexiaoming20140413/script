#!/usr/bin/env python
# _*_ coding: utf-8

import csv
import httplib
import sys
import datetime
import urllib

import MySQLdb
import MySQLdb.cursors
import paramiko
import traceback
import os
import socket
import config
import logging
from decimal import *

from paramiko.py3compat import input

def check_account(orderList):
    '''
    校验账单
    '''

    conn = MySQLdb.connect(host = config.mysql_host,user = config.mysql_user, \
                           passwd = config.mysql_passwd, \
                           port = config.mysql_port,db = config.mysql_db,
                           cursorclass = MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()

    for order in orderList:
        cursor.execute("select money,state from t_recharge_despatch where orderId=%s", [order['orderId']])
        rows = cursor.fetchall()
        money = Decimal(order['money'])

        flag = 0

        if cursor.rowcount == 0:
            logger.error('订单号:%s, 金额:%s 交易异常,龙贷订单号不存在!' % (order['orderId'], order['money']))
            sendAlarmMsg('订单号:%s, 金额:%s 交易异常,龙贷订单号不存在!' % (order['orderId'], order['money']))
            continue

        if rows[0]['state'] == 1:
            if order['result'] != '0':
                logger.error('连连支付 交易状态异常!!! 狙击手准备!')
                flag = 1
                sendAlarmMsg('连连支付 交易状态异常!!! 狙击手准备!')

            if order['status'] != '0':
                logger.error('钱没有到账,龙贷账户竟然成功了!')
                flag = 1
                sendAlarmMsg('钱没有到账,龙贷账户竟然成功了!')

        if money != rows[0]['money']:
            logger.error('我次奥金额不相等!!!!!!!!!!!!')
            flag = 1
            sendAlarmMsg('我次奥金额不相等!!!!!!!!!!!!')
        if flag == 0 :
            logger.debug('订单号:%s, 金额:%s 交易正常!' % (order['orderId'] , order['money']))
        else:
            logger.error('订单号:%s, 金额:%s 交易异常!' % (order['orderId'] , order['money']))
            sendAlarmMsg('订单号:%s, 金额:%s 交易异常!' % (order['orderId'] , order['money']))

    cursor.close()
    conn.close()

def sendAlarmMsg(content):
    httpClient = None
    try:
        params = urllib.urlencode({'content': content,'key':'you_can_you_up_no_can_no_bb'})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        httpClient = httplib.HTTPConnection("api.longdai.com")
        httpClient.request("POST", "/api/alarm/weixin", params, headers)
        response = httpClient.getresponse()
        print response.status
        print response.reason
        print response.read()
    except Exception, e:
        print e
    finally:
        httpClient.close()

def parse_account(date):
    '''
    解析账单文件
    '''

    filename ='account/JYMX_201410231000071502_%s.csv' % \
        (date.strftime('%Y%m%d'))
    if os.path.exists(filename) == False:
        logger.error('马拉戈壁,文件不存在!')
        return
    orderCsv = csv.reader(open(filename, 'rb'))

    order = []
    itercars = iter(orderCsv)
    next(itercars)
    for row in itercars:
        paramStr = ','.join(row)
        param = paramStr.split(',')
        #print '流水号%s 金额:%s 状态:%s 交易结果:%s' %  (param[0][2:-1], param[6], param[7], param[8])
        orderDict = {}
        orderDict = {'orderId': param[0][2:-1], 'money': param[6], \
                     'status': param[7], 'result': param[8] }
        order.append(orderDict)

    check_account(order)

def download_file(date):
    '''
    下载对账的账单文件 根据当前的日期
    一共有三种类型
    '''

    paramiko.util.log_to_file('sftp.log');

    # Paramiko client configuration
    UseGSSAPI = False             # enable GSS-API / SSPI authentication
    DoGSSAPIKeyExchange = False
    Port = 2122
    hostname = '115.238.110.126'

    try:
        t = paramiko.Transport((hostname, Port))
        t.connect(None, 'longdai', 'longdai@123',  gss_host = socket.getfqdn(hostname),
                  gss_auth=UseGSSAPI, gss_kex=DoGSSAPIKeyExchange)
        sftp = paramiko.SFTPClient.from_transport(t)

        sftp.chdir('longdai/201410231000071502')

        #dirlist = sftp.listdir('.')
        filename = 'JYMX_201410231000071502_%s.csv' % \
            (date.strftime('%Y%m%d'))

        logger.info('下载对账文件' + filename)

        sftp.get(filename, 'account/' + filename);

        #with sftp.open('JYMX_201410231000071502_20151113.csv', 'r') as f:
        #    data = f.read();
        #    print data
        t.close()

    except Exception as e:
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        logger.error('文件下载失败')
        sys.exit(1)




formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('app.log')
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger = logging.getLogger('log')
logger.setLevel(logging.DEBUG)

logger.addHandler(fh)
logger.addHandler(ch)

#startDate = datetime.datetime.strptime("2015-01-01", "%Y-%m-%d")
#date = datetime.datetime.now() + datetime.timedelta(days=-1);
#
#while (date > startDate):
#    logger.info('下载 %s 对账文件' % (date.strftime('%Y%m%d')))
#    download_file(date)
#    logger.info('下载 %s 对账文件成功' % (date.strftime('%Y%m%d')))
#    logger.info('开始处理 %s' % (date.strftime('%Y%m%d')))
#    parse_account(date)
#    date = date + datetime.timedelta(days=-1)

date = datetime.datetime.now() + datetime.timedelta(days=-1);
logger.info('下载对账文件')
download_file(date)
logger.info('下载对账文件成功')

logger.info('开始处理')
parse_account(date)
