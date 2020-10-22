'''
This function includes three separate definitions
1. automatic processing LOKI data

Created by : Dong-gyun KIM
Contact : kdk921219@gmail.com
Creation date : 02.07.2020
'''
from loki_gui import date_time_gui
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
from distutils.dir_util import copy_tree
import pandas as pd
import os
import numpy as np
from datetime import datetime
import re
import glob
import shutil
import string
from PIL import Image
import cv2


def copy_loki_folder ():
    '''
    This function siplify the steps of 
    1) Copy the original file and create copy
    '''

    # 1. copy and paste original project's whole directory
    Tk().withdraw()
    print('choose project directory')
    orig_dir_path = askdirectory() # open dialog browser
    wished_dir_path = input('same_directory[s]_or_new_directory[n]:') # if type 's', copied directory will saved to same dir of original otherwise new dir
    if wished_dir_path == 's':
        copy_dir_path = orig_dir_path+'_copy' # set copied directory
    elif wished_dir_path == 'n':
        print('choose new working directory')
        new_dir_path = askdirectory()
        copy_dir_path = new_dir_path+'_copy' # set copied directory

    Path(copy_dir_path).mkdir(exist_ok=True) # create copied directory

    if len(os.listdir(orig_dir_path)) == 1:
        print('copying and pasting files from orignal to copied folder ...')
        copy_tree(orig_dir_path, copy_dir_path)
        print('copying and pasting done')
    elif len(os.listdir(orig_dir_path)) >= 2:

        # create copoeid directory of original but only have haul 1
        i = 0
        for root, dirs, files, in os.walk(orig_dir_path):
            i += 1
            if i == 2:
                copied_root_path = os.path.join(copy_dir_path, root.split(os.sep)[-1])
                Path(copied_root_path).mkdir(exist_ok=True) # create Haul 1
                Path(os.path.join(copied_root_path, dirs[0])).mkdir(exist_ok=True) # create LOKI s/n folder under haul 1
            if i == 3:
                copied_root_path = os.path.join(copy_dir_path, root.split(os.sep)[-2], root.split(os.sep)[-1])
                for i in range(0, len(dirs)):
                    Path(os.path.join(copied_root_path, dirs[i])).mkdir(exist_ok=True)
            if root.split(os.sep)[-1] == 'Pictures':
                copied_root_path = os.path.join(copy_dir_path, 'Haul 1', root.split(os.sep)[-2], root.split(os.sep)[-1])
                for i in range(0, len(dirs)):
                    Path(os.path.join(copied_root_path, dirs[i])).mkdir(exist_ok=True)
        
        # move files
        print('copying and pasting files from orignal to copied folder and collapse to one Haul 1 ...')
        for root, dirs, files in os.walk(orig_dir_path):
            if root.split(os.sep)[-1] == 'Log':
                copied_root_path = os.path.join(copy_dir_path, 'Haul 1', root.split(os.sep)[-2], root.split(os.sep)[-1])
                for i in range(0, len(files)): 
                    shutil.copy2(os.path.join(root, files[i]), os.path.join(copied_root_path, files[i]))

            elif root.split(os.sep)[-1] == 'Telemetrie':
                copied_root_path = os.path.join(copy_dir_path, 'Haul 1', root.split(os.sep)[-2], root.split(os.sep)[-1])
                for i in range(0, len(files)):
                    shutil.copy2(os.path.join(root, files[i]), os.path.join(copied_root_path, files[i]))
            
            elif root.split(os.sep)[-2] == 'Pictures':
                copied_root_path = os.path.join(copy_dir_path, 'Haul 1',root.split(os.sep)[-3], root.split(os.sep)[-2], root.split(os.sep)[-1])
                for i in range(0, len(files)):
                    shutil.copy2(os.path.join(root, files[i]), os.path.join(copied_root_path, files[i]))
        print('copying and pasting done')
        
