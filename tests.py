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


# https://github.com/InsightSoftwareConsortium/itk-napari-conversion/issues/7
# def test_image_layer_from_image_rotate():
# data = np.random.randint(256, size=(10, 10), dtype=np.uint8)
# image = itk.image_view_from_array(data)
# rotate = np.rot90(np.eye(2))
# image.SetDirection(rotate)
# image_layer = itk_napari_conversion.image_layer_from_image(image)
# assert np.array_equal(data, image_layer.data)
# assert np.allclose(rotation, image_layer.rotate)


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
