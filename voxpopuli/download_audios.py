# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import os
from pathlib import Path

from tqdm import tqdm
from torchaudio.datasets.utils import download_url, extract_archive

from voxpopuli import LANGUAGES, YEARS, DOWNLOAD_BASE_URL


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", "-r", type=str, required=True, help="data root path"
    )
    parser.add_argument(
        "--subset", "-s", type=str, required=True,
        choices=["100k", "10k", "asr"] + LANGUAGES,
        help="data subset to download"
    )
    return parser.parse_args()


def download(args):
    if args.subset in LANGUAGES:
        languages = [args.subset]
        years = YEARS
    else:
        languages = {
            "100k": LANGUAGES, "10k": LANGUAGES, "asr": ["original"]
        }.get(args.subset, None)
        years = {
            "100k": YEARS, "10k": [2019, 2020], "asr": YEARS
        }.get(args.subset, None)

    url_list = []
    for l in languages:
        for y in years:
            url_list.append(f"{DOWNLOAD_BASE_URL}/audios/{l}_{y}.tar")

    out_root = Path(args.root) / "raw_audios"
    out_root.mkdir(exist_ok=True, parents=True)
    print(f"{len(url_list)} files to download...")
    for url in tqdm(url_list):
        tar_path = out_root / Path(url).name
        download_url(url, out_root, Path(url).name)
        extract_archive(tar_path.as_posix())
        os.remove(tar_path)


def main():
    args = get_args()
    download(args)


if __name__ == '__main__':
    main()
