# author: Carolin Helbig 2013-07-23, Lars Bilke
# A source object has to be selected in the pipeline browser!
# On first input dialog specify export directory.
# On second input dialog specify nth timesteps to export, 1 for exporting all.
import os, math
try: paraview.simple
except: from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

exporters = servermanager.createModule("exporters")

RenderView1 = GetRenderView()
reader = GetActiveSource()
tsteps = reader.TimestepValues
numtsteps = len(tsteps)
numdigits = int(math.ceil(math.log10(numtsteps)))

dir = raw_input("Export directory: ")
assert os.path.exists(dir), "Directory does not exist "+str(dir)
step = raw_input("Export every nth timestep: ")
if step == '':
    step = 1

for index in range(0, numtsteps, int(step)):
    RenderView1.ViewTime = tsteps[index]
    Render()
    view = GetActiveView()
    FbxExporter = exporters.FbxExporter(FileName=str(dir) + "/" + str(index).zfill(numdigits) + ".fbx")
    FbxExporter.SetView(view)
    FbxExporter.Write()
    
