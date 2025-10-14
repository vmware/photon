#!/usr/bin/env python3

import os
import license_tree

from common import (
    read_license_from_file,
    err_exit,
    cleanup_license_expression,
)


class Comparator:
    def compare_exps(self, exp_a, exp_b, quiet=False):
        set_a = set()
        set_b = set()
        diff_a = set()
        diff_b = set()

        if os.path.isfile(exp_a):
            # We expect to find only one license here,
            # different from other callers. In the case of spec files,
            # assume that all subpackages have the same licensing.
            exps_from_file = read_license_from_file(exp_a)
            for key in exps_from_file:
                exp_a = exps_from_file[key]
        else:
            exp_a = exp_a

        if os.path.isfile(exp_b):
            exps_from_file = read_license_from_file(exp_b)
            for key in exps_from_file:
                exp_b = exps_from_file[key]
        else:
            exp_b = exp_b

        exp_a = exp_a.replace("\n", " ")
        exp_b = exp_b.replace("\n", " ")

        exp_a = " ".join(exp_a.split())
        exp_b = " ".join(exp_b.split())

        exp_a = cleanup_license_expression(
            license_exp=exp_a, exception_list=[], ignore_list=[]
        )
        exp_b = cleanup_license_expression(
            license_exp=exp_b, exception_list=[], ignore_list=[]
        )

        lic_tree = license_tree.create_exp_tree(exp_a, exception_list=[], ignore_list=[])
        for lic in license_tree.get_top_lvl_ands(lic_tree):
            set_a.add(lic)

        lic_tree = license_tree.create_exp_tree(exp_b, exception_list=[], ignore_list=[])
        for lic in license_tree.get_top_lvl_ands(lic_tree):
            set_b.add(lic)

        diff_a = set_a.difference(set_b)
        diff_b = set_b.difference(set_a)

        if not quiet and diff_a:
            print("Exclusive to expression A:")
            for lic in diff_a:
                print(f"\t{lic}")

        if not quiet and diff_b:
            print("Exclusive to expression B:")
            for lic in diff_b:
                print(f"\t{lic}")

        if diff_a or diff_b:
            if not quiet:
                err_exit("License expressions are not equivalent")
            else:
                return -1

        if not quiet:
            print("License expressions are equivalent")

        return 0
