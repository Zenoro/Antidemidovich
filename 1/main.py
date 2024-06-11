import time
import math
import numpy as np
from matplotlib import pyplot as plt
import sympy as sp
from scipy.spatial import distance
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from ttkthemes import ThemedTk
from matplotlib.figure import Figure

area_limits = []
saver = []
num_iter = 0


#   Интерфейс

window = ThemedTk(theme="radiance")
window.resizable(True, True)
#ttk.Style(window).theme_use('black')

window.title('Нахождение гомоклинических точек')

window_frame = ttk.Frame(window)
window_frame.pack(fill=BOTH, expand=True)

tool_bar_1 = ttk.Frame(window_frame)
tool_bar_1.grid(column=0, row=1, columnspan=1)

tool_bar_2 = ttk.Frame(window_frame)
tool_bar_2.grid(column=1, row=1, columnspan=1)

tool_bar = ttk.Frame(window_frame)
tool_bar.grid(column=0, row=2, columnspan=2, )

crosig_entry = ttk.Entry(tool_bar, width=40)
crosig_entry.config(state=DISABLED)
crosig_entry.grid(column=0, row=10, columnspan=2)


def length(a, b):
        [x1, y1], [x2, y2] = a, b
        return (((x1-x2)**2)+((y1-y2)**2))**0.5

    # Функция для итерирования
        
def ccw(A,B,C):
    [ax, ay] = A
    [bx, by] = B
    [cx, cy] = C
    return (cy-ay)*(bx-ax) > (by-ay)*(cx-ax)   

def intersect(A,B,C,D):
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def coef(a, b):
    (x1, y1) = a[0]
    (x2, y2) = a[1]
    (X1, Y1) = b[0]
    (X2, Y2) = b[1]
    if intersect(a[0], a[1], b[0], b[1]) == True:
        a1, b1, c1 = 1/(x2-x1), -1/(y2-y1), x1/(x2-x1) - y1/(y2-y1)
        a2, b2, c2 = 1/(X2-X1), -1/(Y2-Y1), X1/(X2-X1) - Y1/(Y2-Y1)
        if (a1*b2-a2*b1) != 0:
            ha = [(c1*b2-c2*b1)/(a1*b2-a2*b1), (a1*c2-a2*c1)/(a1*b2-a2*b1)]
            if (ha[0] == 0) and (ha[1] == 0):
                return 0
            else:
                return ha
        else:
            return 0
    else: 
        return 0

def intersection(V1_x_folder, V1_y_folder, V2_x_folder, V2_y_folder):
    first_list = list(zip(V1_x_folder,V1_y_folder))
    second_list = list(zip(V2_x_folder, V2_y_folder))
    for i in range(len(first_list)-1):
        for j in range(len(second_list)-1):
            saver = coef([first_list[i], first_list[i+1]], [second_list[j], second_list[j+1]])
            if saver != 0 and saver != None:                
                V1_x_folder = V1_x_folder[:i+1] 
                V1_x_folder.append(saver[0])
                V1_y_folder = V1_y_folder[:i+1] 
                V1_y_folder.append(saver[1])
                return [V1_x_folder, V1_y_folder]


def area(a, b):
    return [a+0.2, a-0.2, b+0.2, b-0.2]

def angle(first_point, second_point, intersection_point):
    x1, y1 = first_point
    x2, y2 = second_point
    x0, y0 = intersection_point
    angl = (x1-x0)*(x2-x0)+(y1-y0)*(y2-y0)/(length(first_point, intersection_point)*length(second_point, intersection_point))
    return math.acos(angl)

