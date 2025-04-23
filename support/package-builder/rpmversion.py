#!/usr/bin/env python3

import re

from functools import total_ordering


def split_evr(evr):
    """
    Splits EVR string into (epoch, version, release).
    """
    if ":" in evr:
        epoch, rest = evr.split(":", 1)
    else:
        epoch = "0"
        rest = evr
    if "-" in rest:
        version, release = rest.rsplit("-", 1)
    else:
        version, release = rest, ""
    return epoch, version, release


def rpmvercmp_part(a, b):
    """
    Compares individual version or release strings using RPM logic.
    """

    def split_segments(s):
        return re.findall(r"\d+|[a-zA-Z]+|[^a-zA-Z\d]+", s)

    sa = split_segments(a)
    sb = split_segments(b)

    while sa or sb:
        x = sa.pop(0) if sa else ""
        y = sb.pop(0) if sb else ""

        if x == y:
            continue

        if x.isdigit():
            if not y.isdigit():
                return 1
            return (int(x) > int(y)) - (int(x) < int(y))
        if y.isdigit():
            return -1

        return (x > y) - (x < y)

    return 0


@total_ordering
class LooseVersion:
    """
    RPM-aware LooseVersion class that compares EVR (epoch:version-release).
    """

    def __init__(self, vstring):
        self.vstring = vstring
        self.epoch, self.version, self.release = split_evr(vstring)

    def __eq__(self, other):
        return (
            int(self.epoch) == int(other.epoch)
            and rpmvercmp_part(self.version, other.version) == 0
            and rpmvercmp_part(self.release, other.release) == 0
        )

    def __lt__(self, other):
        if int(self.epoch) != int(other.epoch):
            return int(self.epoch) < int(other.epoch)
        ver_cmp = rpmvercmp_part(self.version, other.version)
        if ver_cmp != 0:
            return ver_cmp < 0
        rel_cmp = rpmvercmp_part(self.release, other.release)
        return rel_cmp < 0

    def __repr__(self):
        return f"LooseVersion('{self.vstring}')"


if __name__ == "__main__":
    versions = [
        "1:1.2.3-1",
        "0:1.2.3-2",
        "1.2.3-1",
        "1:1.2.4-0",
        "2:1.0-1",
        "1.0-1",
        "1.0a-2",
        "1.10.a-2",
    ]
    sorted_versions = sorted(LooseVersion(v) for v in versions)
    for v in sorted_versions:
        print(v)

    x = "1.26.2-4.ph5"
    y = "1:1.26.2-4.ph5"
    assert not LooseVersion(x) > LooseVersion(y)
    assert not LooseVersion(x) == LooseVersion(y)
    assert LooseVersion(x) < LooseVersion(y)
