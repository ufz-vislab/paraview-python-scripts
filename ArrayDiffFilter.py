def GetUpdateTimestep(algorithm):
    """Returns the requested time value, or None if not present"""
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    if not outInfo.Has(executive.UPDATE_TIME_STEP()):
        return None
    return outInfo.Get(executive.UPDATE_TIME_STEP())

req_time = GetUpdateTimestep(self)

A = self.GetInputDataObject(0, 0)
B = self.GetInputDataObject(0, 1)
pdo = self.GetOutput()
for arrayIndex in range(A.GetPointData().GetNumberOfArrays()):
    array = A.GetPointData().GetArrayName(arrayIndex)
    array0 = A.GetPointData().GetScalars(array)
    array1 = B.GetPointData().GetScalars(array)
    array_diff = vtk.vtkDoubleArray()
    array_diff.SetName(array + "_diff")
    for i in range(A.GetNumberOfPoints()):
        array_diff.InsertNextValue(array1.GetValue(i) - array0.GetValue(i))
    pdo.GetPointData().AddArray(array_diff)

pdo.GetInformation().Set(output.DATA_TIME_STEP(), req_time)
