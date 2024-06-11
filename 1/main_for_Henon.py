import numpy as np
from matplotlib import pyplot as plt
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from ttkthemes import ThemedTk
from matplotlib.figure import Figure

area_limits = []
saver = []
num_iter = 0


#   Интерфейс

window = Tk()
window.resizable(True, True)
#ttk.Style(window).theme_use('black')

window.title('Нахождение гомоклинических точек')

window_frame = ttk.Frame(window)
window_frame.pack(fill=BOTH, expand=True)

tool_bar_1 = ttk.Frame(window_frame)
tool_bar_1.grid(column=0, row=1, columnspan=2)

tool_bar = ttk.Frame(window_frame)
tool_bar.grid(column=0, row=2, columnspan=2, )


def length(a, b):
        [x1, y1], [x2, y2] = a, b
        return (((x1-x2)**2)+((y1-y2)**2))**0.5

def subs(val1, val2, equation):
    global a
    global b

    x = val1
    y = val2
    return eval(equation)

def start():
    plt.ion()
    # Условие

    #X = x + y + a*x*(1-x)
    #Y = y + a*x*(1-x)

    # Ручной ввод
    global saver
    global num_iter
    # global calbas
    global window_frame

    iter = 0

    V1 = [eval(Vector_end_entry_X.get()), eval(Vector_end_entry_Y.get())]
    V0 = [eval(Vector_begin_entry_X.get()), eval(Vector_begin_entry_Y.get())]

    # Длинна отрезка

    def gen(a, b):

    # Отобразили полученные не отображённые границы отрезков
    # Нужно для определения длинны отрезка

        x1 = subs(a[0], a[1], X)
        y1 = subs(a[0], a[1], Y)
        x2 = subs(b[0], b[1], X)
        y2 = subs(b[0], b[1], Y)

        # Проверка на точность

        if length([x1, y1], [x2, y2]) > h:
            return gen(a, [(a[0]+b[0])/2, (a[1]+b[1])/2])+gen([(a[0]+b[0])/2, (a[1]+b[1])/2], b)
        else:
            return [subs(a[0],a[1], X), subs(a[0], a[1], Y)]


    # Для V1

    V1_x_folder = [eval(Vector_begin_entry_X.get()), V1[0], subs(V1[0], V1[1], X)]
    V1_y_folder = [eval(Vector_begin_entry_Y.get()), V1[1], subs(V1[0], V1[1], Y)]


    # Проверили содержание массивов

    # print(V1_x_folder)
    # print(V1_y_folder)

    # Объединяем результаты работы рекурсивной функции и полученные ранее границы отрезков

    u = []
    for i in range(len(V1_x_folder)-1):
        u = u + gen([V1_x_folder[i], V1_y_folder[i]], [V1_x_folder[i+1], V1_y_folder[i+1]])
    # print(u)
    V1_x_folder, V1_y_folder = u[::2], u[1::2]
    # U1 = u
    # Для V2

    saver = [V1_x_folder, V1_y_folder]

    # fig = Figure(figsize=(6, 4), dpi=100)
    # ax = fig.add_subplot(111)
    plt.plot(V1_x_folder, V1_y_folder, color = 'red', label='Прямое отображение')
    plt.grid()
    plt.legend()
    # calbas = FigureCanvasTkAgg(fig, master = window_frame)
    # calbas.get_tk_widget().grid(column=0, row=0, columnspan=2)
    plt.draw()

