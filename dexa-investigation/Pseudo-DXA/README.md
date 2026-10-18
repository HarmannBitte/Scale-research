# Pseudo-DXA

Pseudo-DXA is a generative deep learning model that produces qualitative and quantitative dual-energy X-ray absorptiometry (DXA) scans from three-dimensional (3D) body surface scans. The model was developed for research workflows evaluating body composition measures including fat mass, lean mass, and bone.

This model was developed by [Lambert T Leong](https://github.com/LambertLeong),[PhD](https://www.lambertleong.com/) advised by [John A Shepherd](https://github.com/shepherd-lab) as a part of the [Shepherd Research Lab (SRL)](https://shepherdresearchlab.org/) and the [University of Hawaii Cancer Center](https://www.uhcancercenter.org/component/finder/search?q=lambert+leong&Itemid=926)

[![DOI](https://zenodo.org/badge/721837794.svg)](https://zenodo.org/doi/10.5281/zenodo.10183202)

![Model Results](assets/figure_1_psdxa.png)

## Setup
Pseudo-DXA is intended to run on Linux with a CUDA-enabled GPU for practical inference speed. CPU execution is supported by TensorFlow but is expected to be slower.

Install dependencies:

* Python >= 3.8
* tensorflow >= 2.4
* plyfile >= 0.7.4
* opencv-python >= 4.5.2
* numpy >= 1.19.5

Install from the repository root:

```bash
pip install -e .
```

## 3D Mesh Preprocessing

All 3D scan meshes must be fitted and standardized to a T-pose with 110K points using the [Meshcapade API](https://meshcapade.com/docs/api). The default example configuration samples 22,061 points from the fitted mesh.

## Usage
Update the config file:

* GPU device id. Variable: [`[setup][gpu]`](example.config#L2). Use `-1` to force CPU execution.
* Path to model weights. Variable: [`[model][lleong_psdxa_weights]`](example.config#L8).
* Path to PLY mesh file. Variable: [`[predict][mesh_path]`](example.config#L11).
* Path to output directory. Variable: [`[predict][out_path]`](example.config#L12).

### Trained Weights and Fitted Mesh Test File.
Weights for a version of a working Pseudo-DXA model and a fitted mesh for testing will be made available upon request to the [SRL Website](https://shepherdresearchlab.org/data-software/)  

### Running
```
python predict.py -c model.config
```

or, after installing the package:

```bash
pseudo-dxa-predict -c model.config
```

Expected outputs in the configured output directory:

* `pred.npy`: raw 6-channel Pseudo-DXA prediction.
* `raw_prediction.png`: single-channel preview from the raw prediction.
* `processed_prediction.png`: single-channel processed preview.

### Quantitative Body Composition Analysis
Code for transforming NPY files into proprietary DXA files for analysis cannot be made publicly available. Those at [SRL](https://shepherdresearchlab.org/data-software/) can perform the transformation and should be contacted accordingly. Resulting DXA file can then be analyzed using DXA body composition analysis software as shown below.

![Body Comp Analysis](assets/supfig3_psdxa.png)

## Acknowledgments
The base model was trained using self-supervised learning on over 20K DXA scans from the [Bone Mineral Density in Childhood Study](https://www.nichd.nih.gov/research/supported/bmdcs) and [The Health, Aging and Body Composition Study](https://healthabc.nia.nih.gov/). Code for the self-supervised model is [here: DXA-VAE](https://github.com/LambertLeong/DXA-VAE) and a video of it training is [here!](https://youtu.be/hXSL7NVCeAY).

Training of the final model was on patients from the [Shape Up! Studies](https://shapeup.shepherdresearchlab.org/) who received pairs of DXAs and 3D scans on the same day. The training schema is shown below.

![Training Diagram](assets/supfig2_psdxa.png)

## Contact
Pseudo-DXA is research software and is not distributed as a clinical device. For questions, model access, or collaboration inquiries: [lambert3+psdxa@hawaii.edu](mailto:lambert3+psdxa@hawaii.edu)