def start():
    plt.ion()
    # Условие
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    a = sp.Symbol('a')
    b = sp.Symbol('b')
    c = sp.Symbol('c')

    a = eval(param_entry.get())
    b = eval(second_param_entry.get())
    c = eval(third_param_entry.get())
    h = eval(accuracy_entry.get())

    #X = x + y + a*x*(1-x)
    #Y = y + a*x*(1-x)

    X=eval(Firstpoint_equation_1.get())
    Y=eval(Firstpoint_equation_2.get())

    # Ручной ввод
    global saver
    global num_iter
    # global calbas
    global window_frame
    global area_limits

    iter = 0

    V1 = [eval(First_vector_entry_X.get()), eval(First_vector_entry_Y.get())]
    V2 = [eval(Second_vector_entry_X.get()),  eval(Second_vector_entry_Y.get())]
    # Длинна отрезка

    def gen(a, b):

    # Отобразили полученные не отображённые границы отрезков
    # Нужно для определения длинны отрезка

        x1 = X.subs({x: a[0], y: a[1]})
        y1 = Y.subs({x: a[0], y: a[1]})
        x2 = X.subs({x: b[0], y: b[1]})
        y2 = Y.subs({x: b[0], y: b[1]})

        # Проверка на точность

        if length([x1, y1], [x2, y2]) > h:
            return gen(a, [(a[0]+b[0])/2, (a[1]+b[1])/2])+gen([(a[0]+b[0])/2, (a[1]+b[1])/2], b)
        else:
            return [X.subs({x: a[0], y: a[1]}), Y.subs({x: a[0], y: a[1]})]


    # Для V1

    V1_x_folder = [0.0, V1[0], X.subs({x: V1[0], y: V1[1]})]
    V1_y_folder = [0.0, V1[1], Y.subs({x: V1[0], y: V1[1]})]


    # Проверили содержание массивов

    print(V1_x_folder)
    print(V1_y_folder)

    # Объединяем результаты работы рекурсивной функции и полученные ранее границы отрезков

    u = []
    for i in range(len(V1_x_folder)-1):
        u = u + gen([V1_x_folder[i], V1_y_folder[i]], [V1_x_folder[i+1], V1_y_folder[i+1]])
    print(u)
    V1_x_folder, V1_y_folder = u[::2], u[1::2]
    # U1 = u
    # Для V2

    # Другие формулы для Х и У

    X=eval(Secondpoint_equation_1.get())
    Y=eval(Secondpoint_equation_2.get())

    #X = x - y
    #Y = y - a*(x-y)*(1-x+y)

    V2_x_folder = [0.0, V2[0], X.subs({x: V2[0], y: V2[1]})]
    V2_y_folder = [0.0, V2[1], Y.subs({x: V2[0], y: V2[1]})]

    print(V2_x_folder)
    print(V2_y_folder)
    

    u = []
    for i in range(len(V2_x_folder)-1):
        u = u + gen([V2_x_folder[i], V2_y_folder[i]], [V2_x_folder[i+1], V2_y_folder[i+1]])
    print(u)
    V2_x_folder, V2_y_folder = u[::2], u[1::2]
    # U2 = u


    V1_x_folder, V1_y_folder = intersection(V1_x_folder, V1_y_folder, V2_x_folder, V2_y_folder)
    V2_x_folder, V2_y_folder = intersection(V2_x_folder, V2_y_folder, V1_x_folder, V1_y_folder)
    # U1 = u[:(len(V1_x_folder)*2)]
    # U2 = u[:(len(V2_x_folder)*2)]

    print("Проверка", V2_y_folder[-1])

    saver = [V1_x_folder, V1_y_folder, V2_x_folder, V2_y_folder]

    # angle = V1_x_folder[-2] - V1_x_folderх[-1], V1_y_folder[-2]

    crosig_entry.config(state=NORMAL)
    crosig_entry.delete(0, END)
    crosig_entry.insert(END, [V1_x_folder[-1], V1_y_folder[-1], angle([V1_x_folder[-2], V1_y_folder[-2]], [V2_x_folder[-2], V2_y_folder[-2]], [V1_x_folder[-1], V1_y_folder[-1]])])
    crosig_entry.config(state=DISABLED)

    area_limits = area(V1_x_folder[-1], V1_y_folder[-1])

    # fig = Figure(figsize=(6, 4), dpi=100)
    # ax = fig.add_subplot(111)
    plt.plot(V1_x_folder, V1_y_folder, color = first_plot.get(), label='Прямое отображение')
    plt.plot(V2_x_folder, V2_y_folder, color = second_plot.get(), label='Обратное отображение')
    plt.grid()
    plt.legend()
    # calbas = FigureCanvasTkAgg(fig, master = window_frame)
    # calbas.get_tk_widget().grid(column=0, row=0, columnspan=2)
    plt.draw()

