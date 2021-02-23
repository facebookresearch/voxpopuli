# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import logging
from multiprocessing import Pool
from num2words import num2words
import re
import string
import tqdm

from voxpopuli.text import REMOVE_TRANSLATOR, SPACE_TRANSLATOR, SPACE, WHITESPACE_NORMALIZER


def remove_parentheses(text: str) -> str:
    # remove all substring within () or []
    out = ""
    num_p = 0
    start_i = 0
    for i, c in enumerate(text):
        if c == "(" or c == "[":
            if num_p == 0 and i > start_i:
                out += text[start_i : i]
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
    suffix = "" if out == out_tmp else out[len(out_tmp):]
    out = out_tmp.replace(",", ".")
    out = out.replace(":", ".")
    
    # leading characters, e.g. a10, h1n1, $10
    m = re.search(r"^(\D+)", out)
    if m:
        prefix = m.groups()[0]
        return prefix + " " + digit2text(out[len(prefix):], lang) + suffix

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
        if all([len(s) == 3 for s in segs[1:]]): # 12.000.000
            out = out.replace(".", "")
        else: # date 18.4.2009, IP address, time 18.30, etc.
            norm_segs = []
            for s in segs:
                norm_segs.append(digit2text(s, lang))
            return " ".join(norm_segs) + suffix

    m = re.search(r"\b(\d+)(\D+)", out)
    if m:
        suffix = " " + digit2text(out[len(m.groups()[0]):], lang) + suffix
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


def process_text(text: str, lang: str) -> str:
    # TODO: more rules, e.g. "%" -> percent, "°c" -> "degree celsius" for multiple languages
    out = text.lower()
    out = remove_parentheses(out)
    out = out.replace("’", "'")
    out = out.translate(SPACE_TRANSLATOR)
    out = process_digits(out, lang)
    out = out.translate(REMOVE_TRANSLATOR)
    out = WHITESPACE_NORMALIZER.sub(SPACE, out)

    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser("LM data preparation")
    parser.add_argument(
        "-i", "--input",
        type=str,
        required=True,
        help="Input text data (one sentence per line)"
    )
    parser.add_argument("--lang", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file")
    parser.add_argument(
        "--n_proc",
        type=int,
        default=8,
        help="Number of processes to use",
    )
    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = f.readlines()

    out_data = []
    with Pool(args.n_proc) as p:
        for out in tqdm.tqdm(p.starmap(process_text,
                [(d, args.lang) for d in data])):
            out_data.append(out)

    with open(args.output, "w") as o:
        for line in out_data:
            o.write(line)
            o.write("\n")