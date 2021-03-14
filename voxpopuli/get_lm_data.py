# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import csv
import gzip
import logging
from multiprocessing import Pool
import re
import os
import string
from typing import List, Optional, Set, Tuple
from pathlib import Path
import tarfile

from num2words import num2words
import tqdm
from torchaudio.datasets.utils import download_url

from voxpopuli.text import (
    LANG_TOKENS,
    REMOVE_TRANSLATOR,
    SPACE_TRANSLATOR,
    SPACE,
    WHITESPACE_NORMALIZER,
    is_valid_text,
)
from voxpopuli import DOWNLOAD_BASE_URL

PUNCTUATIONS_TO_REMOVE = (
    string.punctuation.replace("'", "")
    .replace("-", "")
    .replace("–", "")
    .replace("/", "")
    + "«»‟″“”…‘•„‚≤ᵉ"
)
PUNCTUATIONS_TO_SPACE = "-/–·"


def remove_parentheses(text: str) -> str:
    # remove all substring within () or []
    out = ""
    num_p = 0
    start_i = 0
    for i, c in enumerate(text):
        if c == "(" or c == "[":
            if num_p == 0 and i > start_i:
                out += text[start_i:i]
            num_p += 1
        elif c == ")" or c == "]":
            num_p -= 1
            if num_p == 0:
                start_i = i + 1

    if len(text) > start_i:
        out += text[start_i:]

    return out


def digit2text(text: str, lang: str) -> str:
    out = text.strip(" ")
    if len(text) == 0 or all([not c.isdigit() for c in text]):
        return text

    # remove leading and trailing punctuations
    is_negative = text[0] == "-"
    out = text.lstrip((string.punctuation))
    out_tmp = out.rstrip((string.punctuation))
    suffix = "" if out == out_tmp else out[len(out_tmp) :]
    out = out_tmp.replace(",", ".")
    out = out.replace(":", ".")

    # leading characters, e.g. a10, h1n1, $10
    m = re.search(r"^(\D+)", out)
    if m:
        prefix = m.groups()[0]
        return prefix + " " + digit2text(out[len(prefix) :], lang) + suffix

    # leading digits, e.g. 50th, 1900s
    to_format = "cardinal"
    # trailing characters as ordinal numbers, e.g. 50th
    # TODO: more rules for multiple languages, e.g. date
    m = re.search(r"\b(\d+)(st|nd|th)\b", out.lower())
    if m:
        to_format = "ordinal"
        out = m.groups()[0]

    # different cases for xx.xx
    if "." in out:
        segs = out.split(".")
        if all([len(s) == 3 for s in segs[1:]]):  # 12.000.000
            out = out.replace(".", "")
        else:  # date 18.4.2009, IP address, time 18.30, etc.
            norm_segs = []
            for s in segs:
                norm_segs.append(digit2text(s, lang))
            return " ".join(norm_segs) + suffix

    m = re.search(r"\b(\d+)(\D+)", out)
    if m:
        suffix = " " + digit2text(out[len(m.groups()[0]) :], lang) + suffix
        out = m.groups()[0]

    if is_negative:
        out = "-" + out

    try:
        num = int(out)
    except ValueError:
        try:
            num = float(out)
        except Exception as e:
            num = out
            logging.warning(f"cannot transform '{out}' to numbers")

    try:
        d = num2words(num, lang=lang, to=to_format)
    except NotImplementedError:  # lang not supported, default to en
        assert lang != "en"
        d = digit2text(out, lang="en")
    except Exception as e:
        d = ""
        logging.warning(f"cannot process {out} ({num}) with {lang} in {to_format} mode")

    if suffix:
        d = d + suffix

    return d


def process_digits(text: str, lang: str) -> str:
    words = text.split()
    out = [digit2text(w, lang) for w in words]

    return " ".join(out)


def load_from_tsv_gz(in_file: Path) -> List[str]:
    output = []
    with gzip.open(in_file, "rt") as f:
        reader = csv.DictReader(
            f,
            delimiter="|",
            quotechar=None,
            doublequote=False,
            lineterminator="\n",
            quoting=csv.QUOTE_NONE,
        )

        for e in reader:
            e = dict(e)
            if e["split"] != "train":
                continue
            text = e["normed_text"]
            text = text.translate(REMOVE_TRANSLATOR)
            output.append(text)

    return output


