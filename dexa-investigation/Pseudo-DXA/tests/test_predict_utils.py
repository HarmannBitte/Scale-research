import importlib.util
import unittest

if importlib.util.find_spec("numpy") is None:
    raise unittest.SkipTest("numpy is not installed")
if importlib.util.find_spec("cv2") is None:
    raise unittest.SkipTest("cv2 is not installed")

import numpy as np

from predict import scale_to_uint8


class PredictUtilityTests(unittest.TestCase):
    def test_scale_to_uint8_handles_constant_image_without_dividing_by_zero(self):
        image = np.ones((3, 3), dtype=np.float32) * 7.0

        scaled = scale_to_uint8(image)

        self.assertEqual(scaled.dtype, np.uint8)
        self.assertTrue(np.all(scaled == 0))


    def test_scale_to_uint8_scales_dynamic_range(self):
        image = np.array([[1.0, 2.0], [3.0, 5.0]], dtype=np.float32)

        scaled = scale_to_uint8(image)

        self.assertEqual(scaled.min(), 0)
        self.assertEqual(scaled.max(), 255)
