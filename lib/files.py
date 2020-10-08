
import os
import pandas as pd
from openpyxl import load_workbook
from lib import sheets
import str_edit
import random

from lib import setup
from lib import sheets
from lib import records

def take_files(pref):
    files = []
    files_list = os.listdir('./' + pref['input_folder'])
    messege = pref['messeges']['file_list']
    for file in files_list:
        if '.xlsx' in file and '~$' not in file:
            files.append(file)
            messege += '    - ' + file + '\n'
    print(messege)
    return files


def processing(file, pref):
    xl = pd.ExcelFile(pref['input_folder'] + file)
    flag = 1
    valid_sheets_names = 0
    file_name = file.replace('.xlsx', '_processed.xlsx')
    writer = pd.ExcelWriter(pref['output_folder'] + file_name, engine='xlsxwriter')
    messege = ''
    print('▶️ ' + file_name + ': ' + str(xl.sheet_names))
    for sheet in xl.sheet_names:
        if sheet in pref['roles'] or sheet == 'КНД':
            valid_sheets_names += 1;
            print('🔵' + sheet)
            df = xl.parse(sheet)
            messege = sheets.check(df, pref)
            if messege == '':
                data_frame = sheets.processing(df, sheet, pref)
                if not data_frame.empty:
                    print(data_frame)
                    data_frame.to_excel(writer, sheet)
                    flag = 0
            else:
                print(messege)
                df = pd.DataFrame(data={'Ответ': messege}, index=['Ответ'])
                df.to_excel(writer, 'Ошибки')
                flag = 0

    if not valid_sheets_names and not messege:
        answer = {'Ответ': pref['messeges']['no_valid_sheet_names'] + str(xl.sheet_names) +' . Валидные названия:' + str(roles.keys())}
        print(answer)
        df = pd.DataFrame(data=answer, index=['Ответ'])
        print(df)
        df.to_excel(writer, 'Ошибки')
        flag = 0

    writer.save()
    if flag:
        os.remove(pref['output_folder'] + file_name)
        return ''
    else:
        return file_name