# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import torchaudio
import shutil
import os
import torch
import json
import string
from pathlib import Path
from typing import NamedTuple, List, Optional, Set, Tuple
from multiprocessing import Pool

from voxpopuli.text.wer_tools import (
    WordAlignFile,
    load_word_align_file,
    get_partial_transcriptions,
    get_wer,
    get_ler,
    create_word_align_file,
    reinsert_punctuation,
)
from voxpopuli.text.word_align_tools import (
    AlignedData,
    AlignedWord,
    cut_align_data,
    load_audio_align_wav2letter,
)

from voxpopuli.segmentation import is_id_valid, to_wav2letter_format


class CutIndex(NamedTuple):
    index_word: int
    index_align: int


class SilCutConfig(NamedTuple):
    padding_start: float
    padding_end: float
    min_size_sil: float
    min_size_audio: Optional[float] = None


class FullSegConfig(NamedTuple):
    segmentation_cfg: SilCutConfig
    vad_cfg: SilCutConfig
    target_size_segment: int
    sil_symbol: str = "$"


def save_timestamp(ts_segmentation, ts_vad, path_out):

    out = {
        "start": ts_segmentation[0],
        "end": ts_segmentation[1],
        "vad": [(x[0] + ts_segmentation[0], x[1] + ts_segmentation[0]) for x in ts_vad],
    }

    with open(path_out, "w") as f:
        json.dump(out, f, indent=2)


def save_transcription(target: str, decoded: str, path_out: Path):
    path_out = path_out.with_suffix(".json")
    out = {
        "target": target,
        "decoded": decoded,
        "wer": get_wer(target, decoded),
        "ler": get_ler(target, decoded),
    }

    with open(path_out, "w", encoding="utf8") as file:
        json.dump(out, file, indent=2, ensure_ascii=False)


def add_punc_from_tsv(path_tsv, align_text, chars, punc):

    with open(path_tsv, "r") as f:
        text = f.read()
    return reinsert_punctuation(text, align_text, chars, punc)


def cut_with_segment(
    data: torch.tensor,
    sr: int,
    audio_align_data: AlignedData,
    index_align: List[int],
    padding_start: float = 0.1,
    padding_end: float = 0.2,
) -> List[torch.tensor]:

    last_start = 0
    out = []
    timestamps = []
    if len(index_align) == 0:
        return [data], [(0, data.size(0) / sr)]

    for cut_index in index_align:

        last_end = audio_align_data.data[cut_index].start + padding_end
        s = int(last_start * sr)
        e = int(last_end * sr)
        out.append(data[s:e])
        timestamps.append((last_start, last_end))
        last_start = max(last_end, audio_align_data.data[cut_index].end - padding_start)

    if index_align[-1] < len(audio_align_data[-1]):
        s = int(last_start * sr)
        out.append(data[s:])
        timestamps.append((last_start, data.size(0) / sr))

    return out, timestamps


def segment_word_align(
    audio_align_data: AlignedData,
    word_align_data: WordAlignFile,
    sil_symbol: str = "$",
    size_min_sil: float = 0.5,
    target_size_segment: float = 1,
    punc_mark=None,
) -> List[CutIndex]:

    out = []
    cum_size = 0
    index_target_transcription = 0
    index_char_transcription = 0

    if punc_mark is None:
        punc_mark = []

    target = word_align_data.target.split()

    for index_align, align in enumerate(audio_align_data.data[:-1]):

        curr_size = align.end - align.start
        cum_size += curr_size

        if align.word != sil_symbol:
            has_punc = target[index_target_transcription][-1] in punc_mark
            if not has_punc:
                if align.word != target[index_target_transcription]:
                    print(word_align_data.file_id)
                    print(word_align_data.target)
                    print(align.word, target[index_target_transcription])
                assert align.word == target[index_target_transcription]
            index_char_transcription += len(target[index_target_transcription]) + 1
            index_target_transcription += 1
            continue
        if index_align == 0:
            continue
        if word_align_data.align_path[index_target_transcription].action != "=":
            continue
        if not has_punc:
            if cum_size < target_size_segment:
                continue
            if curr_size < size_min_sil:
                continue

        if has_punc:
            index_char_transcription += 1

        out.append(
            CutIndex(index_word=index_char_transcription - 1, index_align=index_align)
        )
        cum_size = 0

    return out


