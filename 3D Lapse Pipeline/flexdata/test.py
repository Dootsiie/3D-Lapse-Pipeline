#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 14:21:49 2020

@author: beb
"""

import display
import os

path = '/media/beb/Elements/Naturalis/MicroCT/Erycina Volwassen/Erycina_volw_1_RECON/result/result2'

array = os.listdir(path)

display.color_project(array, dim=1, sample = 2, bounds=[0.01, 0.1], title=None, cmap='nipy_spectral', file='aaaaaaaaaaaaaa')