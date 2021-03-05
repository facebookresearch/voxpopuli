# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from pathlib import Path
from dataclasses import dataclass
from typing import List, Union
import pickle as pkl
import json
import enum

import torch
import torchaudio


@dataclass
class Timestamp:
    t_start: float
    t_end: float


class LangCode(enum.Enum):
    HR = "hr"
    HU = "hu"
    IT = "it"
    SL = "sl"
    ES = "es"
    BG = "bg"
    NL = "nl"
    ET = "et"
    DE = "de"
    MT = "mt"
    PT = "pt"
    DA = "da"
    EN = "en"
    FI = "fi"
    LV = "lv"
    PL = "pl"
    RO = "ro"
    FR = "fr"
    LT = "lt"
    SK = "sk"
    SV = "sv"
    CS = "cs"
    EL = "el"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


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


def get_batches(list_like, batch_size: int):
    for i in list(range(0, len(list_like), batch_size)):
        yield list_like[i : min(i + batch_size, len(list_like))]


def is_plenary(_id: str):
    return _id.find("-PLENARY") > -1


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


def get_all_years_for_lang(path_root: Union[str, Path], lang: str) -> List[str]:
    path_lang = Path(path_root) / lang
    return [
        x.stem
        for x in path_lang.glob("*")
        if (len(x.stem) == 4 and x.is_dir() and all(p.isdigit() for p in x.stem))
    ]


def get_all_sessions_lang_year(path_root: Path, lang: str, year: str) -> List[str]:

    audio = list((path_root / lang / year).glob(f"*_{lang}.ogg"))
    return [x.stem.split("_")[0] for x in audio]


def get_path_full_audio(path_root: Path, session_id: str, lang: str) -> Path:
    year = session_id[:4]
    return path_root / lang / year / f"{session_id}_{lang}.ogg"


def get_all_audio_for_lang(path_root: Path, lang: str) -> List[Path]:

    audio_paths = []
    years = get_all_years_for_lang(path_root, lang)
    for year in years:
        all_sessions = get_all_sessions_lang_year(path_root, lang, year)
        loc = [
            get_path_full_audio(path_root, session_id, lang)
            for session_id in all_sessions
        ]
        audio_paths += loc
    return audio_paths
