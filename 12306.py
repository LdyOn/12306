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


# 读取配置文件
config = fc.read_setting()
# print(config)
# input()
# 打开浏览器
driver = webdriver.Firefox()
# 记录查询次数
query_times = 1
# 等待5秒
driver.implicitly_wait(5)

print("正在打开12306登录页")
# 进入登录页
driver.get("https://kyfw.12306.cn/otn/resources/login.html")

time.sleep(1)
# 登录
fc.login(driver, config["username"], config["password"])

print("=========================抢票中=============================")

'''进入购票流程'''
# 读取常用联系人，选择要购票的乘客，乘客姓名保存到列表里
if config["passerger"] == '':
	driver.get('https://kyfw.12306.cn/otn/view/passengers.html')
	passengers = fc.choose_passenger(driver)
else:
	passengers = config["passerger"].split()


# 输入出发日期
travel_dates  = config["travel_date"].split();

# 进入车票查询页
driver.get('https://kyfw.12306.cn/otn/leftTicket/init')

# 设置出发地
s = driver.find_element_by_id('fromStationText')
ActionChains(driver).move_to_element(s)\
.click(s)\
.send_keys_to_element(s, config["s_station"])\
.move_by_offset(20,50)\
.click()\
.perform()


# 设置目的地
e = driver.find_element_by_id('toStationText')
ActionChains(driver).move_to_element(e)\
.click(e)\
.send_keys_to_element(e, config["e_station"])\
.move_by_offset(20,50)\
.click()\
.perform()

fc.query_tickets(driver, 
	travel_dates[random.randint(0,len(travel_dates)-1)])


# 选择车次
if config["train_number"] == '':
	trains = fc.choose_train(driver)
else:
	trains = config["train_number"].split()

# 座位
seat_level = config["seat_level"].split()

while True:
	print("查询次数:{0}".format(query_times))
	# 判断能否购买，可以购买进入选择乘客页
	fc.can_buy(driver,fc.list_to_string(trains),
		str(len(passengers)),
		fc.list_to_string(seat_level))
	if driver.current_url=='https://kyfw.12306.cn/otn/confirmPassenger/initDc':
		fc.confirm_buy(driver, fc.list_to_string(passengers))
		break;
	fc.query_tickets(driver, travel_dates[random.randint(0,len(travel_dates)-1)])
	query_times+=1
