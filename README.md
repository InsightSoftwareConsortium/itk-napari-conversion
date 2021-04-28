# itk-napari-conversion

[![PyPI](https://img.shields.io/pypi/v/itk_napari_conversion.svg)](https://pypi.python.org/pypi/itk_napari_conversion)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/InsightSoftwareConsortium/itk-napari-conversion/blob/master/LICENSE)

Convert between itk and napari data structures.

Installation
------------

```
pip install itk-napari-conversion
```

Usage
-----

Convert an `itk.Image` to an `napari.layers.Image`:

```
import itk_napari_conversion

image_layer = itk_napari_conversion.image_from_image_layer(image)
```

Convert to an `napari.layers.Image` to an `itk.Image`:
```
import itk_napari_conversion

image = itk_napari_conversion.image_layer_from_image(image_layer)
```
