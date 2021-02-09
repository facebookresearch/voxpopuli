# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os.path as op
import os
import argparse
import soundfile as sf
import shutil
from tqdm import tqdm
from pathlib import Path
from typing import List, Tuple, Union
from multiprocessing import Pool
from voxpopuli.common import (
    is_plenary,
)
from voxpopuli.common.utils import get_all_ids_from_dir
from voxpopuli.segmentation import get_pyannote_segments
from voxpopuli.common.lang import LangCode
from auditok import AudioRegion


def save_timestamp(path_out: Union[str, Path], start: float, end: float) -> None:

    with open(path_out, "w") as f:
        f.write(f"{start}\t{end}")


def load_timestamp(path_data: Union[str, Path]) -> Tuple[float, float]:
    with open(path_data, "r") as f:
        data = f.readline().strip()

    start, end = data.split()
    return float(start), float(end)


def get_path_timestamp(path_audio: Union[str, Path], timestamp_suffix: str) -> Path:
    return Path(path_audio).with_suffix(timestamp_suffix)


def split_with_vad_wav(
    wav_path: Path,
    out_dir: Path,
    min_dur: float,
    max_dur: float,
    max_silence: float,
    strict_min_dur: bool,
    shift: float = 0,
) -> None:

    assert Path(wav_path).suffix == ".wav"
    audio_region = AudioRegion.load(str(wav_path))
    out_dir = Path(out_dir)
    regions = audio_region.split(
        min_dur=min_dur,
        max_dur=max_dur,
        max_silence=max_silence,
        strict_min_dur=strict_min_dur,
    )

    waveform, sr = sf.read(wav_path, dtype="float32")
    out = []
    for i, r in enumerate(regions):
        start = int(r._meta.start * sr)
        end = int(r._meta.end * sr)
        path_seg = out_dir / f"{out_dir.stem}_{i}.flac"
        path_timestamp = get_path_timestamp(path_seg, ".vad.timestamp")
        save_timestamp(path_timestamp, r._meta.start + shift, r._meta.end + shift)
        sf.write(
            str(path_seg), waveform[start:end], sr, subtype="PCM_16", format="FLAC"
        )
        out.append(path_seg)

    return out


def split_vad_non_wav(
    audio_path: Path,
    out_dir: Path,
    min_dur: float,
    max_dur: float,
    max_silence: float,
    strict_min_dur: bool,
    shift: float = 0,
) -> None:
    path_wav = Path(audio_path).with_suffix(".wav")
    to_wav(audio_path, path_wav)
    out = split_with_vad_wav(
        path_wav, out_dir, min_dur, max_dur, max_silence, strict_min_dur, shift
    )
    os.remove(path_wav)
    return out


def to_wav(path_in: Path, path_out: Path) -> None:

    assert Path(path_out).suffix == ".wav"
    waveform, sr = sf.read(str(path_in), dtype="float32")
    sf.write(str(path_out), waveform, sr, format="WAV")


def split_audio(
    flac_path: Path,
    segments: List[Tuple[float, float, str]],
    out_root: Union[str, Path],
    pyannote_suffix: str,
) -> List[Path]:

    out_root = Path(out_root)
    if out_root.is_dir():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True)

    sr = sf.info(flac_path).samplerate
    flac_path = Path(flac_path)

    def save_clip(i, start, end):
        name = f"{i:03d}_{start:.0f}-{end:.0f}"
        out_audio_path = out_root / f"{name}.flac"
        save_timestamp(get_path_timestamp(out_audio_path, pyannote_suffix), start, end)
        clip, _ = sf.read(flac_path, start=int(start * sr), stop=int(end * sr))
        sf.write(out_audio_path, clip, sr, subtype="PCM_16", format="FLAC")
        return out_audio_path

    last_start, last_end, last_speaker = segments[0]

    out_paths = []
    for i, (start_t, end_t, speaker) in enumerate(segments):
        if speaker == last_speaker:
            last_end = end_t
            continue
        out_audio_path = save_clip(i, last_start, last_end)
        last_start = start_t
        last_speaker = speaker
        last_end = end_t
        out_paths.append(out_audio_path)

    save_clip(len(segments), last_start, last_end)

    return out_paths


def get_segments(en_root, pyannote_cfg, min_duration) -> List[Tuple[float, float, str]]:
    try:
        return get_pyannote_segments(en_root, pyannote_cfg, min_duration=min_duration)
    except FileNotFoundError:
        return None


