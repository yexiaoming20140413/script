# _*_ coding: utf-8
import dbConn
import time


mailType = {
    u'信用额度审核通知': 2,
    u'信用额度审核通知': 2,
    u'基本信息审核通知': 2,
    u'基本信息的审核通知': 2,
    u'基本资料审核通知': 2,
    u'家庭信息的审核通知': 2,
    u'工作信息的审核通知': 2,
    u'资产信息的审核通知': 2,
    u'VIP会员成功扣费': 2,
    u'中奖返利将到帐': 6,
    u'中奖返利已到帐': 6,
    u'中秋切月饼返利通知': 6,
    u'中秋抢楼返利通知': 6,
    u'借款初审报告': 8,
    u'借款发布报告': 8,
    u'借款发布通知': 8,
    u'借款成功报告': 8,
    u'借款撤消报告': 8,
    u'借款转让通知': 8,
    u'借款还款报告': 8,
    u'借款还清通知': 3,
    u'债权已转出通知': 4,
    u'债权转让审核成功通知': 4,
    u'债权转让报告': 4,
    u'债权转让竞拍报告': 4,
    u'充值已到帐': 2,
    u'充值成功': 2,
    u'利息成功提现': 2,
    u'实地认证标垫付通知': 2,
    u'审核成功通知': 2,
    u'恭喜发财': 6,
    u'恭喜您中奖': 6,
    u'恭喜获得完美收官奖': 6,
    u'恭喜获得富甲一方奖': 6,
    u'恭喜获赠红包': 6,
    u'感谢使用龙贷客户端': 2,
    u'成功加入/追加龙聚宝': 5,
    u'成功加入龙聚宝报告': 5,
    u'成功还款': 3,
    u'投标成功通知': 7,
    u'投标满标审核成功通知': 7,
    u'投标满标审核失败通知': 7,
    u'招标进度过半通知': 7,
    u'推荐龙贷赚返利': 6,
    u'提现失败通知': 2,
    u'提现成功通知': 2,
    u'收到还款通知': 3,
    u'放款审核成功通知': 2,
    u'早投标得返利': 6,
    u'更正债权收益': 2,
    u'有人投标通知': 2,
    u'未通过债权转让审核通知': 2,
    u'未通过审核通知': 2,
    u'注册龙贷赚返利': 6,
    u'理财投资成功报告': 2,
    u'理财投资报告': 2,
    u'理财投资撤消报告': 2,
    u'生日红包': 6,
    u'用户还款资金收入报告': 2,
    u'管理员推送测试': 2,
    u'获赠三元提现券': 6,
    u'获赠免费提现券': 6,
    u'被推荐好友已注册': 2,
    u'误返投资管理费更正': 2,
    u'转让中的债权已撤销': 4,
    u'转让债权购买成功通知': 4,
    u'返利余额即将清零': 6,
    u'返利余额已经清零': 6,
    u'返还投资管理费': 6,
    u'还款提前还清通知': 3,
    u'还款结清通知': 3,
    u'银行卡绑定失败': 2,
    u'首笔投资获得返利': 6,
    u'龙客服官方回复': 2,
    u'龙聚宝收益月报': 5,
    u'龙聚宝退出通知': 5,
    u'龙贷官方回复': 2,
    u'龙贷官方客服回复': 2,
    u'龙贷官网客服回复': 2,
    u'龙贷客服回复': 2,
    u'龙贷客服官方回复': 2,
    u'龙贷用户': 2,
    u'债权转让审核失败': 4,
    u'债权转让审核成功': 4,
    u'债权转让购买报告': 4,
    u'收到龙贷垫付还款通知': 3,
    u'test': 2,
    u'投标流标通知': 7,
    u'未通过放款审核通知': 2,
}

def get_mail_count():
    conn = dbConn.get_db_conn()
    cursor = conn.cursor()
    cursor.execute("select count(*) as total from t_mail")
    rows = cursor.fetchall()
    for item in rows:
        count = item['total']
    cursor.close()
    conn.close()
    return count

def move_mail_data_by_page(page,pages):
    conn=dbConn.get_db_conn()
    cursor = conn.cursor()
    cursor.execute("select * from t_mail limit %s,%s",[(page - 1) * pages ,pages])
    rows = cursor.fetchall()
    for item in rows:
        mailId = item['id']
        mailTitle = item['mailTitle']
        mailContent = item['mailContent']
        sendTime = item['sendTime']
        reciver = item['reciver']
        mailStatus = item['mailStatus']
        borrowId = item['borrowId']
        sender = item['sender']
        timeArray = time.strptime(str(sendTime), "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))*1000

        type = mailType.get(mailTitle)
        if mailId is None:
            continue
        if type is None:
            type=2
        if mailStatus is None:
            mailStatus = 3
        cursor.execute("insert into t_user_message(type,userId,title,contentHtml,content,status,sendId,createTime,actionTime,data) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                       [type,reciver,mailTitle,mailContent,mailContent,mailStatus,sender,timeStamp,timeStamp,borrowId])

    conn.commit()
    cursor.close()
    conn.close()

def move_mail_by_page():
    count = get_mail_count();
    print "message count:"+str(count)
    pageSize = 2000
    pages = count/pageSize+2
    print "message pages:"+str(pages)
    for page in range(1,pages):
        print "curr page:"+str(page)
        move_mail_data_by_page(page,pageSize)

    print "move msg end"

move_mail_by_page()