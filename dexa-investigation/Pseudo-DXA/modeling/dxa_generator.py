"""
File Name: dxa_generator.py
Author: Lambert T Leong
Description: Contains code to create the DXA generator
"""

import tensorflow as tf
from tensorflow.keras import layers
from functools import reduce
from typing import Tuple, Union


class ResizeBilinear(layers.Layer):
    """Bilinear resize layer with stable serialization across Keras versions."""

    def __init__(self, scale: int = 2, **kwargs):
        super().__init__(**kwargs)
        if scale <= 0:
            raise ValueError("scale must be a positive integer")
        self.scale = scale

    def call(self, inputs):
        input_shape = tf.shape(inputs)
        new_size = (input_shape[1] * self.scale, input_shape[2] * self.scale)
        return tf.image.resize(inputs, new_size, method=tf.image.ResizeMethod.BILINEAR)

    def compute_output_shape(self, input_shape):
        height = input_shape[1] * self.scale if input_shape[1] is not None else None
        width = input_shape[2] * self.scale if input_shape[2] is not None else None
        return input_shape[0], height, width, input_shape[3]

    def get_config(self):
        config = super().get_config()
        config.update({"scale": self.scale})
        return config


class DXAGenerator(tf.keras.Model):
    def __init__(self, reshape_dim: Tuple[int, int, int], upscale: int, model_path: Union[None, str] = None):
        """
        DXA Image Generator Model.

        Args:
            reshape_dim (Tuple[int, int, int]): Dimensions to reshape the input.
            upscale (int): Upscaling factor for the generated image.
            model_path (Union[None, str]): Path to a pre-trained model if available, otherwise None.
        """
        super(DXAGenerator, self).__init__()
        
        self.reshape_dim = reshape_dim
        self.upscale = upscale
        self.latent_dim = reduce(lambda x, y: x * y, reshape_dim)
        self.gen_input = layers.Input(shape=(self.latent_dim,))
        
        if not model_path: 
            self.get_generator()
        else:
            from tensorflow import keras
            self.model = keras.models.load_model(
                model_path,
                custom_objects={"tf": tf, "ResizeBilinear": ResizeBilinear},
            )

    def get_generator(self):
        """
        Build the DXA image generator model.
        """
        x = layers.Reshape(target_shape=self.reshape_dim)(self.gen_input)
        x = layers.PReLU(shared_axes=[1, 2])(x)
        filters = self.reshape_dim[2]
        if filters < 1:
            raise ValueError("reshape_dim channel count must be positive")
        
        for i in range(5):
            if filters < 1:
                raise ValueError("generator filter count reached zero; reduce upscale or increase reshape_dim channels")
            x = layers.Conv2D(filters, (1, 1), padding="same")(x)
            if i != 0:
                x = layers.Conv2D(filters, (1, 2), padding="same")(x)
            x = layers.PReLU(shared_axes=[1, 2])(x)
            x = self.tf_resize(self.upscale)(x)
            x = layers.Conv2D(filters, (2, 2), padding="same")(x)
            x = layers.PReLU(shared_axes=[1, 2])(x)
            x = layers.Conv2D(filters, (4, 4), padding="same")(x)
            x = layers.PReLU(shared_axes=[1, 2])(x)
            
            if i > 2:
                x = layers.Conv2D(filters, (8, 8), padding="same")(x)
                x = layers.PReLU(shared_axes=[1, 2])(x)
            filters //= self.upscale
        
        if filters < 1:
            raise ValueError("generator final filter count reached zero; reduce upscale or increase reshape_dim channels")
        x = layers.Conv2D(filters, (8, 8), padding="same")(x)
        x = layers.Cropping2D(cropping=((5, 5), (9, 10)))(x)
        x = layers.Conv2D(6, (1, 1), padding="same")(x)
        self.model = tf.keras.models.Model(self.gen_input, x, name="dxa_gen")
    
    def tf_resize(self, scale: int = 2) -> ResizeBilinear:
        """
        Custom TensorFlow layer for resizing.

        Args:
            scale (int): Upscaling factor.

        Returns:
            ResizeBilinear: Bilinear resizing layer.
        """
        return ResizeBilinear(scale=scale)
