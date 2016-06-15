Name = 'StackedBarChartFilter'
Label = 'Stacked Bar Chart Filter'
Help = 'Creates a stacked bar chart (as lines in z-direction) of all point data arrays'

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
        posIndex = 0
        negIndex = 0
        beginIndex = 0
        for v in range(0, numVars-1):
            value = pdi.GetPointData().GetArray(v).GetTuple1(i)
            if value < 0:
                beginIndex = i * numVars + negIndex
                negIndex = v + 1
            else:
                beginIndex = i * numVars + posIndex
                posIndex = v + 1

            beginPoint = newPoints.GetPoint(beginIndex)
            newPointId = newPoints.InsertNextPoint(beginPoint[0], beginPoint[1], beginPoint[2] + value * scalingFactor)
            pdo.InsertNextCell(3, 2, [beginIndex, newPointId]) # VTK_LINE is 3
            valIdArray.SetValue(i*numVars + v, v)
