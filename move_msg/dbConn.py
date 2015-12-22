# _*_ coding: utf-8
import config
import MySQLdb
import MySQLdb.cursors
def get_db_conn():
    conn = MySQLdb.connect(host = config.mysql_host,user = config.mysql_user,
                           passwd = config.mysql_passwd,
                           port = config.mysql_port,db = config.mysql_db,
                           cursorclass = MySQLdb.cursors.DictCursor, charset='utf8')
    return conn