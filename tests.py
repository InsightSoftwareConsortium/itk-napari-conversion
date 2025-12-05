import numpy as np
import itk
import napari
import itk_napari_conversion


def test_image_layer_from_image():
    data = np.random.randint(256, size=(10, 10), dtype=np.uint8)
    image = itk.image_view_from_array(data)
    image_layer = itk_napari_conversion.image_layer_from_image(image)
    assert np.array_equal(data, image_layer.data)


def test_image_layer_from_image_rgb():
    data = np.random.randint(256, size=(10, 10, 3), dtype=np.uint8)
    image = itk.image_view_from_array(data, itk.RGBPixel[itk.UC])
    image_layer = itk_napari_conversion.image_layer_from_image(image)
    assert np.array_equal(data, image_layer.data)
    assert image_layer.rgb is True


def test_image_layer_from_image_metadata():
    data = np.random.randint(256, size=(10, 10), dtype=np.uint8)
    image = itk.image_view_from_array(data)
    image["wookies"] = 7
    image["units"] = "mm"
    image_layer = itk_napari_conversion.image_layer_from_image(image)
    assert np.array_equal(data, image_layer.data)
    assert image_layer.metadata["wookies"] == 7
    assert image_layer.metadata["units"] == "mm"


def test_image_layer_from_image_scale():
    data = np.random.randint(256, size=(10, 10), dtype=np.uint8)
    image = itk.image_view_from_array(data)
    spacing = [1.1, 2.2]
    image.SetSpacing(spacing)
    image_layer = itk_napari_conversion.image_layer_from_image(image)
    assert np.array_equal(data, image_layer.data)
    assert np.allclose(np.array(spacing)[::-1], image_layer.scale)


def test_image_layer_from_image_translate():
    data = np.random.randint(256, size=(10, 10), dtype=np.uint8)
    image = itk.image_view_from_array(data)
    origin = [1.1, 2.2]
    image.SetOrigin(origin)
    image_layer = itk_napari_conversion.image_layer_from_image(image)
    assert np.array_equal(data, image_layer.data)
    assert np.allclose(np.array(origin)[::-1], image_layer.translate)


def test_image_layer_from_image_rotate():
    data = np.random.randint(256, size=(10, 10), dtype=np.uint8)
    image = itk.image_view_from_array(data)

    rotate = np.rot90(np.eye(2))
    image.SetDirection(rotate)
    image_layer = itk_napari_conversion.image_layer_from_image(image)
    assert np.array_equal(data, image_layer.data)
    assert np.allclose(rotate, image_layer.rotate * np.sign(image_layer.scale))

    def check_angle(angle):
        print('angle', angle)
        angle = np.radians(angle)
        rotate = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle),
            np.cos(angle)]], dtype=np.float64)
        image.SetDirection(rotate)
        image_layer = itk_napari_conversion.image_layer_from_image(image)
        assert np.array_equal(data, image_layer.data)
        assert np.allclose(rotate, image_layer.rotate)

    for angle in [0, 30, 45, 60, 90, 120, 150, 180]:
        check_angle(angle)

def test_image_from_image_layer():
    data = np.random.randint(256, size=(10, 10), dtype=np.uint8)
    image_layer = napari.layers.Image(data)
    image = itk_napari_conversion.image_from_image_layer(image_layer)
    assert np.array_equal(data, itk.array_view_from_image(image))

def test_image_from_image_layer_rgb():
    data = np.random.randint(256, size=(10, 10, 3), dtype=np.uint8)
    image_layer = napari.layers.Image(data, rgb=True)
    image = itk_napari_conversion.image_from_image_layer(image_layer)
    assert np.array_equal(data, itk.array_view_from_image(image))
    assert itk.template(image)[1][0] is itk.RGBPixel[itk.UC]

def test_image_from_image_layer_metadata():
    data = np.random.randint(256, size=(10, 10, 3), dtype=np.uint8)
    metadata = {"wookies": 7, "units": "mm" }
    image_layer = napari.layers.Image(data, metadata=metadata)
    image = itk_napari_conversion.image_from_image_layer(image_layer)
    assert np.array_equal(data, itk.array_view_from_image(image))
    assert image["wookies"] == 7
    assert image["units"] == "mm"

