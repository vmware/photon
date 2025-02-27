import common
from common import copytree, run_cmd, err_exit
import shutil
import os
import multiprocessing
import re

try:
    from licensedcode.cache import get_index
except ImportError:
    print("licensedcode import failed, do 'pip3 install scancode-toolkit'")
    raise


class LicDB:
    def _trim_license_file(
        self,
        license_filename=None,
        taint=None,
        taint_lock=None,
        rule_ignore_list=None,
        rule_ignore_lock=None,
    ):
        ret = 0
        if license_filename is None:
            return -1

        with open(f"{common.db_dir}/{license_filename}", "r") as lic_f:
            key = ""
            lic_str = ""
            for line in lic_f:
                if line.startswith("key:"):
                    key = line.split(":")[1].strip()
                elif line.startswith("spdx_license_key"):
                    lic_str = line.split(":")[1].strip()

                if (
                    lic_str
                    and lic_str.startswith("LicenseRef")
                    and "unknown-spdx" not in lic_str
                ):
                    # dont search with this file,
                    # move to some temp location
                    res = run_cmd(
                        f"mv {common.db_dir}/{license_filename} {common.tmp_lic_db}".split(),
                        ignore_rc=True,
                        quiet=True,
                    )
                    ret = 0 if res.returncode == 0 else -1

                    # ignore all rules that mention this key
                    self._trim_rules_for_key(key, rule_ignore_list, rule_ignore_lock)
                    break

        return ret

    def _trim_job(
        self,
        lic_f_list=None,
        rule_ignore_list=None,
        rule_ignore_lock=None,
        taint=None,
        taint_lock=None,
    ):

        if lic_f_list is None or rule_ignore_list is None:
            return

        for lic_file in lic_f_list:
            with taint_lock:
                if taint.value == 1:
                    return

            if (
                self._trim_license_file(
                    lic_file, taint, taint_lock, rule_ignore_list, rule_ignore_lock
                )
                != 0
            ):
                with taint_lock:
                    taint.value = 1
                return

    # Only search for official spdx licenses.
    # Scancode-toolkit has many many other licenses that it
    # recognizes, but these have no SPDX identifiers yet.
    # Also, many of these "unofficial" licenses that scancode
    # recognizes can be mapped to some other similar license
    # For example, bsd-innosys is just InnoSys version of a BSD-2-Clause.
    # Probably it's fine to match bsd-innosys as BSD-2-Clause.
    def trim_lic_db(self):
        lic_file_lists = list()
        num_cpus = (os.cpu_count() + 1) / 2
        processes = list()
        i = 0

        if not os.path.exists(common.tmp_lic_db) or not os.path.isdir(
            common.tmp_lic_db
        ):
            os.makedirs(common.tmp_lic_db)

        # divide license files into separate lists, to be used for multithreading
        while i < num_cpus:
            lic_f_list = list()
            lic_file_lists.append(lic_f_list)
            i += 1

        i = 0
        for lic_file in os.listdir(common.db_dir):
            if i >= num_cpus:
                i = 0
            lic_file_lists[i].append(lic_file)
            i += 1

        with multiprocessing.Manager() as manager:
            # ideally this would be set() but that is not supported
            rule_ignore_list = manager.list()
            rule_ignore_lock = manager.Lock()
            # tells us if the lic_db operation failed in one of the threads.
            taint = manager.Value("b", 0)
            taint_lock = manager.Lock()

            print("Ignoring unofficial licenses and rules")
            for lic_f_list in lic_file_lists:
                p = multiprocessing.Process(
                    target=self._trim_job,
                    args=(
                        lic_f_list,
                        rule_ignore_list,
                        rule_ignore_lock,
                        taint,
                        taint_lock,
                    ),
                )
                p.start()
                processes.append(p)

            for p in processes:
                p.join()

            if taint.value == 1:
                self.restore_lic_db()
                err_exit()

            # move all rule files that have been marked to be ignored
            print("Moving rules which can be ignored...")
            for rule_f in rule_ignore_list:
                # may be duplicates in the list, so check if already moved
                if not os.path.exists(rule_f):
                    continue

                shutil.move(rule_f, common.tmp_rules_dir)

        # reindex with official licenses only
        print(
            "Reindexing license cache without scancode's unofficial licenses, "
            + "this may take a few mins..."
        )
        if get_index(force=True, index_all_languages=True) is None:
            raise Exception("Failed to reindex license cache!")

    def _get_lic_exp_from_rule_file(self, rule_f_path=None):
        rule_f = None
        lic_exp_line = ""

        if not rule_f_path:
            return None

        with open(rule_f_path, "r") as rule_f:
            multiline = False
            for line in rule_f:
                if line.startswith("license_expression"):
                    lic_exp_line += line.split(":")[-1].strip()
                    multiline = True
                elif multiline and re.search("^.*:.*", line):
                    break
                elif multiline:
                    lic_exp_line += " " + line.strip()

        return lic_exp_line

    def _trim_rules_for_key(self, key, rule_ignore_list, rule_ignore_lock):
        with rule_ignore_lock:
            if not os.path.exists(common.tmp_rules_dir) or not os.path.isdir(
                common.tmp_rules_dir
            ):
                os.makedirs(common.tmp_rules_dir)

        for rule_file in os.listdir(common.rules_dir):
            lic_exp_line = self._get_lic_exp_from_rule_file(
                f"{common.rules_dir}/{rule_file}"
            )

            spdx_ids = [
                exp.strip(" \r\t\n()") for exp in re.split("AND|WITH|OR", lic_exp_line)
            ]
            if key in spdx_ids:
                with rule_ignore_lock:
                    rule_ignore_list.append(f"{common.rules_dir}/{rule_file}")

    def restore_lic_db(self):
        if not os.path.exists(common.tmp_lic_db) or not os.path.exists(
            common.tmp_rules_dir
        ):
            return

        print("Restoring scancode database. This may take a few mins...")
        copytree(common.tmp_lic_db, common.db_dir)
        copytree(common.tmp_rules_dir, common.rules_dir)
        get_index(force=True, index_all_languages=True)
        shutil.rmtree(common.tmp_lic_db)
        shutil.rmtree(common.tmp_rules_dir)
