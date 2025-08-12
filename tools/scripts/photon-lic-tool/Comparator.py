#!/usr/bin/env python3

import os

from common import (
    read_license_from_file,
    extract_top_level_expressions,
    err_exit,
    cleanup_license_expression
)

class Comparator:
    # Strip parantheses only if global, i.e
    # (A OR B OR (A AND C)) -> A OR B OR (A AND C)
    def _strip_global_parans(self, expression):
        if not expression.startswith('('):
            return expression

        parans = 0
        idx = 0
        exp_len = len(expression)

        while idx < exp_len - 1:
            if expression[idx] == '(':
                parans+=1
            elif expression[idx] == ')':
                parans-=1

            if parans == 0:
                return expression

            idx+=1

        return expression[1:-1]


    # Recursively sort each basic block alphabetically.
    # Essentially, each paranthetical expression
    def _sort_exp(self, expression):
        expression = cleanup_license_expression(license_exp=expression, exception_list=[], ignore_list=[])
        stripped = self._strip_global_parans(expression)

        if stripped != expression:
            sorted_exp = self._sort_exp(stripped)
            return f"({sorted_exp})"

        top_level_exps = extract_top_level_expressions(stripped)
        sorted_exps = []
        for exp in top_level_exps:
            exp = self._strip_global_parans(exp)

            ors = exp.split("OR")
            ors = [x.strip() for x in ors]
            ors.sort()
            exp = " OR ".join(ors) if ors else exp

            ands = exp.split("AND")
            ands = [x.strip() for x in ands]
            ands.sort()
            exp = " AND ".join(ands) if ands else exp

            sorted_exps.append(f"({exp})")

        sorted_exp = " AND ".join(sorted_exps)

        return sorted_exp


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

        exp_a = exp_a.replace("\n", " ")
        exp_b = exp_b.replace("\n", " ")

        exp_a = " ".join(exp_a.split())
        exp_b = " ".join(exp_b.split())

        # Sort alphabetically all the paranthetical blocks so that we can
        # do proper comparisons without order mattering
        exp_a = self._sort_exp(exp_a)
        exp_b = self._sort_exp(exp_b)

        # Remove excess parantheses. Everything will be in parantheses
        # after above
        exp_a = cleanup_license_expression(
                    license_exp=exp_a,
                    exception_list=[],
                    ignore_list=[]
                )
        exp_b = cleanup_license_expression(
                    license_exp=exp_b,
                    exception_list=[],
                    ignore_list=[]
                )

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
