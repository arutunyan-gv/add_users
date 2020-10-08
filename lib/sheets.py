
import os
import pandas as pd
from openpyxl import load_workbook
from lib import sheets
import str_edit
import random

from lib import setup
from lib import files
from lib import records

def check(df, pref):
    arr = df.keys()
    messege = ''
    if 'qwery' in arr:
        return (messege)
    if not 'Подразделение' in arr:
        messege += pref['messeges']['no_column_dep']
    if not 'Должность' in arr:
        messege += pref['messeges']['no_column_pos']
    if not 'ФИО' in arr:
        messege += pref['messeges']['no_column_fio']
    if not 'Email' in arr:
        messege += pref['messeges']['no_column_email']
    return(messege)

def processing(df, project_name, pref):
    project = pref['roles'][project_name]
    print(str(project) + '')
    index = df.index
    size = len(index)
    print('size: ' + str(size) + '\n\n')
    if size == 0:
        return(pd.DataFrame(None, index=[0]))
    i = 0


    while i < size:
        error = ''
        warning = ''
        # print(df)
        reply = {}
        raw = df.iloc[i]

        print('🔵' + str(i) + ': \n' + str(raw) + '\n')

        if 'qwery' in raw:
            if raw['qwery']:
                print ('✅')
                rep = records.qwery_func(str(raw['qwery']), pref)
                if rep['error']:
                    error += rep['error']
                else:
                    reply['knd'] = rep['res']
        else:
            # Оприделение company_id и company_name
            # Если подразумевается поиск по ИНН
            if 'ИНН' in raw:
                # print('ИНН')
                try:
                    inn = str_edit.main(str(raw['ИНН']), 'mail')
                    # print ('❇️ inn: ' + str(inn) )
                    rep = records.find_inn(project['com_qwery'], inn, pref)
                    # print ('❇️ rep: ' + str(rep) )
                    if rep['error']:
                        error += rep['error']
                    else:
                        reply['company_id'] = rep['company_id']
                        reply['company_name'] = rep['company_name']

                except:
                    error += pref['messeges']['com_inn_not_matched']
                    reply['company_id'] = 0
                    reply['company_name'] = ''
            # Если выбирается пользователем в файле
            elif 'Компания' in raw or 'ОМСУ' in raw:
                if 'Компания' in raw:
                    col_name = 'Компания'
                elif 'ОМСУ' in raw:
                    col_name = 'ОМСУ'
                # print('Компания')
                if raw[col_name]:
                    rep = records.find_company_name(str(raw[col_name]), pref)
                    if rep['error']:
                        error += rep['error']
                    else:
                        reply['company_id'] = rep['company_id']
                        reply['company_name'] = rep['company_name']
                else:
                    error += pref['messeges']['com_is_blank']
            elif project['com_qwery']:
                print('🟢')
                pref['cursor'].execute(project['com_qwery'])
                res = pref['cursor'].fetchone()
                if res:
                    print(res)
                    reply['company_id'] = res[0]
                    reply['company_name'] = res[1]
            else:
                error += pref['messeges']['inn_omsu_com']

            if 'Подразделение' in raw:
                if raw['Подразделение']:
                    reply['division'] = str(raw['Подразделение'])
                else:
                    warning += pref['messeges']['dep_blank']


            # Должность
            if raw['Должность']:
                reply['position'] = str(raw['Должность'])
            else:
                warning += pref['messeges']['pos_blank']

            # Role
            if project['role']:
                rep = records.find_role(project['role'], pref)
                if rep['error']:
                    error += rep['error']
                else:
                    reply['role'] = project['role']
            else:
                error += pref['messeges']['role_blank']

            # ФИО
            if raw['ФИО']:
                name = str_edit.main(str(raw['ФИО']), 'name')
                reply['name'] = name
            else:
                warning += pref['messeges']['fio_blank']



            # Email
            if raw['Email']:
                email = str_edit.main(str(raw['Email']), 'mail')
                reply['email'] = email
            else:
                error += pref['messeges']['email_blank']


            # pass
            if email:
                rep = records.find_pass(email, pref)
                if rep['error']:
                    error += rep['error']
                else:
                    reply['pass'] = rep['pass']

            if not error:
                rep = records.insert_raw(reply, pref)
                if rep['error']:
                    error += rep['error']
                else:
                    reply['res'] = rep['res']
            else:
                reply['res'] = pref['messeges']['project_error']
            if error:
                error = pref['messeges']['ERRORS'] + error
            if warning:
                warning = pref['messeges']['WARNINGS'] + warning
            error = error + '\n' + warning
            reply['error'] = error.replace('\t', ' ')
            # print(reply)
            # {'company_id': reply['company_id']}
        if i == 0:
            new_df = pd.DataFrame(reply, index=[0])
        else:
            new_df.loc[i] = reply
        i += 1

    print('return')
    return new_df