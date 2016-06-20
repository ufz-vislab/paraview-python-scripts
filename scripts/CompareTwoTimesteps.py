import paraview.simple
import vtk
from vtk.util import numpy_support
#for command line args etc
import sys
#enable debugging with pdb.set_trace()
#import pdb
#pdb.set_trace()


print "This will calculate the difference between two given vtu files."
print "Needs two filenames as arguments."
print "Meshes need to be identical."
print "Output written in script directory."
print " "
#print " for i in DISP*.txt; do mkdir ${i%\.txt}; /home/waltherm/11_Apps/ParaView-5.0.0-Qt4-OpenGL2-MPI-Linux-64bit/bin/pvpython gradients.py $(cat ${i}); done"

#get input files as args > 0 (0 = this script)
inStr=sys.argv[1]
inStr2=sys.argv[2]

inLocation=inStr.split("/")[-1]
inLocation2=inStr2.split("/")[-1]

outFileName=inLocation+"_DIFF_"+inLocation2+".vtu"

inFile=paraview.simple.OpenDataFile(inStr)
inFile2=paraview.simple.OpenDataFile(inStr2)

pArrays=inFile.PointArrayStatus
cArrays=inFile.CellArrayStatus

pDiffArrays=[]
cDiffArrays=[]
pDiffArrayNames=[]
cDiffArrayNames=[]

calcName=[]
calc2Name=[]
appAttName=[]
calc_diffName=[]
passArrName=[]


#for points
for pArray in pArrays:
	print pArray
	#pdb.set_trace()
	#pass point array of inputs in new arrays
	calcName.append("calc"+pArray)
	calcName[-1]=paraview.simple.Calculator()
	calcName[-1].Input=inFile
	calcName[-1].ResultArrayName=pArray+"1"
	calcName[-1].Function=pArray
	calc2Name.append("calc2"+pArray)
	calc2Name[-1]=paraview.simple.Calculator()
	calc2Name[-1].Input=inFile2
	calc2Name[-1].ResultArrayName=pArray+"2"
	calc2Name[-1].Function=pArray
	#append two new arrays to new object
	appAttName.append("app"+pArray)
	appAttName[-1]=paraview.simple.AppendAttributes(calcName[-1], calc2Name[-1])
	#calc diff of two new arrays
	diff_name="diff_"+pArray
	pDiffArrayNames.append(diff_name)
	calc_diffName.append("diff"+pArray)
	calc_diffName[-1]=paraview.simple.Calculator()
	calc_diffName[-1].Input=appAttName[-1]
	calc_diffName[-1].ResultArrayName=pDiffArrayNames[-1]
	calc_diffName[-1].Function=pArray+"1 - "+pArray+"2"
	#pass only relevant data
	passArrName.append("passArr"+pArray)
	passArrName[-1]=paraview.simple.PassArrays()
	passArrName[-1].Input=calc_diffName[-1]
	passArrName[-1].PointDataArrays=pDiffArrayNames[-1]


# #for cells
for cArray in cArrays:
	print cArray
	#pdb.set_trace()
	#pass point array of inputs in new arrays
	calcName.append("calc"+cArray)
	calcName[-1]=paraview.simple.Calculator()
	calcName[-1].Input=inFile
	calcName[-1].AttributeMode="Cell Data"
	calcName[-1].ResultArrayName=cArray+"1"
	calcName[-1].Function=cArray
	calc2Name.append("calc2"+cArray)
	calc2Name[-1]=paraview.simple.Calculator()
	calc2Name[-1].Input=inFile2
	calc2Name[-1].AttributeMode="Cell Data"
	calc2Name[-1].ResultArrayName=cArray+"2"
	calc2Name[-1].Function=cArray
	#append two new arrays to new object
	appAttName.append("app"+cArray)
	appAttName[-1]=paraview.simple.AppendAttributes(calcName[-1], calc2Name[-1])
	#calc diff of two new arrays
	diff_name="diff_"+cArray
	cDiffArrayNames.append(diff_name)
	calc_diffName.append("diff"+cArray)
	calc_diffName[-1]=paraview.simple.Calculator()
	calc_diffName[-1].Input=appAttName[-1]
	calc_diffName[-1].AttributeMode="Cell Data"
	calc_diffName[-1].ResultArrayName=cDiffArrayNames[-1]
	calc_diffName[-1].Function=cArray+"1 - "+cArray+"2"
	#pass only relevant data
	passArrName.append("passArr"+cArray)
	passArrName[-1]=paraview.simple.PassArrays()
	passArrName[-1].Input=calc_diffName[-1]
	passArrName[-1].CellDataArrays=cDiffArrayNames[-1]


#collect all data
appData=paraview.simple.AppendAttributes()
appData.Input=passArrName[:]

# write vtu
outFile=paraview.simple.CreateWriter(outFileName, appData)
outFile.UpdatePipeline()
del outFile


# paraview.simple.Show(appData)
# cam = paraview.simple.GetActiveCamera()
# cam.Elevation(270)
# cam.Pitch(30)
# cam.Yaw(20)
# paraview.simple.Interact(view=None)
# paraview.simple.Render()