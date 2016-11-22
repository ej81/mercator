"""Axis transform for spherical Mercator projection in matplotlib."""

__author__ = "Eric Jansen"
__email__ = "eric.jansen@cmcc.it"

import numpy as np
from matplotlib.ticker import AutoLocator
from matplotlib.transforms import Transform
from matplotlib.scale import ScaleBase
from ticker import DegreeFormatter


class MercatorScale(ScaleBase):
    name = 'mercator'

    def __init__(self, axis, **kwargs):
        """
        Create a new scale instance.

        Parameters
        ----------
        maxlat : float, optional, default: 85.0511287798066
            Largest latitude allowed to be drawn. In the Mercator projection a
            latitude of 90 degrees transforms into infinity. To avoid drawing
            issues, all values outside of a predefined range [-maxlat, maxlat]
            will be masked.
        """
        ScaleBase.__init__(self)
        self.maxlat = kwargs.pop('maxlat', 85.0511287798066)

    def get_transform(self):
        return self.MercatorLatitudeTransform(self.maxlat)

    def set_default_locators_and_formatters(self, axis):
        axis.set_major_locator(AutoLocator())
        axis.set_major_formatter(DegreeFormatter())

    def limit_range_for_scale(self, vmin, vmax, minpos):
        return max(vmin, -self.maxlat), min(vmax, self.maxlat)

    class MercatorLatitudeTransform(Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, maxlat):
            Transform.__init__(self)
            self.maxlat = maxlat

        def transform(self, lat):
            try:
                return Transform.transform(self, lat)
            except NotImplementedError:
                return self.transform_non_affine(lat)

        def transform_non_affine(self, lat):
            lat = np.ma.masked_where((lat < -self.maxlat) | (lat > self.maxlat), lat)
            if not lat.mask.any():
                lat = lat.data

            return np.degrees(np.arctanh(np.sin(np.radians(lat))))

        def inverted(self):
            return MercatorScale.InvertedMercatorLatitudeTransform(self.maxlat)

    class InvertedMercatorLatitudeTransform(Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, maxlat):
            Transform.__init__(self)
            self.maxlat = maxlat 

        def transform(self, lat):
            try:
                return Transform.transform(self, lat)
            except NotImplementedError:
                return self.transform_non_affine(lat)

        def transform_non_affine(self, y):
            return np.degrees(np.arctan(np.sinh(np.radians(y))))

        def inverted(self):
            return MercatorScale.MercatorLatitudeTransform(self.maxlat)
