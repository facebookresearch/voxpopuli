# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from dataclasses import dataclass
import numpy as n_procs


@dataclass
class Timestamp:
    t_start: float
    t_end: float
