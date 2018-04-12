#!/bin/python
#coding=utf-8
#-*- coding:utf-8 -*-
#author:ven at 3/26/2018
#This script aims at generate country's language file in json
#usage:python language.py **
#python 2.7


import sys
import os
import json
import xlrd

def trans_xls(cfg):
	item = cfg['file']
	data = {}
	
	if not os.path.isdir(cfg['path']):
		print u'生成语言文件路径 :[   ' + os.getcwd() + '  ]'
	else:
		print u'生成语言文件路径 :[   ' + cfg['path'] + '  ]'
	
	bookHandle=xlrd.open_workbook(item)
	sheetHandle = bookHandle.sheet_by_name('language')
	
	for row in range(3,sheetHandle.nrows):
		if(sheetHandle.cell_value(row,0) != '*' or sheetHandle.cell_value(row,1) != '*'):
			continue
		for col in range(3,sheetHandle.ncols):
			if(sheetHandle.cell_value(0,col) != '*' or sheetHandle.cell_value(1,col)!= '*'):
				continue
			if(sheetHandle.cell_value(2,col) not in cfg['country'] or cfg['country'][sheetHandle.cell_value(2,col)] != 1):
				continue
			
			if(type(sheetHandle.cell_value(row,2)) == unicode):
				key = sheetHandle.cell_value(row,2).encode('unicode_escape')
			else:
				key = sheetHandle.cell_value(row,2)
				
			value = {key:sheetHandle.cell_value(row,col)}
			if(sheetHandle.cell_value(2,col) not in data):
				data[sheetHandle.cell_value(2,col)] = value
			else:
				data[sheetHandle.cell_value(2,col)].update(value)

	for country in data:
		file=open(cfg['path']+'/'+country+'.lang', 'w')
		file.write(json.dumps(data[country]).replace("\\\\","\\")) 
		file.close()
		
def get_cfg():
	try:
		file=open('config')
	except IOError:
		default_data = {'path':os.getcwd(),'file':'Language.xlsx','country':{'en':1,'zh':0,'tr':0}}
		file=open('config','w')
		file.write(json.dumps(default_data))
		file.close()
		return default_data
	else:
		str=file.read()
		str=json.loads(str)
		file.close()
		return str
		
def show_info():
	str=u'''工具介绍：
	
用途：把多语言excel表转成各个语言的的json文件，如en.lang,es.lang,tr.lang 等等.

1	程序默认只转换excel文件里的language表
2	config文件说明：

	****
	{
		"path": "C:\\Users\\eg\\Desktop",  //*.lang文件生成路径
		"file": "Language.xlsx", 			  // excel文件名，默认路径为exe的所在目录
		"country": 
			{
				"tr": 0, 					  //  1 表示生成该国家的语言文件
				"en": 1, 					  // 具体内容可以打开excel表看下表内容	
				"zh": 0
			}
	}
	***
	
3	如果没有config文件，可以先运行下exe程序，
	会自动生成一个默认的config文件，再根据需要改路径即可
	
	
		
	'''
	
	print('\033[1;32m %s \033[0m!' % (str))

		
if __name__=="__main__":
	show_info()
	cfg = get_cfg()
	trans_xls(cfg)
	#m = raw_input()
	os.system("pause")
	