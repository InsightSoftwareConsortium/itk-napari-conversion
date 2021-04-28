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
