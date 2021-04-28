"""Convert between itk and napari data structures."""

__version__ = "0.2.0"

__all__ = ['image_layer_from_image',]

import napari
import itk
import numpy as np

def image_layer_from_image(image):
    rgb = False
    if isinstance(image, itk.Image):
        PixelType = itk.template(image)[1][0]
        if PixelType is itk.RGBPixel[itk.UC] or PixelType is itk.RGBAPixel[itk.UC]:
            rgb = True

    metadata = dict(image)
    scale = image['spacing']

    data = itk.array_view_from_image(image)
    image_layer = napari.layers.Image(data, rgb=rgb, metadata=metadata,
            scale=scale)
    return image_layer
