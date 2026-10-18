"""
File Name: mesh_utils.py
Author: Lambert T Leong
Description: Contains 3D mesh utility functions
"""

import numpy as np
import os
import random
from pathlib import Path

from plyfile import PlyData
from typing import Generator, Tuple
import tensorflow as tf
from typing import List

def convert_mesh_ply_to_npy(ply_dir: str, npy_dir: str) -> int:
    """
    Converts PLY files in a directory to NumPy arrays and saves them.
    
    Args:
        ply_dir (str): Directory containing PLY files.
        npy_dir (str): Directory where NumPy arrays will be saved.

    Returns:
        int: Number of PLY files converted.
    """
    ply_path = Path(ply_dir)
    npy_path = Path(npy_dir)
    npy_path.mkdir(parents=True, exist_ok=True)

    count = 0
    for filename in sorted(os.listdir(ply_path)):
        if Path(filename).suffix.lower() != ".ply":
            continue
        ply = PlyData.read(ply_path / filename)
        xyz = np.vstack((np.array(ply['vertex']['x']), np.array(ply['vertex']['y']), np.array(ply['vertex']['z']))).T
        np.save(npy_path / f"{Path(filename).stem}.npy", xyz)
        count += 1

    return count

def ply_to_npy(path: str) -> np.ndarray:
    """
    Convert a PLY file to a NumPy array.

    Args:
        path (str): Path to the PLY file.

    Returns:
        np.ndarray: NumPy array containing vertex coordinates.
    """
    ply = PlyData.read(path)
    xyz = np.vstack((np.array(ply['vertex']['x']), np.array(ply['vertex']['y']), np.array(ply['vertex']['z']))).T
    return xyz

def load_full_mesh(path: List[str]) -> np.ndarray:
    """
    Load multiple full meshes from a list of file paths.

    Args:
        path (List[str]): List of file paths.

    Returns:
        np.ndarray: NumPy array containing loaded meshes.
    """
    out = []
    count=1
    for name in path:
        #print(name)#,end='\r')
        out+=[np.load(name)]
    out = np.stack(out)
    #print(low_pix, hi_pix)
    return out


def sample_points_uniform(meshes: List[np.ndarray], tot_pts: int = 110306, perc: float = 0.2) -> np.ndarray:
    """
    Sample points uniformly from multiple meshes.

    Args:
        meshes (List[np.ndarray]): List of mesh arrays.
        tot_pts (int): Total number of points to sample.
        perc (float): Percentage of points to sample from each mesh.

    Returns:
        np.ndarray: NumPy array containing sampled points.
    """
    if not meshes:
        raise ValueError("meshes must contain at least one mesh")
    if not 0 < perc <= 1:
        raise ValueError("perc must be in the range (0, 1]")
    if tot_pts <= 0:
        raise ValueError("tot_pts must be a positive integer")

    expected_pts = meshes[0].shape[0]
    num_pts = round(tot_pts * perc)
    if num_pts <= 0:
        raise ValueError("perc selects zero mesh points")
    if tot_pts > expected_pts:
        raise ValueError("tot_pts cannot exceed the number of points in the mesh")

    out = []
    uniform = np.linspace(0, tot_pts - 1, num=num_pts, dtype=int)

    for m in meshes:
        if m.shape[0] < tot_pts:
            raise ValueError("all meshes must contain at least tot_pts points")
        out+=[m[uniform]]
    return np.stack(out)

def sample_points_random(mesh,perc=0.2):
    num_pts=round(mesh.shape[0]*perc)
    sample_ind = random.sample(range(0, mesh.shape[0]), num_pts)
    return mesh[sample_ind]#[:-1]

def sample_points_random_tf(mesh,perc=0.2):
    num_pts = round(mesh.shape[0] * perc)
    sample_ind = tf.random.shuffle(tf.range(mesh.shape[0]))[:num_pts]
    return tf.gather(mesh, sample_ind)

def mesh2dxa_gen(mesh: np.ndarray, dxa: np.ndarray, batch_size: int = 32) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
    """
    Generator function to yield batches of mesh and corresponding DXA data.

    Args:
        mesh (np.ndarray): The mesh data, expected to be a multi-dimensional NumPy array.
        dxa (np.ndarray): The DXA data corresponding to the mesh, expected to be a multi-dimensional NumPy array.
        batch_size (int, optional): The size of the batch to yield. Defaults to 32.

    Yields:
        Generator[Tuple[np.ndarray, np.ndarray], None, None]: 
        A tuple containing a batch of mesh data and the corresponding DXA data.
    """
    while True:
        idx = np.random.choice(range(mesh.shape[0]), size=batch_size, replace=True)
        batch_mesh = [sample_points_random(mesh[i]) for i in idx]
        batch_dxa = [dxa[i] for i in idx]
        yield np.stack(batch_mesh), np.stack(batch_dxa)
