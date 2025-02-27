from common import read_license_from_file, extract_top_level_expressions, err_exit
import os


class Comparator:
    def compare_exps(self, exp_a, exp_b):
        set_a = set()
        set_b = set()
        diff_a = set()
        diff_b = set()

        if not exp_a:
            err_exit("Please input expression A with -a <exp>")

        if not exp_b:
            err_exit("Please input expression B with -b <exp>")

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

        for lic in extract_top_level_expressions(exp_a):
            set_a.add(lic)

        for lic in extract_top_level_expressions(exp_b):
            set_b.add(lic)

        diff_a = set_a.difference(set_b)
        diff_b = set_b.difference(set_a)

        if diff_a:
            print("Exclusive to expression A:")
            for lic in diff_a:
                print(f"\t{lic}")

        if diff_b:
            print("Exclusive to expression B:")
            for lic in diff_b:
                print(f"\t{lic}")

        if diff_a or diff_b:
            err_exit("License expressions are not equivalent")

        print("License expressions are equivalent")
        return 0