def test_image_from_image_layer_scale():
    data = np.random.randint(256, size=(10, 10), dtype=np.uint8)
    metadata = {"wookies": 7, "units": "mm" }
    scale = [1.1, 2.2]
    image_layer = napari.layers.Image(data, scale=scale)
    image = itk_napari_conversion.image_from_image_layer(image_layer)
    assert np.array_equal(data, itk.array_view_from_image(image))
    assert np.allclose(scale, np.array(image["spacing"]))

def test_image_from_image_layer_translate():
    data = np.random.randint(256, size=(10, 10), dtype=np.uint8)
    metadata = {"wookies": 7, "units": "mm" }
    translate = [1.1, 2.2]
    image_layer = napari.layers.Image(data, translate=translate)
    image = itk_napari_conversion.image_from_image_layer(image_layer)
    assert np.array_equal(data, itk.array_view_from_image(image))
    assert np.allclose(translate, np.array(image["origin"]))

def test_image_from_image_layer_rotate():
    data = np.random.randint(256, size=(10, 10), dtype=np.uint8)
    rotate = np.rot90(np.eye(2))
    image_layer = napari.layers.Image(data, rotate=rotate)
    image = itk_napari_conversion.image_from_image_layer(image_layer)
    assert np.array_equal(data, itk.array_view_from_image(image))
    assert np.allclose(rotate, np.array(image["direction"]))

    def check_angle(angle):
        print('angle', angle)
        angle = np.radians(angle)
        rotate = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle),
            np.cos(angle)]], dtype=np.float64)
        image_layer = napari.layers.Image(data, rotate=rotate)
        image = itk_napari_conversion.image_from_image_layer(image_layer)
        assert np.array_equal(data, itk.array_view_from_image(image))
        assert np.allclose(rotate, np.transpose(np.array(image["direction"])))

    for angle in [0, 30, 45, 60, 90, 120, 150, 180]:
        check_angle(angle)


def test_image_from_image_layer_rotate_3d():
    """Test 3D rotation matrix conversion from napari to ITK."""
    data = np.random.randint(256, size=(10, 10, 10), dtype=np.uint8)

    # 45 degree rotation around z-axis
    angle = np.radians(45)
    rotate = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ], dtype=np.float64)

    scale = [2.0, 1.5, 1.5]
    translate = [10.0, 20.0, 30.0]

    image_layer = napari.layers.Image(data, scale=scale, rotate=rotate, translate=translate)
    image = itk_napari_conversion.image_from_image_layer(image_layer)

    assert np.array_equal(data, itk.array_view_from_image(image))

    # napari rotate is transposed compared to ITK direction
    assert np.allclose(rotate, np.transpose(np.array(image["direction"])))

    # Verify we can access direction via dictionary
    direction_array = image["direction"]  # Returns numpy array
    assert direction_array.shape == (3, 3)

    # Verify the actual values in the direction matrix (transpose of rotate)
    expected_direction = np.transpose(rotate)
    assert np.allclose(direction_array, expected_direction)

    # Verify other transformations
    assert np.allclose(scale, np.array(image["spacing"]))
    assert np.allclose(translate, np.array(image["origin"]))

def test_points_layer_from_point_set():
    # Create a simple 3D point set
    PointSetType = itk.PointSet[itk.F, 3]
    point_set = PointSetType.New()

    # Add some points (ITK order: x,y,z)
    points_data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], dtype=np.float32)
    points = itk.vector_container_from_array(points_data.flatten())
    point_set.SetPoints(points)

    # Convert to napari points layer with default reverse_coords=True
    points_layer = itk_napari_conversion.points_layer_from_point_set(point_set)

    # Check that data is reversed (napari order: z,y,x)
    expected = points_data[:, ::-1]
    assert np.allclose(expected, points_layer.data)


