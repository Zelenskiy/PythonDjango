#!/usr/local/bin/python3
# Скрипт предназначен для мониторинга заполняемости таблицы cdr в базе
import fdb
from datetime import timedelta, datetime

# Соединение
con = fdb.connect(dsn='127.0.0.1:d:/MyDoc/PythonDjango/KYRS.FDB', user='sysdba', password='masterkey')

# Объект курсора
cur = con.cursor()

# Выполняем запрос
dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
cur.execute("select  * from contacts")

# cur.fetchall() возвращает список из кортежей. Адресуемся к единственному значению; + перевод строки
row = cur.fetchone()
while row:
    print (row)
    row = cur.fetchone()
con.close()