def cut_sils(
    data: torch.tensor,
    sr: int,
    audio_align_data: AlignedData,
    padding_start: float = 0.5,
    padding_end: float = 0.2,
    sil_symbol: str = "$",
    min_size_sil: float = 0.8,
    min_size_audio: float = 0.5,
) -> List[torch.tensor]:

    out = []
    start = 0
    ts_vad = []
    for align in audio_align_data.data:

        if align.word == sil_symbol:
            if align.end - align.start > min_size_sil:
                end = align.start + padding_end
                if end - start > min_size_audio:
                    s = int(start * sr)
                    e = int(end * sr)
                    out.append(data[s:e])
                    ts_vad.append((start, end))
                start = max(end, align.end - padding_start)
    if float(data.size(0)) / sr - start > min_size_audio:
        s = int(start * sr)
        out.append(data[s:])
        ts_vad.append((start, data.size(0) / sr))

    if len(out) > 0:
        return torch.cat(out, dim=0), ts_vad
    else:
        return None, None


def remove_extremities(
    data: torch.tensor,
    sr: int,
    audio_align_data: AlignedData,
    padding_start: float = 0.5,
    padding_end: float = 0.2,
    sil_symbol: str = "$",
) -> Tuple[torch.tensor, AlignedData]:

    index_start = 0
    while audio_align_data.data[index_start].word == sil_symbol:
        index_start += 1

    index_end = -1
    while audio_align_data.data[index_end].word == sil_symbol:
        index_end -= 1

    start = max(0, audio_align_data.data[index_start].start - padding_start)
    out_data = [
        AlignedWord(max(0, x.start - start), max(0, x.end - start), x.word)
        for x in audio_align_data.data[index_start : index_end + 1]
    ]
    e = int(
        min(data.size(0), (audio_align_data.data[index_end].end + padding_end) * sr)
    )
    s = int(start * sr)
    return data[s:e], AlignedData(audio_align_data.file_id, out_data)


def get_matches(
    word_align_file: List[WordAlignFile], audio_align_file: List[AlignedData]
) -> List[Tuple[WordAlignFile, AlignedData]]:

    word_align_file.sort(key=lambda x: x.file_id)
    audio_align_file.sort(key=lambda x: x.file_id)

    i_ = 0
    out = []
    max_i = len(audio_align_file)
    for w_d in word_align_file:
        while i_ < max_i and audio_align_file[i_].file_id < w_d.file_id:
            i_ += 1

        if i_ < max_i and audio_align_file[i_].file_id == w_d.file_id:
            out.append((w_d, audio_align_file[i_]))

    return out


def process_file(
    word_align_file: WordAlignFile,
    audio_align_file: AlignedData,
    path_audio: Path,
    dir_out: Path,
    full_seg_cfg: FullSegConfig,
    punc_mark=None,
) -> None:

    name_out = word_align_file.file_id
    dir_out.mkdir(exist_ok=True)
    cut_index = segment_word_align(
        audio_align_file,
        word_align_file,
        sil_symbol=full_seg_cfg.sil_symbol,
        size_min_sil=full_seg_cfg.segmentation_cfg.min_size_sil,
        target_size_segment=full_seg_cfg.target_size_segment,
        punc_mark=punc_mark,
    )

    trans_list = get_partial_transcriptions(
        word_align_file, [x.index_word for x in cut_index]
    )

    audio, sr = torchaudio.load(path_audio)
    audio = to_wav2letter_format(audio, sr)
    audio = audio.mean(dim=0)
    sr = 16000

    segs, ts_segmentation = cut_with_segment(
        audio,
        sr,
        audio_align_file,
        [x.index_align for x in cut_index],
        padding_start=full_seg_cfg.segmentation_cfg.padding_start,
        padding_end=full_seg_cfg.segmentation_cfg.padding_end,
    )
    new_align = cut_align_data(
        audio_align_file,
        [x.index_align for x in cut_index],
        sil_symbol=full_seg_cfg.sil_symbol,
        padding_start=full_seg_cfg.segmentation_cfg.padding_start,
        padding_end=full_seg_cfg.segmentation_cfg.padding_end,
    )

    for index, seg in enumerate(segs):

        seg, curr_align = remove_extremities(seg, sr, new_align[index])
        seg_no_sil, ts_vad = cut_sils(
            seg,
            sr,
            curr_align,
            min_size_sil=full_seg_cfg.vad_cfg.min_size_sil,
            padding_start=full_seg_cfg.vad_cfg.padding_start,
            padding_end=full_seg_cfg.vad_cfg.padding_end,
            min_size_audio=full_seg_cfg.vad_cfg.min_size_audio,
        )

        if seg_no_sil is None:
            continue

        if seg_no_sil.size(0) == 0:
            continue

        path_out = dir_out / f"{name_out}_{index}.flac"
        torchaudio.save(str(path_out), seg_no_sil, sr)
        path_trans = dir_out / f"{name_out}_{index}_trans.json"
        target, decoded = trans_list[index]
        save_transcription(target, decoded, path_trans)

        path_timestamps = dir_out / f"{name_out}_{index}_timestamps.json"
        save_timestamp(ts_segmentation[index], ts_vad, path_timestamps)


