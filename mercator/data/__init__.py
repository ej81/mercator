import os
import sys
import zipfile

try:
    from urllib import urlretrieve
except ImportError:
    from urllib.request import urlretrieve


DEFAULT_SOURCE= [
    'http://www.soest.hawaii.edu/pwessel/gshhg/gshhg-shp-2.3.4.zip',
    'http://ej81.github.io/mercator/medsea_shp.zip',
    'http://ej81.github.io/mercator/blacksea_shp.zip'
]


def _progress(count, size, total):
    pct = (100 * count * size) / total
    sys.stdout.write('\b' * 4)
    sys.stdout.write('%3d%%' % pct)
    sys.stdout.flush()


def download(source=None):
    """
    Download coastline data.

    Parameters
    ----------
    source : str, list
        One or more URLs to download. Each URL is expected to point to a .zip
        file containing one or more .shp coastline files.
    """

    if not source:
        source = DEFAULT_SOURCE
    if isinstance(source, str):
        source = [source]

    path = os.path.dirname(__file__)

    if not os.access(path, os.W_OK):
        raise RuntimeError('directory "%s" is not writable (did you forget sudo?)' % path)

    for url in source:
        filename = None
        error = None

        try:
            sys.stdout.write('%-72s ' % url)
            filename, response = urlretrieve(url, reporthook=_progress)
            if getattr(response, 'status', '') != '':
                error = response.status
        except Exception as e:
            error = str(e)
        finally:
            sys.stdout.write('\n')
        
        if error:
            raise Warning('could not download "%s": %s' % (url, error))
            continue

        try:
            archive = zipfile.ZipFile(filename)
            archive.extractall(path)
            archive.close()
        except Exception as e:
            raise Warning('could not unpack "%s": %s' % (url, e))
        finally:
            if filename:
                os.unlink(filename)

