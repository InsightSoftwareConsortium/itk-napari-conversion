"""Convert between itk and napari data structures."""

__version__ = "0.3.0"

__all__ = ["image_layer_from_image", "image_from_image_layer"]

import napari
import itk
import numpy as np


def image_layer_from_image(image):
    """Convert an itk.Image to a napari.layers.Image."""
    rgb = False
    if isinstance(image, itk.Image):
        PixelType = itk.template(image)[1][0]
        if PixelType is itk.RGBPixel[itk.UC] or PixelType is itk.RGBAPixel[itk.UC]:
            rgb = True

    metadata = dict(image)
    scale = image["spacing"]
    translate = image["origin"]
    # Todo: convert the rotation matrix to angles, in degrees
    # rotate = image['direction']
    # https://github.com/InsightSoftwareConsortium/itk-napari-conversion/issues/7

    data = itk.array_view_from_image(image)
    image_layer = napari.layers.Image(
        data, rgb=rgb, metadata=metadata, scale=scale, translate=translate
    )
    return image_layer

def image_from_image_layer(image_layer):
    """Convert a napari.layers.Image to an itk.Image."""
    if image_layer.rgb and image_layer.data.shape[-1] in (3, 4):
        if image_layer.data.shape[-1] == 3:
            PixelType = itk.RGBPixel[itk.UC]
        else:
            PixelType = itk.RGBAPixel[itk.UC]
        image = itk.image_view_from_array(image_layer.data, PixelType)

    else:
        image = itk.image_view_from_array(image_layer.data)

    if image_layer.metadata is not None:
        for k, v in image_layer.metadata.items():
            image[k] = v

    if image_layer.scale is not None:
        image["spacing"] = image_layer.scale.astype(np.float64)

    if image_layer.translate is not None:
        image["origin"] = image_layer.translate.astype(np.float64)

    return image
