# author: Carolin Helbig 2013-07-23
# A source object has to be selected in the pipeline browser!
try: paraview.simple
except: from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

exporters=servermanager.createModule("exporters")

RenderView1 = GetRenderView()
reader = GetActiveSource()
tsteps = reader.TimestepValues


for index in range(len(tsteps)):
    RenderView1.ViewTime = tsteps[index]
    Render()
    view = GetActiveView()
    FbxExporter=exporters.FbxExporter(FileName="C:/Users/vislab/unity/all/Assets/_project/Bayrischer Bahnhof/Meshes/sim-ost/Temp-1.5/" + str(index) + ".fbx")
    FbxExporter.SetView(view)
    FbxExporter.Write()
