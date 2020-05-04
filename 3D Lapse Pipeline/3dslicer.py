#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 11:59:33 2020

3D-Slicer Python script, this script opens the reconstructions in 3DSlicer software program
and builds a 3D timelapse, which will be saved in "Erycina_time_lapse.mpg"

Code has been partly retrieved from the 3D slicer Python documentation

Python code using the Sequence extension have been retrieved from
https://github.com/ChunBoo/3DSlicer/blob/6334b773502f5d21b18b32d518afe8d8f64fb87d/Modules/Scripted/ScreenCapture/ScreenCapture.py

All credits go to these instances.
"""


import sys
import os
import ScreenCapture


def volumeRendering(volumeNode):
    volRenLogic = slicer.modules.volumerendering.logic()
    displayNode = volRenLogic.CreateDefaultVolumeRenderingNodes(volumeNode)


def centerStage():
    layoutManager = slicer.app.layoutManager()
    threeDWidget = layoutManager.threeDWidget(0)
    threeDView = threeDWidget.threeDView()
    threeDView.resetFocalPoint()


def creatingSequence():
    global SequenceNode
    index = 0
    volume = 'vol_000000'
    for x in os.listdir("./Reconstructions"): 
        file = './Reconstructions/'+x+"/vol_000000.tiff"
        erycina = slicer.util.loadVolume(file)
        node = getNode(volume)
        SequenceNode.SetDataNodeAtValue(node, str(index))
        index+=1
        volume = 'vol_000000'+'_'+str(index)


def recordSequence():
    global SequenceNode
    
    SequenceBrowserNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSequenceBrowserNode', 'TimeLapseSequence')
    SequenceBrowserNode.AddSynchronizedSequenceNode(SequenceNode.GetID())
        
    ProxyNode = SequenceBrowserNode.GetProxyNode(SequenceNode)
    ProxyNode.SetAndObserveDisplayNodeID(ProxyNode.GetID())
    
    capture = ScreenCapture.ScreenCaptureLogic()
    
    numberOfImages = len(os.listdir("./Reconstructions"))
    endValue = numberOfImages - 1
    
    capture.captureSequence(getNode('vtkMRMLViewNode1'), SequenceBrowserNode, 0, endValue, numberOfImages, './SlicerCapture/Screenshots', 'capture_%d.png')
    

def main():
    
    # 1) load all data
    # 2) make sequence
    # 3) grayModel sequence
    # 4) center stage sequence
    # 5) save sequence/ record sequence
    
    global SequenceNode
    SequenceNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLSequenceNode', 'Sequence')
    
    creatingSequence()
    # volumeRendering(n)
    
    #centerStage()
    recordSequence()
    
    exit()

main()
