# -*- coding: utf-8 -*- 
"""
Example of batch processing. 
There are three parts in this example: scheduling and runtime of input operations, scheduling and runtime of reconstruction and restoration and restart of a crashed process.

@author: alex

Several changes made by Lotta
"""
#%% Imports
import os

from flexcalc import pipeline
from flexcalc import process
from numpy import linspace
from flexdata import display
import shutil

#from PIL import Image

#%% Initialize and schedule (1):

def timelapse(path, file):
    """
    Aligns reconstructions, bins them and makes new slices
    
    Parameters:
        Path    The folder containing reconstructions of one sample
    """
    lola = pipeline.scheduler('./Scratch/', clean_scratch = True)


# Binning:
    b = 16

# Read data:
    
    lola.read_data(path, 'Erycina_', sampling = b, transpose=[0,1,2], updown = False)

    lola.display('max_projection', dim = 2, title = 'Volume before')
    
    lola.registration(subsamp=1, use_moments=True)
    
    lola.display('max_projection', dim = 2, title = 'Volume after')
    
    #lola.draw_nodes()
    
    lola.write_data('./result', 'vol')
    
    # copy all /result files to ./Reconstructions shutil.copytree(src, dest)
    
#img = Image.open('/media/beb/Elements/Naturalis/MicroCT/Recon/Erycina test 2.1 recon/result/vol_000212.tiff')
#img.show()
    
    #%% Runtime
    
    lola.run()
    
    for x in os.listdir(file):
        src = file+'/'+x+'/result'
        dest = './Reconstructions/result_'+x
        shutil.copytree(src, dest)
        
    
    #path = '/media/beb/Elements/Naturalis/MicroCT/Erycina Volwassen/Erycina_volw_1_RECON/result/result2'

    #array = os.listdir(path)
    
    #array = array[-1]

    #display.color_project(array, dim=1, sample = 2, bounds=[0.01, 0.1], title=None, cmap='nipy_spectral', file=None)

if __name__ == "__main__":
    # Reading data from pathway entered in SnakeFile
    # path = '/media/beb/Elements/Naturalis/MicroCT/Erycina Volwassen/Erycina_volw_1_RECON'
    file = snakemake.input.a
    path = file+'/*'
    
    timelapse(path, file)
   