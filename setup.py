# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from setuptools import setup, find_packages


setup(
    name='voxpopuli_release',
    version='1.0',
    description='The code to build the vox populi dataset',
    author='Facebook AI Research',
    packages=find_packages(),
    classifiers=["License :: OSI Approved :: MIT License",
                 "Intended Audience :: Science/Research",
                 "Topic :: Scientific/Engineering",
                 "Programming Language :: Python"],
)
