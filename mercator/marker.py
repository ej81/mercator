"""Google Maps style pin marker for matplotlib."""

__author__ = "Eric Jansen"
__email__ = "eric@xyrion.org"

from matplotlib.path import Path


pin = Path([[-1.0, 2.0],
            [-1.0, 2.55], [-0.55, 3.0], [0.0, 3.0], 
            [0.55, 3.0], [1.0, 2.55], [1.0, 2.0], 
            [1.0, 1.45], [0.0, 0.55], [0.0, 0.0], 
            [0.0, 0.55], [-1.0, 1.45], [-1.0, 2.0], 
            [-1.0, 2.0]] +
           [[0.5, 2.0], 
            [0.5, 2.275], [0.275, 2.5], [0.0, 2.5], 
            [-0.275, 2.5], [-0.5, 2.275], [-0.5, 2.0], 
            [-0.5, 1.725], [-0.275, 1.5], [0.0, 1.5], 
            [0.275, 1.5], [0.5, 1.725], [0.5, 2.0], 
            [0.5, 2.0]],
           [Path.MOVETO, 
            Path.CURVE4, Path.CURVE4, Path.CURVE4, 
            Path.CURVE4, Path.CURVE4, Path.CURVE4, 
            Path.CURVE4, Path.CURVE4, Path.CURVE4, 
            Path.CURVE4, Path.CURVE4, Path.CURVE4, 
            Path.CLOSEPOLY] +
           [Path.MOVETO, 
            Path.CURVE4, Path.CURVE4, Path.CURVE4,
            Path.CURVE4, Path.CURVE4, Path.CURVE4, 
            Path.CURVE4, Path.CURVE4, Path.CURVE4, 
            Path.CURVE4, Path.CURVE4, Path.CURVE4, 
            Path.CLOSEPOLY])
