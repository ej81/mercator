# Spherical Mercator projection for matplotlib

## Prerequisites
1. matplotlib [http://matplotlib.org]
2. numpy [http://numpy.org]
3. pyshp [https://github.com/GeospatialPython/pyshp]
4. gdal (optional, for clipping shapefiles)

## Installation
To install the package, clone the reposotory and use the ```setup.py``` script:

```
git clone https://github.com/ej81/mercator.git
cd mercator
python setup.py install
```

To automatically download the coastlines you can do:
```
python -c 'import mercator.data; mercator.data.download()'
```

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
    plt.annotate(name, xy=[lon,lat], xytext=(0, -15),
                 textcoords='offset points', ha='center')

plt.savefig('places.pdf')
plt.show()
```


