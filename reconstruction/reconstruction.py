import math

import vtk
from utils.conversion_utils import get_nifti_from_dicomdir
from utils.dicom_utils import get_patient_name
from utils.landmarks_utils import (convert_landmarks_to_ras_coordinates,
                                   get_landmarks_from_network_infer,
                                   load_landmarks_from_file)


class VtkVolume:
    def __init__(self):
        self.reader = None
        self.property = None


class VtkHandler:
    _skull = VtkVolume()
    _detected_landmarks = VtkVolume()
    _real_landmarks = VtkVolume()
    _renderer: vtk.vtkRenderer
    _colors = vtk.vtkNamedColors()
    _render_window: vtk.vtkRenderWindow

    def __init__(self, render_window, renderer):
        self._render_window = render_window
        self._renderer = renderer

    def _point_to_glyph(self, points):
        bounds = points.GetBounds()
        max_len = 0
        for i in range(1, 3):
            max_len = max(bounds[i + 1] - bounds[i], max_len)

        sphere_source = vtk.vtkSphereSource()
        sphere_source.SetRadius(2)

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(points)

        mapper = vtk.vtkGlyph3DMapper()
        mapper.SetInputData(polydata)
        mapper.SetSourceConnection(sphere_source.GetOutputPort())
        mapper.ScalarVisibilityOff()
        mapper.ScalingOff()

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        return actor

    def set_axial_view(self):
        self._renderer.ResetCamera()
        focal_point = self._renderer.GetActiveCamera().GetFocalPoint()
        position = self._renderer.GetActiveCamera().GetPosition()
        distance = math.sqrt((position[0] - focal_point[0]) ** 2 + (
            position[1] - focal_point[1]) ** 2 + (position[2] - focal_point[2]) ** 2)
        self._renderer.GetActiveCamera().SetPosition(
            focal_point[0], focal_point[1], focal_point[2] + distance)
        self._renderer.GetActiveCamera().SetViewUp(0.0, 1.0, 0.0)
        self._renderer.GetActiveCamera().Zoom(1.8)
        self._render_window.Render()

    def set_coronal_view(self):
        self._renderer.ResetCamera()
        focal_point = self._renderer.GetActiveCamera().GetFocalPoint()
        position = self._renderer.GetActiveCamera().GetPosition()
        distance = math.sqrt((position[0] - focal_point[0]) ** 2 + (
            position[1] - focal_point[1]) ** 2 + (position[2] - focal_point[2]) ** 2)
        self._renderer.GetActiveCamera().SetPosition(
            focal_point[0], focal_point[2] - distance, focal_point[1])
        self._renderer.GetActiveCamera().SetViewUp(0.0, 0.5, 0.5)
        self._renderer.GetActiveCamera().Zoom(1.8)
        self._render_window.Render()

    def set_sagittal_view(self):
        self._renderer.ResetCamera()
        focal_point = self._renderer.GetActiveCamera().GetFocalPoint()
        position = self._renderer.GetActiveCamera().GetPosition()
        distance = math.sqrt((position[0] - focal_point[0]) ** 2 + (
            position[1] - focal_point[1]) ** 2 + (position[2] - focal_point[2]) ** 2)
        self._renderer.GetActiveCamera().SetPosition(
            focal_point[2] + distance, focal_point[0], focal_point[1])
        self._renderer.GetActiveCamera().SetViewUp(0.0, 0.0, 1.0)
        self._renderer.GetActiveCamera().Zoom(1.6)
        self._render_window.Render()

    def _reconstruct_skull(self, file_name):
        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileNameSliceOffset(1)
        reader.SetDataByteOrderToBigEndian()
        reader.SetFileName(file_name)
        reader.Update()

        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileName(file_name)
        reader.Update()

        volume = vtk.vtkImageData()
        volume.DeepCopy(reader.GetOutput())

        surface = vtk.vtkFlyingEdges3D()
        surface.SetInputData(volume)
        surface.ComputeNormalsOn()
        surface.SetValue(0, 100)

        coordinates_transform = vtk.vtkTransform()
        coordinates_transform.SetMatrix(reader.GetQFormMatrix())

        transform_filter = vtk.vtkTransformFilter()
        transform_filter.SetTransform(coordinates_transform)
        transform_filter.SetInputConnection(surface.GetOutputPort())
        transform_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(transform_filter.GetOutputPort())
        mapper.ScalarVisibilityOff()

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        property = vtk.vtkProperty()
        property.SetColor(self._colors.GetColor3d('Green'))
        property.SetOpacity(1)

        actor.SetProperty(property)

        return actor, reader, property

    def _get_landmarks_shape(self, lps_landmarks, plot_color):
        ras_landmarks = self._get_ras_landmarks_points(lps_landmarks)

        landmark_transform = vtk.vtkLandmarkTransform()
        landmark_transform.SetSourceLandmarks(ras_landmarks)

        polydata = vtk.vtkPolyData()
        polydata.SetPoints(ras_landmarks)

        glyph_filter = vtk.vtkVertexGlyphFilter()
        glyph_filter.SetInputData(polydata)
        glyph_filter.Update()

        transform_filter = vtk.vtkTransformPolyDataFilter()
        transform_filter.SetInputConnection(glyph_filter.GetOutputPort())
        transform_filter.SetTransform(landmark_transform)
        transform_filter.Update()

        actor = self._point_to_glyph(glyph_filter.GetOutput().GetPoints())

        property = vtk.vtkProperty()
        property.SetColor(self._colors.GetColor3d(plot_color))
        property.SetOpacity(1)

        actor.SetProperty(property)

        return actor, property

    def _get_ras_landmarks_points(self, lps_landmarks):
        ras_landmarks = convert_landmarks_to_ras_coordinates(lps_landmarks)

        points = vtk.vtkPoints()
        [points.InsertNextPoint(landmark) for landmark in ras_landmarks]

        return points

    def set_skull_opacity(self, opacity_value):
        self._skull.property.SetOpacity(opacity_value / 100)
        self._render_window.Render()

    def setup_detected_landmarks(self, path_skull):
        real_landmarks, detected_landmarks = get_landmarks_from_network_infer(
            path_skull)

        real_landmarks_actor, real_landmarks_props = self._get_landmarks_shape(
            real_landmarks, "tomato")
        detected_landmarks_actor, detected_landmarks_props = self._get_landmarks_shape(
            detected_landmarks, "blue")

        self._detected_landmarks.property = detected_landmarks_props
        self._real_landmarks.property = real_landmarks_props

        self._renderer.AddActor(detected_landmarks_actor)
        self._renderer.AddActor(real_landmarks_actor)

        return self._real_landmarks, self._detected_landmarks

    def setup_landmarks_from_file(self, json_file_path):
        real_landmarks = load_landmarks_from_file(json_file_path)

        real_landmarks_actor, real_landmarks_props = self._get_landmarks_shape(
            real_landmarks, "tomato")

        self._real_landmarks.property = real_landmarks_props

        self._renderer.AddActor(real_landmarks_actor)

        return self._real_landmarks

    def setup_skull(self, dicom_dir_path):
        nifti_file_name = get_nifti_from_dicomdir(dicom_dir_path)
        patient_name = get_patient_name(dicom_dir_path)

        actor, reader, property = self._reconstruct_skull(nifti_file_name)

        self._skull.reader = reader
        self._skull.property = property

        self._renderer.AddActor(actor)

        return self._skull, patient_name
