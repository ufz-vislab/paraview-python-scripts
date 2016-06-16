# TODO peak file for dimensions
# http://stackoverflow.com/questions/13311471/skip-a-specified-number-of-columns-with-numpy-genfromtxt

Name = 'EnviMetDerivedSourceTime'
Label = 'EnviMet Derived Data Source Time'
Help = 'Reads custom EnviMet-derived CSV data'

NumberOfInputs = 0
InputDataType = ''
OutputDataType = 'vtkImageData'
ExtraXml = ''
Properties = dict(
    dir = 'x:\\caro\\Vis_Bayr-Bahnhof\\EnviMet\\ostwind\\neuebebauung\\derived',
    date = '21.07.2015',
    num_timesteps = 24,
    variables = 'Conv deltaT EvTrans Q_SH Rad',
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

    req_time = int(round(outInfo.Get(executive.UPDATE_TIME_STEP())))
    time_string = str(req_time).rjust(2, '0')

    for variable in variables.split():
        filename = r"%s %s.00.00 %s.txt" % (variable, time_string, date)
        for file in sorted(os.listdir(dir)):
            if file == filename:
                # print "Loading " + file
                data = np.genfromtxt(dir + os.sep + file, dtype=float, skip_header=1, delimiter=' ', autostrip=True, usecols = range(1, grid_size + 1))
                VTK_data = numpy_support.numpy_to_vtk(num_array=data.ravel('F'), deep=True, array_type=vtk.VTK_FLOAT)
                VTK_data.SetName(variable)
                out.GetPointData().AddArray(VTK_data)

    out.GetInformation().Set(out.DATA_TIME_STEP(), req_time)


def RequestInformation():
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    outInfo.Set(executive.WHOLE_EXTENT(), 0, grid_size-1, 0, grid_size-1, 0, 0)
    outInfo.Set(vtk.vtkDataObject.SPACING(), spacing, spacing, spacing)
    dataType = 10 # VTK_FLOAT
    numberOfComponents = 1
    vtk.vtkDataObject.SetPointDataActiveScalarInfo(outInfo, dataType, numberOfComponents)

    # Time setup
    outInfo.Remove(executive.TIME_STEPS())
    for timestep in xrange(num_timesteps):
        outInfo.Append(executive.TIME_STEPS(), timestep)
    outInfo.Remove(executive.TIME_RANGE())
    outInfo.Append(executive.TIME_RANGE(), 0)
    outInfo.Append(executive.TIME_RANGE(), num_timesteps-1)
