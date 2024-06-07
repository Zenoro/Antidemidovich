from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import draw as dro
from PIL import Image, ImageTk
import os


if os.getcwd().endswith("ODU-solutions"):
    os.chdir("8")


def insert_info_into_entry(entr: Entry, info: str):
    entr.config(state='normal')
    entr.delete(0, END)
    entr.insert(END, info)
    entr.config(state='readonly')


def start_handler():
    try:
        a = eval(a_param_ctch.get())
        b = eval(b_param_ctch.get())
        x_l = eval(x0_ctch.get())
        x_r = eval(x1_ctch.get())
        y_t = eval(y1_ctch.get())
        y_l = eval(y0_ctch.get())
        L = abs(x_r - x_l)
        H = abs(y_t - y_l)
        iter_num = int(combo.get())
        if not os.path.exists('a.out'):
            print("Compiling CPP code...", end='')
            os.system("g++ main(1).cpp")
            print("\tDone!")
        os.system(f"./a.out {x_l} {y_t} {L} {H} {a} {b} {iter_num}")
        with open("res.txt", "r") as fd:
            for line in fd:
                pass
            h, ctr, num_cells, comps, elapsed, lambd, entropy = map(float, line.split())
        insert_info_into_entry(h_entry, str(h))
        insert_info_into_entry(time_elapsed_entry, str(elapsed))
        insert_info_into_entry(cells_entry, f"{int(ctr)}/{int(num_cells)}")
        insert_info_into_entry(comps_entry, str(int(comps)))
        insert_info_into_entry(lambd_entry, str(lambd))
        insert_info_into_entry(entropy_entry, str(entropy))

    except SyntaxError:
        messagebox.showinfo('Ошибка SyntaxError',
                            "Вы не ввели необходимые параметры или передали их неверно.")
    except ValueError:
        messagebox.showinfo('Ошибка ValueError',
                            "Вы ввели необходимые параметры неверно.")


def draw_handler():
    if not os.path.exists("res.txt"):
        messagebox.showinfo('Ошибка ResNotFound',
                            "Файл с результатами не был найден\nПопробуйте запустить \
программу снова либо изменить директорию")
        return
    h = eval(h_entry.get())
    iterc = int(combo.get())
    dro.main("res.txt", h, iterc)


def iteration_handler():
    a = eval(a_param_ctch.get())
    b = eval(b_param_ctch.get())
    x_l = eval(x0_ctch.get())
    x_r = eval(x1_ctch.get())
    y_t = eval(y1_ctch.get())
    y_l = eval(y0_ctch.get())
    L = abs(x_r - x_l)
    H = abs(y_t - y_l)
    iter_num = int(combo.get()) + 1
    combo.delete(0, END)
    combo.insert(END, str(iter_num))
    os.system(f"./a.out {x_l} {y_t} {L} {H} {a} {b} {iter_num}")
    with open("res.txt", "r") as fd:
        for line in fd:
            pass
        h, ctr, num_cells, comps, elapsed = map(float, line.split())
    insert_info_into_entry(h_entry, str(h))
    insert_info_into_entry(time_elapsed_entry, str(elapsed))
    insert_info_into_entry(cells_entry, f"{ctr}/{num_cells}")
    insert_info_into_entry(comps_entry, str(comps))


root = Tk()
root.config(bg="#FFFFFF")
root.title("Вычислительная задача 8")
for i in range(12):
    root.columnconfigure(i, pad=4)
    root.rowconfigure(i, pad=4)

"""Отображение оглавления"""
Label(root,
      text="Построение меры максимальной энтропии \nдля отображения Жюлия",
      font=("Arial Bold", 12), bg="#FFFFFF").grid(row=0,
                                                  column=0,
                                                  columnspan=4)

"""Картинка отображения"""
img_otobrazh_shower = Label(root, bg="#FFFFFF")
img_otobr = Image.open("icons/otobrzhenie.png").resize((158, 55))
img_otobr_tk = ImageTk.PhotoImage(img_otobr)
img_otobrazh_shower.config(image=img_otobr_tk)
img_otobrazh_shower.grid(row=1, column=0, columnspan=6)

"""Ввод параметра A"""
Label(root, text="a = ", bg="#FFFFFF").grid(row=2,
                                            column=0,
                                            sticky=E)
a_param_ctch = Entry(root,
                     width=9)
a_param_ctch.insert(END, '0.0')
a_param_ctch.grid(row=2,
                  column=1,
                  sticky=W)

"""Ввод параметра B"""
Label(root, text="b = ", bg="#FFFFFF").grid(row=2,
                                            column=2,
                                            sticky=E)
b_param_ctch = Entry(root,
                     width=9)
b_param_ctch.insert(END, '-0.6')
b_param_ctch.grid(row=2,
                  column=3,
                  sticky=W)

"""Текст координат"""
Label(root, text="Координаты изначальной области",
      font=("Arial Bold", 10),
      bg="#FFFFFF").grid(row=3, column=0,
                         columnspan=4)