def intersection_late(V1_x_folder, V1_y_folder, V2_x_folder, V2_y_folder):
    global area_limits
    first_list = list(zip(V1_x_folder,V1_y_folder))
    second_list = list(zip(V2_x_folder, V2_y_folder))
    for i in range(len(first_list)-1):
        for j in range(len(second_list)-1):
            saver = coef([first_list[i], first_list[i+1]], [second_list[j], second_list[j+1]])
            if saver != 0 and saver != None:
                if (area_limits[3] <= saver[1]) and (area_limits[1] <= float(saver[0])):
                    if (area_limits[2] >= saver[1]) and (area_limits[0] >= float(saver[0])):
                        V1_x_folder = V1_x_folder[:i+1] 
                        V1_x_folder.append(saver[0])
                        V1_y_folder = V1_y_folder[:i+1] 
                        V1_y_folder.append(saver[1])
                        return [V1_x_folder, V1_y_folder]    

def iter(V1_x_folder, V1_y_folder, V2_x_folder, V2_y_folder):
    # Связующие переменные
    global saver
    global num_iter
    # global calbas
    global crosig_entry

    num_iter = num_iter + 1


    # if calbas:
    #     calbas.get_tk_widget().destroy()

    #Объявляем символы
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    a = sp.Symbol('a')
    b = sp.Symbol('b')
    c = sp.Symbol('c')

    #Считываем точность и параметры
    a = eval(param_entry.get())
    b = eval(second_param_entry.get())
    c = eval(third_param_entry.get())
    h = eval(accuracy_entry.get())

    #Для первого вектора

    #X = x + y + a*x*(1-x)
    #Y = y + a*x*(1-x)


    V1_x_folder, V1_y_folder, V2_x_folder, V2_y_folder = saver[:4]
    #Считываем первое отображение
    X=eval(Firstpoint_equation_1.get())
    Y=eval(Firstpoint_equation_2.get())

    # for i in range(eval(iter_entry.get())):
    def gen(a, b):

    # Отобразили полученные не отображённые границы отрезков
    # Нужно для определения длинны отображённого отрезка
        x1 = X.subs({x: a[0], y: a[1]})
        y1 = Y.subs({x: a[0], y: a[1]})
        x2 = X.subs({x: b[0], y: b[1]})
        y2 = Y.subs({x: b[0], y: b[1]})

    # Проверка на точность
        if length([x1, y1], [x2, y2]) > h:
            return gen(a, [(a[0]+b[0])/2, (a[1]+b[1])/2])+gen([(a[0]+b[0])/2, (a[1]+b[1])/2], b)
        else:
            return [X.subs({x: a[0], y: a[1]}), Y.subs({x: a[0], y: a[1]})]

    # Для правильного подсчёта точки пересечения (см. далее)
    V1_len = len(V1_x_folder)
    V2_len = len(V2_x_folder)

    V1_x_new = []
    V1_y_new = []

    # Добавляем новую отображённую точку в массив
    for i in range(V1_len):
        V1_x_new.append(X.subs({x: V1_x_folder[i], y: V1_y_folder[i]}))
        V1_y_new.append(Y.subs({x: V1_x_folder[i], y: V1_y_folder[i]}))
        
    # Объединяем результаты работы рекурсивной функции и полученные ранее границы отрезков
    U1 = []
    for i in range(0, len(V1_x_new)-1):
        U1 = U1 + gen([V1_x_new[i], V1_y_new[i]], [V1_x_new[i+1], V1_y_new[i+1]])
    V1_x_new, V1_y_new = U1[0::2], U1[1::2]
        
        
    # Для второго вектора

    # Считываем второе отображение
    X=eval(Secondpoint_equation_1.get())
    Y=eval(Secondpoint_equation_2.get())

    #X = x - y
    #Y = y - a*(x-y)*(1-x+y)

    V2_x_new = []
    V2_y_new = []

    # Добавляем новую отображённую точку в массив
    for i in range(V2_len):
        V2_x_new.append(X.subs({x: V2_x_folder[i], y: V2_y_folder[i]}))
        V2_y_new.append(Y.subs({x: V2_x_folder[i], y: V2_y_folder[i]}))
        
    # Объединяем результаты работы рекурсивной функции и полученные ранее границы отрезков
    U2 = []
    for i in range(0, len(V2_x_new)-1):
        U2 = U2 + gen([V2_x_new[i], V2_y_new[i]], [V2_x_new[i+1], V2_y_new[i+1]])
    V2_x_new, V2_y_new = U2[0::2], U2[1::2]
        
    #Ищем точки пересечения для новых участков кривых
    #print(intersection_late(V1_x_new, V1_y_new, V2_x_new, V2_y_new))
    V1_x_folder_new, V1_y_folder_new = intersection_late(V1_x_new, V1_y_new, V2_x_new, V2_y_new)
    V2_x_folder_new, V2_y_folder_new = intersection_late(V2_x_new, V2_y_new, V1_x_new, V1_y_new)
        
    #Дополняем массивы координат новыми координатами
    # V1_x_folder = V1_x_folder_new
    # V2_x_folder = V2_x_folder_new
    # V1_y_folder = V1_y_folder_new
    # V2_y_folder = V2_y_folder_new
        
    #Сохраняем полученный результат и отображаем его
    saver = [V1_x_folder_new, V1_y_folder_new, V2_x_folder_new, V2_y_folder_new, V1_x_folder, V1_y_folder, V2_x_folder, V2_y_folder]
    
    crosig_entry.config(state=NORMAL)
    crosig_entry.delete(0, END)
    crosig_entry.insert(END, [V1_x_folder_new[-1], V1_y_folder_new[-1], angle([V1_x_folder[-2], V1_y_folder[-2]], [V2_x_folder[-2], V2_y_folder[-2]], [V1_x_folder[-1], V1_y_folder[-1]])])
    crosig_entry.config(state=DISABLED)

    plt.clf()
    # fig = Figure(figsize=(6, 4), dpi=100)
    # ax = fig.add_subplot(111)
    plt.plot(V1_x_folder_new, V1_y_folder_new, color = first_plot.get(), label='Прямое отображение')
    plt.plot(V2_x_folder_new, V2_y_folder_new, color = second_plot.get(), label='Обратное отображение')
    plt.grid()
    # calbas = FigureCanvasTkAgg(fig, master = window_frame)
    # calbas.get_tk_widget().grid(column=0, row=0, columnspan=2)
    plt.draw()

