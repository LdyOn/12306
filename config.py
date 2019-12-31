import re
class Config():
	"""配置文件"""
	def __init__(self):
		self.config = {}
		self.read_setting()

	# 从配置文件读取配置
	def read_setting(self):
		s_file = open("setting.ini", encoding='UTF-8')
		lines = s_file.readlines()
		for x in lines:
			if re.match(";", x) == None :
				x = x.strip('\n')
				s = x.split("=")
				self.config[s[0].strip()] = s[1].strip()




		