def iter(V1_x_folder, V1_y_folder):
    # Связующие переменные
    global saver
    global num_iter
    # global calbas

    num_iter = num_iter + 1

    # if calbas:
    #     calbas.get_tk_widget().destroy()


    #Для первого вектора

    #X = x + y + a*x*(1-x)
    #Y = y + a*x*(1-x)

    # for i in range(eval(iter_entry.get())):
    def gen(a, b):

        # Отобразили полученные не отображённые границы отрезков
        # Нужно для определения длинны отрезка

            x1 = subs(a[0], a[1], X)
            y1 = subs(a[0], a[1], Y)
            x2 = subs(b[0], b[1], X)
            y2 = subs(b[0], b[1], Y)

            # Проверка на точность

            if length([x1, y1], [x2, y2]) > h:
                return gen(a, [(a[0]+b[0])/2, (a[1]+b[1])/2])+gen([(a[0]+b[0])/2, (a[1]+b[1])/2], b)
            else:
                return [subs(a[0],a[1], X), subs(a[0], a[1], Y)]
            
    # Для правильного подсчёта точки пересечения (см. далее)
    V1_len = len(V1_x_folder)

    V1_x_new = []
    V1_y_new = []

    # Добавляем новую отображённую точку в массив
    for i in range(V1_len):
        V1_x_new.append(subs(V1_x_folder[i], V1_y_folder[i], X))
        V1_y_new.append(subs(V1_x_folder[i], V1_y_folder[i], Y))
        
    # Объединяем результаты работы рекурсивной функции и полученные ранее границы отрезков
    U1 = []
    for i in range(0, len(V1_x_new)-1):
        U1 = U1 + gen([V1_x_new[i], V1_y_new[i]], [V1_x_new[i+1], V1_y_new[i+1]])
    V1_x_new, V1_y_new = U1[0::2], U1[1::2]
        
    
    #Сохраняем полученный результат и отображаем его
    saver = [V1_x_new, V1_y_new]

    plt.clf()
    # fig = Figure(figsize=(6, 4), dpi=100)
    # ax = fig.add_subplot(111)
    plt.plot(V1_x_new, V1_y_new, color = "red", label='Прямое отображение')
    plt.grid()
    # calbas = FigureCanvasTkAgg(fig, master = window_frame)
    # calbas.get_tk_widget().grid(column=0, row=0, columnspan=2)
    plt.draw()


Entrope_entry_txt = ttk.Label(tool_bar, text="Энтропия: ")
Entrope_entry_txt.grid(column=0, row=9, sticky=W, padx=8, pady=8)
Entrope_entry = ttk.Entry(tool_bar, width=40)
Entrope_entry.config(state=DISABLED)
Entrope_entry.grid(column=1, row=9, padx=8, pady=8)


def entropy():
    global saver
    global num_iter
    Entrope_entry.config(state=NORMAL)
    N1 = len(saver[0])

    # print(num_iter)
    Entrope_entry.delete(0, END)
    Entrope_entry.insert(END, np.log(N1)/num_iter)
    Entrope_entry.config(state=DISABLED)

def ass():
    c = 0
    while c < eval(iter_entry.get()):
        iter(*saver[:2])
        c+=1

start_btn = ttk.Button(
    master = tool_bar, 
    text = 'Решить', 
    command = start, 

)
start_btn.grid(column=0, row=7, padx=8, pady=8)

iter_btn = ttk.Button(
    master = tool_bar, 
    text = 'Итерация', 
    command = ass, 

)
iter_btn.grid(column=1, row=7, padx=8, pady=8)

iter_btn = ttk.Button(
    master = tool_bar, 
    text = 'Посчитать энтропию', 
    command = entropy, 

)
iter_btn.grid(column=0, row=8, columnspan=2, padx=8, pady=8)

accuracy_label=ttk.Label(tool_bar, text="Точность (h): ")
# accuracy_label.config(font=("Courier", 20))
accuracy_label.grid(column=0, row=2, sticky=E, padx=8, pady=8)

accuracy_entry = ttk.Entry(tool_bar, width=17)
# accuracy_entry.config(font=("Courier", 20))
accuracy_entry.grid(column=1, row=2, padx=8, pady=8)
accuracy_entry.insert(END, '0.1')

param_label=ttk.Label(tool_bar, text="Параметр A:")
# param_label.config(font=("Courier", 20))
param_label.grid(column=0, row=0, sticky=E, padx=8, pady=8)

second_param_label=ttk.Label(tool_bar, text="Параметр B:")
# second_param_label.config(font=("Courier", 20))
second_param_label.grid(column=0, row=1, sticky=E, padx=8, pady=8)

