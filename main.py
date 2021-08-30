import sqlite3
from tkinter import *
from datetime import datetime
from tkinter import ttk
import socket

window = Tk()  # Создаем окно ткинтера
window.title("kvant SMD cheker")  # Назвние окна
window.geometry('1000x800')  # Размеры окна
global board  # Переменная отвечающая за выбор проектра платы внутри программы
board = 0  # 0=проект не выбран
sqlite_file = 'Z:\SMT\database\pro.db'


def entr1(event):  # Функция вызова функции нажатия кнопки при возврате каретки
    clicked()
    txt1.focus()
    # btn.bind('<Return>', clicked)


def entr2(event):  # Функция вызова функции нажатия кнопки при возврате каретки
    clicked1()
    txt2.focus()


def entr3(event):  # Функция вызова функции нажатия кнопки при возврате каретки
    clicked2()
    txt.focus()


def clicked():  # Функция нажатия первой кнопки

    global operator  # Переменная хранящая в себе имя оператора
    global current_datetime  # Переменная хранящая в себе дату и время
    current_datetime = datetime.now()  # Присваивание переменной текущую дату и время
    operator = format(txt.get())  # Заносим в переменную данные считываемые с первой строки
    lbl.configure(text='Хорошо, {},сканируй компонент'.format(operator),
                  font='Times 25')  # Просим оператора сканировать компонент
    txt1.focus()  # Переносим фокус на вторую строку для считывания шк
    txt1.bind('<Return>', entr2)  # Бинд на перенос каретки


def clicked1():  # Функция нажатия второй кнопки
    global component1  # Переменная закончившегося компонента
    component1 = format(txt1.get())  # Заносим в перемнную данные со сканера

    conn = sqlite3.connect(sqlite_file)  # Конектимся к бд
    cur = conn.cursor()  # Создлаем курсор
    conn.commit()
    cur.execute("SELECT * FROM project where  komp= ?", (component1,))
    global dd  # Переменная в которую запишется из бд данные о месте где стоит компонент
    dd = cur.fetchall()
    # if dd==None:
    #     lbl1.configure(text="222",font='Times 25') #Выводим данные на экран
    str2 = ','.join(map(' '.join, dd))
    str2 = str2.replace(",", "\n")
    # if str2==' ':
    #     lbl1.configure(text="222",font='Times 25') #Выводим данные на экран
    lbl1.configure(text=dd, font='Times 25')  # Выводим данные на экран
    txt2.focus()  # Переносим фокус на 3 строку
    txt2.bind('<Return>', entr3)


def clicked2():  # Функкция нажатия 3 кнопки
    flag = 0  # Флаг проверки совпадения компонентов
    global component2  # Переменная нового компонента
    component2 = format(txt2.get())  # Заносим данные со сканера
    for i in dd:  # Сравниваем закончившийся компонент и новый
        for j in i:
            if j == component2:
                flag = 1  # Если совпадает поднимаем флаг
    if flag == 1:  # Если компоненты совпали
        lbl.configure(text="Оператор", font='Times 25')  # Меняем текст для следующей итерации
        lbl1.configure(text=" ", font='Times 25')
        lbl2.configure(text=" ", font='Times 25', bg="#F0F0F0")
        lbl3.configure(text="Все правильно, ставь", font='Times 25', bg="green")  # Уведомление для оператора
        txt.focus()  # Фокус на первую строку
        txt.delete(0, END)  # Очищаем строки
        txt1.delete(0, END)
        txt2.delete(0, END)

    if flag == 0:  # Если компоненты не совпали
        lbl2.configure(text='Еще раз попробуй, {}'.format(operator), font='Times 32',
                       bg="red")  # Уведомление для оператора
        lbl3.configure(text=" ", font='Times 25', bg="#F0F0F0")
        txt.delete(0, END)  # Очищаем строки
        txt1.delete(0, END)
        txt2.delete(0, END)
        conn = sqlite3.connect(sqlite_file)  # Заносим ошибку оператора в бд
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS error (operator, time, component1,component2)")
        cur.execute("insert into error (operator, time, component1,component2) values (?, ?, ?,?)",
                    (operator, current_datetime, component1, component2))
        conn.commit()
    conn = sqlite3.connect(sqlite_file)  # Заносим информацию о операции замены компонента в бд
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS operation (operator, time, component)")
    cur.execute("insert into operation (operator, time, component) values (?, ?, ?)",
                (operator, current_datetime, component1))
    conn.commit()