def process_session_lang(
    path_wer: Path,
    path_align: Path,
    dir_audio: Path,
    dir_out: Path,
    full_seg_cfg: FullSegConfig,
    max_wer: Optional[float] = None,
    max_ler: Optional[float] = None,
    chars=string.ascii_lowercase,
    punc_mark=None,
):

    word_align_data = load_word_align_file(path_wer)
    audio_align_data = load_audio_align_wav2letter(path_align)

    if max_wer is not None:
        word_align_data = [x for x in word_align_data if x.wer < max_wer]

    if max_ler is not None:
        word_align_data = [x for x in word_align_data if x.ler < max_ler]

    matches = get_matches(word_align_data, audio_align_data)
    print(f"{path_wer.stem} : {len(matches)} matches found")

    for w_d, a_d in matches:
        align_text = " ".join([x.word for x in a_d.data if x.word != "$"])
        if len(align_text) == 0:
            continue
        try:
            if punc_mark is not None:
                path_tsv = dir_audio / f"{w_d.file_id}.tsv"
                align_text = add_punc_from_tsv(path_tsv, align_text, chars, punc_mark)
            final_wd = create_word_align_file(w_d.file_id, align_text, w_d.decoded)
            dir_session = dir_out / final_wd.file_id
            path_audio = dir_audio / f"{final_wd.file_id}.flac"
            if not path_audio.is_file():
                print(f"ERROR: {str(path_audio)} not found")
                continue
            dir_out.mkdir(exist_ok=True, parents=True)
            process_file(
                final_wd,
                a_d,
                path_audio,
                dir_session,
                full_seg_cfg,
                punc_mark=punc_mark,
            )

            path_speaker = dir_audio / f"{final_wd.file_id}.speaker"
            path_out_speaker = dir_session / f"{final_wd.file_id}.speaker"
            if path_out_speaker.is_file():
                os.remove(path_out_speaker)
            shutil.copyfile(path_speaker, path_out_speaker)
        except FileNotFoundError:
            continue


class FinalAudioSegmenter:
    def __init__(
        self,
        root_audio: Path,
        root_wer: Path,
        root_align: Path,
        root_out: Path,
        lang: str,
        full_seg_cfg: FullSegConfig,
        max_wer: Optional[float] = None,
        max_ler: Optional[float] = None,
        chars=string.ascii_lowercase,
        punc_mark=";.?!",
    ):

        self.root_audio = root_audio
        self.root_wer = root_wer
        self.root_align = root_align
        self.root_out = root_out
        self.full_seg_cfg = full_seg_cfg
        self.max_wer = max_wer
        self.max_ler = max_ler
        self.lang = lang
        self.chars = chars
        self.punc_mark = punc_mark

    def processs_session(self, session_id: str):

        path_wer = self.root_wer / f"{session_id}_{self.lang}_wer_no_lm_wav2letter.json"
        path_align = self.root_align / f"{session_id}_{self.lang}_align_wav2letter.txt"

        dir_audio = self.get_dir_paragraph(session_id)

        if not dir_audio.is_dir():
            raise RuntimeError(f"ERROR: paragraph data not found at {dir_audio}")

        dir_out = self.root_out / session_id
        process_session_lang(
            path_wer,
            path_align,
            dir_audio,
            dir_out,
            self.full_seg_cfg,
            self.max_wer,
            self.max_ler,
            chars=self.chars,
            punc_mark=self.punc_mark,
        )

    def get_dir_paragraph(self, session_id: str):
        return self.root_audio / "original" / session_id / "paragraphs"

    def process_db(self, session_ids: List[str], num_proc: int = 8):

        print(f"Launching the segmentation on {len(session_ids)} sessions")
        with Pool(num_proc) as pool:
            out = list(
                pool.imap_unordered(self.processs_session, session_ids, chunksize=30)
            )