Entrope_entry = ttk.Entry(tool_bar, width=40)
Entrope_entry.config(state=DISABLED)
Entrope_entry.grid(column=0, row=9, columnspan=2)


def entropy():
    global saver
    global num_iter
    Entrope_entry.config(state=NORMAL)
    N1 = len(saver[4])
    N2 = len(saver[6])
    print(num_iter)
    Entrope_entry.delete(0, END)
    Entrope_entry.insert(END, [max(np.log(N1)/num_iter, np.log(N2)/num_iter)])
    Entrope_entry.config(state=DISABLED)
    print(np.log(N1)/num_iter, np.log(N2)/num_iter)

def ass():
    c = 0
    while c < eval(iter_entry.get()):
        iter(*saver[:4])
        c+=1

start_btn = ttk.Button(
    master = tool_bar, 
    text = 'Решить', 
    command = start, 

)
start_btn.grid(column=0, row=7)

iter_btn = ttk.Button(
    master = tool_bar, 
    text = 'Итерация', 
    command = ass, 

)
iter_btn.grid(column=1, row=7)

iter_btn = ttk.Button(
    master = tool_bar, 
    text = 'Энтропия для этой итерации', 
    command = entropy, 

)
iter_btn.grid(column=0, row=8, columnspan=2)

accuracy_label=ttk.Label(tool_bar, text="Введите точность:")
accuracy_label.grid(column=0, row=0, sticky=E)

accuracy_entry = ttk.Entry(tool_bar, width=17)
accuracy_entry.grid(column=1, row=0)
accuracy_entry.insert(END, '0.1')

param_label=ttk.Label(tool_bar, text="Введите параметр a:")
param_label.grid(column=0, row=1, sticky=E)

second_param_label=ttk.Label(tool_bar, text="Введите параметр b:")
second_param_label.grid(column=0, row=2, sticky=E)

