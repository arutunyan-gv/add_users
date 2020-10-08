
from lib import setup
from lib import files
from lib import sheets

import os
import pandas as pd
from openpyxl import load_workbook
from lib import sheets
import str_edit
import random

def find_inn(qwery, inn, pref):
    reply = {'error': ''}
    try:
        inn = int(float(inn))
    except:
        reply['error'] += pref['messeges']['inn_only_num']
        print('🟡' + str(inn))
        return reply
    if inn <= 0:
        reply['error'] += pref['messeges']['inn_only_natural']
        return reply
    if qwery == '':
        reply[
            'error'] += pref['messeges']['inn_convert_error']
        return reply
    qwery = qwery.replace('__arg__', str(inn))
    try:
        pref['cursor'].execute(qwery)
        res = pref['cursor'].fetchone()
    except:
        print('⛔️ find_inn')
        reply['error'] += pref['messeges']['connection_error']
    if not res:
        reply['error'] += pref['messeges']['inn_search_failure']
        return reply
    reply['company_id'] = res[0]
    reply['company_name'] = res[1]
    return reply


def find_company_name(company, pref):
    reply = {'error': ''}
    company = str(company)
    company = company.replace('-', '—')
    company_arr = company.split(' — ')
    try:
        company_id = int(company_arr[1])
    except:
        reply['error'] += pref['messeges']['com_blank']
        reply['error'] += pref['messeges']['com_sep_val']
        reply['error'] += pref['messeges']['com_only_natural']
        return(reply)
    if (company_id <= 0):
        reply['error'] += pref['messeges']['com_only_positive']
    else:
        reply['company_id'] = company_id
    try:
        pref['cursor'].execute(pref['qwerys']['find_company_name'].replace('__arg__', str(company_id)))
        res = pref['cursor'].fetchone()
        if not res:
            reply['error'] += pref['messeges']['com_search_failure']
            return reply
        else:
            reply['company_name'] = res[0]
    except:
        print('⛔️ find_company_name')
        reply['error'] += pref['messeges']['connection_error']
    return reply


def find_role(role, pref):
    reply = {'error': ''}
    try:
        role = int(role)
    except:
        reply['error'] += pref['messeges']['role_only_natural']
    try:
        pref['cursor'].execute(pref['qwerys']['find_type_user'].replace('__arg__', str(role)))
        res = pref['cursor'].fetchone()
        if not res:
            reply['error'] += pref['messeges']['no_role']
            return reply
        else:
            reply['role'] = res[0]
    except:
        print('⛔️ find_role')
        reply['error'] += pref['messeges']['connection_error']

    return reply


def find_pass(email, pref):
    reply = {'error': ''}
    qwery = pref['qwerys']['find_pass'].replace('__arg__', email)
    try:
        pref['cursor'].execute(qwery)
        res = pref['cursor'].fetchone()
        res2 = pref['cursor'].fetchone()
        if not res2:
            if not res:
                reply['pass'] = 'kn' + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(
                    random.randint(0, 9)) + str(random.randint(0, 9))
            else:
                reply['pass'] = res[0]
        else:
            reply['error'] += pref['messeges']['many_pass']
    except:
        print('⛔️ find_pass')
        reply['error'] += pref['messeges']['connection_error']

    return reply


def insert_raw(raw, pref):
    reply = {'error': ''}

    qwery = f"select company_id, type_user_id, email from tmp.all_users where email = '{raw['email']}' and company_id = {raw['company_id']} and type_user_id = {raw['role']}"
    print(qwery)
    try:
        pref['cursor'].execute(qwery)
        res = pref['cursor'].fetchone()
    except:
        print('⛔️ insert_raw')
        reply['error'] += pref['messeges']['connection_error']
    camp_1 = ''
    if res:
        camp_1 = str(res[0]) + ' ' + str(res[1]) + ' ' + str(res[2])
    camp_2 = str(raw['company_id']) + ' ' + str(raw['role']) + ' ' + str(raw['email'])
    if camp_1 == camp_2:
        reply['res'] = pref['messeges']['project_already_appointed']
        return(reply)
    # com_id = raw['company_id'].replace("\'", "`")
    a = "'"
    b = "\'"
    qwery = f"insert into tmp.all_users (company_id, company, division, pos, type_user_id, name, email, password, is_new) select {raw['company_id']}, E'{raw['company_name'].replace(a, b)}', E'{raw['division'].replace(a, b)}', E'{raw['position'].replace(a, b)}', {raw['role']}, E'{raw['name'].replace(a, b)}', '{raw['email']}', '{raw['pass']}', true"
    print('🟢: ' + qwery)
    try:
        pref['cursor'].execute(qwery)
        reply['res'] = pref['messeges']['project_success']
    except:
        reply['res'] = pref['messeges']['project_error']
        reply['error'] += pref['messeges']['qwery_error'] + qwery.replace('\n', ' ') + '\n'

    return reply

def qwery_func(qwery, pref):
    reply = {'error': ''}
    print(qwery)
    try:
        pref['cursor'].execute(qwery)
        reply['res'] = pref['cursor'].fetchone()
    except:
        print('⛔️ qwery_func')
        reply['error'] += pref['messeges']['connection_error']
    return reply