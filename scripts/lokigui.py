'''
script for loki gui
includes function to handle pre-, post- processing of loki and zoomie processing

created by: Dong-gyun Kim

'''
import tkinter as tk
from tkinter import ttk
from data_prep_func import *
from data_export_func import *

def date_time_gui ():
    win = tk.Tk()
    win.title('LOKI powered by Python') # win title
    win.geometry('700x400') # size of win

    # add label on the win
    label = tk.Label(win, 
        text='type the heaving datetime and out water datetime',
        font = ('Arial Bold',25)
        )
    label.place(relx = 0.5, rely = 0.05, anchor = 'n')

    # label and entry for heaving datetime
    heaving_label = tk.Label(win,
        text='type heaving datetime',
        font = ('Arial Bold', 15)
        )
    heaving_label.place(relx = 0.1, rely = 0.3, anchor = 'w')

    h_year_label = tk.Label(win, text='YEAR (4 digits) :')
    h_year_label.place(relx = 0.1, rely = 0.4, anchor = 'w')
    h_year = tk.Entry(win, fg='black', width = 5)
    h_year.place(relx = 0.3, rely = 0.4, anchor = 'w')


    h_month_label = tk.Label(win, text='MONTH (2 digits) :')
    h_month_label.place(relx = 0.1, rely = 0.5, anchor = 'w')
    h_month = tk.Entry(win, fg='black', width = 5)
    h_month.place(relx = 0.3, rely = 0.5, anchor = 'w')


    h_date_label = tk.Label(win, text='DATE (2 digits) :')
    h_date_label.place(relx = 0.1, rely = 0.6, anchor = 'w')
    h_date = tk.Entry(win, fg='black', width = 5)
    h_date.place(relx = 0.3, rely = 0.6, anchor = 'w')


    h_hour_label = tk.Label(win, text='HOUR (24h, 2 digits) :')
    h_hour_label.place(relx = 0.1, rely = 0.7, anchor = 'w')
    h_hour = tk.Entry(win, fg='black', width = 5)
    h_hour.place(relx = 0.3, rely = 0.7, anchor = 'w')

    h_minute_label = tk.Label(win, text='MINUTE (2 digits) :')
    h_minute_label.place(relx = 0.1, rely = 0.8, anchor = 'w')
    h_minute = tk.Entry(win, fg='black', width = 5)
    h_minute.place(relx = 0.3, rely = 0.8, anchor = 'w')



    # label and entry for out water datetime
    outwater_label = tk.Label(win,
        text='type out water datetime',
        font = ('Arial Bold', 15)
        )
    outwater_label.place(relx = 0.5, rely = 0.3, anchor = 'w')

    o_year_label = tk.Label(win, text='YEAR (4 digits) :')
    o_year_label.place(relx = 0.5, rely = 0.4, anchor = 'w')
    o_year = tk.Entry(win, fg='black', width = 5)
    o_year.place(relx = 0.7, rely = 0.4, anchor = 'w')


    o_month_label = tk.Label(win, text='MONTH (2 digits) :')
    o_month_label.place(relx = 0.5, rely = 0.5, anchor = 'w')
    o_month = tk.Entry(win, fg='black', width = 5)
    o_month.place(relx = 0.7, rely = 0.5, anchor = 'w')


    o_date_label = tk.Label(win, text='DATE (2 digits) :')
    o_date_label.place(relx = 0.5, rely = 0.6, anchor = 'w')
    o_date = tk.Entry(win, fg='black', width = 5)
    o_date.place(relx = 0.7, rely = 0.6, anchor = 'w')


    o_hour_label = tk.Label(win, text='HOUR (24h, 2 digits) :')
    o_hour_label.place(relx = 0.5, rely = 0.7, anchor = 'w')
    o_hour = tk.Entry(win, fg='black', width = 5)
    o_hour.place(relx = 0.7, rely = 0.7, anchor = 'w')

    o_minute_label = tk.Label(win, text='MINUTE (2 digits) :')
    o_minute_label.place(relx = 0.5, rely = 0.8, anchor = 'w')
    o_minute = tk.Entry(win, fg='black', width = 5)
    o_minute.place(relx = 0.7, rely = 0.8, anchor = 'w')

    def run_func ():
        global heaving
        global outwater
        heaving = h_year.get()+'.'+h_month.get()+'.'+h_date.get()+' '+h_hour.get()+' '+h_minute.get()
        outwater = o_year.get()+'.'+o_month.get()+'.'+o_date.get()+' '+o_hour.get()+' '+o_minute.get()
        win.destroy()
        win.quit()

    button = ttk.Button(win, text = 'run', command = run_func)  
    button.place(relx = 0.8, rely = 0.9, anchor = 'w')
    win.mainloop()
    return heaving, outwater


def main_loki_gui():
    window = tk.Tk()
    window.title('LOKI powered by Python') # window title
    window.geometry('700x400') # size of window

    # add label on the window
    label = tk.Label(window, 
        text='Choose (a) function(s) to run the script',
        font = ('Arial Bold',30)
        )
    label.place(relx = 0.5, rely = 0.05, anchor = 'n')

    # add User input box
    #entry = tk.Entry(window, fg='Yellow')

    # add button on the window
    var1 = tk.BooleanVar()
    button1 = ttk.Checkbutton(window, var=var1, text='copy_loki_folder : copy original LOKI project')
    button1.place(relx = 0.2, rely = 0.3, anchor = 'w')

    var2 = tk.BooleanVar()
    button2 = ttk.Checkbutton(window, var=var2, text='split_loki_folder : split copied folder for LOKI browser')
    button2.place(relx = 0.2, rely = 0.4, anchor = 'w')

    var3 = tk.BooleanVar()
    button3 = ttk.Checkbutton(window, var=var3, text='Browser_to_Zoomie : LOKI browser export.txt to Zoomie.csv')
    button3.place(relx = 0.2, rely = 0.5, anchor = 'w')

    var4 = tk.BooleanVar()
    button4 = ttk.Checkbutton(window, var=var4, text='to_png_contrast : convert bmp to png and enhance contrast')
    button4.place(relx = 0.2, rely = 0.6, anchor = 'w')

    var5 = tk.BooleanVar()
    button5 = ttk.Checkbutton(window, var=var5, text='Zommie_to_EcoTaxa : zommie.csv to ecotaxa.txt')
    button5.place(relx = 0.2, rely = 0.7, anchor = 'w')


    # create run button and function to run the ticked funtion
    def run_func():
        window.destroy() # quit GUI
        if var1.get()==True:
            print('copy_loki_folder')
            copy_loki_folder()
        if var2.get()==True:
            print('split_loki_folder')
            split_loki_folder()
        if var3.get()==True:
            print('Browser_to_Zoomie')
            Browser_to_Zoomie()
        if var4.get()==True:
            print('to_png_contrast')
            to_png_contrast()
        if var5.get()==True:
            print('Zoomie_to_Ecotaxa')
            Zoomie_to_Ecotaxa()
        quit()

    button5 = ttk.Button(window, text = 'run', command = run_func)
    button5.place(relx = 0.8, rely = 0.8, anchor = 'n')

    window.mainloop() # pop up widget

if __name__ == "__main__":
    main_loki_gui()