iter_label=ttk.Label(tool_bar, text="Кол-во итераций:")
# iter_label.config(font=("Courier", 20))
iter_label.grid(column=0, row=3, sticky=E, padx=8, pady=8)

First_vector_label=ttk.Label(tool_bar_1, text="Отображение Хенона")
# First_vector_label.config(font=("Courier", 20))
First_vector_label.grid(column=0, row=0, columnspan=4, padx=8, pady=8)

canvas = Canvas(tool_bar_1,
                        height=110,
                        width=350,
                        bg="#FFFFFF")
img = PhotoImage(file='/home/zenoro/SOme-Kodes/Homoclinic_tangle/henon.png', width=150, height=70)
image = canvas.create_image(0, 0, anchor='nw', image=img)
canvas.grid(row=1,
            column=0,
            columnspan=4, padx=8, pady=8)

End_point_x_label = ttk.Label(tool_bar_1, text="X₂:")
# End_point_x_label.config(font=("Courier", 20))
End_point_x_label.grid(column=2, row=2, sticky=E, padx=8, pady=8)

Vector_end_entry_X = ttk.Entry(tool_bar_1, width=17)
# Vector_end_entry_X.config(font=("Courier", 20))
Vector_end_entry_X.grid(column=3, row=2, sticky=W, padx=8, pady=8)
Vector_end_entry_X.insert(END, '1')

End_point_y_label = ttk.Label(tool_bar_1, text="Y₂:")
# End_point_y_label.config(font=("Courier", 20))
End_point_y_label.grid(column=2, row=3, sticky=E, padx=8, pady=8)

Vector_end_entry_Y = ttk.Entry(tool_bar_1, width=17)
# Vector_end_entry_Y.config(font=("Courier", 20))
Vector_end_entry_Y.grid(column=3, row=3, sticky=W, padx=8, pady=8)
Vector_end_entry_Y.insert(END, '1')


End_point_x_label = ttk.Label(tool_bar_1, text="X₁:")
# End_point_x_label.config(font=("Courier", 20))
End_point_x_label.grid(column=0, row=2, sticky=E, padx=8, pady=8)

Vector_begin_entry_X = ttk.Entry(tool_bar_1, width=17)
# Vector_begin_entry_X.config(font=("Courier", 20))
Vector_begin_entry_X.grid(column=1, row=2, sticky=W, padx=8, pady=8)
Vector_begin_entry_X.insert(END, '0')

End_point_y_label = ttk.Label(tool_bar_1, text="Y₁:")
# End_point_y_label.config(font=("Courier", 20))
End_point_y_label.grid(column=0, row=3, sticky=E, padx=8, pady=8)

Vector_begin_entry_Y = ttk.Entry(tool_bar_1, width=17)
# Vector_begin_entry_Y.config(font=("Courier", 20))
Vector_begin_entry_Y.grid(column=1, row=3, sticky=W, padx=8, pady=8)
Vector_begin_entry_Y.insert(END, '0')

param_entry = ttk.Entry(tool_bar, width=17)
# param_entry.config(font=("Courier", 20))
param_entry.grid(column=1, row=0)
param_entry.insert(END, '1.4')

second_param_entry = ttk.Entry(tool_bar, width=17)
# second_param_entry.config(font=("Courier", 20))
second_param_entry.grid(column=1, row=1, padx=8, pady=8)
second_param_entry.insert(END, '0.3')

iter_entry = ttk.Entry(tool_bar, width=17)
# iter_entry.config(font=("Courier", 20))
iter_entry.grid(column=1, row=3, padx=8, pady=8)
iter_entry.insert(END, '1')

a = eval(param_entry.get())
b = eval(second_param_entry.get())
h = eval(accuracy_entry.get())


Firstpoint_equation_1 = ttk.Entry(tool_bar_1, width=20)
Firstpoint_equation_1.insert(END, "1+y-a*x*x")

Firstpoint_equation_2 = ttk.Entry(tool_bar_1, width=20)
Firstpoint_equation_2.insert(END, "b*x")

X=Firstpoint_equation_1.get()
Y=Firstpoint_equation_2.get()


window.mainloop()
