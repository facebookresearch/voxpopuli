###
# Run pyannote speaker diarization (SD) models
###

import os.path as op
import pickle as pkl
import argparse
import torchaudio
from tqdm import tqdm
import torch
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import List
from voxpopuli.common import get_batches, get_lang_dir, is_plenary, get_all_ids_from_dir


def check(root: str, pyannote_cfg="dia_ami"):
    if not op.exists(op.join(root, "full.flac")):
        return True
    rttm_path = op.join(root, f"pyannote.{pyannote_cfg}.rttm")
    pkl_path = op.join(root, f"pyannote.{pyannote_cfg}.pkl")
    if op.exists(rttm_path) and op.exists(pkl_path):
        return True
    json_path = op.join(root, f"pyannote.{pyannote_cfg}.json")
    if op.exists(json_path):
        return True
    return False


def segment_audio_overlap(
    path_audio: Path, dir_out: Path, max_size_sec: int
) -> List[Path]:

    info = torchaudio.info(str(path_audio))[0]
    s_data = info.length // info.channels
    sr = info.rate
    frames = int(sr * max_size_sec)
    if frames % 1 == 0:
        frames += 1

    n_cuts = s_data // frames
    if s_data % frames > min(sr, s_data):
        n_cuts += 1

    n_cuts += n_cuts - 1

    out = []
    offset = 0
    print(f"{path_audio.parent.name} : {n_cuts} segments to save")
    for index in range(n_cuts):
        num_frames = min(frames, s_data - offset)
        if num_frames <= 0:
            break
        data = torchaudio.load(str(path_audio), num_frames=num_frames, offset=offset)[0]
        path_out = dir_out / f"{path_audio.stem}_{index}.flac"
        torchaudio.save(str(path_out), data, sr)
        offset += frames // 2
        out.append(path_out)
    print(f"{path_audio.parent.name} : {n_cuts} segments saved")

    return out, max_size_sec / 2


def merge_segments(path_list_pkl: List[Path], size_overlap: float):

    out = []
    shift = 0
    last_start = None
    for i_pkl, pkl_path in enumerate(path_list_pkl):
        with open(pkl_path, "rb") as f:
            annotation = pkl.load(f)
        segments = [
            (
                shift + round(segment.start, 3),
                shift + round(segment.end, 3),
                f"{i_pkl}_{label}",
            )
            for segment, track, label in annotation.itertracks(yield_label=True)
        ]
        if len(segments) == 0:
            continue

        start_index = 0
        if last_start is not None:
            min_diff = size_overlap + 1
            for i, pack in enumerate(segments):
                s = pack[0]
                d = abs(s - last_start)
                if d < min_diff:
                    min_diff = d
                    start_index = i

        if len(out) > 0:
            s, e, l = segments[start_index]
            out[-1] = last_start, e, l
            start_index += 1

        if start_index < len(segments):
            out += segments[start_index:]

        if len(out) > 0:
            last_start = out[-1][0]

        shift += size_overlap
    return out


def get_segments(
    root: str, device: int = 0, pyannote_cfg="dia_ami", max_size_sec: int = 10 * 60
):

    flac_path = op.join(root, "full.flac")
    if not op.exists(flac_path):
        return

    torch.cuda.set_device(device)

    id_ = Path(flac_path).parent.name

    with TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        list_str, overlapp = segment_audio_overlap(
            Path(flac_path), tmp_dir, max_size_sec
        )
        pyannote_pipeline = torch.hub.load(
            "pyannote/pyannote-audio", pyannote_cfg, pipeline=True
        )
        path_pkls = []
        for index, path_ in enumerate(list_str):
            print(f"{id_}: running pyannote on {index} / {len(list_str)}")
            sd = pyannote_pipeline({"uri": "filename", "audio": path_})
            rttm_path = Path(tmp_dir) / f"pyannote.{pyannote_cfg}_{index}.rttm"
            with open(rttm_path, "w") as f:
                sd.write_rttm(f)
            pkl_path = op.join(tmp_dir, f"pyannote.{pyannote_cfg}_{index}.pkl")
            with open(pkl_path, "wb") as f:
                pkl.dump(sd, f)
            path_pkls.append(pkl_path)

        out_seg = merge_segments(path_pkls, overlapp)

    path_out = Path(root) / f"pyannote.{pyannote_cfg}.json"

    with open(path_out, "w") as f:
        json.dump(out_seg, f, indent=2)


