"""
File Name: pseudo_DXA.py
Author: Lambert T Leong
Description: Code to create the Pseudo-DXA model
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.models import Model
from typing import Optional, Sequence

from utils import DXA_utils as dxa


class PseudoDXA(tf.keras.Model):
    def __init__(
        self,
        encoder: Model,
        generator: Model,
        build_loss_model: bool = False,
        selected_layers: Optional[Sequence[int]] = None,
        selected_layer_weights: Optional[Sequence[float]] = None,
        vgg_weights: Optional[str] = "imagenet",
    ):
        """
        PseudoDXA Model.

        Args:
            encoder (Model): Encoder model.
            generator (Model): Generator model.
            build_loss_model (bool): If True, build the VGG16 perceptual loss model
                during initialization. Keep False for inference.
            selected_layers (Sequence[int], optional): VGG16 layer indices used by
                the perceptual loss.
            selected_layer_weights (Sequence[float], optional): Per-layer loss weights.
            vgg_weights (str, optional): Weights argument passed to VGG16. Use None for
                offline tests or "imagenet" for training.
        """        
        super(PseudoDXA, self).__init__()
        assert isinstance(encoder, models.Model) and isinstance(generator, models.Model), \
            "Both encoder and generator must be instances of tf.keras.models.Model"
        self.encoder = encoder
        self.generator = generator
        self.selectedLayers = list(selected_layers) if selected_layers is not None else [
            1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18
        ]
        self.selected_layer_weights = (
            list(selected_layer_weights)
            if selected_layer_weights is not None
            else [.5, .75, .5, .5, .8, .8, .5, .5, .3, .3, .5, .5, .3, .8, .8, .5]
        )
        self.vgg_weights = vgg_weights
        self.lossModel = self.get_loss_model() if build_loss_model else None
    
    def build_model(self):
        """
        Build the PseudoDXA model by unrolling layers of encoder and generator.
        """
        self.encoder._name = 'mesh_encoder_ll'
        self.generator._name = 'dxa_generator_ll'
        inputs = layers.Input(shape=self.encoder.input_shape[1:], name='input_fitted_mesh')
        encoded = self.encoder(inputs)
        gen = self.generator(encoded)
        self.model = models.Model(inputs, gen)
    
    def freeze_generator(self, freeze: bool = True):
        """
        Freeze or unfreeze the generator's layers.

        Args:
            freeze (bool): If True, freeze the generator's layers. If False, unfreeze them.
        """
        self.generator.trainable = not freeze
        for layer in self.generator.layers:
            layer.trainable = not freeze
    
    def get_loss_model(self) -> Model:
        """
        Get the loss model for perceptual loss.

        Returns:
            Model: The loss model.
        """       
        if len(self.selectedLayers) != len(self.selected_layer_weights):
            raise ValueError(
                "selected_layers and selected_layer_weights must have the same length "
                f"({len(self.selectedLayers)} != {len(self.selected_layer_weights)})"
            )

        # Initialize VGG16 model
        lossModel = tf.keras.applications.VGG16(include_top=False, weights=self.vgg_weights)
        # Set the entire model as non-trainable
        lossModel.trainable = False
        for layer in lossModel.layers:
            layer.trainable = False
        # Extract outputs for each selected layer
        self.selectedOutputs = [lossModel.layers[i].output for i in self.selectedLayers]
        # Create a new model with multiple outputs
        return tf.keras.models.Model(inputs=lossModel.inputs, outputs=self.selectedOutputs)

    def _loss_model(self) -> Model:
        if self.lossModel is None:
            self.lossModel = self.get_loss_model()
        return self.lossModel

    def call(self, inputs):
        # Encode the inputs using the encoder
        latent_space = self.encoder(inputs)
        # Decode the latent space using the generator
        reconstructed = self.generator(latent_space)
        return reconstructed
    
    def perceptual_loss_leong(self, input_image: tf.Tensor, reconstruct_image: tf.Tensor) -> tf.Tensor:
        """
        Calculate the perceptual loss between an input image and its reconstruction.

        Args:
            input_image (tf.Tensor): The original input image.
            reconstruct_image (tf.Tensor): The reconstructed image.

        Returns:
            tf.Tensor: The calculated perceptual loss.
        """
        lossModel = self._loss_model()
        rc_loss = 0.0
        transform_loss = 0.0
        mse_loss=0.0
        # Process the images through the Hologic function
        #act_ims = self.process_raw_dxa(input_image)
        #rec_ims = self.process_raw_dxa(reconstruct_image)
        act_ims = self.transform_raw_dxa(input_image)
        rec_ims = self.transform_raw_dxa(reconstruct_image)
        #print(act_ims[0],'\n\n\n')
        #print(act_ims)
        #sys.exit(0)
        # Calculate transform loss for processed images
        for i in range(len(act_ims)):
            h1_list = lossModel(act_ims[i])  
            h2_list = lossModel(rec_ims[i])  
            for h1, h2, weight in zip(h1_list, h2_list, self.selected_layer_weights):
                h1 = tf.reshape(h1, [tf.shape(h1)[0], -1])
                h2 = tf.reshape(h2, [tf.shape(h2)[0], -1]) 
                transform_loss += weight * tf.reduce_sum(tf.abs(h1 - h2), axis=-1)
                mse_loss += tf.keras.losses.mean_squared_error(h1, h2)
        # 6 phase loss for the first three channels
        h1_list = lossModel(input_image[:,:,:,:3])
        h2_list = lossModel(reconstruct_image[:,:,:,:3])
        for h1, h2, weight in zip(h1_list, h2_list, self.selected_layer_weights):
            h1 = tf.reshape(h1, [tf.shape(h1)[0], -1])
            h2 = tf.reshape(h2, [tf.shape(h2)[0], -1])
            rc_loss += weight * tf.reduce_sum(tf.abs(h1 - h2), axis=-1)

        # 6 phase loss for the last three channels
        h1_list = lossModel(input_image[:,:,:,-3:])
        h2_list = lossModel(reconstruct_image[:,:,:,-3:])
        for h1, h2, weight in zip(h1_list, h2_list, self.selected_layer_weights):
            h1 = tf.reshape(h1, [tf.shape(h1)[0], -1])
            h2 = tf.reshape(h2, [tf.shape(h2)[0], -1])
            rc_loss += weight * tf.reduce_sum(tf.abs(h1 - h2), axis=-1)
        
        return (rc_loss*.2)+(transform_loss*.5) + (mse_loss)
    
    def transform_raw_dxa(self, input_image: tf.Tensor):
        """
        Transform raw DXA image data.

        The expected channel order is:
        air high, air low, bone high, bone low, tissue high, tissue low.

        Args:
            input_image (tf.Tensor): Input DXA image.

        Returns:
            Tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]: Transformed images.
        """
        return dxa.transform_raw_dxa(input_image)
