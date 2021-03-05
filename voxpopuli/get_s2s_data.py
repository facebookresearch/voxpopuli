# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
from pathlib import Path
import csv
import gzip
from typing import Tuple, List
from collections import defaultdict

import torchaudio
from torchaudio.datasets.utils import download_url
from tqdm import tqdm

from voxpopuli import (S2S_SRC_LANGUAGES, S2S_TGT_LANGUAGES, DOWNLOAD_BASE_URL,
                       S2S_TGT_LANGUAGES_WITH_HUMAN_TRANSCRIPTION)
from voxpopuli.utils import multiprocess_run


def parse_src_id(id_):
    event_id, utt_id = id_.split("_", 1)
    event_id, lang = event_id.rsplit("-", 1)
    return event_id, lang, utt_id


def _segment(info: Tuple[str, List[Tuple[str, float, float]]]):
    in_path, out_path_and_timestamps = info
    waveform, sr = torchaudio.load(in_path)
    for out_path, start, end in out_path_and_timestamps:
        start, end = int(start * sr), min(waveform.size(1), int(end * sr))
        torchaudio.save(out_path, waveform[:, start: end], sr)


def get(args):
    src_lang, tgt_lang = args.source_lang, args.target_lang
    if args.use_annotated_target:
        assert tgt_lang in S2S_TGT_LANGUAGES_WITH_HUMAN_TRANSCRIPTION
    in_root = Path(args.root) / "raw_audios" / tgt_lang
    asr_root = Path(args.root) / "transcribed_data" / src_lang
    out_root = asr_root / tgt_lang
    out_root.mkdir(exist_ok=True, parents=True)
    # Get metadata TSV
    url = f"{DOWNLOAD_BASE_URL}/annotations/asr/asr_{src_lang}.tsv.gz"
    tsv_path = asr_root / Path(url).name
    if not tsv_path.exists():
        download_url(url, asr_root.as_posix(), Path(url).name)
    with gzip.open(tsv_path, "rt") as f:
        src_metadata = [x for x in csv.DictReader(f, delimiter="|")]
    src_metadata = {
        "{}-{}".format(r["session_id"], r["id_"]): (
            r["original_text"], r["speaker_id"]
        )
        for r in src_metadata
    }
    ref_sfx = "_ref" if args.use_annotated_target else ""
    url = f"{DOWNLOAD_BASE_URL}/annotations/s2s/s2s_{tgt_lang}{ref_sfx}.tsv.gz"
    tsv_path = out_root / Path(url).name
    if not tsv_path.exists():
        download_url(url, out_root.as_posix(), Path(url).name)
    with gzip.open(tsv_path, "rt") as f:
        tgt_metadata = [x for x in csv.DictReader(f, delimiter="\t")]
    # Get segment into list
    items = defaultdict(list)
    manifest = []
    print("Loading manifest...")
    for r in tqdm(tgt_metadata):
        src_id = r["id"]
        event_id, _src_lang, utt_id = parse_src_id(src_id)
        if _src_lang != src_lang:
            continue
        year = event_id[:4]
        in_path = in_root / year / f"{event_id}_{tgt_lang}.ogg"
        cur_out_root = out_root / year
        cur_out_root.mkdir(exist_ok=True, parents=True)
        tgt_id = f"{event_id}-{tgt_lang}_{utt_id}"
        out_path = cur_out_root / f"{tgt_id}.ogg"
        items[in_path.as_posix()].append(
            (out_path.as_posix(), float(r["start_time"]), float(r["end_time"]))
        )
        src_text, src_speaker_id = src_metadata[src_id]
        tgt_text = r["tgt_text"] if args.use_annotated_target else ""
        manifest.append((src_id, src_text, src_speaker_id, tgt_id, tgt_text))
    items = list(items.items())
    # Segment
    print(f"Segmenting {len(items):,} files...")
    multiprocess_run(items, _segment)
    # Output per-data-split list
    header = ["src_id", "src_text", "src_speaker_id", "tgt_id", "tgt_text"]
    with open(out_root / f"s2s{ref_sfx}.tsv", "w") as f_o:
        f_o.write("\t".join(header) + "\n")
        for cols in manifest:
            f_o.write("\t".join(cols) + "\n")


def get_args():
    parser = argparse.ArgumentParser("Prepare S2S interpretation data")
    parser.add_argument(
        "--root",
        help="data root path",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--source-lang",
        required=True,
        type=str,
        choices=S2S_SRC_LANGUAGES,
    )
    parser.add_argument(
        "--target-lang",
        required=True,
        type=str,
        choices=S2S_TGT_LANGUAGES,
    )
    parser.add_argument("--use-annotated-target", action="store_true")
    return parser.parse_args()


def main():
    args = get_args()
    get(args)


if __name__ == '__main__':
    main()
