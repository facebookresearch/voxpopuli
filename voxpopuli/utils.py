# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Optional
from multiprocessing import Pool

from tqdm import tqdm


def multiprocess_unordered_run(
        a_list: list, func: callable, n_workers: Optional[int] = None
):
    with Pool(processes=n_workers) as pool:
        for _ in tqdm(pool.imap_unordered(func, a_list), total=len(a_list)):
            pass
