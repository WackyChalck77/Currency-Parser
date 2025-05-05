import requests
from bs4 import BeautifulSoup
import lxml
import datetime
import schedule
import time

#Объявляем переменные
#Ссылка на сайт с курсом Узбецкого сума
url_1='https://ratestats.com/uzbekistani-som/'
#Ссылка на сайт с курсом Белорусского рубля
url_2='https://ratestats.com/belarusian-ruble/'

#Действие по ссылке url_1 Узбецкий сум
#r=requests.get(url_1)
#content=r.text
#Действие по ссылке url_2 Белорусский рубль
#r_2=requests.get(url_2)
#content=r_2.text

    #Упрощаю soup = BeautifulSoup(content, 'lxml', from_encoding='ISO-8859-1')

#Функция, которая подключается к ссылке, загружает текст html, ищет СУМ
def pars_sum(url):
    r=requests.get(url)
    content=r.text
    #Получение имени на Заголовок сайта с курсом Узбецкого сума
    soup = BeautifulSoup(content, 'lxml')
    title=soup.title.string
    print(title)
    #Поиск Ячейки с цифрой сума
    curs_sum=soup.find("span", {"class": "b-current-rate__value"}).text
    return curs_sum

#Функция, которая подключается к ссылке, загружает текст html, ищет Бел. РУБ
def pars_belrub(url):
    r=requests.get(url)
    content=r.text
    #Получение имени на Заголовок сайта с курсом Белорусского рубля
    soup = BeautifulSoup(content, 'lxml')
    title=soup.title.string
    print(title)
    #Поиск Ячейки с курсом белорусского рубля
    curs_bel=soup.find("span", {"class": "b-current-rate__value"}).text
    return curs_bel
    
#функция определяющая время текущее
def whats_time_now():
    #Выясняем текущую дату и время
    time_now=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=3)
    #Форматируем под удобный нам формат 06.03.2024  0:01:03
    time_now_format=time_now.strftime('%d.%m.%Y %H:%M:%S')
    return time_now_format

#функция по записи даты и курсов валют в файл
def record_new_data(a, b):
    time_now_format=whats_time_now()
    #Открываем файл, записываем в него данные в prn, разделение табуляцией \t
    #возможно понадобится пошаманить с кодировкой my_file=open("Course_report.csv", "a", encoding='utf-8')
    curs_sum=a
    curs_bel=b
    my_file=open("course_report.prn", "a")
    my_file.write(f'{time_now_format}\t{curs_bel}\t{curs_sum}\n')
    my_file.close()
    print(f'данные на момент {time_now_format} добавлены')

#Цикл, который проверяет время каждую минуту и запускает задачу
def job():
    #выясняем текущую дату
    whats_time_now()
    #узнаем и печатаем курс СУМ
    curs_sum=pars_sum(url_1)
    print(curs_sum)
    #узнаем и печатаем курс Бел.РУБ
    curs_bel=pars_belrub(url_2)
    print(curs_bel)
    #Записываем данные в файл
    record_new_data(curs_sum, curs_bel)
    #print(f'Программа исполняется,{time_now_format}')    
    print('Программа (функция job) исполняется..'+'\n')

#Запланируем выполнение функции по записи новых данных в таблицу на каждый день
#в 21:40 чтобы можно было сделать отчет ночью например
#schedule.every().day.at("10:35").do(job)
#вариант ежеминутный
schedule.every(5).minutes.do(job)
#вариант каждые n часа
#schedule.every(1).hours.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
    print("Парсинг курсов (модуль shedule) валют выполняется..\n")
