import os

from lib import setup
from lib import files
from lib import sheets

# Чтение настроек
pref = setup.read_json('prefs/prefs.json')

# Чтение сообщений и запросов
pref['messeges'] = setup.read_json(pref['messeges_file'])
pref['qwerys'] = setup.read_json(pref['qwerys_file'])
pref['db_cred'] = setup.read_json(pref['db_cred_file'])
pref['messege'] = ''

# Подключение к базе
print(pref['messeges']['connecting'])
pref['conn'] = setup.db_connect(pref)

# Подключение удалось
if pref['conn']:
    pref['conn'].autocommit = True
    pref['cursor'] = pref['conn'].cursor()
    print(pref['messeges']['connecting_established'])

    # Чтение настроек по проектам из базы данных
    print(pref['messeges']['roles_read'])
    pref['roles'] = setup.read_roles(pref)
    print (pref['roles'])
    print(pref['messeges']['roles_read_succeed'])

    # Обработка файлов
    file_list = files.take_files(pref)
    for one_file in file_list:
        if files.processing(one_file, pref):
            os.remove(pref['input_folder'] + one_file)
            print(one_file + ' — ✅ OK!')

    # Применение изменений
    print(pref['messeges']['appling_changes'])
    pref['cursor'].execute('select all_support()')
    print(pref['messeges']['changes_applied'])

    # Отключение от базы
    pref['conn'].close()
    pref['cursor'].close()

# Неудалось подключится к базе и программа завершается
else:
    print(pref['messeges']['connection_error'])
    print(pref['messeges']['program_immediate_exit'])
