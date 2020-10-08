# test GUI

import tkinter as tk
from tkinter import ttk
from data_prep_func import *
from data_export_func import *

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