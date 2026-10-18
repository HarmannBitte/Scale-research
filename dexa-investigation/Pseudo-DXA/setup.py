from pathlib import Path

from setuptools import find_packages, setup

README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")

setup(
    name='Pseudo-DXA',  
    version='1.0.1',
    description='A model for generating pseudo-DXA images from 3D body surface meshes.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/LambertLeong/Pseudo-DXA',
    author='Lambert Leong',
    author_email='lamberttleong@gmail.com',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    packages=find_packages(include=["modeling", "modeling.*", "utils", "utils.*"]),
    py_modules=["predict"],
    install_requires=[
        'numpy>=1.19.5',
        'opencv-python>=4.5.2',
        'plyfile>=0.7.4',
        'tensorflow>=2.4',
    ],
    entry_points={
        "console_scripts": [
            "pseudo-dxa-predict=predict:main",
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',  
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