def test_points_layer_from_point_set_with_features():
    # Create a 3D point set with point data
    PointSetType = itk.PointSet[itk.F, 3]
    point_set = PointSetType.New()

    # Add points (ITK order: x,y,z)
    points_data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], dtype=np.float32)
    points = itk.vector_container_from_array(points_data.flatten())
    point_set.SetPoints(points)

    # Add point data (features)
    feature_data = np.array([10.0, 20.0, 30.0], dtype=np.float32)
    point_data = itk.vector_container_from_array(feature_data)
    point_set.SetPointData(point_data)

    # Convert to napari points layer with default reverse_coords=True
    points_layer = itk_napari_conversion.points_layer_from_point_set(point_set)

    # Check that data is reversed (napari order: z,y,x)
    expected = points_data[:, ::-1]
    assert np.allclose(expected, points_layer.data)
    assert points_layer.features is not None
    assert 'feature' in points_layer.features
    assert np.allclose(feature_data, points_layer.features['feature'])


def test_point_set_from_points_layer():
    # Create napari points layer (napari order: z,y,x)
    data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    points_layer = napari.layers.Points(data)

    # Convert to ITK point set with default reverse_coords=True
    point_set = itk_napari_conversion.point_set_from_points_layer(points_layer)

    # Check points are reversed (ITK order: x,y,z)
    points_array = itk.array_from_vector_container(point_set.GetPoints())
    expected = data[:, ::-1]
    assert np.allclose(expected, points_array)


def test_point_set_from_points_layer_with_features():
    # Create napari points layer with features (napari order: z,y,x)
    data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    features = {'feature': np.array([10.0, 20.0, 30.0])}
    points_layer = napari.layers.Points(data, features=features)

    # Convert to ITK point set with default reverse_coords=True
    point_set = itk_napari_conversion.point_set_from_points_layer(points_layer)

    # Check points are reversed (ITK order: x,y,z)
    points_array = itk.array_from_vector_container(point_set.GetPoints())
    expected = data[:, ::-1]
    assert np.allclose(expected, points_array)

    # Check point data - verify it was set
    point_data = point_set.GetPointData()
    assert point_data.Size() > 0, "Point data should be set"
    point_data_array = itk.array_from_vector_container(point_data)
    assert np.allclose(features['feature'], point_data_array)


def test_point_set_from_points_layer_with_scale():
    # Create napari points layer with scale (napari order: z,y,x)
    data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    scale = np.array([2.0, 3.0, 4.0])
    points_layer = napari.layers.Points(data, scale=scale)

    # Convert to ITK point set with default reverse_coords=True
    point_set = itk_napari_conversion.point_set_from_points_layer(points_layer)

    # Check that points are scaled and reversed (ITK order: x,y,z)
    points_array = itk.array_from_vector_container(point_set.GetPoints())
    expected = (data * scale)[:, ::-1]
    assert np.allclose(expected, points_array)


def test_point_set_from_points_layer_with_translate():
    # Create napari points layer with translation (napari order: z,y,x)
    data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    translate = np.array([10.0, 20.0, 30.0])
    points_layer = napari.layers.Points(data, translate=translate)

    # Convert to ITK point set with default reverse_coords=True
    point_set = itk_napari_conversion.point_set_from_points_layer(points_layer)

    # Check that points are translated and reversed (ITK order: x,y,z)
    points_array = itk.array_from_vector_container(point_set.GetPoints())
    expected = (data + translate)[:, ::-1]
    assert np.allclose(expected, points_array)


def test_point_set_from_points_layer_with_rotate():
    # Create napari points layer with rotation (napari order: z,y,x)
    data = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])

    # 90 degree rotation around z-axis
    angle = np.radians(90)
    rotate = np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ], dtype=np.float64)

    points_layer = napari.layers.Points(data, rotate=rotate)

    # Convert to ITK point set with default reverse_coords=True
    point_set = itk_napari_conversion.point_set_from_points_layer(points_layer)

    # Check that points are rotated and reversed (ITK order: x,y,z)
    points_array = itk.array_from_vector_container(point_set.GetPoints())
    expected = (data @ rotate.T)[:, ::-1]
    assert np.allclose(expected, points_array, atol=1e-10)


