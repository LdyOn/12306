import time
import random
import re
import smtplib
import mail

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from email.mime.text import MIMEText
from email.utils import formataddr
from selenium import webdriver

# 从配置文件读取配置
def read_setting():
	s_file = open("setting.ini", encoding='UTF-8')
	config = {}
	lines = s_file.readlines()
	for x in lines:
		if re.match(r'[^;]+=.*', x) != None :
			x = x.strip('\n')
			s = x.split("=")
			config[s[0].strip()] = s[1].strip()

	return config

# 登录函数
# 图形验证码不太好破解，这里手动登陆
def login(driver,username,password):
	# 执行js脚本选择账号密码登陆
	try:
		WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CLASS_NAME,"login-hd")))
		driver.execute_script('var c = document.querySelectorAll\
			(".login-hd-account > a:nth-child(1)");c[0].click();')
	except Exception as e:
		print(e)
	# 在表单中填入用户名和密码
	driver.find_element_by_id('J-userName').send_keys(username)
	driver.find_element_by_id('J-password').send_keys(password)
	#验证码图片
	# img_code = driver.find_element_by_id('J-loginImg')
	# 输入验证码选择
	# select = list(map(int,input("请选择验证码图片(输入1-8，多张用空格分隔):").split()))
	"""将选择的图片序号转换为坐标，共有八张图片，
	第一张图片坐标大约为（40，50）,左右、上下间隔大约为70，下面是八张图片
	的近似点击坐标"""
	# site = { 
	# 	1 :(40,68),
	# 	2 :(110,67),
	# 	3:(180,65),
	# 	4:(250,59),
	# 	5:(40,132),
	# 	6:(110,129),
	# 	7:(183,135),
	# 	8:(259,132),
	# }
	input("登陆成功后，按任意键继续")
	# 逐个点击图片
	# for x in select:
	# 	webdriver.ActionChains(driver).move_to_element_with_offset(img_code,
	# 		site[x][0],site[x][1]).click().perform()

# 选择乘客
def choose_passenger(driver):		
	while not ('https://kyfw.12306.cn/otn/view/passengers.html' in driver.current_url):
		driver.get('https://kyfw.12306.cn/otn/view/passengers.html')
	# 保存常用联系人
	passengers = []
	choose = []
	while True:
		try:
			print("search passengers...")
			# 找到展示姓名的元素
			name_element = driver.find_elements_by_class_name('name-yichu')
			for x in name_element:
				passengers.append(x.text)
			# 写一段js进行翻页
			js = 'var next = document.getElementsByClassName("next");\
			next[0].click();'
			driver.execute_script(js)
			time.sleep(1)
		except Exception as e:
			print(e)
			print("乘客信息如下：")
			for i in range(len(passengers)):
				print('{0:3}  {1:5}'.format(i,passengers[i]))
			choose =  list(map(int,input("选择乘客（输入名字前的序号，多个用空格分隔）:")\
				.split()))		
			name = []
			for x in choose:
				name.append(passengers[x])

			return name


# 查询车票
def  query_tickets(driver, travel_date):
	# 设置出发日
	driver.execute_script('document.getElementById("train_date").removeAttribute("readonly");')
	date = driver.find_element_by_id('train_date')
	date.clear()
	date.send_keys(travel_date)
	# 点击查询
	driver.execute_script('document.getElementById("query_ticket").click();')

	time.sleep(1)


# 选择车次
def choose_train(driver):
	trains = {}
	train_number = driver.find_elements_by_class_name('number')
	s_time = driver.find_elements_by_class_name('start-t')
	length = len(train_number)
	for i in range(length):
		trains[train_number[i].text] = s_time[i].text

	print("{0:6} {1:6}".format("车次","出发时间"))
	for x in trains.items():
		print("{0:6} {1:6}".format(x[0],x[1]))

	return list(input("选择车次，多个用空格分隔：").split())

# 判断是否有票
def can_buy(driver,train_number,passenger_num,seat_level):
	if driver.current_url != 'https://kyfw.12306.cn/otn/leftTicket/init':
		return
	js ='var tb = document.getElementById("queryLeftTable");\
		var rows = tb.children;\
		var train_number = '+train_number+';\
		var passenger_num = '+passenger_num+';\
		var seat_level = '+seat_level+';\
		var length = rows.length;\
		for (var i = 0; i <length; i++) {\
			if(rows[i].children.length==0)continue;\
			var number = rows[i].children[0].children[0]\
			.children[0].children[0].textContent.trim();\
			if(train_number.indexOf(number)==-1)\
				continue;\
			for (var j = seat_level.length - 1; j >= 0; j--) {\
				if(rows[i].children[seat_level[j]].textContent == "有"){\
					rows[i].lastElementChild.firstChild.click();\
				}\
				if(rows[i].children[seat_level[j]].textContent >=passenger_num){\
					rows[i].lastElementChild.firstChild.click();\
				}\
			}\
		}'
	driver.execute_script(js)


# 点击下单，确认购买
def confirm_buy(driver, passengers):
	try:
		ticket = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.ID,"ticket_tit_id")))
	except Exception as e:
		print(e)

	print("为您预订：{0}".format(ticket.text))

	js = 'var passengers='+passengers+';\
		console.log(passengers);\
		var passengers_list = document.getElementById("normal_passenger_id");\
		var li = passengers_list.children;\
		for(var i = 0; i<li.length; i++){\
			if(passengers.indexOf(li[i].children[1].textContent)==-1){\
				continue;\
			}\
			li[i].children[0].click();\
		}\
		document.getElementById("submitOrder_id").click();\
	'
	# 等待
	time.sleep(3)

	driver.execute_script(js)

	time.sleep(1)

	driver.execute_script('document.getElementById("qr_submit_id").click()')

	print("订单已提交，请登录12306完成支付")


def list_to_string(li):
	t_n = ""
	for x in li:
		t_n += '"'+str(x)+'",'
	t_n = '['+t_n+']'

	return t_n

# 发送邮件
def mail(msg_body, my_sender, my_pass, my_user):
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