def split_loki_folder ():
    '''
    This function siplify the steps of
    1) Split the copied folder into several subfolder (folder count <4500)
    '''

    Tk().withdraw()
    print('choose copied project directory')
    copied_dir_path = askdirectory() # open dialog browser

    pic_dict = {} # create dictionary having key as picture directory and values as picture images
    for root, dirs, files in os.walk(copied_dir_path):
        if root.split(os.sep)[-2] == 'Pictures':
            if '._' not in files:
                pic_dict[root] = files

    if sum(len(v) for v in pic_dict.values()) < 5000:
        print('number of the images is %s. Split not necessary' % (sum(len(v) for v in pic_dict.values()),))
        return

    pic_dir_list = list(pic_dict.keys())
    # delete downcast and out-water images and following files (telemetrie)
    heaving_datetime, out_water_datetime = date_time_gui() # gui for heaving datetime and ourwater datetime
    print('deleting downcast and out water images ...')

    heaving_index = [i for i, s in enumerate(pic_dir_list) if heaving_datetime in s] # consider to apply next function
    out_water_index = [i for i, s in enumerate(pic_dir_list) if out_water_datetime in s]

    p = 0
    for pic_folder, pic_files in pic_dict.items():
        
        if not heaving_index[0] < p <= out_water_index[0]:
            print(pic_folder)
            shutil.rmtree(pic_folder)
        if p == out_water_index[0]:
            print('select the first image after out of the water')
            out_water_file = askopenfilename()

            out_water_file_index = [i for i, s in enumerate(pic_files) if out_water_file.split(os.sep)[-1] in s]
            for i in range(0, len(pic_files)):
                if i >= out_water_file_index[0]:
                    os.remove(os.path.join(pic_folder, pic_files[i]))
        p += 1
    
    # delete downcast and out-water telemetrie files
    print('deleting telemetrie ... ')
    deleted_pic_dict = {}
    telemetrie_dict = {}
    for root, dirs, files in os.walk(copied_dir_path):
        if root.split(os.sep)[-2] == 'Pictures':
            deleted_pic_dict[root] = files
        elif root.split(os.sep)[-1] == 'Telemetrie':
            telemetrie_dict[root] = files
    
    deleted_pic_files = list(deleted_pic_dict.values())
    begin_pic = deleted_pic_files[0][0].split(' ')
    end_pic = deleted_pic_files[-1][-1].split(' ')

    print(begin_pic, end_pic)
    print(list(telemetrie_dict.values())[0])
    telemetrie_begin_index = next(i for i, s in enumerate(list(telemetrie_dict.values())[0]) if str(begin_pic[0]+' '+begin_pic[1]) in s)
    telemetrie_end_index = next(i for i, s in enumerate(list(telemetrie_dict.values())[0]) if str(end_pic[0]+' '+end_pic[1]) in s) + 1

    t = 0
    for tel_folder, tel_files in telemetrie_dict.items():
        for i in range(0, len(tel_files)):
            if telemetrie_begin_index <= t <= telemetrie_end_index:
                pass
            else:
                os.remove(os.path.join(tel_folder, tel_files[t]))
            t += 1

    # creat split folder and copy and paste corresponding images
    print('creating splited folders ... ')
    pic_count = 0
    alphabet_count = 0
    alphabet_list = list(string.ascii_lowercase)
    split_dir_path = copied_dir_path.replace('_copy', alphabet_list[0])
    
    # create directories and move telemetrie and log files
    Path(split_dir_path).mkdir(exist_ok=True)
    for root, dirs, files, in os.walk(copied_dir_path):
        
        if  'Haul' in root.split(os.sep)[-1]:
            copied_root_path = os.path.join(split_dir_path, root.split(os.sep)[-1])
            Path(copied_root_path).mkdir(exist_ok=True) # create Haul 1
            Path(os.path.join(copied_root_path, dirs[0])).mkdir(exist_ok=True) # create LOKI s/n folder under haul 1
        elif 'Haul' in root.split(os.sep)[-2]:
            copied_root_path = os.path.join(split_dir_path, root.split(os.sep)[-2], root.split(os.sep)[-1])
            for i in range(0, len(dirs)):
                Path(os.path.join(copied_root_path, dirs[i])).mkdir(exist_ok=True) # create log, pictures, telemetrie dirs

        if root.split(os.sep)[-1] == 'Log': # move log file 
            copied_root_path = os.path.join(split_dir_path, root.split(os.sep)[-3], root.split(os.sep)[-2], root.split(os.sep)[-1])
            for i in range(0, len(files)): 
                shutil.copy2(os.path.join(root, files[i]), os.path.join(copied_root_path, files[i]))
               
        elif root.split(os.sep)[-1] == 'Telemetrie': # move telemetrie file
            copied_root_path = os.path.join(split_dir_path, root.split(os.sep)[-3], root.split(os.sep)[-2], root.split(os.sep)[-1])
            for i in range(0, len(files)):
                shutil.copy2(os.path.join(root, files[i]), os.path.join(copied_root_path, files[i]))
    

    # copy and paste pictures 
    for pic_folder, pic_files in deleted_pic_dict.items():
        pic_count += len(pic_files)
        print(pic_folder)
        if pic_count < 5000:
            # create picture subpic_folder
            split_root_path = os.path.join(split_dir_path, pic_folder.split(os.sep)[-4], pic_folder.split(os.sep)[-3], pic_folder.split(os.sep)[-2], pic_folder.split(os.sep)[-1])
            Path(split_root_path).mkdir(exist_ok=True)
            for i in range(0, len(pic_files)):
                shutil.copy2(os.path.join(pic_folder, pic_files[i]), os.path.join(split_root_path, pic_files[i])) # move to split pic_folder 
            
        elif pic_count > 5000:
            pic_count = len(pic_files)
            alphabet_count += 1

            split_dir_path = copied_dir_path.replace('_copy', alphabet_list[alphabet_count]) # create project sub pic_folder
            Path(split_dir_path).mkdir(exist_ok=True)
            for root, dirs, files, in os.walk(copied_dir_path):
                
                if  'Haul' in root.split(os.sep)[-1]:
                    copied_root_path = os.path.join(split_dir_path, root.split(os.sep)[-1])
                    Path(copied_root_path).mkdir(exist_ok=True) # create Haul 1
                    Path(os.path.join(copied_root_path, dirs[0])).mkdir(exist_ok=True) # create LOKI s/n pic_folder under haul 1
                elif 'Haul 1' in root.split(os.sep)[-2]:
                    copied_root_path = os.path.join(split_dir_path, root.split(os.sep)[-2], root.split(os.sep)[-1])
                    for i in range(0, len(dirs)):
                        Path(os.path.join(copied_root_path, dirs[i])).mkdir(exist_ok=True)

                if root.split(os.sep)[-1] == 'Log':
                    copied_root_path = os.path.join(split_dir_path, root.split(os.sep)[-3], root.split(os.sep)[-2], root.split(os.sep)[-1])
                    for i in range(0, len(files)): 
                        shutil.copy2(os.path.join(root, files[i]), os.path.join(copied_root_path, files[i]))

                elif root.split(os.sep)[-1] == 'Telemetrie':
                    copied_root_path = os.path.join(split_dir_path, root.split(os.sep)[-3], root.split(os.sep)[-2], root.split(os.sep)[-1])
                    for i in range(0, len(files)):
                        shutil.copy2(os.path.join(root, files[i]), os.path.join(copied_root_path, files[i]))
            
            # create picture subpic_folder
            split_root_path = os.path.join(split_dir_path, pic_folder.split(os.sep)[-4], pic_folder.split(os.sep)[-3], pic_folder.split(os.sep)[-2], pic_folder.split(os.sep)[-1])
            Path(split_root_path).mkdir(exist_ok=True)
            for i in range(0, len(pic_files)):
                shutil.copy2(os.path.join(pic_folder, pic_files[i]), os.path.join(split_root_path, pic_files[i])) # move to split folder

    print('spliting done')


def to_png_contrast():
    # choose folder exported from LOKI_Browser
    print('Choose the directory exported from LOKI Browser')
    Tk().withdraw()
    proj_dir = askdirectory()

    # create png directory
    png_dir_path = os.path.join(proj_dir, 'png')
    Path(png_dir_path).mkdir(exist_ok=True)

    # convert .bmp to .png and increase the contrast
    print('converting from .bmp to .png and enhacing the contrast')
    for bmp_file in glob.glob(str(proj_dir+os.sep+'*.bmp')):
        
        img = cv2.imread(bmp_file, cv2.IMREAD_GRAYSCALE) # reading in imagefile

        clahe = cv2.createCLAHE(clipLimit=3, tileGridSize=(5,5)) # enhacne the contrast
        img_enhanced = clahe.apply(img)

        cv2.imwrite(os.path.join(png_dir_path ,bmp_file.split(os.sep)[-1].replace('.bmp', '.png')) ,img_enhanced) # save bmp to png