def process_text(
        text: str, lang: str, tokens: Optional[Set[str]] = None
) -> Tuple[str, Set]:
    # TODO: more rules, e.g. "%" -> percent, "°c" -> "degree celsius", "‰", etc.
    # for multiple languages
    out = text.lower()
    out = remove_parentheses(out)
    out = out.replace("’", "'")
    out = out.translate(SPACE_TRANSLATOR)
    out = process_digits(out, lang)
    out = out.translate(REMOVE_TRANSLATOR)
    out = re.sub("'+", "'", out)
    out = out.strip("'").replace("' ", " ").replace(" '", " ")
    out = WHITESPACE_NORMALIZER.sub(SPACE, out)

    vocab = set()
    if tokens:
        for w in out.split():
            if is_valid_text(w, tokens):
                vocab.add(w)

    return out, vocab


def main(args):
    out_root = Path(args.root) / "lm_data" / args.lang
    out_root.mkdir(exist_ok=True, parents=True)
    asr_root = Path(args.root) / "transcribed_data" / args.lang
    asr_root.mkdir(exist_ok=True, parents=True)

    # Get VoxPopuli transcript
    url = f"{DOWNLOAD_BASE_URL}/annotations/asr/asr_{args.lang}.tsv.gz"
    path = asr_root / Path(url).name
    if not path.exists():
        download_url(url, asr_root.as_posix(), Path(url).name)
    text = load_from_tsv_gz(path)
    # Get Europarl data
    if args.lang != "hr":
        for filename in ["europarl.tgz", "tools.tgz"]:
            url = f"https://www.statmt.org/europarl/v7/{filename}"
            if not (out_root / filename).exists():
                download_url(url, out_root.as_posix(), filename)
        with tarfile.open(out_root / "europarl.tgz", "r:gz") as f:
            members = [
                i for i in f.getmembers()
                if i.name.startswith(f"txt/{args.lang}")
                   and not (out_root / i.name).exists()
            ]
            f.extractall(out_root, members=members)
        with tarfile.open(out_root / "tools.tgz", "r:gz") as f:
            f.extractall(out_root)
        cur_text = set()
        paths = list((out_root / "txt" / args.lang).glob("*.txt"))
        for p in tqdm.tqdm(paths):
            cur_out_path = p.with_suffix('.out')
            script_path = out_root / "tools" / "split-sentences.perl"
            os.system(
                f"perl {script_path.as_posix()} -l {args.lang} -q "
                f"< {p.as_posix()} > {cur_out_path.as_posix()}"
            )
            with open(cur_out_path) as f_o:
                cur_text.update(r.strip() for r in f_o if not r.startswith("<"))
        text.extend(cur_text)
    assert len(text) > 0, "Cannot load any text. Aborting."

    tokens = LANG_TOKENS[args.lang]

    out_text = []
    vocab = set()
    with Pool(args.n_proc) as p:
        for norm_text, uniq_vocab in tqdm.tqdm(
            p.starmap(process_text, [(t, args.lang, tokens) for t in text])
        ):
            out_text.append(norm_text)
            if tokens:
                vocab |= uniq_vocab

    out_path = out_root / "sentences.txt"
    with open(out_path, "w") as o:
        for line in out_text:
            o.write(line + "\n")

    vocab_path = out_root / "vocabulary.txt"
    vocab = sorted(vocab)
    with open(vocab_path, "w") as o:
        o.write(" ".join(vocab))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("LM data preparation")
    parser.add_argument(
        "--root",
        help="data root path",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--lang",
        type=str,
        required=True,
        choices=LANG_TOKENS.keys(),
        help=f"Language of the input text. VoxPopuli provides labelled data in ({', '.join(LANG_TOKENS.keys())})",
    )
    parser.add_argument(
        "--n-proc",
        type=int,
        default=8,
        help="Number of processes to use",
    )
    args = parser.parse_args()

    main(args)