"""Ввод координат"""
# x coords
Label(root, text="x0 ", bg="#FFFFFF").grid(row=4,
                                           column=0,
                                           sticky=E)
x0_ctch = Entry(root,
                width=9)
x0_ctch.insert(END, '-2')
x0_ctch.grid(row=4,
             column=1,
             sticky=W)

Label(root, text="x1 ", bg="#FFFFFF").grid(row=4,
                                           column=2,
                                           sticky=E)
x1_ctch = Entry(root,
                width=9)
x1_ctch.insert(END, '2')
x1_ctch.grid(row=4,
             column=3,
             sticky=W)

# y coords
Label(root, text="y0 ", bg="#FFFFFF").grid(row=5,
                                           column=0,
                                           sticky=E)
y0_ctch = Entry(root,
                width=9)
y0_ctch.insert(END, '-2')
y0_ctch.grid(row=5,
             column=1,
             sticky=W)

Label(root, text="y0 ", bg="#FFFFFF").grid(row=5,
                                           column=2,
                                           sticky=E)
y1_ctch = Entry(root,
                width=9)
y1_ctch.insert(END, '2')
y1_ctch.grid(row=5,
             column=3,
             sticky=W)

"""Выбор количества итераций"""
Label(root, text="Количество итераций",
      bg="#FFFFFF").grid(row=6,
                         column=0,
                         columnspan=2,
                         sticky=E)

combo = Combobox(root)
combo['values'] = list(range(5, 15))
combo.current(3)
combo.grid(row=6, column=2,
           columnspan=2,
           sticky=W)

"""Задание кнопки запуска"""
Button(root, text="Построить решение",
       bg="green", fg="black",
       command=draw_handler).grid(row=7,
                                  column=0,
                                  pady=16)

Button(root, text="Запуск программы",
       bg="black", fg="red",
       command=start_handler).grid(row=7,
                                   column=1,
                                   columnspan=2,
                                   pady=16)

Button(root, text="Следующая итерация",
       bg="purple", fg="blue",
       command=iteration_handler).grid(row=7,
                                       column=3,
                                       pady=16)

"""Полученный шаг"""
Label(root, text="Диаметр ячейки",
      bg="#FFFFFF").grid(row=8,
                         column=0,
                         sticky=E,
                         columnspan=2,
                         padx=4, pady=1)
h_entry = Entry(root, width=10, bg="#FFFFFF")
h_entry.config(state='readonly')
h_entry.grid(row=8, column=2,
             columnspan=2, sticky=W,
             padx=4, pady=1)

"""Затраченное время"""
Label(root, text="Затраченное время (s)",
      bg="#FFFFFF").grid(row=9,
                         column=0,
                         sticky=E,
                         columnspan=2,
                         padx=4, pady=1)
time_elapsed_entry = Entry(root, width=10, bg="#FFFFFF")
time_elapsed_entry.config(state='readonly')
time_elapsed_entry.grid(row=9,
                        column=2,
                        columnspan=2,
                        sticky=W,
                        padx=4, pady=1)

"""Количество ячеек"""
Label(root, text="Количество ячеек",
      bg="#FFFFFF").grid(row=10,
                         column=0,
                         sticky=E,
                         columnspan=2,
                         padx=4, pady=1)
cells_entry = Entry(root, width=20, bg="#FFFFFF")
cells_entry.config(state='readonly')
cells_entry.grid(row=10, column=2,
                 columnspan=2,
                 sticky=W,
                 padx=4, pady=1)

"""Компонент сильной связности"""
Label(root, text="Компонент сильной связности",
      bg="#FFFFFF").grid(row=11,
                         column=0,
                         sticky=E,
                         columnspan=2,
                         padx=4, pady=1)
comps_entry = Entry(root, width=10, bg="#FFFFFF")
comps_entry.config(state='readonly')
comps_entry.grid(row=11, column=2,
                 columnspan=2,
                 sticky=W,
                 padx=4, pady=1)

"""Лямбда вставка"""
Label(root, text="Значение ln(lambda)", bg="#FFFFFF").grid(row=12,
                                                           column=0,
                                                           sticky=E,
                                                           columnspan=2,
                                                           padx=4, pady=2)
lambd_entry = Entry(root, width=10, bg="#FFFFFF")
lambd_entry.config(state="readonly")
lambd_entry.grid(row=12, column=2, columnspan=2,
                 sticky=W,
                 padx=4, pady=2)

"""Вставка меры"""
Label(root, text="Энтропия", bg="#FFFFFF").grid(row=13,
                                                column=0,
                                                sticky=E,
                                                columnspan=2,
                                                padx=4, pady=2)
entropy_entry = Entry(root, width=10, bg="#FFFFFF")
entropy_entry.config(state="readonly")
entropy_entry.grid(row=13, column=2, columnspan=2,
                   sticky=W,
                   padx=4, pady=2)

root.mainloop()

if os.path.exists("res.txt"):
    os.remove("res.txt")
