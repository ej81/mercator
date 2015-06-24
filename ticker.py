"""Axis label formatter for latitude/longitude (decimal or minutes)."""

__author__ = "Eric Jansen"
__email__ = "eric.jansen@cmcc.it"

import math
from matplotlib.ticker import Formatter, MaxNLocator

class DegreeFormatter(Formatter):
    """
    Formatter for latitude/longitude values.
    """

    def __init__(self, **kwargs):
        """
        Create a new formatter instance.

        Parameters
        ----------
        labels : array, optional
            Labels for denoting negative and positive values on this axis, e.g.
            ['W','E'] for a horizontal axis or ['S','N'] for a vertical axis.
            Without labels negative degrees are displayed.
        minutes : bool, optional, default: False
            Express axis scales in degrees and arcminutes instead of in decimal
            degrees.
        """
        try:
            Formatter.__init__(self)
        except AttributeError:
            pass

        self.labels = kwargs.pop('labels', None)
        self.minutes = kwargs.pop('minutes', False)

    def __call__(self, x, pos=None):
        dec = abs(x) % 1
        mnt = dec * 60 if dec > 1e-10 else 0
        if x == 0 or self.labels == None:
            return '%g%s' % (x, unichr(176))
        elif not self.minutes or mnt == 0:
            return '%g%s%s' % (abs(x), unichr(176), self.labels[0 if x < 0 else 1])
        else:
            return "%d%s%g'%s" % (int(abs(x)), unichr(176), mnt, self.labels[0 if x < 0 else 1])

class MinuteLocator(MaxNLocator):
    """
    Tick locator for degree-arcminute axes.
    """

    def __init__(self):
        """
        Create a new locator instance.
        """
        # Select divisions that are round minutes
        MaxNLocator.__init__(self, nbins=8, steps=[1, 5/3., 10/3., 5, 10])
