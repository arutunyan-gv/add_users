#!/usr/bin/python3
# -*- coding=utf-8 -*-

import sys
import re
import os
import unicodedata


def str_len(string):
	string = str(string.__len__())
	return (str(string))


def str_upper(string):
	string = string.upper()
	return (str(string))


def str_lower(string):
	string = string.lower()
	return (str(string))


def str_title(string):
	string = string.title()
	return (str(string))


def str_trim(string):
	string = string.strip()
	return (str(string))


def str_space(string):
	while string.find('  ') != -1:
		string = string.replace('  ', ' ')
	return (str(string))


def str_space_ultimate(string):
	string = string.replace(' ', '')
	return (str(string))


def str_tab(string):
	string = string.replace('\t', ' ')
	return (str(string))


def str_new_line(string):
	string = string.replace('\n', '')
	return (str(string))


def str_return(string):
	string = string.replace('\r', '')
	return (str(string))


def str_vet_tab(string):
	string = string.replace('\v', '')
	return (str(string))


def str_multiply_nl(string, arg):
	nl = ''
	string_new = ''
	num = int(arg[1:])
	if string[len(string) - 1] != '\n':
		nl = '\n'
	while num:
		string_new += string + nl
		num = num - 1
	return (str(string_new[:-1]))


def str_multiply(string, arg):
	string_new = ''
	num = int(arg[1:])
	while num:
		string_new += string
		num = num - 1
	return str(string_new[:-1])


def str_not_print(string):
	string = str_new_line(string)
	string = str_tab(string)
	string = str_return(string)
	string = str_vet_tab(string)
	return (str(string))


def str_excel(arr, args):
	arr = arr.split('\r\n')
	new_arr = ''
	for row in arr:
		row = row.split('\t')
		new_row = ''
		for cell in row:
			cell = excel_apply(cell, args)
			new_row = new_row  + cell  + '\t'
		new_arr = new_arr  + new_row[:-1]   + '\r\n'
	return (new_arr)


def str_excel_test(arr, args):
	arr = arr.split('\r\n')
	new_arr = ''
	for row in arr:
		row = row.split('\t')
		new_row = ''
		for cell in row:
			cell = excel_apply(cell, args)
			new_row = new_row + '<' + cell + '>'
		new_arr = new_arr + '[' + new_row + ']'
	return (new_arr)


def excel_apply(string, args):
	if ('ln' in args):
		string = str_len(string)
	if ('u' in args):
		string = str_upper(string)
	if ('l' in args):
		string = str_lower(string)
	if ('c' in args):
		string = str_title(string)
	if ('t' in args):
		string = str_trim(string)
	if ('s' in args):
		string = str_space(string)
	if ('pr' in args):
		string = str_not_print(string)
	if ('tb' in args):
		string = str_tab(string)
	if ('nl' in args):
		string = str_new_line(string)
	if ('vt' in args):
		string = str_tab(string)
	if ('rt' in args):
		string = str_new_line(string)

	if ('name' in args):
		string = str_trim(string)
		string = str_space(string)
		string = str_title(string)
		string = str_not_print(string)
	if ('mail' in args):
		string = str_trim(string)
		string = str_space_ultimate(string)
		string = str_lower(string)
		string = str_not_print(string)

	if ('norm' in args):
		string = str_trim(string)
		string = str_space(string)
		string = str_not_print(string)

	return (string)


def str_cirilik_norm(string):
	#не трогать буквы в скобках!!!
	string = string.replace('й', 'й')
	string = string.replace('ё', 'ё')
	string = string.replace('Й', 'Й')
	string = string.replace('Ё', 'Ё')
	return(string)


def repeat(string, number):
	new_str = string
	if (new_str[-1] != '\n'):
		new_str = new_str + '\n'
	string = ''
	while (number > 0):
		string = string + new_str
		number = number - 1
	return(string[0:-1])


def main(string, args):
	args = args.split(' ')
	string = str_cirilik_norm(string)
	if 'x' in args:
		string = str_excel(string, args)
	elif 'test' in args:
		string = str_excel_test(string, args)
	else:
		string = excel_apply(string, args)
	return string

