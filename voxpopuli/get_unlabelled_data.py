# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import gzip
import csv
from pathlib import Path
from collections import defaultdict
from typing import Tuple, List

from tqdm import tqdm
from torchaudio.datasets.utils import download_url
import torchaudio

from voxpopuli import LANGUAGES, LANGUAGES_V2, DOWNLOAD_BASE_URL
from voxpopuli.utils import multiprocess_run


def _segment(item: Tuple[str, List[Tuple[str, float, float]], str]):
    in_path, segments, out_root = item
    _in_path = Path(in_path)
    event_id = _in_path.stem
    lang, year = _in_path.parent.parent.stem, _in_path.parent.stem
    waveform, sr = torchaudio.load(in_path)
    for i, s, e in segments:
        start, end = int(s * sr), min(waveform.size(1), int(e * sr))
        out_path = Path(out_root) / lang / year / f'{event_id}_{i}.ogg'
        torchaudio.save(out_path.as_posix(), waveform[:, start: end], sr)


def get_metadata(out_root, subset):
    def predicate(id_):
        is_plenary = id_.find("PLENARY") > -1
        if subset in {"10k", "10k_sd"}:
            return is_plenary and 20190101 <= int(id_[:8]) < 20200801
        elif subset in {"100k"}:
            return is_plenary
        elif subset in LANGUAGES:
            return is_plenary and id_.endswith(subset)
        elif subset in LANGUAGES_V2:
            return id_.endswith(subset.split("_")[0])
        return True

    filename = "unlabelled_sd" if subset == "10k_sd" else "unlabelled_v2"
    url = f"{DOWNLOAD_BASE_URL}/annotations/{filename}.tsv.gz"
    tsv_path = out_root / Path(url).name
    if not tsv_path.exists():
        download_url(url, out_root.as_posix(), Path(url).name)
    if subset == '10k_sd':
        with gzip.open(tsv_path, mode="rt") as f:
            rows = [
                (r["session_id"], r["id_"], r["start_time"], r["end_time"])
                for r in csv.DictReader(f, delimiter="|")
                if predicate(r["session_id"])
            ]
    else:
        with gzip.open(tsv_path, mode="rt") as f:
            rows = [
                (r["event_id"], r["segment_no"], r["start"], r["end"])
                for r in csv.DictReader(f, delimiter="\t")
                if predicate(r["event_id"])
            ]
    return rows


def get(args):
    audio_root = Path(args.root) / "raw_audios"
    out_root = Path(args.root) / "unlabelled_data"
    out_root.mkdir(exist_ok=True, parents=True)
    items = defaultdict(list)
    print("Loading manifest...")
    manifest = get_metadata(out_root, args.subset)
    for event_id, seg_no, start, end in tqdm(manifest):
        lang, year = event_id.rsplit("_", 1)[1], event_id[:4]
        cur_out_root = out_root / lang / year
        cur_out_root.mkdir(exist_ok=True, parents=True)
        path = audio_root / lang / year / f"{event_id}.ogg"
        items[path.as_posix()].append((seg_no, float(start), float(end)))
    items = [(k, v, out_root.as_posix()) for k, v in items.items()]
    print(f"Segmenting {len(items):,} files...")
    multiprocess_run(items, _segment)


def get_args():
    parser = argparse.ArgumentParser("Prepare unlabelled data")
    parser.add_argument(
        "--root", "-r", type=str, required=True, help="data root path"
    )
    parser.add_argument(
        "--subset", "-s", type=str, required=True,
        choices=["400k", "100k", "10k", "10k_sd"] + LANGUAGES + LANGUAGES_V2,
        help="data subset to download"
    )
    return parser.parse_args()


def main():
    args = get_args()
    get(args)


if __name__ == "__main__":
    main()
