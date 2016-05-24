# TODO peak file for dimensions
# http://stackoverflow.com/questions/13311471/skip-a-specified-number-of-columns-with-numpy-genfromtxt

Name = 'EnviMetDerivedSource'
Label = 'EnviMet Derived Data Source'
Help = 'Reads custom EnviMet-derived CSV data'

NumberOfInputs = 0
InputDataType = ''
OutputDataType = 'vtkImageData'
ExtraXml = ''
Properties = dict(
    dir = 'X:\\caro\\Vis_Bayr-Bahnhof\\EnviMet\\daniel',
    origin = [0,0,0],
    spacing = 1.0,
    grid_size = 225
)

def RequestData():
    import os
    import numpy as np
    from vtk.util import numpy_support

    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    updateExtent = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in xrange(6)]

    out = self.GetOutput()
    out.SetOrigin(origin)
    out.SetSpacing(spacing, spacing, spacing)
    out.SetDimensions(grid_size, grid_size, 1)

    for file in sorted(os.listdir(dir)):
        data = np.genfromtxt(dir + os.sep + file, dtype=float, skip_header=1, delimiter=' ', autostrip=True, usecols = range(1, grid_size + 1))
        VTK_data = numpy_support.numpy_to_vtk(num_array=data.ravel('F'), deep=True, array_type=vtk.VTK_FLOAT)
        VTK_data.SetName(os.path.basename(file))
        out.GetPointData().AddArray(VTK_data)


def RequestInformation():
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    outInfo.Set(executive.WHOLE_EXTENT(), 0, grid_size-1, 0, grid_size-1, 0, 0)
    outInfo.Set(vtk.vtkDataObject.SPACING(), spacing, spacing, spacing)
    dataType = 10 # VTK_FLOAT
    numberOfComponents = 1
    vtk.vtkDataObject.SetPointDataActiveScalarInfo(outInfo, dataType, numberOfComponents)
