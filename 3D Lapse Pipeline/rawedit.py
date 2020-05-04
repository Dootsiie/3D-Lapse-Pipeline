#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 14:22:52 2019

@author: Lotta Vaskimo
"""
"""
This module corrects dimensions of every reconstruction for it to be
used in the 3-D time lapse pipeline.
"""
import os
from shutil import copy2

            
def folder_control(path):
    """
    Running through the individual reconstrucion folder, checking whether
    unnecessary files (like previews) can be removed.
    Also, the mandatory geometry.toml file will me placed in the folder,
    in order for the timelapce.py script to work.
    The number of images in the reconstrucion folder will be calculated
    
    Parameters:
        path      The pathway to the reconstruction folder
    
    Returns:
        penalty   How many files in the reconstruction folder are not 
                  reconstructory images
        geometry  Boolean, whether the geometry files exists in the current 
                  working folder
        result    Boolean, whether the result folder exists in the current
                  working folder
    """
    penalty = 0
    geometry = False
    result = False
    log = False
    
    for fname in os.listdir(path):
        if "pp" in fname or 'spr.' in fname:
            # Deleting unecessary files
            os.remove(os.path.join(path, fname))
        if ".log" in fname and log == False:
            # Checking and renaming .log files
            name = fname[1:]
            newname = "e" + name
            penalty += 1
            print('Log file exists named as', fname, 'in the current reconstruction folder')
            log = True
            os.rename(os.path.join(path, fname), os.path.join(path, newname))
        if "result" == fname and result == False:
            # Checking whether the results folder already exists, in this case it will be overwritten
            print("Result folder already exists! This folder's contents will be overwritten...")
            result = True
            #penalty += 1
    if  os.path.exists(path+"geometry.toml"):
        print('Geometry file exists!')
        geometry=True
        penalty += 1
            
    return penalty, geometry, result


def dimension_resize(max_size, geometry, penalty, result, path):
    """
    Copies the geometry.toml file into the folder, if this is missing from the
    current working folder.
    If the current reconstruction folder contains too many images, in conmparison
    to the max size estimated in __main__, the correct amount of images shall
    be removed from the top, with exclusion from special files and folders like
    'results', 'geometry.toml' and the log file.
    In any other case, no deletory actions shall be taken
    
    Parameters:
        max_size       Maximum number of images allowed in the reconstruction
                       folder
        geometry       Boolean, whether the geometry files exists in the current 
                       working folder
        penalty        How many files in the reconstruction folder are not 
                       reconstructory images
        result         Boolean, whether the result folder exists in the current
                       working folder
        path           The pathway to the reconstruction folder
    """
    if geometry == False:
        copy2('./Geometry/geometry.toml', path)
        penalty += 1
        print('Geometryfile absent, this file shall be added to the folder in question.')
    num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
    files = num_files - penalty
    print('\nThe penalty is:', penalty, 'and shall be substracted from the total number of files to estimate correct object dimensions')
    print("\nThis reconstruction currently contains", files, "images")
    if files > max_size:
        # Check whether there is too many images
        print('This reconstruction contains too many images, the dimensions shall be matched correctly')
        difference = files - max_size
        images = os.listdir(path)
        print(difference, 'image(s) shall be removed from the top to match the dimension requirements')
        # Calculating how many images should be removed, and from where to trim
        if result == True:
            start=-3
            stop = start-(difference)
            #print(start)
        else:
            start=-2
            stop = start-(difference)
        if difference > 0:
            for y in images[::-1]:
                #print("y is",y)
                if "Erycina" in y:
                    # Removing images 
                    print(y, "shall be removed in order to continue")
                    difference-=1
                    os.remove(os.path.join(path, y))
                if difference == 0:
                    break
        num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
        files = num_files - penalty
        # Checking whether the reconstruction does have the correct dimensions now
        if files > max_size:
            print('The reconstruction still contains too many images')
        elif files < max_size:
            print('The reconstructions contains too little images')
        elif files == max_size:
            print('The reconstruction contains the right amount of images to proceed')
    elif files < max_size:
        print('This reconstruction contains too little images, the pipeline will exit. Make sure your reconstructions are of equal lenght',
              'or lower the maximum dimension size.')
        exit
    else:
        print('\nThis reconstruction has the correct dimensions, no further actions shall be taken\n\n')
        

if __name__ == "__main__":
    # Input pathway from SnakeFile, still hardcoded to check how many max images there should be
    path = snakemake.input.a
    max_size = 100000
    '''
    if "Jong" in path: 
        max_size = 2000
    elif "Volwassen" in path:
        max_size = 3920
    elif "Marked" in path:
        max_size= 4125
    '''
    file = path.split('/')[:-1]
    print(file)
    directory = '/'.join(file)
    print(directory)
    choice = '0'
    
    for x in os.listdir(directory):
        size = len(os.listdir(directory+'/'+x))
        if size < max_size:
            max_size = size
            if max_size < 2000:
                print('Reconstruction', x, 'has a dangerously low number of images, this may cause the trimming of importan parts of the scan.')
                while choice != 'yes' and choice != 'no':
                    choice = input('Do you wish to continue anywway? (yes/no)')
                    if choice == 'yes':
                        pass
                    elif choice == 'no':
                        print('The pipeline will now exit, please check the reconstruction in question and try again.')
                        exit()       
    print(max_size)  
    print("\n\n------------------------------------------------------------------------------------------")
    print('New folder opened, from: ', path, '\n')
    penalty, geometry, result = folder_control(path)
    dimension_resize(max_size, geometry, penalty, result, path)
