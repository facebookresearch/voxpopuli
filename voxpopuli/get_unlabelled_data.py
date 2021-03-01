# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import gzip
from pathlib import Path
from collections import defaultdict
from typing import Tuple, List

from tqdm import tqdm
from torchaudio.datasets.utils import download_url
import torchaudio

from voxpopuli import LANGUAGES, DOWNLOAD_BASE_URL
from voxpopuli.utils import multiprocess_unordered_run


def get_args():
    parser = argparse.ArgumentParser("Prepare unlabelled data")
    parser.add_argument(
        "--root", "-r", type=str, required=True, help="data root path"
    )
    parser.add_argument(
        "--subset", "-s", type=str, required=True,
        choices=["100k", "10k"] + LANGUAGES, help="data subset to download"
    )
    return parser.parse_args()


def _segment(item: Tuple[Path, List[Tuple[int, float, float]], Path]):
    in_path, segments, out_root = item
    event_id = in_path.stem
    lang, year = in_path.parent.parent.stem, in_path.parent.stem
    waveform, sr = torchaudio.load(in_path.as_posix())
    for i, s, e in segments:
        start, end = int(s * sr), int(e * sr)
        torchaudio.save(
            (out_root / lang / year / f'{event_id}_{i}.ogg').as_posix(),
            waveform[start: end],
            sr
        )


def get(args):
    audio_root = Path(args.root) / "raw_audios"
    out_root = Path(args.root) / "unlabelled_data"
    out_root.mkdir(exist_ok=True, parents=True)
    url = f"{DOWNLOAD_BASE_URL}/annotations/unlabelled.tsv.gz"
    tsv_path = out_root / Path(url).name
    if not tsv_path.exists():
        download_url(url, out_root.as_posix(), Path(url).name)

    predicates = {lang: lambda x: x.endswith(lang) for lang in LANGUAGES}
    predicates["100k"] = lambda x: True
    predicates["10k"] = lambda x: 20190101 <= int(x[:8]) < 20200801
    predicate = predicates[args.subset]
    items = defaultdict(list)
    print("Reading segment list...")
    with gzip.open(tsv_path, mode="rt") as f:
        next(f)
        for r in tqdm(f):
            event_id, seg_no, start, end = r.strip().split("\t")
            if predicate(event_id):
                lang, year = event_id.rsplit("_", 1)[1], event_id[:4]
                cur_out_root = out_root / lang / year
                cur_out_root.mkdir(exist_ok=True, parents=True)
                path = audio_root / lang / year / f"{event_id}.ogg"
                items[path].append((seg_no, float(start), float(end)))
    items = [(k, v, out_root) for k, v in items.items()]
    print(f"Segmenting {len(items)} files...")
    _ = multiprocess_unordered_run(items, _segment)


def main():
    args = get_args()
    get(args)


if __name__ == '__main__':
    main()
