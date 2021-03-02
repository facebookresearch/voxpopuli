# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import pickle as pkl
import json
from pathlib import Path


def load_segments_from_pkl(pkl_path, min_duration):
    with open(pkl_path, "rb") as f:
        annotation = pkl.load(f)
    segments = [
        (round(segment.start, 3), round(segment.end, 3), label)
        for segment, track, label in annotation.itertracks(yield_label=True)
    ]
    segments = [(s, t, l) for s, t, l in segments if t - s >= min_duration]
    return segments


def get_pyannote_segments(path_audio, pyannote_cfg, min_duration=0.1):
    pkl_path = path_audio.parent / f"{path_audio.stem}.pyannote.{pyannote_cfg}.pkl"
    if pkl_path.is_file():
        return load_segments_from_pkl(pkl_path, min_duration)

    json_path = path_audio.parent / f"{path_audio.stem}.pyannote.{pyannote_cfg}.json"
    if json_path.is_file():
        with open(json_path, "r") as f:
            segments = json.load(f)
        return [(s, t, l) for s, t, l in segments if t - s >= min_duration]

    raise FileNotFoundError(f"{pkl_path} and {json_path} not found")
