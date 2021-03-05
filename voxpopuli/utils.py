# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Optional

from tqdm.contrib.concurrent import process_map


def multiprocess_run(
        a_list: list, func: callable, n_workers: Optional[int] = None
):
    process_map(func, a_list, max_workers=n_workers, chunksize=1)
