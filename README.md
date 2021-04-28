# itk-napari-conversion

[![PyPI](https://img.shields.io/pypi/v/itk_napari_conversion.svg)](https://pypi.python.org/pypi/itk_napari_conversion)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/InsightSoftwareConsortium/itk-napari-conversion/blob/master/LICENSE)

Convert between [itk](https://itk.org) and [napari](https://napari.org) data structures.

Installation
------------

```
pip install itk-napari-conversion
```

Usage
-----

Convert an `itk.Image` to an `napari.layers.Image`:

```
from itk_napari_conversion import image_from_layer

image_layer = image_layer_from_image(image)
```

Convert to an `napari.layers.Image` to an `itk.Image`:
```
from itk_napari_conversion import image_from_image_layer

image = image_from_image_layer(image_layer)
```
