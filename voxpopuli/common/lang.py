# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import enum


class LangCode(enum.Enum):
    HR = "hr"
    HU = "hu"
    IT = "it"
    SL = "sl"
    ES = "es"
    BG = "bg"
    NL = "nl"
    ET = "et"
    DE = "de"
    MT = "mt"
    PT = "pt"
    DA = "da"
    EN = "en"
    FI = "fi"
    LV = "lv"
    PL = "pl"
    RO = "ro"
    FR = "fr"
    LT = "lt"
    SK = "sk"
    SV = "sv"
    CS = "cs"  # Czech
    MK = "mk"  # Macedonian
    SQ = "sq"  # Albanian
    BS = "bs"  # Bosnian
    RU = "ru"  # Russian
    AR = "ar"  # Arabic
    YAP = "yap"  # Yapese
    SA = "sa"  # Sanskrit
    XAL = "xal"  # Kalmyk
    BR = "br"  # Breton
    CU = "cu"  # Church Slavic
    GA = "ga"  # Irish
    LA = "la"  # Latin
    TR = "tr"  # Turkish
    SR = "sr"  # Serbian
    FA = "fa"  # Persian
    UK = "uk"  # Ukrainian
    ZU = "zu"  # Zuru
    ORIGINAL = ""
    UNKNOWN = "unk"  # Other languages not listed here

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
