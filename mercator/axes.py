"""Implementation of a spherical Mercator projection in matplotlib."""

__author__ = "Eric Jansen"
__email__ = "eric@xyrion.org"

import math
from matplotlib.axes import Axes
from matplotlib.ticker import AutoLocator

from .ticker import DegreeFormatter, MinuteLocator
from .coastline import Coastline


class MercatorAxes(Axes):
    name = 'mercator'

    def __init__(self, *args, **kwargs):
        """
        Create a new axes instance.

        Parameters
        ----------
        maxlat : float, optional, default: 85.0511287798066
            Largest latitude allowed to be drawn. In the Mercator projection a
            latitude of 90 degrees transforms into infinity. To avoid drawing
            issues, all values outside of a predefined range [-maxlat, maxlat]
            will be masked.
        minutes : bool, optional, default: False
            Express axis scales in degrees and arcminutes instead of in decimal
            degrees. This changes both the position and formatting of the axes.

        Other parameters
        ----------------
        kwargs : axes properties
            Passed on to :class:`~matplotlib.Axes`.
        """
        self.maxlat = kwargs.pop('maxlat', 85.0511287798066)
        self.minutes = kwargs.pop('minutes', False)

        Axes.__init__(self, *args, **kwargs)

    def cla(self):
        """
        Initialise object to default values.
        """
        Axes.cla(self)
        self.set_aspect('equal', adjustable='datalim', anchor='C')
        self.set_yscale('mercator')
        self.grid(which='both')
        self.xaxis.set_major_formatter(DegreeFormatter(labels=['W', 'E'], minutes=self.minutes))
        self.yaxis.set_major_formatter(DegreeFormatter(labels=['S', 'N'], minutes=self.minutes))
        self.xaxis.set_major_locator(MinuteLocator() if self.minutes else AutoLocator())
        self.yaxis.set_major_locator(MinuteLocator() if self.minutes else AutoLocator())

    def coastline(self, filename, **kwargs):
        """
        Draw the coastline as a background to the data.

        Parameters
        ----------
        filename : str
            ESRI shapefile (located under data/) to use for the coastline.
        sea : color, optional, default: 'lightblue'
            Background fill color (sea color).
        zorder: int, optional, default: -1
            Place of the coastline polygons in the drawing order. Use positive
            values to make filled land polygons overlap data.

        Other parameters
        ----------------
        kwargs : coastline properties
            Passed on to :class:`~mercator.coastline.Coastline`.
        """
        sea = kwargs.pop('sea', 'lightblue')
        if sea:
            try:
                # matplotlib >= 2.0
                self.set_facecolor(sea)
            except AttributeError:
                # matplotlib < 2.0
                self.set_axis_bgcolor(sea)

        zorder = kwargs.pop('zorder', -1)
        coastline = Coastline(filename, zorder=zorder, **kwargs)
        self.add_patch(coastline)

    def get_fig_ratio(self, position=None):
        """
        Returns the figure aspect ratio.
        """
        if not position:
            position = self.get_position(original=True)
        xsize, ysize = position.size
        width, height = self.get_figure().get_size_inches()

        return (xsize / ysize) * (width / height)

    def apply_aspect(self, position=None):
        """
        Change the axes bounds to achieve the desired aspect ratio.
        """
        aspect = self.get_aspect()
        if aspect == 'auto':
            return
        elif aspect == 'equal':
            aspect = 1

        xtrans = self.xaxis.get_transform()
        ytrans = self.yaxis.get_transform()
        xbound = self.get_xbound()
        ybound = self.get_ybound()
        xmin, xmax = xtrans.transform(xbound[0]), xtrans.transform(xbound[1])
        ymin, ymax = ytrans.transform(ybound[0]), ytrans.transform(ybound[1])
        xsize = max(math.fabs(xmax - xmin), 1e-30)
        ysize = max(math.fabs(ymax - ymin), 1e-30)

        factor = (self.get_fig_ratio(position) * aspect) / (xsize / ysize)

        if (self._autoscaleXon and factor >= 1) or not self._autoscaleYon or self in self._shared_y_axes:
            xmin -= (xsize * (factor - 1))/2
            xmax += (xsize * (factor - 1))/2
            self.set_xbound(xtrans.inverted().transform(xmin),
                            xtrans.inverted().transform(xmax))
        elif (self._autoscaleYon and factor < 1) or not self._autoscaleXon or self in self._shared_x_axes:
            factor = 1/factor
            ymin -= (ysize * (factor - 1))/2
            ymax += (ysize * (factor - 1))/2
            self.set_ybound(ytrans.inverted().transform(ymin),
                            ytrans.inverted().transform(ymax))
        else:
            warnings.warn("both axes are shared or have autoscale disabled, unable to set aspect ratio")
            return

    def _update_patch_limits(self, patch):
        if (isinstance(patch, Coastline)):
            # Coastline should not affect limits
            return
        else:
            Axes._update_patch_limits(self, patch)
