import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import RK as rk


if os.getcwd().endswith("ODU-solutions"):
    os.chdir("0_RK")


def insert_info_into_entry(entr: tk.Entry, info: str):
    entr.config(state='normal')
    entr.delete(0, tk.END)
    entr.insert(tk.END, info)
    entr.config(state='readonly')


def start_handler():
    try:
        if os.path.exists('res.png'):
            os.remove('res.png')
        alpha = eval(alpha_param_ctch.get())
        beta = eval(beta_param_ctch.get())
        omega = eval(omega_param_ctch.get())
        B = eval(b_param_ctch.get())
        k = eval(k_param_ctch.get())
        t0 = eval(t0_ctch.get())
        tmax = eval(tmax_ctch.get())
        x0 = eval(x0_ctch.get())
        y0 = eval(y0_ctch.get())
        h = eval(step_ctch.get())
        rk.main(t0, tmax, x0, y0, h, alpha, beta, omega, k, B)
        with open('buf.txt', 'r') as fd:
            elapsed_time = float(fd.readline())
        insert_info_into_entry(time_elapsed_entry, str(elapsed_time))
        img = Image.open("res.png")  # .resize((600,233))
        img_shower = tk.Label(image_frm)
        img_tk = ImageTk.PhotoImage(img)
        img_shower.image = img_tk
        img_shower.config(image=img_tk)
        img_shower.grid(row=0, column=0)
    except SyntaxError:
        messagebox.showinfo('Ошибка SyntaxError',
                            "Вы не ввели необходимые параметры или передали их неверно.")
    except ValueError:
        messagebox.showinfo('Ошибка ValueError',
                            "Вы ввели необходимые параметры неверно.")


def draw_handler():
    os.system("python3 drawer.py")


root = tk.Tk()
root.config(bg="#FFFFFF")
# root.geometry("600x450")
root.title("Runge-Kutta solution")


"""Отображение оглавления"""
tk.Label(root, text="Программа для решения уравнения\nметодом Рунге-Кутты",
         font=("Arial Bold", 12), bg="#FFFFFF").pack()

img_otobrazh_shower = tk.Label(root, bg="#FFFFFF")
img_otobr = Image.open("icons/uravnenie.png").resize((222, 25))
img_otobr_tk = ImageTk.PhotoImage(img_otobr)
img_otobrazh_shower.config(image=img_otobr_tk)
img_otobrazh_shower.pack()

params = tk.Frame(root, bg="#FFFFFF")
params.pack()

"""Ввод параметра k"""
tk.Label(params, text="k = ", bg="#FFFFFF").grid(row=0,
                                                 column=0,
                                                 sticky=tk.E)
k_param_ctch = tk.Entry(params, width=9)
k_param_ctch.insert(tk.END, '0.25')
k_param_ctch.grid(row=0,
                  column=1,
                  sticky=tk.W)

"""Ввод параметра alpha"""
tk.Label(params, text="α = ", bg="#FFFFFF").grid(row=0,
                                                 column=2,
                                                 sticky=tk.E)
alpha_param_ctch = tk.Entry(params, width=9)
alpha_param_ctch.insert(tk.END, '1')
alpha_param_ctch.grid(row=0,
                      column=3,
                      sticky=tk.W)

"""Ввод параметра B"""
tk.Label(params, text="B = ", bg="#FFFFFF").grid(row=1,
                                                 column=0,
                                                 sticky=tk.E)
b_param_ctch = tk.Entry(params, width=9)
b_param_ctch.insert(tk.END, '0.3')
b_param_ctch.grid(row=1,
                  column=1,
                  sticky=tk.W)

"""Ввод параметра beta"""
tk.Label(params, text="β = ", bg="#FFFFFF").grid(row=1,
                                                 column=2,
                                                 sticky=tk.E)
