# itk-napari-conversion

[![PyPI](https://img.shields.io/pypi/v/itk_napari_conversion.svg)](https://pypi.python.org/pypi/itk_napari_conversion)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/InsightSoftwareConsortium/itk-napari-conversion/blob/master/LICENSE)
[![tests](https://github.com/InsightSoftwareConsortium/itk-napari-conversion/actions/workflows/test_and_deploy.yml/badge.svg)](https://github.com/InsightSoftwareConsortium/itk-napari-conversion/actions/workflows/test_and_deploy.yml)

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
from itk_napari_conversion import image_layer_from_image

image_layer = image_layer_from_image(image)
```

Convert to an `napari.layers.Image` to an `itk.Image`:
```
from itk_napari_conversion import image_from_image_layer

image = image_from_image_layer(image_layer)
```

Hacking
-------

Contributions are welcome!

To test locally:

```
git clone https://github.com/InsightSoftwareConsortium/itk-napari-conversion.git
cd itk-napari-conversation
pip install flit pytest
flit install --symlink
pytest tests.py
```

Follow the [itk contributing
guidelines](https://github.com/InsightSoftwareConsortium/ITK/blob/master/CONTRIBUTING.md)
and the [itk code of
conduct](https://github.com/InsightSoftwareConsortium/ITK/blob/master/CODE_OF_CONDUCT.md).
