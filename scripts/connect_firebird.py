#!/usr/local/bin/python3
# Скрипт предназначен для мониторинга заполняемости таблицы cdr в базе
import fdb
from datetime import timedelta, datetime

# Соединение
con = fdb.connect(dsn='192.168.7.15:e:/path/db_asterisk.fdb', user='user', password='password')

# Объект курсора
cur = con.cursor()

# Выполняем запрос
dt = (datetime.now() - timedelta(minutes=30)).replace(microsecond=0)
cur.execute("select iif(exists(select * from cdr c where c.calldate > '" + str(dt) + "'), 1, 0) from rdb$database")

# cur.fetchall() возвращает список из кортежей. Адресуемся к единственному значению; + перевод строки
print(str(cur.fetchall()[0][0]))