beta_param_ctch = tk.Entry(params, width=9)
beta_param_ctch.insert(tk.END, '-1')
beta_param_ctch.grid(row=1,
                     column=3,
                     sticky=tk.W)

"""Ввод параметра omega"""
tk.Label(params, text="ω = ", bg="#FFFFFF").grid(row=2,
                                                 column=0,
                                                 columnspan=2,
                                                 sticky=tk.E)
omega_param_ctch = tk.Entry(params, width=9)
omega_param_ctch.insert(tk.END, '1')
omega_param_ctch.grid(row=2,
                      column=2,
                      columnspan=2,
                      sticky=tk.W)

coord = tk.Frame(root, bg="#FFFFFF")
coord.pack()
"""Текст координат"""
tk.Label(coord, text="Координаты изначальной области",
         font=("Arial Bold", 10), bg="#FFFFFF").grid(row=0,
                                                     column=0,
                                                     columnspan=4)

"""Ввод координат"""
# t coords
tk.Label(coord, text="t0 ", bg="#FFFFFF").grid(row=1,
                                               column=0,
                                               sticky=tk.E)
t0_ctch = tk.Entry(coord, width=9)
t0_ctch.insert(tk.END, '0')
t0_ctch.grid(row=1,
             column=1,
             sticky=tk.W)

tk.Label(coord, text="t max ", bg="#FFFFFF").grid(row=1,
                                                  column=2,
                                                  sticky=tk.E)
tmax_ctch = tk.Entry(coord, width=9)
tmax_ctch.insert(tk.END, '20')
tmax_ctch.grid(row=1,
               column=3,
               sticky=tk.W)

# x0 coord
tk.Label(coord, text="x0 ", bg="#FFFFFF").grid(row=2,
                                               column=0,
                                               sticky=tk.E)
x0_ctch = tk.Entry(coord, width=9)
x0_ctch.insert(tk.END, '0.01')
x0_ctch.grid(row=2,
             column=1,
             sticky=tk.W)

# x'0 coord
tk.Label(coord, text="x'0 ", bg="#FFFFFF").grid(row=2,
                                                column=2,
                                                sticky=tk.E)
y0_ctch = tk.Entry(coord, width=9)
y0_ctch.insert(tk.END, '0.1')
y0_ctch.grid(row=2,
             column=3,
             sticky=tk.W)

other_params = tk.Frame(root, bg="#FFFFFF")
other_params.pack()
"""Ввод шага"""
tk.Label(other_params, text="Шаг (h): ", bg="#FFFFFF").grid(row=0,
                                                            column=0,
                                                            columnspan=2,
                                                            sticky=tk.E)
step_ctch = tk.Entry(other_params, width=9)
step_ctch.insert(tk.END, '0.1')
step_ctch.grid(row=0,
               column=2,
               columnspan=2,
               sticky=tk.W)

buttons_frm = tk.Frame(root, bg="#FFFFFF")
buttons_frm.pack()
"""Задание кнопки запуска"""
tk.Button(buttons_frm, text="Запуск программы",
          bg="black", fg="red", command=start_handler).grid(row=1,
                                                            column=1,
                                                            columnspan=2,
                                                            padx=5)

info_frm = tk.Frame(root, bg="#FFFFFF")
info_frm.pack()
"""Затраченное время"""
tk.Label(info_frm, text="Затраченное время (ms)",
         bg="#FFFFFF").grid(row=0,
                            column=0,
                            sticky=tk.E,
                            columnspan=2,
                            padx=4)
time_elapsed_entry = tk.Entry(info_frm, width=8, bg="#FFFFFF")
time_elapsed_entry.config(state='readonly')
time_elapsed_entry.grid(row=0,
                        column=2,
                        columnspan=2,
                        sticky=tk.W,
                        padx=4)

image_frm = tk.Frame(root, bg="#FFFFFF")
image_frm.pack()

root.mainloop()

if os.path.exists('buf.txt'):
    os.remove('buf.txt')
