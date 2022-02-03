# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

LANGUAGES = [
    "en", "de", "fr", "es", "pl", "it", "ro", "hu", "cs", "nl", "fi", "hr",
    "sk", "sl", "et", "lt", "pt", "bg", "el", "lv", "mt", "sv", "da"
]
LANGUAGES_V2 = [f"{x}_v2" for x in LANGUAGES]

YEARS = list(range(2009, 2020 + 1))

ASR_LANGUAGES = [
    "en", "de", "fr", "es", "pl", "it", "ro", "hu", "cs", "nl", "fi", "hr",
    "sk", "sl", "et", "lt"
]
ASR_ACCENTED_LANGUAGES = [
    "en_accented"
]

S2S_SRC_LANGUAGES = ASR_LANGUAGES

S2S_TGT_LANGUAGES = [
    "en", "de", "fr", "es", "pl", "it", "ro", "hu", "cs", "nl", "fi", "hr",
    "sk", "sl", "et", "lt", "pt", "bg", "el", "lv", "mt", "sv", "da"
]

S2S_TGT_LANGUAGES_WITH_HUMAN_TRANSCRIPTION = ["en", "fr", "es"]

DOWNLOAD_BASE_URL = "https://dl.fbaipublicfiles.com/voxpopuli"
