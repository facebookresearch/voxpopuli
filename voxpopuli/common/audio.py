# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
###
# Run pyannote speaker diarization (SD) models
###
import torchaudio
import torch


def to_wav2letterFormat(data: torch.tensor, sr: int) -> torch.tensor:
    r"""
    Wav2letter needs mono 16kHz inputs
    """
    if len(data.size()) == 2:
        data = data.mean(dim=0, keepdim=True)
    elif len(data.size()) == 1:
        data = data.view(1, -1)
    else:
        raise ValueError("Invalid tensor format")
    if sr != 16000:
        data = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)(data)
        data = torch.clamp(data, min=-1.0, max=1.0)
    return data
