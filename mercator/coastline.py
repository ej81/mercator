"""Coastline polygons read from an ESRI shapefile, for plotting with matplotlib."""

__author__ = "Eric Jansen"
__email__ = "eric@xyrion.org"

import os
import shapefile
import warnings
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import Polygon


def _find(name, path):
    if os.path.isfile(os.path.join(path, name)):
        return os.path.join(path, name)
    else:
        name = os.path.basename(name)
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
    return None


def _split(points, parts):
    num = len(parts)

    if num > 1:
        result = []
        for index in range(0, num):
            start = parts[index]
            if index < num-1:
                end = parts[index+1]
            else:
                end = -1
            result += [points[start:end]]
        return result
    else:
        return [points]


class Coastline(Polygon):
    """
    Coastline background polygon. Clips itself to the axes when drawn.
    """

    def __init__(self, filename, **kwargs):
        """
        Create a new coastline polygon.

        Parameters
        ----------
        color : color, optional, default 'gray'
            Line color of the coastline.
        land : color, optional, default 'seashell'
            Fill color of the land polygons.

        Other parameters
        ----------------
        kwargs : polygon properties
            Other parameters passed on to :class:`~matplotlib.patches.Polygon`,
            e.g. zorder=N to control drawing the land polygons above/below
            other data.
        """
        color = kwargs.pop('color', 'gray')
        land = kwargs.pop('land', 'seashell')
        self.data = []
        self.extents = None

        if not color:
            color = 'none'
        if not land:
            land = 'none'

        xy = [[None, None], [None, None]]
        Polygon.__init__(self, xy, edgecolor=color, facecolor=land, **kwargs)

        datapath = os.path.join(os.path.dirname(__file__), 'data')
        coastfile = _find(filename, datapath)
        if coastfile:
            file = shapefile.Reader(coastfile)
            for shape in file.shapes():
                for points in _split(shape.points, shape.parts):
                    self.data += [Path(points)]
        else:
            raise Warning('coastline "%s" not found in directory "%s"' % (filename, datapath))

    def draw(self, renderer):
        """
        Clip the polygons to the view limits and let the parent handle drawing.
        """
        bbox = self.axes.viewLim

        if not np.array_equal(bbox.get_points(), self.extents):
            self._visible = False
            xy = [[None, None], [None, None]]

            for path in self.data:
                try:
                    for point in path.clip_to_bbox(bbox).vertices:
                        xy += [point]
                        self._visible = True
                except ValueError:
                    pass

                if not np.array_equal(xy[-1], [None, None]):
                    xy += [[None, None]]

            self.set_xy(xy)
            self.extents = np.copy(bbox.get_points())

        return super(Coastline, self).draw(renderer)
