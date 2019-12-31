# -*- coding: UTF-8 -*-
# python购票脚本
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import funcs12306 as fc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# 打开浏览器
driver = webdriver.Firefox()
# 记录查询次数
query_times = 1
# 等待5秒
driver.implicitly_wait(5)
print("正在登录12306...")
# 进入登录页
driver.get("https://kyfw.12306.cn/otn/resources/login.html")
time.sleep(1)
# 登录
while True:
	fc.login(driver)
	time.sleep(1)
	if driver.current_url!='https://kyfw.12306.cn/otn/resources/login.html':		
		break;
	print("输入信息有误，请重新输入：")
	driver.execute_script('location.reload();')

print("==================== 登陆成功！ ======================")

'''进入购票流程'''
# 等待进入个人中心
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,"welcome-data")))
# 读取常用联系人，选择要购票的乘客，乘客姓名保存到列表里
driver.get('https://kyfw.12306.cn/otn/view/passengers.html')
passengers = fc.choose_passenger(driver)

#输入出发站和终点站
station = list(input("输入出发站和终点站（空格分隔）：").split())

# 输入出发日期
travel_dates = list(\
	input("输入出行日期（例2020-01-09，多个用空格分隔）：")\
	.split());

# 进入车票查询页
driver.get('https://kyfw.12306.cn/otn/leftTicket/init')

# 设置出发地
s = driver.find_element_by_id('fromStationText')
ActionChains(driver).move_to_element(s)\
.click(s)\
.send_keys_to_element(s, station[0])\
.move_by_offset(20,50)\
.click()\
.perform()


# 设置目的地
e = driver.find_element_by_id('toStationText')
ActionChains(driver).move_to_element(e)\
.click(e)\
.send_keys_to_element(e, station[1])\
.move_by_offset(20,50)\
.click()\
.perform()


# 设置出发日
driver.execute_script('document.getElementById("train_date").removeAttribute("readonly");')
date = driver.find_element_by_id('train_date')
date.clear()
date.send_keys(travel_dates[random.randint(0,len(travel_dates)-1)])

# 点击查询
driver.execute_script('document.getElementById("query_ticket").click();')
# 选择车次
trains = fc.choose_train(driver)

"""
	票种：
		1:商务座
		2：一等座
		3：二等座
		4：高级软卧
		5：软卧一等卧
		6：动卧
		7：硬卧二等卧
		8：软座
		9：硬座
		10：无座
"""
# 默认抢一等座、二等座、硬卧、硬座
seat_level = [2,3,7,9]

while True:
	print("查询次数:{0}".format(query_times))
	# 判断能否购买，可以购买进入选择乘客页
	fc.can_buy(driver,fc.list_to_string(trains),
		str(len(passengers)),
		fc.list_to_string(seat_level))
	if driver.current_url=='https://kyfw.12306.cn/otn/confirmPassenger/initDc':
		fc.confirm_buy(driver, fc.list_to_string(passengers))
		break;
	fc.query_tickets(driver, travel_dates)
	query_times+=1
	
	