def test_points_layer_from_point_set_no_reverse():
    """Test points_layer_from_point_set with reverse_coords=False."""
    # Create a simple 3D point set
    PointSetType = itk.PointSet[itk.F, 3]
    point_set = PointSetType.New()

    # Add some points (ITK order: x,y,z)
    points_data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], dtype=np.float32)
    points = itk.vector_container_from_array(points_data.flatten())
    point_set.SetPoints(points)

    # Convert to napari points layer with reverse_coords=False
    points_layer = itk_napari_conversion.points_layer_from_point_set(point_set, reverse_coords=False)

    # Check that data is NOT reversed
    assert np.allclose(points_data, points_layer.data)


def test_point_set_from_points_layer_no_reverse():
    """Test point_set_from_points_layer with reverse_coords=False."""
    # Create napari points layer
    data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    points_layer = napari.layers.Points(data)

    # Convert to ITK point set with reverse_coords=False
    point_set = itk_napari_conversion.point_set_from_points_layer(points_layer, reverse_coords=False)

    # Check points are NOT reversed
    points_array = itk.array_from_vector_container(point_set.GetPoints())
    assert np.allclose(data, points_array)


def test_roundtrip_itk_to_napari_to_itk():
    """Test roundtrip conversion from ITK to napari and back to ITK."""
    # Create a simple 3D point set with ITK coordinates (x,y,z)
    PointSetType = itk.PointSet[itk.F, 3]
    original_point_set = PointSetType.New()

    # Add some points with distinct x,y,z values for testing
    original_data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]], dtype=np.float32)
    points = itk.vector_container_from_array(original_data.flatten())
    original_point_set.SetPoints(points)

    # Convert ITK -> napari (reverses coords) -> ITK (reverses back)
    points_layer = itk_napari_conversion.points_layer_from_point_set(original_point_set)
    roundtrip_point_set = itk_napari_conversion.point_set_from_points_layer(points_layer)

    # Check that the roundtrip produces the original data
    roundtrip_array = itk.array_from_vector_container(roundtrip_point_set.GetPoints())
    assert np.allclose(original_data, roundtrip_array)


def test_roundtrip_napari_to_itk_to_napari():
    """Test roundtrip conversion from napari to ITK and back to napari."""
    # Create napari points layer with napari coordinates (z,y,x)
    original_data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    original_layer = napari.layers.Points(original_data)

    # Convert napari -> ITK (reverses coords) -> napari (reverses back)
    point_set = itk_napari_conversion.point_set_from_points_layer(original_layer)
    roundtrip_layer = itk_napari_conversion.points_layer_from_point_set(point_set)

    # Check that the roundtrip produces the original data
    assert np.allclose(original_data, roundtrip_layer.data)


def test_points_layer_from_point_set_2d():
    """Test points_layer_from_point_set with 2D points."""
    # Create a simple 2D point set
    PointSetType = itk.PointSet[itk.F, 2]
    point_set = PointSetType.New()

    # Add some points (ITK order: x,y)
    points_data = np.array([[1.0, 2.0], [4.0, 5.0], [7.0, 8.0]], dtype=np.float32)
    points = itk.vector_container_from_array(points_data.flatten())
    point_set.SetPoints(points)

    # Convert to napari points layer with default reverse_coords=True
    points_layer = itk_napari_conversion.points_layer_from_point_set(point_set)

    # Check that data is reversed (napari order: y,x)
    expected = points_data[:, ::-1]
    assert np.allclose(expected, points_layer.data)


def test_point_set_from_points_layer_2d():
    """Test point_set_from_points_layer with 2D points."""
    # Create napari points layer (napari order: y,x)
    data = np.array([[1.0, 2.0], [4.0, 5.0], [7.0, 8.0]])
    points_layer = napari.layers.Points(data)

    # Convert to ITK point set with default reverse_coords=True
    point_set = itk_napari_conversion.point_set_from_points_layer(points_layer)

    # Check points are reversed (ITK order: x,y)
    points_array = itk.array_from_vector_container(point_set.GetPoints())
    expected = data[:, ::-1]
    assert np.allclose(expected, points_array)

