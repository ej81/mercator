# Spherical Mercator projection for matplotlib

## Prerequisites
1. matplotlib
2. numpy
3. gdal (optional, for clipping shapefiles)

## Installation
An installation script is not yet available. To install this package, just
download the source with ```git clone https://github.com/ej81/mercator.git```.
Place the directory ```mercator/``` directly inside the project that you are
working on or set the environment variable ```$PYTHONPATH``` to point to it.

For example:
```
mkdir $HOME/python
cd $HOME/python
git clone https://github.com/ej81/mercator.git
export PYTHONPATH=$HOME/python:$PYTHONPATH
```

## Map data
In order to display the coastline in your figures, you need to download the
GSHHS database in ESRI shapefile format from
[http://www.soest.hawaii.edu/pwessel/gshhg/]. The files should be placed inside
the package directory in the subdirectory `data/`. 

If you are only interested in a small region, performance can be increased by
clipping the shapefiles to roughly the correct area. For example for the
Mediterranean Sea you can do:

```
for res in f h l i c; do
  ogr2ogr medsea_${res}.shp ${res}/GSHHS_${res}_L1.shp -clipsrc -20 15 50 60
done
```

Then you can do ```ax.coastline('medsea_f.shp')``` instead of
```ax.coastline('GSHHS_f_L1.shp')```. Especially for the higher resolutions
this should make a big difference.

## Examples

### Plotting locations on a map
Create a file ```places.txt``` with your favourite cities:
```
# latitude,longitude,name
52.366667,4.9,Amsterdam
51.507222,-0.1275,London
48.8567,2.3508,Paris
52.516667,13.383333,Berlin
```
Then run the following code to plot:
```
import mercator
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(facecolor='white')
axes = plt.axes(projection='mercator', minutes=True)
axes.coastline('GSHHS_i_L1.shp')
fig.add_axes(axes)

plt.title("Places where I've been")

data = np.genfromtxt('places.txt', delimiter=',', usecols=(0,1,2), dtype=None)
for lat, lon, name in data:
    plt.plot(lon, lat, 'r', marker=mercator.marker.pin, ms=25)
    plt.annotate(name, xy=[lon,lat], xytext=(0, -15), textcoords='offset points', ha='center')

plt.savefig('places.pdf')
plt.show()
```


