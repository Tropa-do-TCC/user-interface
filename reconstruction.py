import vtk

class VtkShape:
    def __init__(self):
        self.reader = None
        self.property = None

def read_volume(file_name):
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileNameSliceOffset(1)
    reader.SetDataByteOrderToBigEndian()
    reader.SetFileName(file_name)
    reader.Update()

    # reader
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(file_name)
    reader.Update()

    # volume
    volume = vtk.vtkImageData()
    volume.DeepCopy(reader.GetOutput())

    # surface
    surface = vtk.vtkFlyingEdges3D()
    surface.SetInputData(volume)
    surface.ComputeNormalsOn()
    surface.SetValue(0, 100)

    # transformations
    coordinates_transform = vtk.vtkTransform()
    coordinates_transform.SetMatrix(reader.GetQFormMatrix())

    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetTransform(coordinates_transform)
    transform_filter.SetInputConnection(surface.GetOutputPort())
    transform_filter.Update()

    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(transform_filter.GetOutputPort())
    mapper.ScalarVisibilityOff()

    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # property
    colors = vtk.vtkNamedColors()

    property = vtk.vtkProperty()
    property.SetColor(colors.GetColor3d('Green'))
    property.SetOpacity(1)

    actor.SetProperty(property)

    return actor, reader, property


def setup_skull(renderer, file):
    skull = VtkShape()
    actor, reader, property = read_volume(file) 

    skull.reader = reader
    skull.property = property

    renderer.AddActor(actor) 

    return skull