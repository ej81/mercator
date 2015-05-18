import unittest
import numpy as np
from scale import MercatorScale

class MercatorScaleTest(unittest.TestCase):

    def setUp(self):
        self.maxlat = 88
        self.scale = MercatorScale(None, maxlat=self.maxlat)
        self.trans = self.scale.get_transform()
        self.invtrans = self.trans.inverted()

    def testTransform(self):
        original = np.arange(-self.maxlat, self.maxlat, 0.1)
        transformed = self.trans.transform_non_affine(original)
        inverse = self.invtrans.transform_non_affine(transformed)
        
        for lat1, lat2 in zip(original, inverse):
            self.assertAlmostEqual(lat1, lat2)

if __name__ == '__main__':
    unittest.main()
