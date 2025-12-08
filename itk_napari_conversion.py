"""Convert between itk and napari data structures."""

__version__ = "0.5.1"

__all__ = [
    "image_layer_from_image",
    "image_from_image_layer",
    "points_layer_from_point_set",
    "point_set_from_points_layer",
]

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
    rotate = np.transpose(image['direction'])

    data = itk.array_view_from_image(image)
    image_layer = napari.layers.Image(
        data, rgb=rgb, metadata=metadata,
        scale=scale, translate=translate, rotate=rotate,
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

    if image_layer.rotate is not None:
        image["direction"] = np.ascontiguousarray(np.transpose(image_layer.rotate)).astype(np.float64)

    return image


def points_layer_from_point_set(point_set, reverse_coords=True):
    """Convert an itk.PointSet to a napari.layers.Points.

    Parameters
    ----------
    point_set : itk.PointSet
        The ITK PointSet to convert.
    reverse_coords : bool, optional
        If True (default), reverse the coordinate order from ITK's x,y,z
        to napari's z,y,x order.

    Returns
    -------
    napari.layers.Points
        The converted napari Points layer.
    """
    # Get points as numpy array
    number_of_points = point_set.GetNumberOfPoints()

    if number_of_points == 0:
        data = np.array([]).reshape(0, 3)  # Default to 3D empty array
    else:
        points_array = itk.array_from_vector_container(point_set.GetPoints())
        if reverse_coords:
            # Reverse coordinate order from ITK (x,y,z) to napari (z,y,x)
            data = points_array[:, ::-1]
        else:
            data = points_array

    # Get point data (features) if available
    point_data = point_set.GetPointData()
    features = None
    if point_data.Size() > 0:
        point_data_array = itk.array_from_vector_container(point_data)
        # Use first component as feature if it's a scalar
        if point_data_array.ndim == 1:
            features = {'feature': point_data_array}
        else:
            # If multi-component, use first component
            features = {'feature': point_data_array[:, 0] if point_data_array.shape[1] > 0 else point_data_array[:, 0:1].flatten()}

    points_layer = napari.layers.Points(
        data,
        features=features,
    )
    return points_layer


def point_set_from_points_layer(points_layer, reverse_coords=True):
    """Convert a napari.layers.Points to an itk.PointSet.

    Parameters
    ----------
    points_layer : napari.layers.Points
        The napari Points layer to convert.
    reverse_coords : bool, optional
        If True (default), reverse the coordinate order from napari's z,y,x
        to ITK's x,y,z order.

    Returns
    -------
    itk.PointSet
        The converted ITK PointSet.
    """
    # Apply transformations (rotate, scale, translate) to points
    data = points_layer.data.copy()  # Make a copy to avoid modifying original

    # Napari always has an affine that includes scale and translate
    # We need to apply it to get world coordinates
    # Apply transformations in order: scale, rotate, translate
    if points_layer.scale is not None:
        data = data * points_layer.scale
    if points_layer.rotate is not None:
        # Apply rotation matrix to each point
        rotate_matrix = np.asarray(points_layer.rotate)
        data = data @ rotate_matrix.T
    if points_layer.translate is not None:
        data = data + points_layer.translate

    # Determine dimension from data
    if len(data) == 0:
        dimension = 3  # Default to 3D
    else:
        dimension = data.shape[1]

    # Create ITK PointSet
    # Use float pixel type for point data by default
    PointSetType = itk.PointSet[itk.F, dimension]
    point_set = PointSetType.New()

    # Set points
    if len(data) > 0:
        if reverse_coords:
            # Reverse coordinate order from napari (z,y,x) to ITK (x,y,z)
            data = data[:, ::-1]
        points = itk.vector_container_from_array(data.astype(np.float32).flatten())
        point_set.SetPoints(points)

    # Set point data from features if available
    if points_layer.features is not None and len(points_layer.features) > 0:
        feature_keys = list(points_layer.features.keys())
        if len(feature_keys) > 0:
            # Use the first feature column as point data
            feature_name = feature_keys[0]

            # Handle both dict and DataFrame
            if hasattr(points_layer.features, 'iloc'):
                # It's a pandas DataFrame
                feature_data = points_layer.features[feature_name].values
            else:
                # It's a dict
                feature_data = points_layer.features[feature_name]

            if isinstance(feature_data, (list, np.ndarray)):
                feature_array = np.array(feature_data).astype(np.float32)
                if len(feature_array) > 0:
                    point_data = itk.vector_container_from_array(feature_array)
                    point_set.SetPointData(point_data)

    return point_set
