import paraview.simple
#for command line args etc
import sys
#enable debugging with pdb.set_trace()
import pdb


print "This will calculate travel times in coast shapes setups."
print "Needs list of filenames as arguments."
print "Will get coast length from file names."
print "Output written in _existing_ directories are csvs with same base name."
print "Example: for i in DISP*; do mkdir ${i%.txt}; /home/waltherm/11_Apps/ParaView-5.0.0-Qt4-OpenGL2-MPI-Linux-64bit/bin/pvpython travel_times.py $(cat ${i}); done"

#get input files as args > 0 (0 = this script)
inStr=sys.argv[1:]

#loop over all files
for thisFile in inStr:
	#get coastlength
	thisLocation=thisFile.split("/")
	thisProps=str(thisLocation[-1]).split("_")
	thisShelfLength=float((thisProps[2]).split("S")[1])
	print "Current coast length: ", thisShelfLength
	
	#gen outfilename
	# example output: last_vtus_disp10/filename.csv
	outFileName=thisLocation[-2] + "/" + thisLocation[-1] + ".csv"

	#current inFile
	currInFile = paraview.simple.OpenDataFile(thisFile)

	# cell to point data
	c2p=paraview.simple.CellDatatoPointData()
	c2p.Input=currInFile

	#make slice
	x_origin = 0
	y_origin = 0
	z_origin = 149.99
	x_normal = 1
	y_normal = 0
	z_normal = thisShelfLength/150.
	slice=paraview.simple.Slice()
	slice.Input=c2p
	slice.SliceType='Plane'
	slice.SliceType.Origin=[x_origin,y_origin,z_origin]
	slice.SliceType.Normal=[x_normal,y_normal,z_normal]
	slice.SliceOffsetValues=0

	#slice for points along z-axis
	sliceZ=paraview.simple.Slice()
	sliceZ.Input=slice
	sliceZ.SliceType='Plane'
	sliceZ.SliceType.Origin=[0,0,150]
	sliceZ.SliceType.Normal=[0,0,1]
	sliceZ.SliceOffsetValues=[0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -38, -39, -40, -41, -42, -43, -44, -45, -46, -47, -48, -49, -50, -51, -52, -53, -54, -55, -56, -57, -58, -59, -60, -61, -62, -63, -64, -65, -66, -67, -68, -69, -70, -71, -72, -73, -74, -75, -76, -77, -78, -79, -80, -81, -82, -83, -84, -85, -86, -87, -88, -89, -90, -91, -92, -93, -94, -95, -96, -97, -98, -99, -100, -101, -102, -103, -104, -105, -106, -107, -108, -109, -110, -111, -112, -113, -114, -115, -116, -117, -118, -119, -120, -121, -122, -123, -124, -125, -126, -127, -128, -129, -130, -131, -132, -133, -134, -135, -136, -137, -138, -139, -140, -141, -142, -143, -144, -145, -146, -147, -148, -149, -150]

	stTrCustom=paraview.simple.StreamTracerWithCustomSource()
	stTrCustom.Input=c2p
	stTrCustom.SeedSource=sliceZ
	stTrCustom.Vectors="ELEMENT_VELOCITY"
	stTrCustom.IntegrationDirection="FORWARD"
	stTrCustom.MaximumSteps=20000
	stTrCustom.MaximumStreamlineLength=100000

	#contour c=0.5
	cont=paraview.simple.Contour()
	cont.Input=stTrCustom
	cont.ContourBy="CONCENTRATION1"
	cont.Isosurfaces=[0.5]

	#threshold for only positiv x-vel
	threshold=paraview.simple.Threshold()
	threshold.Scalars="ELEMENT_VELOCITY_X"
	threshold.ThresholdRange=[0,1]



	stats=paraview.simple.DescriptiveStatistics()
	stats.VariablesofInterest="IntegrationTime"

	# # pass variables
	# passArr=paraview.simple.PassArrays()
	# passArr.Input=threshold
	# passArr.PointDataArrays="IntegrationTime", "ELEMENT_VELOCITY"

	# paraview.simple.Show(threshold)
	# paraview.simple.Show(stats)
	# cam = paraview.simple.GetActiveCamera()
	# cam.Elevation(270)
	# cam.Pitch(30)
	# cam.Yaw(20)
	# paraview.simple.Interact(view=None)
	# paraview.simple.Render()
	# del cam


	# write csv
	outFile=paraview.simple.CreateWriter(outFileName, stats)
	#outFile.FieldAssociation="Points"
	#outFile.Precision=10
	#outFile.UseScientificNotation=1
	outFile.UpdatePipeline()
	del outFile
