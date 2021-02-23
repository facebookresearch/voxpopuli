# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import re
import string


PUNCTUATIONS_TO_REMOVE = \
    string.punctuation.replace("'", "").replace("-", "").replace("–", "").replace("/", "") + "«»“”…‘"
PUNCTUATIONS_TO_SPACE = '-/–·'
REMOVE_TRANSLATOR = str.maketrans("", "", PUNCTUATIONS_TO_REMOVE)
SPACE_TRANSLATOR = str.maketrans(PUNCTUATIONS_TO_SPACE, ' '*len(PUNCTUATIONS_TO_SPACE))

SPACE = chr(32)
WHITESPACE_NORMALIZER = re.compile(r'\s+')


def correct_name_fbcluster_output(name_in: str) -> str:
    r"""A quick patch to solve some discreepancies from the output names
    in the align / WER pipeliness without having to relaunch everything"""

    split_ = name_in.split("-")
    if len(split_) == 3:
        return "-".join(split_[:2])

    return name_in
