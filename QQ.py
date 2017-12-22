#!/usr/bin/python3
# encoding=utf-8
#by 黑小马
import urllib.request, json, time, http.cookiejar,re
from http import client
from urllib import parse
import sqlite3
uin=0
UA=''
qzone_cookie=''
class MySql:
	def __init__(self):
		#print('建立数据库')
		con=sqlite3.connect("qq.db")
		self.conn=con
		#print("获取游标")
		self.cur=con.cursor()
	def create_table(self,sql):
		#print("建立表")
		self.cur.execute(sql)
	def execs(self,sql):
		self.cur.execute(sql)
	def get_res(self,sql):
		res=self.cur.execute(sql)
		return res
	def get_save(self):
		self.conn.commit()
def make_g_tk(cookie):
	'''
	通过Cookie生成g_tk
	'''
	ss=re.search('p_skey=([^;^\']*)',cookie).group(1)
	hash = 5381
	for i in ss:
		hash+=(hash<<5)+ord(i)
	return str(hash & 0x7fffffff)

def get_friends(uin):
	'''
	请求网页输出到文本
	'''
	url="https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin="+uin+"&do=1&rd=0.04546179743896972&fupdate=1&clean=1&g_tk="+(make_g_tk(qzone_cookie))
	req = urllib.request.Request(url, headers={'Cookie': qzone_cookie, 'User-Agent': UA})
	html=urllib.request.urlopen(req)
	str=html.read()
	data = str.decode('UTF-8')
	data_json=json.loads(data[10:-2])
	data_list=data_json['data']['items_list']
	i=0
	while i<len(data_list):
		qq=data_list[i]['uin']
		get_qq_msg(qq)
		i+=1
def get_qq_msg(d_qq):
	'''
	开始点赞
	'''	
	body={'_q':str(d_qq),'bkn':194588796,'src':'mobile'}
	headers = {
	'Cookie': qzone_cookie,
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
	
	}
	urll='/cgi-bin/more_profile_card/more_profile_card'
	httpClient = http.client.HTTPConnection("ti.qq.com")
	httpClient.request("POST", urll, urllib.parse.urlencode(body), headers)
	response = httpClient.getresponse()
	data=response.read().decode('UTF-8')
	data_json=json.loads(data)
	
	if data_json['ec']==0:
		#qq号
		print(d_qq)
		#网名
		nick=data_json["profile"][0]["nick"]
		print(nick)
		#年龄
		age=data_json["profile"][0]["age"]
		print(age)
		#出生年
		year=data_json["profile"][0]["birthday"]["year"]
		print(year)
		#地区
		city=data_json["profile"][0]["location_state"]+data_json["profile"][0]["hometown_city"]
		print(city)
		#性别
		if data_json["profile"][0]["gender"]==1:
			print("男")
			sql="insert into qq(qq,nick,age,year,city,sex) values ('%s','%s','%s','%s','%s','男')"%(d_qq,nick,age,year,city)
		else:
			print("女")
			sql="insert into qq(qq,nick,age,year,city,sex) values ('%s','%s','%s','%s','%s','女')"%(d_qq,nick,age,year,city)
		print("-------------------------")
		#塞进数据库
		ms.execs(sql)
		#塞进后就保存下
		ms.get_save()
	httpClient.close()
		

def load_data():
	global uin
	global UA
	global qzone_cookie
	qq_value = input('请输入QQ号码：')
	uin=qq_value
	cookie_value = input('请输入QQ空间Cookie：')
	qzone_cookie =cookie_value
	UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
	get_friends(str(uin))
def select_all(ms):
	res=ms.get_res('select * from qq')
	for item in res.fetchall():
			print(item)
def select_nv(ms):
	res=ms.get_res("select * from qq where sex='女'")
	for item in res.fetchall():
			print(item)
def select_nan(ms):
	res=ms.get_res("select * from qq where sex='男'")
	for item in res.fetchall():
			print(item)
def select_age(ms):
	res=ms.get_res("select * from qq where age>20")
	for item in res.fetchall():
			print(item)
	
if __name__ == '__main__':
	print("欢迎使用QQ一键分析程序")
	#初始化数据库
	ms=MySql()
	#没有表就创建表
	ms.create_table("create table IF NOT EXISTS qq(id integer primary key autoincrement not null,qq int,nick text,age int,year int,city text,sex text)")
	print("数据库初始化完毕")
	
	while True:
		type= input('选择操作类型(如：1)\n1，加载数据  2，显示所有数据\n3，显示女性数据  4，显示男性数据\n5，显示年龄大于20的\n')
		if type=="1":
			load_data()
		elif type=="2":
			select_all(ms)
		elif type=="3":
			select_nv(ms)
		elif type=="4":
			select_nan(ms)	
		elif type=="5":
			select_age(ms)
		else:
			print("错误__")
	

	
	




	
	
	
	
	
	
	
	
	
	
	