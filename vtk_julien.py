#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 11:01:08 2022

@author: julien
"""

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    VTK_VERSION_NUMBER,
    vtkVersion
)
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersCore import (
    vtkFlyingEdges3D,
    vtkMarchingCubes
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkImagingHybrid import vtkVoxelModeller
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

colors = vtkNamedColors()

volume = vtkImageData()
reader = vtkTIFFReader()
reader.SetFileName("/Users/julien/Desktop/PROENC/code/tif/line1.tif")
reader.Update()
volume.DeepCopy(reader.GetOutput())

surface = vtkMarchingCubes()
surface.SetInputData(volume)
surface.ComputeNormalsOn()
surface.SetValue(0, 1)

#renderer = vtkRenderer()
#renderer.SetBackground(colors.GetColor3d('DarkSlateGray'))

#render_window = vtkRenderWindow()
#render_window.AddRenderer(renderer)
#render_window.SetWindowName('MarchingCubes')

#interactor = vtkRenderWindowInteractor()
#interactor.SetRenderWindow(render_window)

import vtk

obj = vtk.vtkSTLWriter()
obj.SetInputConnection(surface.GetOutputPort())
obj.SetFileName("/Users/julien/Desktop/line1_mc.stl")
obj.Write()


