

import json
import psycopg2


def debug(is_debugg_true, string):
    if is_debugg_true:
        print(string)

def read_json(file_name):
    try:
        json_file = open(file_name)
    except:
        print('Не найден файл ' + file_name)
        return None
    try:
        json_str = json_file.read()
    except:
        print('Не удалось прочитать содержимое файла ' + file_name)
        return None
    try:
        json_d = json.loads(json_str)
    except:
        print('Возникла ошибка при парсинге json:')
        print(json_str)
    return json_d



def db_connect(pref):
    try:
        conn = psycopg2.connect(
            dbname=pref['db_cred']['dbname'],
            host=pref['db_cred']['host'],
            port=pref['db_cred']['port'],
            user=pref['db_cred']['user'],
            password=pref['db_cred']['password'])
        return conn
    except:
        print(pref['messeges']['connection_establish_error'])
        print(str(pref['db_cred']))
        return None



def read_roles(pref):
    pref['cursor'].execute(pref['qwerys']['read_roles'])
    res = pref['cursor'].fetchone()
    dict = {}
    while res:
        dict[res[0]] = {'role': res[1], 'com_qwery': res[2]}
        res = pref['cursor'].fetchone()
    return (dict)