# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
###
# Run pyannote speaker diarization (SD) models
###

import json
from typing import Iterable, NamedTuple, List, Tuple
from pathlib import Path

import edlib
import editdistance

from voxpopuli.segmentation import correct_name_fbcluster_output


class CharAlignToken(NamedTuple):
    index_decoded: int
    action: str


class WordAlignFile(NamedTuple):
    file_id: str
    target: str
    decoded: str
    wer: float
    ler: float
    align_path: List[CharAlignToken]


def quick_norm(str_in, char_set):

    str_in = str_in.lower().strip()
    str_in = " ".join(str_in.split())
    out = "".join([x for x in str_in if x in char_set])
    return out


def get_wer(query, decoded):
    return get_ler(query.split(), decoded.split())


def get_ler(query, decoded):
    d = editdistance.eval(query, decoded)
    return 100 * float(d) / (1e-8 + len(query))


def expand_cigar_format(path_cigar: str) -> str:

    out = ""
    size = len(path_cigar)
    i_ = 0
    while i_ < size:
        next = i_ + 1
        while path_cigar[next].isdigit():
            next += 1
        n = int(path_cigar[i_:next])
        v = path_cigar[next]
        out += n * v
        i_ = next + 1

    return out


def get_align_index_path(query: Iterable, target: Iterable) -> List[CharAlignToken]:

    path_ = edlib.align(query, target, task="path")["cigar"]
    if path_ is None:
        return []
    path_ = expand_cigar_format(path_)

    index_out = 0
    index_path = 0
    out = []
    for index_query in range(len(query)):
        while path_[index_path] == "D":
            index_out += 1
            index_path += 1

        action = path_[index_path]

        out.append(CharAlignToken(index_out, action))
        if action == "=":
            assert query[index_query] == target[index_out]
        if action in ["=", "X"]:
            index_out += 1

        index_path += 1

    return out


def get_partial_transcriptions(
    data: WordAlignFile, word_cuts: List[int]
) -> List[Tuple[str, str]]:

    last_index = 0
    last_index_decoded = data.align_path[0].index_decoded

    output = []
    for word_index in word_cuts:
        i_decoded = data.align_path[word_index].index_decoded
        # Go until the end of the next word
        while i_decoded < len(data.decoded) and data.decoded[i_decoded] != " ":
            i_decoded += 1
        while word_index < len(data.target) and data.target[word_index] != " ":
            word_index += 1
        out_target = data.target[last_index:word_index]
        out_decoded = data.decoded[last_index_decoded:i_decoded]
        last_index = word_index
        last_index_decoded = i_decoded
        output.append((out_target, out_decoded))

    if last_index < len(data.target):
        out_target = data.target[last_index:]
        out_decoded = data.decoded[last_index_decoded:]
        output.append((out_target, out_decoded))

    return output


def reinsert_punctuation(
    str_original: str, str_normed: str, char_set: str, punc_list: str
) -> str:

    quick_norm_ref = quick_norm(str_original, char_set + punc_list)
    align_path = get_align_index_path(quick_norm_ref, str_normed)
    punc_indexes = [(i, x) for i, x in enumerate(quick_norm_ref) if x in punc_list]
    last_index = 0

    out = ""

    for p_index, punc in punc_indexes:
        i_normed = align_path[p_index].index_decoded
        if i_normed <= last_index:
            continue
        while i_normed < len(str_normed) and str_normed[i_normed] != " ":
            i_normed += 1
        loc_norm = str_normed[last_index:i_normed]
        out += loc_norm + punc + " "
        last_index = i_normed

    if last_index < len(str_normed):
        out += str_normed[last_index:]

    return out


def create_word_align_file(file_id: str, target: str, decoded: str) -> WordAlignFile:

    return WordAlignFile(
        file_id=file_id,
        target=target,
        decoded=decoded,
        wer=get_wer(target, decoded),
        ler=get_ler(target, decoded),
        align_path=get_align_index_path(target, decoded),
    )


def load_word_align_file(path_file: Path) -> List[WordAlignFile]:

    with open(path_file, "r") as file:
        data = json.load(file)

    out = []

    for file_data in data:
        align_path = get_align_index_path(
            file_data["target"], file_data["word_prediction_no_lm"]
        )
        if len(align_path) == 0:
            continue
        out.append(
            WordAlignFile(
                file_id=correct_name_fbcluster_output(file_data["sample_id"]),
                target=file_data["target"],
                decoded=file_data["word_prediction_no_lm"],
                wer=file_data["wer"],
                ler=file_data["ler"],
                align_path=align_path,
            )
        )
    return out
