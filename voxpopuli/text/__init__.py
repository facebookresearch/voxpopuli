def correct_name_fbcluster_output(name_in: str) -> str:
    r"""A quick patch to solve some discreepancies from the output names
    in the align / WER pipeliness without having to relaunch everything"""

    split_ = name_in.split("-")
    if len(split_) == 3:
        return "-".join(split_[:2])

    return name_in
