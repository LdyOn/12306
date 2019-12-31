# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
 
my_sender='1185946887@qq.com' # 发件人邮箱账号
my_pass = 'svpmgkriyjhsidgd'# 发件人邮箱密码
my_user='1185946887@qq.com' # 收件人邮箱账号，我这边发送给自己

def mail(msg_body):
    ret=True
    try:
        msg=MIMEText(msg_body,'plain','utf-8')
        msg['From']=formataddr(["ldy",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["亲爱的用户",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="12306抢票通知"                # 邮件的主题，也可以说是标题

        server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception as e:
        print(e)  
        ret=False
    return ret
 

