Name = 'StackedBarChartFilter'
Label = 'Stacked Bar Chart Filter'
Help = 'Creates a stacked bar chart (as lines) of all point data data arrays'

NumberOfInputs = 2
InputDataType = 'vtkPolyData'
OutputDataType = 'vtkPolyData'
ExtraXml = ''
Properties = dict(
	scalingFactor = 1.0
)

def RequestData():

    pdi = self.GetPolyDataInput()
    pdo = self.GetPolyDataOutput()

    numPoints = pdi.GetNumberOfPoints()
    numVars = pdi.GetPointData().GetNumberOfArrays()
    numCells = numPoints * numVars

    pdo.Allocate(numCells)

    newPoints = vtk.vtkPoints()
    pdo.SetPoints(newPoints)

    valIdArray = vtk.vtkIntArray()
    valIdArray.SetName("ArrayIds")
    valIdArray.SetNumberOfComponents(1)
    valIdArray.SetNumberOfTuples(numCells)
    pdo.GetCellData().AddArray(valIdArray)

    for i in range(0, numPoints-1):
        currentPoint = pdi.GetPoints().GetPoint(i)
        basePointId = newPoints.InsertNextPoint(currentPoint)
        for v in range(0, numVars):
            value = pdi.GetPointData().GetArray(v).GetTuple1(i)
            newPointId = newPoints.InsertNextPoint(currentPoint[0], currentPoint[1], currentPoint[2] + value * scalingFactor)
            linepoints = [basePointId + v, newPointId]
            pdo.InsertNextCell(3, 2, linepoints) # VTK_LINE is 3
            valIdArray.SetValue(i*numVars + v, v)