class FileSegmenter:
    def __init__(
        self,
        root_in: str,
        out_dir: str,
        languages: List[str],
        pyannote_cfg="sad_ami",
        min_duration=1.0,
        split_vad=True,
        min_dur_vad=15,
        max_dur_vad=30,
        max_silence_vad=1.5,
        strict_min_dur_vad=True,
    ):

        self.root_in = root_in
        self.out_dir = out_dir
        self.languages = languages
        self.pyannote_cfg = pyannote_cfg
        self.min_duration = min_duration
        self.split_vad = split_vad
        self.min_dur_vad = min_dur_vad
        self.max_dur_vad = max_dur_vad
        self.max_silence_vad = max_silence_vad
        self.strict_min_dur_vad = strict_min_dur_vad

    def get_root_lang_id(self, id_: str, lang_code: str) -> bool:
        return Path(self.root_in) / id_ / f"{id_}_{lang_code}"

    def get_out_root(self, id_, lang_code) -> Path:
        return (
            Path(self.out_dir)
            / id_
            / f"{id_}_{lang_code}"
            / f"paragraphs_{self.pyannote_cfg}"
        )

    def split_audio(self, id_):

        found = 0
        for lang in self.languages:
            en_root = self.get_root_lang_id(id_, lang)
            if not en_root.is_dir():
                continue
            segments = get_segments(en_root, self.pyannote_cfg, self.min_duration)
            if segments is None:
                continue

            found += 1
            flac_path = en_root / "full.flac"
            out_root = self.get_out_root(id_, lang)

            pyannote_suffix = f".pyannote.{self.pyannote_cfg}"
            out_audio = split_audio(flac_path, segments, out_root, pyannote_suffix)

            if not self.split_vad:
                continue

            for flac_path in out_audio:
                dir_out = flac_path.parent / flac_path.stem
                dir_out.mkdir()
                path_timestamp_audio = get_path_timestamp(flac_path, pyannote_suffix)
                shift = load_timestamp(path_timestamp_audio)[0]
                vad_seq = split_vad_non_wav(
                    flac_path,
                    dir_out,
                    min_dur=self.min_dur_vad,
                    max_dur=self.max_dur_vad,
                    max_silence=self.max_silence_vad,
                    strict_min_dur=self.strict_min_dur_vad,
                    shift=shift,
                )
                os.remove(flac_path)
                if len(vad_seq) == 0:
                    shutil.rmtree(dir_out)
                    os.remove(flac_path.with_suffix(f".pyannote.{self.pyannote_cfg}"))

        return found


def get_all(args):
    id_list = [x for x in get_all_ids_from_dir(Path(args.root))]
    if args.mode == "plenary":
        id_list = [x for x in id_list if is_plenary(x)]
    if args.mode == "non_plenary":
        id_list = [x for x in id_list if not is_plenary(x)]
    if args.max_num is not None:
        id_list = id_list[: args.max_num]

    segmenter = FileSegmenter(
        args.root,
        args.output,
        args.languages,
        pyannote_cfg=args.pyannote_cfg,
        min_duration=args.min_duration,
        split_vad=not args.no_vad,
        min_dur_vad=args.min_dur_vad,
        max_dur_vad=args.max_dur_vad,
        max_silence_vad=args.max_silence_vad,
    )
    found = 0
    with Pool(args.nproc) as p:
        for x in tqdm(
            p.imap_unordered(segmenter.split_audio, id_list), total=len(id_list)
        ):
            found += x

    print(f"{found} audio data segmented")


def main():
    parser = argparse.ArgumentParser(
        "Cut the data by speaker. " "run_pyanote_sd.py must have been run before"
    )
    parser.add_argument("--root", type=str, required=True, help="Input root directory")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output directory, if different from the input " "one",
    )
    parser.add_argument(
        "--languages",
        type=str,
        nargs="*",
        help="If given, Ttranslated data to deal with",
    )
    parser.add_argument(
        "--max-num",
        default=None,
        type=int,
        help="If given, maximum number of session to deal with",
    )
    parser.add_argument("--nproc", default=8, type=int, help="Number of processes")
    parser.add_argument(
        "--pyannote-cfg",
        default="dia_ami",
        type=str,
        choices=["dia", "dia_ami", "sad_ami"],
    )
    parser.add_argument("--min-duration", default=1.0, type=float)
    parser.add_argument("--no-vad", action="store_true")
    parser.add_argument("--min-dur-vad", default=15, type=int)
    parser.add_argument("--max-dur-vad", default=30, type=int)
    parser.add_argument("--max-silence-vad", default=1.5, type=float)
    parser.add_argument(
        "--mode", choices=["all", "plenary", "non_plenary"], default="all"
    )
    args = parser.parse_args()

    if args.output is None:
        args.output = args.root

    if args.languages is None:
        args.languages = [x.value for x in LangCode]

    get_all(args)


if __name__ == "__main__":
    main()