def get_session_ids(root_align: Path, root_wer: Path, lang: str) -> Set[str]:

    files_align = [
        x.name
        for x in root_align.glob(f"*_{lang}_align_wav2letter.txt")
        if is_id_valid(x.name[:-24])
    ]
    files_wer = [
        x.name
        for x in root_wer.glob(f"*_{lang}_wer_no_lm_wav2letter.json")
        if is_id_valid(x.name[:-29])
    ]
    ids_align = {x[:-24] for x in files_align}
    ids_wer = {x[:-29] for x in files_wer}

    return ids_align.intersection(ids_wer)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        "Using the decoded data and the word alignment, segment the labelled "
        "sequences in small chunk with their estimated WER"
    )
    parser.add_argument(
        "--dir_wer",
        type=str,
        required=True,
        help="Directory containing the decoding output",
    )
    parser.add_argument(
        "--dir_align",
        type=str,
        required=True,
        help="Directory containing the alignment output",
    )
    parser.add_argument(
        "--dir_audio",
        type=str,
        required=True,
        help="Directory containing the audio data",
    )
    parser.add_argument(
        "--n_proc",
        type=int,
        default=8,
        help="Number of processes to use",
    )
    parser.add_argument("--lang", type=str, required=True, help="Language Code.")
    parser.add_argument(
        "-o", "--output", type=str, required=True, help="Output directory."
    )
    parser_segmentation = parser.add_argument_group("Segmentation parameters")
    parser_segmentation.add_argument(
        "--target_size_segment",
        type=int,
        default=20,
        help="Target size of each segment",
    )
    parser_segmentation.add_argument(
        "--padding_start_seg",
        type=float,
        default=0.4,
        help="Padding start segmentation",
    )
    parser_segmentation.add_argument(
        "--padding_end_seg", type=float, default=0.4, help="Padding end segmentation"
    )
    parser_segmentation.add_argument(
        "--min_size_sil_seg",
        type=float,
        default=0.7,
        help="Minimum size of a silence when cutting a sequence.",
    )
    parser_segmentation.add_argument(
        "--max_wer",
        type=float,
        default=None,
        help="Ignores all sequences with a Word Error Rate (WER) higher than "
        "the given value",
    )
    parser_segmentation.add_argument(
        "--max_ler",
        type=float,
        default=100,
        help="Ignores all sequences with a Letter Error Rate (LER) higher than "
        "the given value",
    )
    parser_segmentation.add_argument(
        "--ignore_punctuation",
        action="store_true",
        help="Activates to ignore all punctuation and cut only by silence.",
    )
    parser_segmentation.add_argument(
        "--path_chars",
        type=str,
        default=None,
        help="Path to the char file containing the tokens of the considered language. (Default tokens are english latin)",
    )
    parser_sil = parser.add_argument_group("VAD extraction parameters")
    parser_sil.add_argument(
        "--padding_start_vad",
        type=float,
        default=0.2,
        help="Padding start segmentation",
    )
    parser_sil.add_argument(
        "--padding_end_vad", type=float, default=0.5, help="Padding end segmentation"
    )
    parser_sil.add_argument(
        "--min_size_sil_vad",
        type=float,
        default=1,
        help="Minimum size of a silence when considering voice activity.",
    )
    parser_sil.add_argument(
        "--min_size_audio_vad",
        type=float,
        default=0.5,
        help="Isolated audio segments smaller than the given threshold will"
        " be removed",
    )
    args = parser.parse_args()

    args.dir_audio = Path(args.dir_audio)
    args.dir_wer = Path(args.dir_wer)
    args.dir_align = Path(args.dir_align)
    args.output = Path(args.output)

    seg_cfg = SilCutConfig(
        padding_start=args.padding_start_seg,
        padding_end=args.padding_end_seg,
        min_size_sil=args.min_size_sil_seg,
    )
    vad_cfg = SilCutConfig(
        padding_start=args.padding_start_vad,
        padding_end=args.padding_end_vad,
        min_size_sil=args.min_size_sil_vad,
        min_size_audio=args.min_size_audio_vad,
    )
    full_seg_cfg = FullSegConfig(
        segmentation_cfg=seg_cfg,
        vad_cfg=vad_cfg,
        target_size_segment=args.target_size_segment,
    )

    id_list = get_session_ids(args.dir_align, args.dir_wer, args.lang)
    print(f"{len(id_list)} sessions found")

    letters = string.ascii_lowercase
    if args.path_chars is not None:
        with open(args.path_chars, "r") as f:
            letters = "".join([x.strip() for x in f.readlines()])

    punc_mark = None if args.ignore_punctuation else ".;?!"

    segmenter = FinalAudioSegmenter(
        args.dir_audio,
        args.dir_wer,
        args.dir_align,
        args.output,
        args.lang,
        full_seg_cfg,
        max_wer=args.max_wer,
        max_ler=args.max_ler,
        chars=letters,
        punc_mark=punc_mark,
    )
    segmenter.process_db(list(id_list), num_proc=args.n_proc)
