"""Package for fast and efficient plotting of scientific data on a world map."""

__author__ = "Eric Jansen"
__email__ = "eric@xyrion.org"

from matplotlib.scale import register_scale
from matplotlib.projections import register_projection

from .scale import MercatorScale
from .axes import MercatorAxes
from .marker import pin


register_projection(MercatorAxes)
register_scale(MercatorScale)
