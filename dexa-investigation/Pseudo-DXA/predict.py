"""
File Name: predict.py
Author: Lambert T Leong
Description: This code loads 3D meshes, fitted/standardized using meshcapade, as a *.ply file, loads the Pseudo-DXA model, runs the mesh through the model, predicts a DXA scan, and outputs the raw DXA data.
"""

import argparse
import configparser
import os
from pathlib import Path

import cv2
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logging (1: WARNING, 2: ERROR, 3: FATAL)
from argparse import RawTextHelpFormatter
from functools import reduce
import numpy as np

def parse_arguments():
    parser = argparse.ArgumentParser(epilog="""
    list index (--config, -c)
            - path to config file 
     """,
    formatter_class=RawTextHelpFormatter)
    parser.add_argument('--config', '-c', action='store',
    required=True, dest='config', metavar='<config file>',
    help='"path to config file"')
    return parser.parse_args()

def load_config(configfile: str) -> configparser.ConfigParser:
    config_path = Path(configfile)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file does not exist: {config_path}")

    config = configparser.ConfigParser()
    read_files = config.read(config_path)
    if not read_files:
        raise ValueError(f"Unable to read config file: {config_path}")

    required = {
        "setup": ["gpu"],
        "model": ["input_size", "upscale", "reshape_dims", "lleong_psdxa_weights"],
        "predict": ["mesh_path", "out_path"],
    }
    for section, keys in required.items():
        if section not in config:
            raise KeyError(f"Missing required config section: [{section}]")
        for key in keys:
            if key not in config[section]:
                raise KeyError(f"Missing required config value: [{section}][{key}]")

    return config

def scale_to_uint8(image: np.ndarray) -> np.ndarray:
    min_val = np.min(image)
    max_val = np.max(image)
    if np.isclose(max_val, min_val):
        return np.zeros_like(image, dtype=np.uint8)
    return ((image - min_val) / (max_val - min_val) * 255).astype(np.uint8)

def write_image(path: Path, image: np.ndarray) -> None:
    if not cv2.imwrite(str(path), image):
        raise IOError(f"Failed to write image: {path}")

def main():
    argv = parse_arguments()
    config = load_config(str(argv.config))
    desired_gpu_index = int(config['setup']['gpu'])

    # CUDA_VISIBLE_DEVICES must be set before TensorFlow is imported.
    os.environ["CUDA_VISIBLE_DEVICES"] = str(desired_gpu_index) if desired_gpu_index >= 0 else "-1"

    import tensorflow as tf
    from modeling import DXAGenerator, MeshEncoder, PseudoDXA
    from utils import mesh_utils as mesh
    
    # Check for available GPU devices.
    gpu_devices = tf.config.experimental.list_physical_devices('GPU')
    if gpu_devices:
        print(f"Using visible GPU: {gpu_devices[0].name}")
    else:
        print("No visible CUDA-enabled GPU found. Using CPU.")
        
    input_size = int(config['model']['input_size'])
    upscale_factor = int(config['model']['upscale'])
    reshape_dims = [int(x) for x in config['model']['reshape_dims'].split(',')]
    psdxa_weights = Path(config['model']['lleong_psdxa_weights'])
    if not psdxa_weights.exists():
        raise FileNotFoundError(f"Model weights do not exist: {psdxa_weights}")

    mesh_path = Path(config['predict']['mesh_path'])
    if not mesh_path.exists():
        raise FileNotFoundError(f"Mesh file does not exist: {mesh_path}")

    latent_dim = reduce((lambda x, y: x * y), reshape_dims)
    outpath = Path(config['predict']['out_path'])
    outpath.mkdir(parents=True, exist_ok=True)

    print('Loading Model and Weights')
    encoder = MeshEncoder(latent_dim, num_pts=input_size).model
    generator = DXAGenerator(reshape_dim=reshape_dims, upscale=upscale_factor).model
    psdxa = PseudoDXA(encoder, generator)
    psdxa.build_model()
    psdxa.model.load_weights(str(psdxa_weights))

    print('Loading and Processing Data')
    npy = mesh.ply_to_npy(str(mesh_path))
    npy_u = mesh.sample_points_uniform([npy], tot_pts=npy.shape[0], perc=input_size / npy.shape[0])
    if npy_u.shape[1] != input_size:
        raise ValueError(f"Sampled mesh has {npy_u.shape[1]} points; expected {input_size}")
    
    print('Sending Data to Model')
    pred = psdxa.predict(npy_u, verbose=1)
    
    np.save(outpath / 'pred.npy', pred)
    pred_resize = cv2.resize(pred[0], dsize=None, fx=3/2, fy=5/2, interpolation=cv2.INTER_LINEAR)
    out_raw = pred_resize[:,:,0]
    scaled_image = scale_to_uint8(out_raw)
    write_image(outpath / 'raw_prediction.png', scaled_image)

    out_processed = pred_resize[:,:,3]-pred_resize[:,:,2]
    out_processed = scale_to_uint8(out_processed)
    write_image(outpath / 'processed_prediction.png', out_processed)
    
if __name__ == '__main__':
    main()
