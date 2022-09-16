import json

import vtk


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
            self.renderer.ResetCamera()
        focal_point = self.renderer.GetActiveCamera().GetFocalPoint()
        position = self.renderer.GetActiveCamera().GetPosition()
        distance = math.sqrt((position[0] - focal_point[0]) ** 2 + (
            position[1] - focal_point[1]) ** 2 + (position[2] - focal_point[2]) ** 2)
        self.renderer.GetActiveCamera().SetPosition(
            focal_point[0], focal_point[1], focal_point[2] + distance)
        self.renderer.GetActiveCamera().SetViewUp(0.0, 1.0, 0.0)
        self.renderer.GetActiveCamera().Zoom(1.8)
        self.render_window.Render()

    def set_coronal_view(self):
        self.renderer.ResetCamera()
        focal_point = self.renderer.GetActiveCamera().GetFocalPoint()
        position = self.renderer.GetActiveCamera().GetPosition()
        distance = math.sqrt((position[0] - focal_point[0]) ** 2 + (
            position[1] - focal_point[1]) ** 2 + (position[2] - focal_point[2]) ** 2)
        self.renderer.GetActiveCamera().SetPosition(
            focal_point[0], focal_point[2] - distance, focal_point[1])
        self.renderer.GetActiveCamera().SetViewUp(0.0, 0.5, 0.5)
        self.renderer.GetActiveCamera().Zoom(1.8)
        self.render_window.Render()

    def set_sagittal_view(self):
        self.renderer.ResetCamera()
        focal_point = self.renderer.GetActiveCamera().GetFocalPoint()
        position = self.renderer.GetActiveCamera().GetPosition()
        distance = math.sqrt((position[0] - focal_point[0]) ** 2 + (
            position[1] - focal_point[1]) ** 2 + (position[2] - focal_point[2]) ** 2)
        self.renderer.GetActiveCamera().SetPosition(
            focal_point[2] + distance, focal_point[0], focal_point[1])
        self.renderer.GetActiveCamera().SetViewUp(0.0, 0.0, 1.0)
        self.renderer.GetActiveCamera().Zoom(1.6)
        self.render_window.Render()

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

    def _convert_landmarks_to_ras_coordinates(self, lps_landmarks):
        for lps_landmark in lps_landmarks:
            yield [-lps_landmark[0], -lps_landmark[1], lps_landmark[2]]

    def _get_ras_landmarks_points(self, lps_landmarks):
        points = vtk.vtkPoints()

        ras_landmarks = self._convert_landmarks_to_ras_coordinates(
            lps_landmarks)

        [points.InsertNextPoint(landmark) for landmark in ras_landmarks]

        return points

    def _load_landmarks_from_file(self, json_file_path):
        with open(json_file_path, 'r') as json_file:
            landmarks_obj = json.load(json_file)['markups'][0]['controlPoints']
            lps_landmarks = [obj['position'] for obj in landmarks_obj]

        return lps_landmarks

    def _detect_landmarks(self):
        mock_real_landmarks = [[-41.37749481201172, -71.82634735107422, 14.915303230285645], [-35.485530853271484, -72.81812286376953, -5.548721790313721], [7.642332553863525, -93.41370391845703, 15.821390151977539], [54.65541458129883, -71.99036407470703, -4.924007415771484], [58.362796783447266, -74.64672088623047, 14.933220863342285], [62.50477981567383, -69.75077056884766, 20.013507843017578], [-45.34592819213867, -68.8386001586914, 20.963350296020508], [5.025712490081787, -106.49911499023438, -2.1380300521850586], [0.4708743393421173,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              -4.421438217163086, 115.38072204589844]]

        mock_detected_landmarks = [[-41.37749481201172 + 6, -71.82634735107422, 14.915303230285645], [-35.485530853271484 + 6, -72.81812286376953, -5.548721790313721], [7.642332553863525 + 6, -93.41370391845703, 15.821390151977539], [54.65541458129883 + 6, -71.99036407470703, -4.924007415771484], [58.362796783447266 + 6, -74.64672088623047, 14.933220863342285], [62.50477981567383 + 6, -69.75077056884766, 20.013507843017578], [-45.34592819213867 + 6, -68.8386001586914, 20.963350296020508], [5.025712490081787 + 6, -106.49911499023438, -2.1380300521850586], [0.4708743393421173 + 6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  -4.421438217163086, 115.38072204589844]]

        return mock_real_landmarks, mock_detected_landmarks

    def set_skull_opacity(self, opacity_value):
        self._skull.property.SetOpacity(opacity_value / 100)
        self.render_window.Render()

    def setup_detected_landmarks(self):
        real_landmarks, detected_landmarks = self._detect_landmarks()

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
        real_landmarks = self._load_landmarks_from_file(json_file_path)

        real_landmarks_actor, real_landmarks_props = self._get_landmarks_shape(
            real_landmarks, "tomato")

        self._real_landmarks.property = real_landmarks_props

        self._renderer.AddActor(real_landmarks_actor)

        return self._real_landmarks

    def setup_skull(self, file_path):
        actor, reader, property = self._reconstruct_skull(file_path)

        self._skull.reader = reader
        self._skull.property = property

        self._renderer.AddActor(actor)

        return self._skull
