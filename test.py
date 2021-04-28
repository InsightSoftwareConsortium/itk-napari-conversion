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
    image['wookies'] = 7
    image['units'] = 'mm'
    image_layer = itk_napari_conversion.image_layer_from_image(image)
    assert np.array_equal(data, image_layer.data)
    assert image_layer.metadata['wookies'] == 7
    assert image_layer.metadata['units'] == 'mm'

def test_image_layer_from_image_scale():
    data = np.random.randint(256, size=(10, 10), dtype=np.uint8)
    image = itk.image_view_from_array(data)
    spacing = [1.1, 2.2]
    image.SetSpacing(spacing)
    image_layer = itk_napari_conversion.image_layer_from_image(image)
    assert np.array_equal(data, image_layer.data)
    assert np.allclose(np.array(spacing)[::-1], image_layer.scale)
