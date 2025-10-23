# itk-napari-conversion

[![PyPI](https://img.shields.io/pypi/v/itk_napari_conversion.svg)](https://pypi.python.org/pypi/itk_napari_conversion)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/InsightSoftwareConsortium/itk-napari-conversion/blob/master/LICENSE)
[![tests](https://github.com/InsightSoftwareConsortium/itk-napari-conversion/actions/workflows/test_and_deploy.yml/badge.svg)](https://github.com/InsightSoftwareConsortium/itk-napari-conversion/actions/workflows/test_and_deploy.yml)

Convert between [itk](https://itk.org) and [napari](https://napari.org) data structures.

## Installation

```sh
pip install itk-napari-conversion
```

## Usage

### Image Conversion

#### Convert ITK Image to napari Image Layer

Convert an `itk.Image` to a `napari.layers.Image`:

```python
from itk_napari_conversion import image_layer_from_image

image_layer = image_layer_from_image(image)
```

**Features:**
- Automatically detects and handles RGB/RGBA images
- Preserves image metadata (spacing, origin, direction, custom metadata)
- Converts ITK's physical space information to napari's layer transformations:
  - `spacing` → `scale`
  - `origin` → `translate`
  - `direction` → `rotate`

**Example:**
```python
import itk
import napari
from itk_napari_conversion import image_layer_from_image

# Read an image
image = itk.imread('path/to/image.nrrd')

# Add custom metadata
image['units'] = 'mm'
image['patient_id'] = '12345'

# Convert to napari layer
image_layer = image_layer_from_image(image)

# The layer will have:
# - image_layer.scale = image spacing (in reverse order for NumPy)
# - image_layer.translate = image origin (in reverse order for NumPy)
# - image_layer.rotate = image direction matrix (in reverse order for NumPy)
# - image_layer.metadata = all custom metadata
```

#### Convert napari Image Layer to ITK Image

Convert a `napari.layers.Image` to an `itk.Image`:

```python
from itk_napari_conversion import image_from_image_layer

image = image_from_image_layer(image_layer)
```

**Features:**
- Automatically handles RGB/RGBA layers
- Converts napari layer transformations back to ITK physical space:
  - `scale` → `spacing`
  - `translate` → `origin`
  - `rotate` → `direction`
- Preserves all metadata from the layer

**Example:**
```python
import numpy as np
import napari
from itk_napari_conversion import image_from_image_layer

# Create a napari image layer with transformations
viewer = napari.Viewer()
data = np.random.rand(100, 100, 100)

# 45 degree rotation around z-axis
angle = np.radians(45)
rotate = np.array([
    [np.cos(angle), -np.sin(angle), 0],
    [np.sin(angle), np.cos(angle), 0],
    [0, 0, 1]
], dtype=np.float64)

layer = viewer.add_image(
    data,
    scale=[2.0, 1.5, 1.5],  # anisotropic spacing
    rotate=rotate,
    translate=[10.0, 20.0, 30.0],
    metadata={'description': 'My volume'}
)

# Convert to ITK
image = image_from_image_layer(layer)

# The ITK image will have:
# - spacing: coordinates in ITK order, so reversed from napari `scale`: [1.5, 1.5, 2.0]
# - origin: coordinates in ITK order, so reversed from napari `translate`: [30.0, 20.0, 10.0]
# The ITK image will have:
# - spacing: coordinates in ITK order, so reversed from napari `scale`: [1.5, 1.5, 2.0]
# - origin: coordinates in ITK order, so reversed from napari `translate`: [30.0, 20.0, 10.0]
# - direction: transpose of napari `rotate` matrix

# Access the direction matrix via dictionary access (recommended):
direction = image["direction"]
print(direction)
# [[0.70710678 0.70710678 0.        ]
#  [-0.70710678 0.70710678 0.        ]
#  [0.         0.         1.        ]]

# This is the transpose of napari's rotate matrix:
#   [[cos(45°), sin(45°), 0],
#    [-sin(45°), cos(45°), 0],
#    [0, 0, 1]]

# Note: image.GetDirection() may return a different matrix because it accesses
# the underlying ITK image metadata differently. Use dictionary access for
# consistency with how the direction was set.
```

### Point Set Conversion

#### Convert ITK PointSet to napari Points Layer

Convert an `itk.PointSet` to a `napari.layers.Points`:

```python
from itk_napari_conversion import points_layer_from_point_set

points_layer = points_layer_from_point_set(point_set)
```

**Features:**
- Extracts point coordinates from ITK PointSet using `itk.array_from_vector_container()`
- Converts point data (if present) to napari features dictionary
  - Uses the first component as the 'feature' key
- Returns a `napari.layers.Points` object

**Example:**
```python
import itk
import numpy as np
from itk_napari_conversion import points_layer_from_point_set

# Create ITK PointSet
PointSetType = itk.PointSet[itk.F, 3]
point_set = PointSetType.New()

# Add points
points_data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=np.float32)
points = itk.vector_container_from_array(points_data.flatten())
point_set.SetPoints(points)

# Add point data (features)
feature_data = np.array([10.0, 20.0], dtype=np.float32)
point_data = itk.vector_container_from_array(feature_data)
point_set.SetPointData(point_data)

# Convert to napari
points_layer = points_layer_from_point_set(point_set)
# points_layer.features['feature'] will contain [10.0, 20.0]
```

#### Convert napari Points Layer to ITK PointSet

Convert a `napari.layers.Points` to an `itk.PointSet`:

```python
from itk_napari_conversion import point_set_from_points_layer

point_set = point_set_from_points_layer(points_layer)
```

**Features:**
- Applies napari transformations (scale, rotate, translate) to point coordinates before conversion
- Extracts points from napari layer data
- Converts the first feature column (if present) to ITK point data
- Returns an `itk.PointSet` object with dimension determined from the data

**Example:**
```python
import napari
import numpy as np
from itk_napari_conversion import point_set_from_points_layer

# Create napari Points layer with transformations
data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
features = {'intensity': np.array([10.0, 20.0])}
scale = np.array([2.0, 2.0, 2.0])
translate = np.array([100.0, 200.0, 300.0])

# Optional: add rotation (90 degrees around z-axis)
angle = np.radians(90)
rotate = np.array([
    [np.cos(angle), -np.sin(angle), 0],
    [np.sin(angle), np.cos(angle), 0],
    [0, 0, 1]
])

points_layer = napari.layers.Points(
    data,
    features=features,
    scale=scale,
    rotate=rotate,
    translate=translate
)

# Convert to ITK PointSet
point_set = point_set_from_points_layer(points_layer)

# The points in the ITK PointSet will be in world coordinates:
# ((data * scale) @ rotate.T) + translate
# Point data will be stored from the 'intensity' feature
```

### Transformation Handling

#### Images
- **ITK → napari**: Physical space metadata (spacing, origin, direction) is converted to napari layer transformations
- **napari → ITK**: Layer transformations are converted back to ITK physical space metadata

#### Points
- **ITK → napari**: Points are copied as-is without transformations (identity transform assumed)
- **napari → ITK**: Layer transformations (scale, rotate, translate) are **applied to points** to convert them to world coordinates
  - Transformations are applied in order: scale → rotate → translate

### Notes

**Images:**
- Supports 2D, 3D, and multi-dimensional images
- RGB and RGBA images are automatically detected and handled
- Axis order is automatically reversed between ITK (x, y, z) and NumPy/napari (z, y, x)
- Metadata is preserved bidirectionally

**Points:**
- Point data in ITK is stored as float32
- Only the first feature column from napari is used for ITK point data
- Empty point sets are handled gracefully
- Dimension is automatically determined from the point data shape
- Metadata conversion is not currently supported for point sets

## Hacking
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
