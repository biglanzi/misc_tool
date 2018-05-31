#!/bin/python
#coding=utf-8
#-*- coding:cp936 -*-
#author:steven at 6/26/2017
#This script aims at finding the matching xlsx file that containing the wanted sheet
#usage:python find_xls.py **

import sys
import os
import xlrd

if(len(sys.argv) < 2):
	print "usage:python find_xls.py txtName"
	sys.exit()
	
def match_xls():
	#t_path = unicode('D:\dir',"utf-8")
	t_path=u'D:\dir'
	arg_1 = sys.argv[1]
	
	all_t = os.listdir(t_path)
	for item in all_t:
		if(item.split('.')[-1] == "xlsx"):
			print item
			os.chdir(t_path)
			data=xlrd.open_workbook(item)
			name=data.sheet_names()
			for single in name:
				if arg_1 == single:
					print ""
					print "Result:[ "+item + " ]"
					sys.exit()
	
	print "Result:-------------oops,not find wanted excel file"
		
if __name__=="__main__":
	match_xls()