def get(root: str, device: int = 0, pyannote_cfg="dia_ami"):
    assert pyannote_cfg in {"dia_ami", "dia", "sad_ami"}
    flac_path = op.join(root, "full.flac")

    if not op.exists(flac_path):
        return

    torch.cuda.set_device(device)

    pyannote_pipeline = torch.hub.load(
        "pyannote/pyannote-audio", pyannote_cfg, pipeline=True
    )
    if not check(root, pyannote_cfg=pyannote_cfg):
        sd = pyannote_pipeline({"uri": "filename", "audio": flac_path})
        rttm_path = op.join(root, f"pyannote.{pyannote_cfg}.rttm")
        with open(rttm_path, "w") as f:
            sd.write_rttm(f)
        pkl_path = op.join(root, f"pyannote.{pyannote_cfg}.pkl")
        with open(pkl_path, "wb") as f:
            pkl.dump(sd, f)


def get_multiprocess(i, items, pyannote_cfg="dia_ami", max_size_min_input: int = None):
    if i >= len(items):
        return

    if max_size_min_input is not None:
        get_segments(
            items[i], i, pyannote_cfg=pyannote_cfg, max_size_sec=max_size_min_input * 60
        )
    else:
        get(items[i], i, pyannote_cfg=pyannote_cfg)


def get_all(args):
    languages = [lang if lang != "original" else "" for lang in args.languages]
    sessions = get_all_ids_from_dir(Path(args.root))

    if args.filter == "plenary":
        sessions = [id_ for id_ in sessions if is_plenary(id_)]
    elif args.filter == "non_plenary":
        sessions = [id_ for id_ in sessions if not is_plenary(id_)]

    lang_dirs = []
    for session_id in sessions:
        path_session = Path(args.root) / session_id
        langs = [
            get_lang_dir(path_session, lang)
            for lang in languages
            if get_lang_dir(path_session, lang).is_dir()
        ]
        lang_dirs += langs

    items = [d for d in lang_dirs if not check(d, args.pyannote_cfg)]

    if args.max_num is not None:
        items = items[: args.max_num]
    n_devices = torch.cuda.device_count()

    if n_devices < 2:
        for d in items:
            get(d)
    else:
        batches = list(get_batches(items, batch_size=n_devices))
        for batch in tqdm(batches):
            torch.multiprocessing.spawn(
                fn=get_multiprocess,
                args=(batch, args.pyannote_cfg, args.segment_min),
                nprocs=n_devices,
            )


def main():
    parser = argparse.ArgumentParser(
        "Speaker diarization with pyannote."
        " Compute the speakers boundaries for the given audio files"
    )
    parser.add_argument(
        "--root", type=str, help="Root directory containing the session directories"
    )
    parser.add_argument(
        "--filter",
        type=str,
        default="all",
        help="All sessions / plenary sessions only / non plenary only "
        "(default is all sessions).",
        choices=["all", "plenary", "non_plenary"],
    )
    parser.add_argument(
        "--max-num",
        default=None,
        type=int,
        help="If given, maximal number of session to deal with.",
    )
    parser.add_argument(
        "-l",
        "--languages",
        type=str,
        nargs="*",
        required=True,
        help="Languages to deal with. 'original' stands for the original audio.",
    )
    parser.add_argument(
        "--segment-min",
        type=int,
        default=None,
        help="If given, will split the inpit audio into several "
        "overlapping chunks of size segment_min and merge the "
        "resulting segmentation. In this case, a single speaker may end "
        "with several labels if he speaks across several segments."
        "In this case, the output file will be in json format "
        "(to avoid confusion with the proper diharisation output).",
    )
    parser.add_argument(
        "--pyannote-cfg",
        type=str,
        choices=["dia_ami", "dia", "sad_ami"],
        help="Pyannote configuration.",
        default="dia_ami",
    )
    args = parser.parse_args()

    get_all(args)


if __name__ == "__main__":
    main()
