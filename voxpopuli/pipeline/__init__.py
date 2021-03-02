# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import torch


def is_id_valid(name: str):

    # An id should have the following format
    # YYYYMMDD-XXXX-[NAME]
    # YYYYMMDD : is the date of the session
    # XXXX : is a 4 digits identification number
    # [NAME] : can be any string

    data = name.split("-")
    if len(data) < 3:
        return False

    date = data[0]
    if len(date) != 8 or any((not x.isdigit()) for x in date):
        return False

    if int(date[4:6]) > 12:
        return False
    if int(date[6:]) > 31:
        return False

    session_id = data[1]
    if any((not x.isdigit()) for x in session_id):
        return False

    return True


def to_wav2letter_format(data: torch.tensor, sr: int) -> torch.tensor:
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


def correct_name_fbcluster_output(name_in: str) -> str:
    r"""A quick patch to solve some discreepancies from the output names
    in the align / WER pipeliness without having to relaunch everything"""

    split_ = name_in.split("-")
    if len(split_) == 3:
        return "-".join(split_[:2])

    return name_in
