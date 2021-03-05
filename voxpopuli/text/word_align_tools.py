# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


from pathlib import Path
from typing import List, NamedTuple

from voxpopuli.segmentation import correct_name_fbcluster_output


class AlignedWord(NamedTuple):
    start: float
    end: float
    word: str


class AlignedData(NamedTuple):
    file_id: str
    data: List[AlignedWord]


def load_audio_align_wav2letter(input_path: Path) -> List[AlignedData]:

    with open(input_path, "r") as file:
        data = file.readlines()

    output = []

    for line in data:
        file_id, segments = line.split("\t")
        file_id = correct_name_fbcluster_output(file_id)
        segments = segments.split("\\n")
        samples = []
        for s in segments:
            (_, _, start, duration, word) = s.split(" ")
            end = float(start) + float(duration)
            samples.append(AlignedWord(float(start), end, word.strip()))
        output.append(AlignedData(file_id, samples))

    return output


def cut_align_data(
    audio_align_data: AlignedData,
    index_align: List[int],
    sil_symbol: str = "$",
    padding_start: float = 0.1,
    padding_end: float = 0.2,
) -> List[AlignedData]:

    base_name = audio_align_data.file_id
    out = []
    last_index = 0
    last_end = 0
    shift = 0

    if len(index_align) == 0:
        return [audio_align_data]

    for cut_index in index_align:

        last_end = audio_align_data.data[cut_index].start + padding_end
        out_align = [
            AlignedWord(max(0, x.start - shift), max(0, x.end - shift), x.word)
            for x in audio_align_data.data[last_index:cut_index]
        ]
        out.append(AlignedData(f"{base_name}_{len(out)}", out_align))
        last_index = cut_index
        shift = max(last_end, audio_align_data.data[last_index].end - padding_start)

    if last_index < len(audio_align_data[-1]):
        out_align = [
            AlignedWord(max(0, x.start - shift), max(0, x.end - shift), x.word)
            for x in audio_align_data.data[index_align[-1] :]
        ]
        out.append(AlignedData(f"{base_name}_{len(out)}", out_align))

    return out