third_param_label=ttk.Label(tool_bar, text="Введите параметр c:")
third_param_label.grid(column=0, row=3, sticky=E)

iter_label=ttk.Label(tool_bar, text="Введите кол-во итераций:")
iter_label.grid(column=0, row=4, sticky=E)

First_vector_label=ttk.Label(tool_bar_1, text="Первая точка")
First_vector_label.grid(column=0, row=0, columnspan=2)

Firstpoint_equation_1 = ttk.Entry(tool_bar_1, width=20)
Firstpoint_equation_1.grid(column=1, row=1)
Firstpoint_equation_1.insert(END, "x + y + a*x*(1-x)")

Firstpoint_equation_2 = ttk.Entry(tool_bar_1, width=20)
Firstpoint_equation_2.grid(column=1, row=2)
Firstpoint_equation_2.insert(END, "y + a*x*(1-x)")

First_point_x_label = ttk.Label(tool_bar_1, text="X:")
First_point_x_label.grid(column=0, row=4, sticky=E)

First_vector_entry_X = ttk.Entry(tool_bar_1, width=17)
First_vector_entry_X.grid(column=1, row=4, sticky=W)
First_vector_entry_X.insert(END, '((11**0.5)+1)/2')

First_point_y_label = ttk.Label(tool_bar_1, text="Y:")
First_point_y_label.grid(column=0, row=5, sticky=E)

First_vector_entry_Y = ttk.Entry(tool_bar_1, width=17)
First_vector_entry_Y.grid(column=1, row=5, sticky=W)
First_vector_entry_Y.insert(END, '1')



Second_vector_label=ttk.Label(tool_bar_2, text="Вторая точка")
Second_vector_label.grid(column=0, row=0, columnspan=2)

Secondpoint_equation_1 = ttk.Entry(tool_bar_2, width=20)
Secondpoint_equation_1.grid(column=1, row=1)
Secondpoint_equation_1.insert(END, "x - y")

Secondpoint_equation_2 = ttk.Entry(tool_bar_2, width=20)
Secondpoint_equation_2.grid(column=1, row=2)
Secondpoint_equation_2.insert(END, "y - a*(x-y)*(1-x+y)")

Second_point_x_label = ttk.Label(tool_bar_2, text="X:")
Second_point_x_label.grid(column=0, row=4, sticky=E)

Second_vector_entry_X = ttk.Entry(tool_bar_2, width=17)
Second_vector_entry_X.grid(column=1, row=4, sticky=W)
Second_vector_entry_X.insert(END, '((11**0.5)-1)/2')

Second_point_y_label = ttk.Label(tool_bar_2, text="Y:")
Second_point_y_label.grid(column=0, row=5, sticky=E)

Second_vector_entry_Y = ttk.Entry(tool_bar_2, width=17)
Second_vector_entry_Y.grid(column=1, row=5, sticky=W)
Second_vector_entry_Y.insert(END, '-1')

param_entry = ttk.Entry(tool_bar, width=17)
param_entry.grid(column=1, row=1)
param_entry.insert(END, '1.35')

second_param_entry = ttk.Entry(tool_bar, width=17)
second_param_entry.grid(column=1, row=2)
second_param_entry.insert(END, '0.7')

third_param_entry = ttk.Entry(tool_bar, width=17)
third_param_entry.grid(column=1, row=3)
third_param_entry.insert(END, '0.4')

iter_entry = ttk.Entry(tool_bar, width=17)
iter_entry.grid(column=1, row=4)
iter_entry.insert(END, '1')

first_plot = ttk.Combobox(
    tool_bar_1,
    width = 5,
    state="readonly",
    values=['red', 'blue', 'green', 'black', 'yellow', 'cyan', 'magenta']
)
first_plot.grid(column=0, row=6, columnspan=2)
first_plot.current(0)

second_plot = ttk.Combobox(
    tool_bar_2,
    width = 5,
    state="readonly",
    values=['red', 'blue', 'green', 'black', 'yellow', 'cyan', 'magenta']
)
second_plot.grid(column=0, row=6, columnspan=2)
second_plot.current(3)
'''
window.columnconfigure(0, minsize=500)
window.rowconfigure(0, minsize=200)
'''

window.mainloop()
