import importlib.util
import unittest

if importlib.util.find_spec("numpy") is None:
    raise unittest.SkipTest("numpy is not installed")
if importlib.util.find_spec("tensorflow") is None:
    raise unittest.SkipTest("tensorflow is not installed")
if importlib.util.find_spec("plyfile") is None:
    raise unittest.SkipTest("plyfile is not installed")

import numpy as np
import tensorflow as tf

from modeling.dxa_generator import DXAGenerator
from modeling.mesh_encoder import MeshEncoder
from modeling.pseudo_DXA import PseudoDXA
from utils.mesh_utils import sample_points_uniform


class TensorFlowContractTests(unittest.TestCase):
    def test_mesh_encoder_is_deterministic_by_default(self):
        encoder = MeshEncoder(latent_dim=8, num_pts=16, dropout_rate=0.0).model
        mesh = np.ones((1, 16, 3), dtype=np.float32)

        first = encoder(mesh, training=False).numpy()
        second = encoder(mesh, training=False).numpy()

        np.testing.assert_allclose(first, second)


    def test_generator_output_geometry(self):
        generator = DXAGenerator(reshape_dim=(5, 4, 512), upscale=2).model
        latent = np.zeros((1, 5 * 4 * 512), dtype=np.float32)

        output = generator(latent, training=False)

        self.assertEqual(tuple(output.shape[1:]), (150, 109, 6))


    def test_loss_layer_weights_align_without_instantiating_vgg(self):
        encoder = tf.keras.Sequential([tf.keras.layers.Input((16, 3)), tf.keras.layers.Flatten(), tf.keras.layers.Dense(8)])
        generator = tf.keras.Sequential([tf.keras.layers.Input((8,)), tf.keras.layers.Dense(150 * 109 * 6), tf.keras.layers.Reshape((150, 109, 6))])

        psdxa = PseudoDXA(encoder, generator)

        self.assertIsNone(psdxa.lossModel)
        self.assertEqual(len(psdxa.selectedLayers), len(psdxa.selected_layer_weights))


    def test_uniform_sampling_respects_requested_count(self):
        mesh = np.arange(30, dtype=np.float32).reshape(10, 3)

        sampled = sample_points_uniform([mesh], tot_pts=10, perc=0.5)

        self.assertEqual(sampled.shape, (1, 5, 3))
