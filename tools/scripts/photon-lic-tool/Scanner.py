# Scanner class, which is used to conduct license scanning for packages.
# Includes ability to scan SRPMS, archives, normal files, and even to
# build source trees from spec files under SPECS/<pkg>/<pkg>.spec
import common
from common import (
    copytree,
    run_cmd,
    pr_err,
    err_exit,
    get_exceptions_list,
    extract_top_level_expressions,
    strip_license_id,
    cleanup_license_expression,
    is_extractable,
    download_file,
    copy_spec_to_rpm_build_root,
)
from CacheUtil import CacheUtil
from LicDB import LicDB
from DockerUtil import DockerUtil

import yaml
import os
import multiprocessing
import shutil
import re
import hashlib
import json


class Scanner:
    # parse scan yaml output and produce a valid SPDX expression
    def _parse_scan_yaml(self, yaml_fn=None, exceptions_list=[], cached_spdx_ids=set()):
        license_exps = set()
        lic_str = None

        if yaml_fn is None:
            pr_err("No yaml file passed to parse function!")
            return None

        print("Opening " + yaml_fn)
        with open(yaml_fn, "r") as yaml_f:
            scancode_yaml = yaml.load(yaml_f, Loader=yaml.SafeLoader)
            for license_detection in scancode_yaml["license_detections"]:
                spdx_exp = license_detection["license_expression_spdx"]

                if not spdx_exp:
                    continue

                # A little on the logic here:
                # License expressions reported by scancode are typically for one
                # file only For cases with ANDs, e.g A AND B, this is the license
                # expression for 1 file. So, if we have another file which is
                # licensed under C, how to construct the overall expression? There
                # are two options:
                # 1. (A AND B) AND C
                # 2. A AND B AND C
                #
                # Option 1 preserves the license expression for each file, wherea
                # option 2 combines into one expression. Option 2 should be correct,
                # because we are attempting to provide terms under which the entire
                # package is to be licensed under. It should be accurate to say the
                # entire package needs to be licensed under the terms of A and
                # B and C.
                #
                # C can also be a composite expression such as (C OR D) - ORs should
                # be preserved within parantheses, because the OR operator is
                # disjunctive. The conjunctive AND must be used at the top level to
                # connect all license expressions.
                #
                # What about crazier expressions like:
                # ((A AND B) OR C) AND D
                #
                # It should be handled in the same way - keep the OR together.
                # For expressions such as ((A AND B) AND C) AND D, these will be
                # flattened by the license_tree API in cleanup_license_expression().
                spdx_exps = extract_top_level_expressions(spdx_exp)
                for exp in spdx_exps:
                    exp = strip_license_id(exp)
                    exp = cleanup_license_expression(
                        ignore_list=common.ignore_list,
                        exception_list=exceptions_list,
                        license_exp=exp,
                    )
                    license_exps.add(exp)

        license_exps.update(cached_spdx_ids)

        for exp in license_exps:
            if exp is None or exp == "":
                continue

            # Add parantheses now, then we can flatten the expression later
            if (
                ("AND" in exp or "OR" in exp)
                and not (exp.startswith("(") and exp.endswith(")"))
                and len(license_exps) > 1
            ):
                exp = f"({exp})"

            if lic_str is None:
                lic_str = exp
            else:
                lic_str = f"{lic_str} AND {exp}"

        # Cleanup extra parantheses, connectors, etc., from the final expression
        lic_str = cleanup_license_expression(
            ignore_list=common.ignore_list,
            exception_list=exceptions_list,
            license_exp=lic_str,
        )

        return lic_str

    def _install_build_reqs(self, spec_path=None):
        build_reqs = []

        if not spec_path:
            return

        with open(spec_path, "r") as spec_f:
            for line in spec_f:
                match = re.match("BuildRequires:.*", line)
                if match:
                    build_reqs.append(match.group().split(":")[1].strip())

        install_cmd = [
            "tdnf",
            "install",
            "-y",
        ]

        install_cmd.extend(build_reqs)

        result = run_cmd(install_cmd, ignore_rc=True)

        if result.returncode != 0:
            err_exit(
                f"Failed to install package dependencies for {spec_path}\n"
                f"{result.stdout.decode()}"
            )

    # Find all extracted archives, i.e dirs with -extract at the end.
    # And delete them, so they are not copied to the scanning dir
    def _remove_extracted_archives(self, top_dir=None):
        if not top_dir:
            return

        for root, dirs, files in os.walk(top_dir):
            if not os.path.basename(root).endswith("-extract"):
                continue

            # archive path is the same, just without the added extension
            archive_path = re.sub("-extract$", "", root)
            try:
                print(f"[DELETE EXTRACTED ARCHIVE]: {archive_path}")
                os.remove(archive_path)
            except Exception as e:
                pr_err(
                    f"Failed to delete extracted archive {archive_path} "
                    + f"for extracted dir {root}!\n"
                    + f"Error: {e}"
                )

    # downloads all required sources from .spec file and validates
    # against checksum
    def _download_srcs(
        self,
        spec_path=None,
        output_dir=None,
        dist_tag="",
        alt_src_url="",
        photon_root="",
    ):
        config_yaml_path = f"{os.path.dirname(spec_path)}/config.yaml"
        config_yaml = None
        archive = ""
        archive_checksum = ""
        src_url = ""
        local_checksum = ""

        if not spec_path:
            return

        with open(config_yaml_path, "r") as config_yaml_f:
            config_yaml = yaml.load(config_yaml_f, Loader=yaml.SafeLoader)

        for source in config_yaml["sources"]:
            archive = source["archive"]
            archive_checksum = source["archive_sha512sum"]
            src_url = f"https://packages.vmware.com/photon/photon_sources/1.0/{archive}"

            if not is_extractable(archive):
                pr_err(
                    f"WARNING: {archive} doesn't appear to have an archive extension, is "
                    + "this intentional?"
                )

            # check locally first
            local_path = f"{photon_root}/stage/SOURCES/{archive}"
            output_path = f"{output_dir}/{archive}"
            if os.path.exists(local_path) and not os.path.exists(output_path):
                print(f"LOCAL: Found {archive} at {local_path}, copying...")
                shutil.copy2(local_path, output_path)
            elif not os.path.exists(output_path):
                rc = download_file(src_url, output_path, allow_failure=True)
                if rc < 0 and alt_src_url:
                    pr_err(f"Failed to download {src_url}, trying alternative")
                    src_url = f"{alt_src_url}/{archive}"

                    rc = download_file(src_url, output_path, allow_failure=True)

                # Finally, try downloading from the outside URL
                if rc < 0 and "url" in source:
                    pr_err(f"Failed to download {src_url}, trying directly")
                    src_url = source["url"]
                    rc = download_file(src_url, output_path, allow_failure=True)

                if rc < 0:
                    err_exit(f"Failed to download {src_url}!")

            # Validate checksum
            with open(output_path, "rb") as src_f:
                local_checksum = hashlib.file_digest(src_f, "sha512").hexdigest()

            if local_checksum != archive_checksum:
                err_exit(
                    f"For source: {archive}\n"
                    f"Downloaded {local_checksum} != {archive_checksum} from config.yaml\n"
                    f"config.yaml: {archive_checksum}\n"
                    f"Downloaded: {local_checksum}"
                )
            else:
                print(f"Checksum integrity check passed for {archive}")

    # run rpmbuild -bp to get the source RPM to scan
    def _extract_src_rpm(self, rpm_path=None):
        dist_tag = None
        rpm_build_cmds = []

        if rpm_path is None:
            return None

        if not os.path.exists(common.rpm_install_root):
            os.makedirs(common.rpm_build_root)

        # clean the working dir
        shutil.rmtree(common.rpm_install_root)

        result = run_cmd(f"rpm -i {rpm_path} --root {common.rpm_install_root}")
        if result.returncode != 0:
            pr_err("Failed to install source RPM!")
            return None

        # should only be one spec file here, since it's a clean dir
        spec_fn = ""
        for spec in os.listdir(f"{common.rpm_build_root}/SPECS"):
            spec_fn = spec
            break

        rpm_build_cmds = [
            "rpmbuild",
            "-bp",
            "--nodeps",
            "--define",
            f"%_topdir {common.rpm_build_root}",
            "--define",
            "%with_check 0",
        ]

        if spec_fn.startswith("linux"):
            src_rpm_basename = os.path.basename(rpm_path)
            dist_tag = re.search(r"\.ph.*\.src", src_rpm_basename).group().split(".")[1]

            rpm_build_cmds += ["--define", f"%dist .{dist_tag}"]

        rpm_build_cmds.append(f"{common.rpm_build_root}/SPECS/{spec_fn}")

        result = run_cmd(
            rpm_build_cmds,
            ignore_rc=True,
        )

        if result.returncode != 0:
            pr_err(f"Failed to prep src rpm for {spec_fn}:\n{result.stdout.decode()}")
            return None

        return f"{common.rpm_build_root}/BUILD"

    # Build the scan directory from a photon spec file,
    # e.g SPECS/<pkg name>/<pkg.spec>. Similar to extract_src_rpm()
    def _build_scan_dir_from_spec_dir(self, spec_path=None, alt_src_url=None):
        dist_tag = ""
        attempts = 0
        ph_root = ""

        if not spec_path:
            return None

        copy_spec_to_rpm_build_root(spec_path)

        # find build-config.json
        ph_root = os.path.abspath(spec_path)
        while os.path.basename(ph_root) != "SPECS" and ph_root:
            ph_root = os.path.dirname(ph_root)

        if not ph_root:
            err_exit(f"Failed to find the SPECS path for {spec_path}!")

        ph_root = os.path.dirname(ph_root)

        spec_fn = os.path.basename(spec_path)
        if spec_fn.startswith("linux"):
            with open(f"{ph_root}/build-config.json") as build_conf:
                build_config_json = json.load(build_conf)
                dist_tag = build_config_json["photon-build-param"]["photon-dist-tag"]

        self._download_srcs(
            spec_path,
            f"{common.rpm_build_root}/SOURCES",
            dist_tag=dist_tag,
            alt_src_url=alt_src_url,
            photon_root=ph_root,
        )

        rpm_build_cmds = [
            "rpmbuild",
            "-bp",
            "--nodeps",
            "--define",
            f"%_topdir {common.rpm_build_root}",
            "--define",
            "%with_check 0",
        ]

        if dist_tag:
            rpm_build_cmds.extend(["--define", f"%dist {dist_tag}"])

        rpm_build_cmds.append(f"{common.rpm_build_root}/SPECS/{spec_fn}")

        while attempts < 2:
            attempts += 1
            result = run_cmd(
                rpm_build_cmds,
                ignore_rc=True,
            )

            if result.returncode != 0:
                pr_err(
                    f"Failed to build src directory for {spec_fn}:\n{result.stdout.decode()}"
                )

                print("Trying to install required packages and trying again...")
                self._install_build_reqs(spec_path)
            else:
                break

        return f"{common.rpm_build_root}/BUILD"

    def _setup_scan_dir(self, path="", build_spec=False, alt_src_url=None):
        scan_dir = ""

        if not path:
            err_exit("No path given to Scanner._setup_scan_dir()")

        if path.endswith(".src.rpm"):
            scan_dir = self._extract_src_rpm(path)
            if not scan_dir:
                err_exit(f"Failed to extract {path} as .src.rpm")
        elif build_spec:
            # this is a Photon spec directory, i.e SPECS/<pkg name>
            if not path.endswith(".spec"):
                err_exit("--build_spec option requires --path to point to a .spec file")
            scan_dir = self._build_scan_dir_from_spec_dir(path, alt_src_url)

            if not scan_dir:
                err_exit(f"Failed to build source directory for {path}")
        elif not os.path.isdir(path):
            shutil.copy2(path, f"{common.ph_scan_dir}")

            input_file = f"{common.ph_scan_dir}/{os.path.basename(path)}"

            # extract with scancode universal extractor
            print(f"Extracting output from {input_file}...")
            res = run_cmd(f"extractcode {input_file} --shallow")
            if res.returncode != 0:
                err_exit(f"ERROR: Extraction of {input_file} failed!")

            if os.path.exists(f"{input_file}-extract"):
                scan_dir = (
                    f"{common.ph_scan_dir}/{os.path.basename(input_file)}-extract"
                )
            else:
                # if not an archive, just use the whole default scan dir
                scan_dir = common.ph_scan_dir
        else:
            dir_path = path
            if dir_path[-1] == "/":
                dir_path = dir_path[:-1]

            dir_path = os.path.basename(dir_path)
            os.makedirs(f"{common.ph_scan_dir}/{dir_path}", exist_ok=True)
            copytree(path, f"{common.ph_scan_dir}/{dir_path}")

            scan_dir = os.path.abspath(f"{common.ph_scan_dir}/{dir_path}")

        # extract any latent archives which are not yet extracted
        # do it as a best effort, as it may fail occasionally
        run_cmd(f"extractcode {scan_dir}", ignore_rc=True)
        self._remove_extracted_archives(scan_dir)

        return scan_dir

    def _remove_known_failures_from_scan_dir(self, scan_dir=None):
        if not scan_dir:
            return

        for root, dirs, files in os.walk(scan_dir):
            for file in files:
                full_path = f"{root}/{file}"
                if not os.path.exists(full_path) or os.path.isdir(full_path):
                    continue

                with open(full_path, "rb") as check_f:
                    checksum = hashlib.file_digest(check_f, "md5").hexdigest()

                if checksum in common.known_failures:
                    os.remove(full_path)

    # Main scanning function
    def scan(
        self,
        build_spec=None,
        path=None,
        score=90,
        yaml=None,
        cpus=1,
        docker=False,
        alt_src_url=None,
    ):
        yaml_tmp_path = f"{common.ph_scan_dir}/scan-results.yaml"
        cwd = os.getcwd()
        scan_dir = None
        yaml_output_path = ""
        exceptions_list = None
        cache_util = None
        lic_db = None
        cached_spdx_ids = set()

        if not path:
            err_exit("ERROR: No input given for scan!")

        if docker:
            docker_util = DockerUtil()
            docker_util.run_docker_cmd(
                cmd="scan",
                build_spec=build_spec,
                path=path,
                redis_host=common.redis_host,
                redis_port=common.redis_port,
                redis_ttl=common.redis_ttl,
                score=score,
                yaml=yaml,
                cpus=cpus,
            )
            return

        if not cpus:
            cpus = multiprocessing.cpu_count()

        if not score:
            score = 90

        if common.redis_host and common.redis_port:
            cache_util = CacheUtil(
                common.redis_host, common.redis_port, common.redis_ttl
            )
        elif common.redis_host or common.redis_port:
            err_exit("For redis cache, need both the host and the port!")

        # clean out the dir if anything there before
        if os.path.exists(common.ph_scan_dir):
            shutil.rmtree(common.ph_scan_dir)

        os.makedirs(common.ph_scan_dir)

        scan_dir = self._setup_scan_dir(path, build_spec, alt_src_url)

        if not common.no_trimming:
            lic_db = LicDB()
            print(
                "Trimming license DB to include only valid SPDX licenses "
                + "before scan..."
            )
            try:
                lic_db.trim_lic_db()
            except Exception as e:
                pr_err(f"Failed to trim license database: {e}")
                lic_db.restore_lic_db()
                err_exit()

        # if redis cache, use it
        if cache_util:
            scan_dir = cache_util.populate_scan_dir(scan_dir)
        else:
            # Don't need to run this if cache_util, because cache_util
            # will check when populating the scan dir
            self._remove_known_failures_from_scan_dir(scan_dir)

        # run the scan
        result = run_cmd(
            [
                "scancode",
                "--license",
                "-n",
                str(cpus),
                "--license-score",
                str(score),
                "--yaml",
                yaml_tmp_path,
                scan_dir,
            ]
        )

        if result.returncode != 0:
            pr_err("ERROR: scancode failed during scanning process :(")
            if not common.no_trimming:
                lic_db.restore_lic_db()
            err_exit()

        if not common.no_trimming:
            print("Restoring license DB after scan completion")
            lic_db.restore_lic_db()

        exceptions_list = get_exceptions_list()

        if cache_util:
            cache_util.add_all_scan_results_to_cache(
                scan_dir, yaml_tmp_path, exceptions_list
            )
            cached_spdx_ids = cache_util.cached_spdx_ids

        # Produce full SPDX expression using scancode output results
        spdx_exp = self._parse_scan_yaml(
            yaml_fn=yaml_tmp_path,
            exceptions_list=exceptions_list,
            cached_spdx_ids=cached_spdx_ids,
        )

        if yaml:
            if yaml.startswith("/"):
                yaml_output_path = yaml
            else:
                # local file, relative path
                yaml_output_path = f"{cwd}/{yaml}"

            shutil.copy(yaml_tmp_path, yaml_output_path)
            print(f"Detailed scan yaml produced at: {yaml_output_path}")

            # also produce a yaml for the cached results
            if cache_util:
                cache_util.report_cache_results(
                    yaml_output_dir=os.path.dirname(yaml_output_path)
                )

        print(f"SPDX Expression: {spdx_exp}")

        try:
            if os.path.exists(scan_dir):
                shutil.rmtree(scan_dir)

            if os.path.exists(common.ph_scan_dir):
                shutil.rmtree(common.ph_scan_dir)
        except Exception as e:
            pr_err(f"Failed to remove temp dir(s) after scan: {e}")