def clicked6():
    global compBK
    global compBK1
    compBK = format(txt3.get())
    conn = sqlite3.connect(sqlite_file)  # Конектимся к бд
    cur = conn.cursor()  # Создлаем курсор

    cur.execute("SELECT * FROM desc where  copm= ?", (compBK,))
    conn.commit()
    global desc
    desc = cur.fetchall()
    str1 = ';'.join(map('!'.join, desc))
    compBK, descr = str1.split('!', 1)
    # compBK1="^XA^FO300,100^BQN,2,8^FDQA,aa^FS^CFA,18^FO550,100^FDaye gg^FS^XZ"
    # compBK1="^XA^FO 300,20^BY3^BCN,200,Y,N,N ^FDaa^FS^FO 400,300^CFA,15^FDgg^FS ^XZ"
    # compBK1="^XA^FO 700,20^BY3^BCN,200,Y,N,N ^FDaa^FS^FO 500,300^CFA,32^FDgg^FS ^XZ"
    compBK1 = "^XA^FO 700,20^BY3^BCN,200,N ^FDaa^^FS^FO750,250^A0N,43,44^FDaa^FS^FO 500,300^CFA,32^FDgg^FS ^XZ"
    compBK1 = compBK1.replace("aa", compBK)
    # compBK1=compBK1.replace("aye",compBK)
    compBK1 = compBK1.replace("gg", descr)
    print_BK()
    txt3.delete(0, END)


def clicked5():
    txt3.focus()


def print_BK():
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.1.126"
    port = 9100
    try:
        mysocket.connect((host, port))  # connecting to host
        mysocket.send(compBK1.encode())  # using bytes
        mysocket.close()  # closing connection
    except:
        print("Error with the connection")


lbl = Label(window, font='Times 25', text="ОПЕРАТОР")
lbl.grid(column=3, row=1)
lbl1 = Label(window, font='Times 25', text="Закончившийся компонент")
lbl1.grid(column=3, row=2)
lbl2 = Label(window, font='Times 25', text="Новый компонент")
lbl2.grid(column=3, row=3)
lbl3 = Label(window, font='Times 25', text="   ")
lbl3.grid(column=1, row=10)

txt = Entry(window, font='Times 25', width=20)
txt.grid(column=1, row=1)
txt.focus()
txt.bind('<Return>', entr1)
txt1 = Entry(window, font='Times 25', width=20)
txt1.grid(column=1, row=2)
txt2 = Entry(window, font='Times 25', width=20)
txt2.grid(column=1, row=3)
txt3 = Entry(window, font='Times 25', width=20)
# txt3.grid(column=111, row=1)
txt3.place(x=200, y=760, anchor="c")

btn = Button(window, text="go", font='Times 25', command=clicked)
btn.grid(column=2, row=1)
btn1 = Button(window, text="go", font='Times 25', command=clicked1)
btn1.grid(column=2, row=2)
btn2 = Button(window, text="go", font='Times 25', command=clicked2)
btn2.grid(column=2, row=3)
btn6 = Button(window, text="Печать ШТРИХ КОДА", font='Times 12', command=clicked5)
# btn6.grid(column=111, row=7)
btn6.place(x=800, y=730, anchor="c")
btn7 = Button(window, text="Печать", font='Times 12', command=clicked6)
# btn7.grid(column=112, row=1)
btn7.place(x=450, y=760, anchor="c")

window.mainloop()
