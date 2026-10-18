"""
File Name: DXA_utils.py
Author: Lambert T Leong
Description: Contains DXA utility functions
"""

import random as rnd
import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from typing import List

def load_npys(list_of_paths: List[str]) -> np.ndarray: ### system has 1TB or RAM. Use flow from methods on smaller systems
    """
    Load and stack NumPy arrays from a list of file paths.

    Args:
        list_of_paths (List[str]): List of file paths to load NumPy arrays from.

    Returns:
        np.ndarray: Stacked NumPy arrays.
    """
    out = []
    pad=np.zeros((150,1,6))
    for i in list_of_paths:
        npy=np.load(i)/16383
        npy= npy[:,:,:]
        out+=[npy]
    out = np.stack(out)
    return out

### AUGMENTATION FUNC FOR DXA ###
def random_blackout(image,min_channels=4,boxmin=5,boxmax=75):
    black_height, black_width = rnd.randint(boxmin,boxmax),rnd.randint(boxmin,boxmax)
    blackbox_one = np.ones((black_height, black_width))
    im_height, im_width, num_channels = image.shape
    height, width = im_height, im_width
    channel_list = rnd.sample(range(num_channels),rnd.randint(min_channels,num_channels))
    for ch in channel_list:
        black_height, black_width = rnd.randint(boxmin,boxmax),rnd.randint(boxmin,boxmax)
        blackbox_one = np.ones((black_height, black_width))
        height_bound, width_bound = im_height-black_height, im_width-black_width
        while height > (height_bound) and width > (width_bound):
            height, width = rnd.randint(0,height_bound), rnd.randint(0,width_bound)
        flat=image[height:height+black_height,width:width+black_width,ch].flatten()
        np.random.shuffle(flat)
        image[height:height+black_height,width:width+black_width,ch]=flat.reshape((black_height, black_width))
        height,width = im_height,im_width
    return image 

### GEN DXA R IMAGES ###
def transform_raw_dxa(input_image: tf.Tensor):
    """
    Transform six-channel DXA attenuation data into R-value/high/low image triplets.

    Expected channel order:
    air high, air low, bone high, bone low, tissue high, tissue low.

    The bone and tissue channels are air-background corrected once. Derived
    mixed-phase images are then built from those corrected line-integral terms.

    Args:
        input_image (tf.Tensor): 4D image tensor with six attenuation channels.

    Returns:
        Tuple[tf.Tensor, ...]: air, tissue, and bone R/high/low triplets.
    """
    if input_image.shape[-1] is not None and input_image.shape[-1] != 6:
        raise ValueError("transform_raw_dxa expects a 6-channel DXA tensor")

    min_clip = 1 / (2 ** 14 - 1)

    air_hi_raw, air_lo_raw = input_image[..., 0], input_image[..., 1]
    bone_hi_raw, bone_lo_raw = input_image[..., 2], input_image[..., 3]
    tissue_hi_raw, tissue_lo_raw = input_image[..., 4], input_image[..., 5]

    air_hi = tf.clip_by_value(air_hi_raw, min_clip, 1.0)
    air_lo = tf.clip_by_value(air_lo_raw, min_clip, 1.0)

    bone_hi = tf.clip_by_value(bone_hi_raw - air_hi_raw, min_clip, 1.0)
    bone_lo = tf.clip_by_value(bone_lo_raw - air_lo_raw, min_clip, 1.0)
    tissue_hi = tf.clip_by_value(tissue_hi_raw - air_hi_raw, min_clip, 1.0)
    tissue_lo = tf.clip_by_value(tissue_lo_raw - air_lo_raw, min_clip, 1.0)

    air_bone_hi = tf.clip_by_value(air_hi_raw + (bone_hi_raw - air_hi_raw), min_clip, 1.0)
    air_bone_lo = tf.clip_by_value(air_lo_raw + (bone_lo_raw - air_lo_raw), min_clip, 1.0)
    air_tissue_hi = tf.clip_by_value(air_hi_raw + (tissue_hi_raw - air_hi_raw), min_clip, 1.0)
    air_tissue_lo = tf.clip_by_value(air_lo_raw + (tissue_lo_raw - air_lo_raw), min_clip, 1.0)

    tissue_air_hi = tf.clip_by_value(tissue_hi + air_hi, min_clip, 1.0)
    tissue_air_lo = tf.clip_by_value(tissue_lo + air_lo, min_clip, 1.0)
    tissue_bone_hi = tf.clip_by_value(tissue_hi + bone_hi, min_clip, 1.0)
    tissue_bone_lo = tf.clip_by_value(tissue_lo + bone_lo, min_clip, 1.0)

    bone_air_hi = tf.clip_by_value(bone_hi + air_hi, min_clip, 1.0)
    bone_air_lo = tf.clip_by_value(bone_lo + air_lo, min_clip, 1.0)
    bone_tissue_hi = tf.clip_by_value(bone_hi + tissue_hi, min_clip, 1.0)
    bone_tissue_lo = tf.clip_by_value(bone_lo + tissue_lo, min_clip, 1.0)

    air_r = tf.stack([air_lo / air_hi, air_bone_lo / air_bone_hi, air_tissue_lo / air_tissue_hi], axis=-1)
    air_high = tf.stack([air_hi, air_bone_hi, air_tissue_hi], axis=-1)
    air_low = tf.stack([air_lo, air_bone_lo, air_tissue_lo], axis=-1)

    tissue_r = tf.stack([tissue_lo / tissue_hi, tissue_air_lo / tissue_air_hi, tissue_bone_lo / tissue_bone_hi], axis=-1)
    tissue_high = tf.stack([tissue_hi, tissue_air_hi, tissue_bone_hi], axis=-1)
    tissue_low = tf.stack([tissue_lo, tissue_air_lo, tissue_bone_lo], axis=-1)

    bone_r = tf.stack([bone_lo / bone_hi, bone_air_lo / bone_air_hi, bone_tissue_lo / bone_tissue_hi], axis=-1)
    bone_high = tf.stack([bone_hi, bone_air_hi, bone_tissue_hi], axis=-1)
    bone_low = tf.stack([bone_lo, bone_air_lo, bone_tissue_lo], axis=-1)

    return air_r, air_high, air_low, tissue_r, tissue_high, tissue_low, bone_r, bone_high, bone_low


def process_raw_dxa(input_image: tf.Tensor):
    """
    Backward-compatible alias for the shared DXA transform.
    """
    return transform_raw_dxa(input_image)
