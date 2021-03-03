# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import re
import string
from typing import Set


PUNCTUATIONS_TO_REMOVE = (
    string.punctuation.replace("'", "")
    .replace("-", "")
    .replace("–", "")
    .replace("/", "")
    + "«»‟″“”…‘•„‚≤ᵉ"
)
PUNCTUATIONS_TO_SPACE = "-/–·"
REMOVE_TRANSLATOR = str.maketrans("", "", PUNCTUATIONS_TO_REMOVE)
SPACE_TRANSLATOR = str.maketrans(
    PUNCTUATIONS_TO_SPACE, " " * len(PUNCTUATIONS_TO_SPACE)
)

SPACE = chr(32)
WHITESPACE_NORMALIZER = re.compile(r"\s+")

# fmt: off
LANG_TOKENS = {
    "cs": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "á", "é", "í", "ó", "ú", "ý", "č", "ď", "ě", "ň", "ř", "š", "ť", "ů", "ž",},
    "de": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ß", "ä", "ö", "ü",},
    "en": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",},
    "es": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "á", "é", "í", "ñ", "ó", "ú", "ü",},
    "et": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ä", "õ", "ö", "ü", "š", "ž",},
    "fi": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ä", "å", "ö",},
    "fr": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "à", "â", "æ", "ç", "è", "é", "ê", "ë", "î", "ï", "ô", "ù", "û", "ü", "œ", "ÿ",},
    "hr": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ć", "č", "đ", "š", "ž",},
    "hu": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "á", "é", "ó", "ö", "ú", "ü", "ő", "ű",},
    "it": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "à", "è", "é", "ì", "í", "ï", "ò", "ó", "ù",},
    "lt": {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ą", "č", "ė", "ę", "į", "š", "ū", "ų", "ž",},
    "nl": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "à", "ç", "è", "é", "ê", "ë", "í", "ï", "ö", "ü",},
    "pl": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "ó", "ą", "ć", "ę", "ł", "ń", "ś", "ź", "ż",},
    "ro": {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "â", "î", "ă", "ș", "ț",},
    "sk": {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "á", "ä", "é", "í", "ó", "ô", "ú", "ý", "č", "ď", "ĺ", "ľ", "ň", "ŕ", "š", "ť", "ž",},
    "sl": {"'", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "č", "š", "ž",},
}
# fmt: on


def correct_name_fbcluster_output(name_in: str) -> str:
    r"""A quick patch to solve some discreepancies from the output names
    in the align / WER pipeliness without having to relaunch everything"""

    split_ = name_in.split("-")
    if len(split_) == 3:
        return "-".join(split_[:2])

    return name_in


def is_valid_text(text: str, tokens: Set[str]) -> bool:
    chars = "".join(text.split())
    return all(x in tokens for x in chars)
