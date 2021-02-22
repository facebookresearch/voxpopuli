# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from pathlib import Path
from typing import Union


def get_batches(list_like, batch_size: int):
    for i in list(range(0, len(list_like), batch_size)):
        yield list_like[i : min(i + batch_size, len(list_like))]


def is_plenary(_id: str):
    return _id.find("-PLENARY") > -1


def get_lang_dir(path_dir: Path, lang: str) -> Path:
    path_dir = Path(path_dir)
    return path_dir / f"{path_dir.stem}_{lang}"


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


def get_all_ids_from_dir(path_root: Union[str, Path]):
    return [
        x.stem
        for x in Path(path_root).glob("*")
        if (x.is_dir() and is_id_valid(x.stem))
    ]
