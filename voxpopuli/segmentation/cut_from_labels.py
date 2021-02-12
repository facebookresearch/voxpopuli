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
from voxpopuli.audio.utils import Timestamp
from typing import Dict, List, Tuple
from multiprocessing import Pool


def parse_seq_path(seq_path: str) -> Tuple[str, str, str]:
    out = seq_path.split("/")
    assert len(out) == 3
    return out[0], out[1], out[2]


def load_annot_file(path_input: Path) -> Dict[str, Dict[Path, List[Timestamp]]]:
    with open(path_input, "r") as csvfile:
        data = csv.reader(csvfile, delimiter="|")

        names = next(data)
        idx_ = {x: i for i, x in enumerate(names)}

        idx_seq_name = idx_["path_seq"]
        idx_vad = idx_["vad"]

        out = {}
        for row in data:
            path_seq = row[idx_seq_name]
            session_name, _, _ = parse_seq_path(path_seq)

            vad = ast.literal_eval(row[idx_vad])

            if session_name not in out:
                out[session_name] = {}
            out[session_name][Path(path_seq)] = [Timestamp(x[0], x[1]) for x in vad]

    return out


# TODO: update with the ogg final path
def get_path_flac_from_session_name(dir_original: Path, session_name: str) -> Path:

    return dir_original / session_name / f"{session_name}_" / "full.flac"


def cut_session(
    root_original: Path,
    root_out: Path,
    session_name: str,
    ts_2_names: Dict[str, List[Timestamp]],
) -> None:

    sound, sr = sf.read(
        str(get_path_flac_from_session_name(root_original, session_name))
    )
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
        annot_dict: Dict[str, Dict[Path, List[Timestamp]]],
    ):

        self.root_original = root_original
        self.root_out = root_out
        self.annot_dict = annot_dict

    def cut_session(self, session_id: str):
        cut_session(
            self.root_original, self.root_out, session_id, self.annot_dict[session_id]
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

    annot_dict = load_annot_file(path_annotations)
    segmenter = FileSegmenter(path_data, path_out, annot_dict)
    segmenter.run(n_procs=args.n_procs)


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Segment the data from the given labels")
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

    main(parser.parse_args())
