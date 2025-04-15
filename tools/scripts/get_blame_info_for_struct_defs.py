# /*
# * Copyright © 2023 VMware, Inc.
# * SPDX-License-Identifier: Apache-2.0 OR GPL-2.0-only
# */
#
# This script extracts the blame informationfrom git repo
# of linux kernel and append that information in given object
# file.
#
# Required Arguments:
# - Linux kernel Git repo path
# - path to object file
#
# Command:
# python get_blame_info_for_struct_defs.py <path_to_objFile> <path_to_git_repo>
#
#
# Changelog:
# - Tue 15 Apr Ankit Jain <ankit-aj.jain@broadcom.com>
# * Adding initial version


import re
import subprocess
import os
import logging
import argparse
from datetime import datetime, date


class DeferredLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.logs = []

    def emit(self, record):
        self.logs.append(self.format(record))

    def flush_logs(self):
        for log in self.logs:
            print(log)
        self.logs = []


logger = logging.getLogger(__name__)


def generate_pahole_output(obj_file):
    try:
        result = subprocess.run(
            ["pahole", "--show_decl_info", obj_file],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        logger.error(f"Pahole failed on {obj_file}: {e}")
        return []
    except FileNotFoundError:
        logger.error("Pahole command not found, make sure it's installed")
        return []


def parse_structure_definition(pahole_lines):
    structures = []
    struct_name = None
    all_lines = []
    source_file = None
    brace_count = 0

    pat = r"__attribute__\s*\(\s*\(\s*__aligned__\s*\(\s*\d+\s*\)\s*\)\s*\)"

    for line in pahole_lines:
        line = line.strip()
        if re.match(r"/\*.*:\d+\s*\*/", line):
            file_match = re.search(r"([\/\w\.\-]+):\d+", line)
            if file_match:
                source_file = file_match.group(1).strip()
                logger.debug(
                    f"extracted source file path: {source_file}"
                )
        if not struct_name and re.match(r"struct\s+(\w+)\s*{", line):
            struct_name = re.match(r"struct\s+(\w+)\s*{", line).group(1)
            all_lines = [line]
            brace_count = 1
            continue
        if struct_name:
            brace_count += line.count("{") - line.count("}")
            if brace_count == 0 and "}" in line:
                all_lines.append("};")
                if struct_name and source_file:
                    structures.append((struct_name, all_lines, source_file))
                    logger.debug(
                        f"Parsed {struct_name} with {len(all_lines)} lines"
                    )
                struct_name = None
                all_lines = []
                source_file = None
                brace_count = 0
                continue
            if not (line.startswith("}") and re.search(pat, line)):
                all_lines.append(line)
    if struct_name and brace_count == 0 and all_lines and source_file:
        structures.append((struct_name, all_lines, source_file))
        logger.debug(
            f"Parsed structure {struct_name} with {len(all_lines)} lines"
        )
    elif struct_name:
        logger.error(
            f"Incomplete def for {struct_name}, brace_count: {brace_count}"
        )
    return structures


def is_valid_git_repo(repo_path):
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip() == "true"
    except subprocess.CalledProcessError:
        return False
    except Exception as e:
        logger.error(f"Error: Git repository at {repo_path}: {e}")
        return False


def count_members(lines):
    pat = r"__attribute__\s*\(\s*\(\s*__aligned__\s*\(\s*\d+\s*\)\s*\)\s*\)"
    member_count = 0
    brace_count = 0
    for line in lines:
        line = line.strip()
        if (
            not line
            or line.startswith("/*")
            or line in ["{", "}", "};"]
            or (line.startswith("}") and re.search(pat, line))
        ):
            continue

        if re.match(r"(struct|union)\s+\w*\s*{", line):
            if brace_count == 0:
                member_count += 1
            brace_count += 1
        elif brace_count > 0:
            brace_count += line.count("{") - line.count("}")
            if brace_count == 0 and "}" in line:
                continue
        else:
            if not re.match(r"struct\s+\w+\s*{", line):
                member_count += 1

    return member_count


def find_structure_in_repo(struct_name, pahole_lines, repo_path, source_file):
    if not is_valid_git_repo(repo_path):
        logger.error(f"invalid or inaccessible Git repository: {repo_path}")
        return None, None, None

    try:
        if not source_file.startswith("./"):
            source_file = "./" + source_file
        full_file_path = os.path.join(repo_path, source_file.lstrip("./"))

        if not os.path.exists(full_file_path):
            logger.error(
                f"src file {source_file} not found in repository {repo_path}"
            )
            return None, None, None

        logger.debug(
            f"using source file {source_file} for structure {struct_name}"
        )

        cat_cmd = ["git", "-C", repo_path, "show", f"HEAD:{source_file}"]
        file_content = subprocess.check_output(
            cat_cmd, text=True, stderr=subprocess.DEVNULL
        ).splitlines()

        start_found = False
        source_lines = []
        line_numbers = []
        brace_count = 0

        for i, line in enumerate(file_content, 1):
            line = line.strip()
            if (
                not line
                or line.startswith("/*")
                or line.startswith("//")
                or line.startswith("*")
                or line.startswith("#")
            ):
                continue

            if not start_found and f"struct {struct_name} {{" in line:
                logger.debug(f"match found {line} at line number {i}")
                start_found = True
                source_lines.append(line)
                line_numbers.append(i)
                brace_count = 1
            elif start_found:
                if not (
                    line.startswith("/*")
                    or line.startswith("//")
                    or line.startswith("*")
                    or not line
                    or line.startswith("#")
                ):
                    source_lines.append(line)
                    line_numbers.append(i)
                    brace_count += line.count("{") - line.count("}")
                    if brace_count == 0 and "}" in line:
                        source_lines.append("}")
                        break

        if not source_lines or source_lines[-1] != "}" or brace_count != 0:
            logger.error(
                f"could not find complete structure definition for"
                f"{struct_name} in {source_file}, brace_count: {brace_count}"
            )
            return None, None, None

        pahole_members = [
            line
            for line in pahole_lines
            if not line.startswith("/*") and line not in ["{", "}", "};"]
        ]
        pahole_member_count = count_members(pahole_members)

        source_members = [
            line
            for line in source_lines
            if not line.startswith("/*") and line not in ["{", "}", "};"]
        ]
        source_member_count = count_members(source_members)

        if pahole_member_count != source_member_count:
            logger.debug(
                "member count mismatch:"
                f"Pahole has {pahole_member_count} members {pahole_members},"
                f"source has {source_member_count} members {source_members}"
                f"for structure {struct_name}"
            )
            # Uncomment this line to stop the script upon this error
            # General usecase is parse everything without stopping and
            # let all errors be thrown at the end of the script execution.
            # return None, None, None

        logger.debug(
            "member count mismatch:"
            f"Pahole has {pahole_member_count} members {pahole_members},"
            f"source has {source_member_count} members {source_members}"
            f"for structure {struct_name}"
        )
        if not line_numbers:
            logger.error("No line numbers found for structure block")
            return None, None, None

        return source_lines, line_numbers, source_file
    except subprocess.CalledProcessError as e:
        logger.error(f"Git cmd failed for {struct_name}: {e}")
        return None, None, None
    except Exception as e:
        logger.error(f"Unexpected error for {struct_name}: {e}")
        return None, None, None


def get_blame_info(src_lines, line_nums, repo_path, src_file, struct_name):
    blame_info = []
    blame_dates = []
    partial_line = 0
    if not line_nums:
        return blame_info, blame_dates
    for i, line_num in enumerate(line_nums):
        blame_cmd = [
            "git",
            "-C",
            repo_path,
            "blame",
            "-l",
            src_file,
            f"-L{line_num},{line_num}",
        ]
        try:
            blame_output = subprocess.check_output(
                blame_cmd, text=True, stderr=subprocess.DEVNULL
            ).strip()
            if blame_output:
                blame_line = blame_output.split("\n")[0]
                if (
                    "\t" in blame_line
                    or f"struct {struct_name} {{" in blame_line
                ):
                    parts = blame_line.split("(", 1)
                    if len(parts) > 1:
                        commit_id_line = parts[0].strip().split(maxsplit=1)
                        if commit_id_line:
                            commit_id = commit_id_line[0][:11]
                        else:
                            commit_id = "Unknown"
                        date_line = ""
                        commit_author = parts[1].strip().split(" ")
                        if len(commit_author) > 1:
                            author = commit_author[0]
                            for j in range(1, len(commit_author)):
                                if commit_author[j][0].isdigit():
                                    date_line = parts[1].strip().split(
                                        maxsplit=j)[j]
                                    break
                                else:
                                    author += " " + commit_author[j]
                        else:
                            author = "Unknown"
                        date_str = date_line.split(" ", 1)[0]
                        try:
                            blame_date = datetime.strptime(
                                date_str, "%Y-%m-%d").date()
                            blame_dates.append(blame_date)
                        except ValueError:
                            logger.warning(
                                f"Invalid date format in blame: {date_str}")
                            blame_dates.append(date.min)
                        linenum = date_line.split()[3].rstrip(")").strip()

                        blame_comment = (
                            f"/* {commit_id} {author} {date_str} {linenum} */"
                        )
                        if i < len(src_lines):
                            if partial_line > 0:
                                logger.debug(f"{blame_line}")
                            else:
                                blame_info.append(
                                    (src_lines[i], blame_comment))
                            logger.debug(f"{blame_line}")
                            if (
                                f"struct {struct_name} {{" not in src_lines[i]
                                and ";" not in src_lines[i]
                                and "struct {{" not in src_lines[i]
                                and "union {{" not in src_lines[i]
                            ):
                                partial_line += 1
                            else:
                                partial_line = 0
                    else:
                        blame_info.append(
                            (src_lines[i], "/* No blame info */"))
                else:
                    blame_info.append((src_lines[i], "/* No blame info */"))
            else:
                blame_info.append((src_lines[i], "/* No blame info */"))
        except subprocess.CalledProcessError as e:
            logger.error(
                f"Git blame failed for line {line_num} in {src_file}: {e}"
            )
            blame_info.append((src_lines[i], "/* Blame error */"))
    return blame_info, blame_dates


def append_final_output(pahole_lines, blame_info, blame_dates, struct_name):
    pat = r"__attribute__\s*\(\s*\(\s*__aligned__\s*\(\s*\d+\s*\)\s*\)\s*\)"
    final_blame_info = []
    source_idx = 0
    current_date = date.today()
    most_recent_date = (
        max(blame_dates)
        if blame_dates and max(blame_dates) != date.min
        else current_date
    )
    days_since_change = (current_date - most_recent_date).days
    years_since_change = days_since_change // 365

    for pahole_line in pahole_lines:
        if (
            not pahole_line
            or pahole_line.startswith("/*")
            or pahole_line in ["}", "};"]
            or (pahole_line.startswith("}") and re.search(pat, pahole_line))
        ):
            final_blame_info.append((pahole_line, ""))
            continue
        if f"struct {struct_name} {{" in pahole_line:
            if source_idx < len(blame_info):
                blame_comment = blame_info[source_idx][1]
                blame_comment += (
                    f" /* No changes since last {years_since_change} years */"
                )
                final_blame_info.append((pahole_line, blame_comment))
                source_idx += 1
            else:
                final_blame_info.append((pahole_line, "/* No blame info */"))
            continue

        while source_idx < len(blame_info) and (
            blame_info[source_idx][0].startswith("/*")
            or blame_info[source_idx][0] in ["{", "}"]
        ):
            source_idx += 1

        if source_idx < len(blame_info):
            final_blame_info.append((pahole_line, blame_info[source_idx][1]))
            source_idx += 1
        else:
            final_blame_info.append((pahole_line, "/* Not found in source */"))

    return final_blame_info, years_since_change


def main():
    parser = argparse.ArgumentParser(
        description="Extract structure definitions from object file and"
                    " get git blame info."
    )
    parser.add_argument(
        "obj_file",
        help="Path to object(.o) file",
    )
    parser.add_argument(
        "repo_path", help="Path to the Git repository (Linux kernel)")
    args = parser.parse_args()

    obj_file = args.obj_file
    git_repo_path = args.repo_path

    deferred_handler = DeferredLogHandler()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[deferred_handler],
    )
    logger.handlers = [deferred_handler]

    if not os.path.isfile(obj_file):
        logger.error(f"Invalid Object file: {obj_file}")
        deferred_handler.flush_logs()
        return
    if not os.path.isdir(git_repo_path):
        logger.error(f"Invalid repository path: {git_repo_path}")
        deferred_handler.flush_logs()
        return

    pahole_lines = generate_pahole_output(obj_file)
    if not pahole_lines:
        logger.error(f"Invalid object file: {obj_file}")
        deferred_handler.flush_logs()
        return

    structures = parse_structure_definition(pahole_lines)

    if not structures:
        logger.error("No structure definitions parsed or error occurred.")
        deferred_handler.flush_logs()
        return

    for struct_name, lines, source_file in structures:
        source_lines, line_numbers, src_file = find_structure_in_repo(
            struct_name, lines, git_repo_path, source_file
        )

        print(
            f"\nStructure Definition with Blame Information:"
            f" {struct_name} in {source_file}"
        )
        if source_lines is None:
            print("  /* No git blame information found for this structure */")
            for line in lines:
                print(f"  {line}")
            continue

        blame_info, blame_dates = get_blame_info(
            source_lines, line_numbers, git_repo_path, src_file, struct_name
        )
        final_blame_info, years_since_change = append_final_output(
            lines, blame_info, blame_dates, struct_name
        )
        if final_blame_info:
            for line, blame_comment in final_blame_info:
                print(f"  {line} {blame_comment}")

    deferred_handler.flush_logs()


if __name__ == "__main__":
    main()
