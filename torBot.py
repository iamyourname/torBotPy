import sys

import libtorrent as lt
import time
import datetime
import psycopg2

# Функция обновления статуса торрента
def torUpdate(torrent_name):
    try:
        t_conn = psycopg2.connect(dbname='domofon', user='domofon', password='xid123mt', host='45.139.77.167')
        t_cursor = t_conn.cursor()
        t_insert_query = """
        UPDATE torrents set t_status = %s
        where torrent_name = %s
        ;
        """
        t_data = ('DONE',torrent_name)
        t_cursor.execute(t_insert_query, t_data)
        print("Status updated")
        t_conn.commit()
        t_cursor.close()
        t_conn.close()
    except:
        print('Can`t establish connection to database')
# Функция добавления нового торрента в БД
def torWrite(torrent_name, t_status):
    try:
        t_conn = psycopg2.connect(dbname='domofon', user='domofon', password='xid123mt', host='45.139.77.167')
        t_cursor = t_conn.cursor()
        t_insert_query = """
        INSERT INTO torrents(torrent_name,t_status) 
        VALUES (%s, %s);
        """
        t_data = (torrent_name, t_status)
        t_cursor.execute(t_insert_query, t_data)
        print("New torrent added")
        t_conn.commit()
        t_cursor.close()
        t_conn.close()
    except:
        print('Can`t establish connection to database')
# Функция записи лога в БД
def logWrite(t_name, mes):
    try:
        conn = psycopg2.connect(dbname='domofon', user='domofon', password='xid123mt', host='45.139.77.167')
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO log(torrent_name, message)
        VALUES (%s, %s);
        """
        data = (t_name, mes)
        cursor.execute(insert_query, data)
        #print("Data Inserted")
        conn.commit()
        cursor.close()
        conn.close()
    except:
        print('Can`t establish connection to database')

#link = ('magnet:?xt=urn:btih:3E6A63DAA3D35E3BC0AFE7B04CE009090C11EA95&tr=http%3A%2F%2Fbt4.t-ru.org%2Fann%3Fmagnet&dn=Windows%2010%20PE%201.2021%20by%20Ratiborus%20(x86%2Fx64%2FRUS)%201.2021%20x86%20x64%20%5B10.02.2021%2C%20RUS%5D')
#link = ('/Users/m.moiseev/PycharmProjects/PythonProject1/deep.torrent')
link = ('')
isSome = False

ses = lt.session()
info = lt.torrent_info(sys.argv[1])
print(info)
ses.listen_on(6881, 6891)
params = {
    'save_path': '/Users/m.moiseev/PycharmProjects/PythonProject1/',
    'storage_mode': lt.storage_mode_t(2)}

def download(torrent):
 # handle = lt.add_magnet_uri(ses, torrent, params)
  handle = ses.add_torrent({'ti': info, 'save_path': '.'})
  ses.start_dht()

  begin = time.time()
  print(datetime.datetime.now())
  print ('Получение метаданных...')

  while (not handle.has_metadata()):
      time.sleep(1)
  print ('Метаданные получены, начинается торрент-загрузка...')

  print('Запуск', handle.name())
  ss = handle.status()
  sss = handle.name()
  torWrite(sss, 'downloading')

  while (handle.status().state != lt.torrent_status.seeding):
      s = handle.status()
      state_str = ['queued', 'checking', 'downloading metadata', \
              'downloading', 'finished', 'seeding', 'allocating']
      mes_log = ('%.2f%% информация (загрузка: %.1f kb/s отправка: %.1f kB/s пиры: %d) %s ' % \
              (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
              s.num_peers, state_str[s.state]))
      logWrite(sss, mes_log)
      print ('%.2f%% информация (загрузка: %.1f kb/s отправка: %.1f kB/s пиры: %d) %s ' % \
              (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
              s.num_peers, state_str[s.state]))
      time.sleep(5)

  end = time.time()
  print(handle.name(), 'Загрузка закончена')
  logWrite(sss, 'Загрузка закончена')
  torUpdate(sss)
  print('Затрачено времени: ', int((end-begin)//60), 'минут ',
        int((end-begin)%60), 'секунд')

  print(datetime.datetime.now())

if isSome:
  for torrent in link:
    print(torrent)
    download(torrent)
else:
  download(link)
