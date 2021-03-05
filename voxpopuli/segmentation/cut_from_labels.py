# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import soundfile as sf
import csv
import argparse
import tqdm
import numpy as np
import ast
from pathlib import Path
from voxpopuli.segmentation import Timestamp, get_path_full_audio
from typing import Callable, Dict, List, Tuple
from multiprocessing import Pool


VadData = List[Timestamp]


def parse_seq_path(seq_path: str) -> Tuple[str, str, str]:
    out = seq_path.split("/")
    assert len(out) == 3
    return out[0], out[1], out[2]


def get_path_paragraph(row, idx_: Dict[str, int]) -> Path:
    base_path = Path(row[idx_["session_id"]]) / row[idx_["paragraph_id"]]
    if "lang" in idx_:
        base_path = Path(row[idx_["lang"]]) / base_path
    return base_path


def get_path_fully_segmented(row, idx_: Dict[str, int]) -> Path:
    return get_path_paragraph(row, idx_) / row[idx_["id_"]]


def get_ts_base(row, idx_: Dict[str, int]) -> List[Timestamp]:
    return [Timestamp(float(row[idx_["start_time"]]), float(row[idx_["end_time"]]))]


def get_ts_speaker(row, idx_: Dict[str, int]) -> List[Timestamp]:
    return [
        Timestamp(float(row[idx_["speaker_start"]]), float(row[idx_["speaker_end"]]))
    ]


def get_ts_vad(row, idx_: Dict[str, int]) -> List[Timestamp]:
    vad = ast.literal_eval(row[idx_["vad"]])
    return [Timestamp(x[0], x[1]) for x in vad]


def load_annot_file(
    path_input: Path,
    path_extractor: Callable,
    timestamp_extractor: Callable,
    suffix: str = ".flac",
) -> Dict[Tuple[str, str], Dict[Path, VadData]]:
    with open(path_input, "r") as csvfile:
        data = csv.reader(csvfile, delimiter="|")

        names = next(data)
        idx_ = {x: i for i, x in enumerate(names)}
        idx_name = idx_["session_id"]
        idx_lang = idx_.get("lang", None)

        out = {}
        for row in data:
            session_name = row[idx_name]
            path_seq = path_extractor(row, idx_).with_suffix(suffix)
            vad = timestamp_extractor(row, idx_)
            lang = "original" if idx_lang is None else row[idx_lang]

            index = session_name, lang
            if index not in out:
                out[index] = {}
            out[index][path_seq] = vad

    return out


def cut_session(
    root_original: Path,
    root_out: Path,
    session_name: str,
    ts_2_names: Dict[str, List[Timestamp]],
    lang: str,
) -> None:

    sound, sr = sf.read(str(get_path_full_audio(root_original, session_name, lang)))
    for loc_path, vad in ts_2_names.items():
        full_path = root_out / loc_path
        full_path.parent.mkdir(exist_ok=True, parents=True)
        sf.write(
            full_path,
            cut_with_vad(sound, sr, vad),
            sr,
            subtype="PCM_16",
        )


def cut_with_vad(sound: np.array, sr: int, vad: List[Timestamp]) -> np.array:

    out = []
    for ts in vad:
        out += [sound[int(ts.t_start * sr) : int(ts.t_end * sr)]]
    return np.concatenate(out, axis=0)


class FileSegmenter:
    def __init__(
        self,
        root_original: Path,
        root_out: Path,
        annot_dict: Dict[str, Dict[Path, List[Timestamp]]]
    ):

        self.root_original = root_original
        self.root_out = root_out
        self.annot_dict = annot_dict

    def cut_session(self, session_id_lang: Tuple[str, str]):
        session_id, lang = session_id_lang
        cut_session(
            self.root_original,
            self.root_out,
            session_id,
            self.annot_dict[session_id_lang],
            lang,
        )

    def run(self, n_procs: int = 8):

        with Pool(processes=n_procs) as pool:
            for _ in tqdm.tqdm(
                pool.imap_unordered(self.cut_session, self.annot_dict),
                total=len(self.annot_dict),
            ):
                pass


def main(args):

    path_data = Path(args.root_original)
    path_out = Path(args.output)
    path_annotations = Path(args.tsv_file)

    path_extractor = get_path_fully_segmented
    if args.mode == "labelled":
        timestamp_extractor = get_ts_vad
    elif args.mode == "per_speaker_vad":
        timestamp_extractor = get_ts_base
    elif args.mode == "per_speaker":
        timestamp_extractor = get_ts_speaker
        path_extractor = get_path_paragraph
    else:
        raise RuntimeError(f"Invalid mode {args.mode}")

    annot_dict = load_annot_file(path_annotations, path_extractor, timestamp_extractor)
    segmenter = FileSegmenter(path_data, path_out, annot_dict)
    segmenter.run(n_procs=args.n_procs)


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Segment the data from the given .tsv file. "
                                     "Can be used for a customed segmentation of the 10k timetsamps")
    parser.add_argument(
        "--root_original",
        help="Root directory where the original data are stored.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--tsv_file",
        help="Path to the .tsv file containing the labels.",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-o", "--output", help="Path to the outpit directory.", type=str, required=True
    )
    parser.add_argument(
        "--n-procs", help="Number of processes to run", type=int, default=8
    )
    parser.add_argument(
        "--lang", help="Lang to consider", type=str, required=True
    )
    parser.add_argument(
        "--mode",
        required=True,
        type=str,
        choices=["labelled", "per_speaker", "per_speaker_vad"],
        help="labelled to segment the labelled data. "
              "per_speaker to cut the 10k data per speaker "
              "per_speaker_vad to add the vad of top of the segmentation of the 10k data."
    )

    main(parser.parse_args())
