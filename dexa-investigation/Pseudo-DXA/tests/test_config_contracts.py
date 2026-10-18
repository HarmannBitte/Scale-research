import ast
import configparser
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ConfigContractTests(unittest.TestCase):
    def test_perceptual_loss_config_layers_and_weights_are_aligned(self):
        config = configparser.ConfigParser()
        config.read(REPO_ROOT / "example.config")

        layers = ast.literal_eval(config["perceptual_loss"]["selected_layers"])
        weights = ast.literal_eval(config["perceptual_loss"]["selected_layer_weights"])

        self.assertEqual(len(layers), len(weights))
        self.assertNotIn(0, layers)
