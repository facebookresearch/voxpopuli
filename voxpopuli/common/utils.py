# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from pathlib import Path
from typing import List, Union


def get_batches(list_like, batch_size: int):
    for i in list(range(0, len(list_like), batch_size)):
        yield list_like[i : min(i + batch_size, len(list_like))]


def is_plenary(_id: str):
    return _id.find("-PLENARY") > -1


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
