# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import csv
import argparse
from tqdm import tqdm
from ast import literal_eval
import gzip
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

import torch
import torchaudio
from torchaudio.datasets.utils import download_url

from voxpopuli import ASR_LANGUAGES, ASR_ACCENTED_LANGUAGES, DOWNLOAD_BASE_URL
from voxpopuli.utils import multiprocess_run


SPLITS = ["train", "dev", "test"]


def cut_session(info: Tuple[str, Dict[str, List[Tuple[float, float]]]]) -> None:
    in_path, out_path_to_timestamps = info
    waveform, sr = torchaudio.load(in_path)
    duration = waveform.size(1)
    for out_path, timestamps in out_path_to_timestamps.items():
        segment = torch.cat(
            [waveform[:, int(s * sr): min(int(t * sr), duration)]
             for s, t in timestamps],
            dim=1
        )
        torchaudio.save(out_path, segment, sr)


def get(args):
    in_root = Path(args.root) / "raw_audios" / "original"
    out_root = Path(args.root) / "transcribed_data" / args.lang
    out_root.mkdir(exist_ok=True, parents=True)
    # Get metadata TSV
    url = f"{DOWNLOAD_BASE_URL}/annotations/asr/asr_{args.lang}.tsv.gz"
    tsv_path = out_root / Path(url).name
    if not tsv_path.exists():
        download_url(url, out_root.as_posix(), Path(url).name)
    with gzip.open(tsv_path, "rt") as f:
        metadata = [x for x in csv.DictReader(f, delimiter="|")]
    # Get segment into list
    items = defaultdict(dict)
    manifest = []
    for r in tqdm(metadata):
        split = r["split"]
        if split not in SPLITS:
            continue
        event_id = r["session_id"]
        year = event_id[:4]
        in_path = in_root / year / f"{event_id}_original.ogg"
        cur_out_root = out_root / year
        cur_out_root.mkdir(exist_ok=True, parents=True)
        out_path = cur_out_root / "{}-{}.ogg".format(event_id, r["id_"])
        timestamps = [(t[0], t[1]) for t in literal_eval(r["vad"])]
        items[in_path.as_posix()][out_path.as_posix()] = timestamps
        manifest.append(
            (
             out_path.stem,
             r["original_text"],
             r["normed_text"],
             r["speaker_id"],
             split,
             r["gender"],
             r.get("is_gold_transcript", str(False)),
             r.get("accent", str(None))
            )
        )
    items = list(items.items())
    # Segment
    multiprocess_run(items, cut_session)
    # Output per-split manifest
    header = [
        "id", "raw_text", "normalized_text", "speaker_id", "split",
        "gender", "is_gold_transcript", "accent"
    ]
    for split in SPLITS:
        with open(out_root / f"asr_{split}.tsv", "w") as f_o:
            f_o.write("\t".join(header) + "\n")
            for cols in manifest:
                if cols[4] == split:
                    f_o.write("\t".join(cols) + "\n")


def get_args():
    parser = argparse.ArgumentParser("Prepare transcribed data")
    parser.add_argument(
        "--root",
        help="data root path",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--lang",
        required=True,
        type=str,
        choices=ASR_LANGUAGES + ASR_ACCENTED_LANGUAGES,
    )
    return parser.parse_args()


def main():
    args = get_args()
    get(args)


if __name__ == "__main__":
    main()
