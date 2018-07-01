#coding:utf-8
import requests
import threading
from bs4 import BeautifulSoup
import re
import os
import time
import sys


req_header={
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': 'UM_distinctid=16454fb6d7c4ec-0c452c2438881c-3f63440c-144000-16454fb6d7d96; CNZZDATA1261736110=1366147894-1530431518-https%253A%252F%252Fblog.csdn.net%252F%7C1530431518; Hm_lvt_5ee23c2731c7127c7ad800272fdd85ba=1530434122; Hm_lpvt_5ee23c2731c7127c7ad800272fdd85ba=1530434122',
'Host': 'www.qu.la',
'Referer': 'https://blog.csdn.net/baidu_26678247/article/details/75086587',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
}

req_url_base='http://www.qu.la'           #小说主地址
req_url=req_url_base+"/book/161/"           #单独一本小说地址


def get_book():
	r=requests.get(req_url,params=req_header)
	soup=BeautifulSoup(r.text,"html.parser")
	section_list=soup.select('#wrapper .box_con #list dl dd a')
	book={}
	book['url_list']=list(map(lambda x: x['href'].split('/')[-1], filter(lambda x: len(x['href'].split('/'))==4, section_list)))
	book['title']=soup.select('#wrapper .box_con #maininfo #info h1')[0].text


	return book

def get_text(query, req_header):
	#请求当前章节页面  params为请求参数
	r=requests.get(req_url+query,params=req_header)
	#soup转换
	soup=BeautifulSoup(r.text,"html.parser")
	#获取章节名称
	section_name=soup.select('#wrapper .content_read .box_con .bookname h1')[0].text
	#获取章节文本
	section_text=soup.select('#wrapper .content_read .box_con #content')[0].text
	section_text=re.sub( '\s+', '\r\n\t', section_text).strip('\r\n')

	print("章节名: " + section_name)
	print("章节内容：\n"+section_text)
	article = {
		'section_name': section_name,
		'section_text': section_text
	}

	return article

for query in get_book()['url_list']:
    article = get_text(query, req_header)
    fo = open(get_book()['title'] + '.txt', "ab+")
    fo.write(('\r' + article['section_name'] + '\r\n').encode('UTF-8'))
    fo.write((article['section_text']).encode('UTF-8'))
    fo.close()