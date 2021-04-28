"""Convert between itk and napari data structures."""

__version__ = "0.1.0"

__all__ = ['image_layer_from_image',]

import napari
import itk
import numpy as np

def image_layer_from_image(image):
    data = itk.array_view_from_image(image)
    image_layer = napari.layers.Image(data)
    return image_layer
