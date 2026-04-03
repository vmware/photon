#!/usr/bin/env python3

# Scanner class, which is used to conduct license scanning for packages.
# Includes ability to scan SRPMS, archives, normal files, and even to
# build source trees from spec files under SPECS/<pkg>/<pkg>.spec
import common
import license_tree
import yaml
import os
import multiprocessing
import shutil
import re
import hashlib
import json
import errno
import tempfile

from DockerUtil import DockerUtil

from common import (
    err_exit,
    pr_err
)


class Scanner:
    _extra_repo_urls = None
    _config_yaml = {}
    _used_sources = []
    _ph_root = None
    _dist_tag = None

    # parse scan yaml output and produce a valid SPDX expression
    def _parse_scan_yaml(self, yaml_fn=None, exceptions_list=[], cached_spdx_ids=set()):
        license_exps = set()
        lic_str = None

        if yaml_fn is None:
            pr_err("No yaml file passed to parse function!")
            return None

        print(f"Opening: '{yaml_fn}'")
        scancode_yaml = {}
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
            lic_tree = license_tree.create_exp_tree(spdx_exp, exception_list=[], ignore_list=[])
            spdx_exps = license_tree.get_top_lvl_ands(lic_tree)
            for exp in spdx_exps:
                exp = common.strip_license_id(exp)
                exp = common.cleanup_license_expression(
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
        lic_str = common.cleanup_license_expression(
            ignore_list=common.ignore_list,
            exception_list=exceptions_list,
            license_exp=lic_str,
        )

        return lic_str

    # Restore versions of required python packages
    # Keep this in line with list in Dockerfile
    def _restore_python_reqs(self):
        pkgs_vers = {
            "requests": "2.32.3",
            "charset-normalizer": "3.4.2",
            "lxml": "5.4.0",
            "markupsafe": "3.0.2",
            "pyyaml": "6.0.2",
            "redis": "6.0.0",
            "argparse": "1.4.0",
        }

        # check for pip3 command existence
        if not shutil.which("pip3"):
            err_exit(
                "'pip3' command not found, please install with "
                "'tdnf install -y python3-pip'"
            )

        pkg_update_cmd = "pip3 install"

        for pkg in pkgs_vers:
            pkg_update_cmd += f" {pkg}=={pkgs_vers[pkg]}"

        common.run_cmd(pkg_update_cmd)

    def _install_build_reqs(self, spec_path=None):
        build_reqs = []

        if not spec_path:
            return

        # Create the populated spec file
        result = common.run_cmd(
            [
                "rpmspec",
                "-P",
                spec_path,
                "-D",
                f"_topdir {common.rpm_build_root}",
                "-D",
                f"_sourcedir {os.path.dirname(spec_path)}",
            ],
            capture=True,
        )

        populated_spec_path = f"/tmp/{os.path.basename(spec_path)}"
        with open(populated_spec_path, "w") as populated_spec_f:
            populated_spec_f.write(result.stdout.decode())

        spec_path = populated_spec_path

        with open(spec_path, "r") as spec_f:
            for line in spec_f:
                match = re.match(r"BuildRequires:\s+(.*)", line, flags=re.IGNORECASE)
                if match:
                    build_req = match.group(1).replace(" ", "")
                    build_reqs.append(build_req)
                    continue

                match = re.match(r"%define\s+ExtraBuildRequires\s+(.*)", line, flags=re.IGNORECASE)
                if match:
                    for extra_build_req in match.group(1).split(','):
                        extra_build_req = extra_build_req.replace(" ", "")
                        build_reqs.append(extra_build_req)

        install_cmd = "tdnf install -y".split()

        install_cmd.extend(build_reqs)

        if self._extra_repo_urls:
            for i, url in enumerate(self._extra_repo_urls.split(",")):
                extra_repo = f"--repofrompath extra_repo{i},{url}"
                install_cmd.extend(extra_repo.split())

        result = common.run_cmd(install_cmd, ignore_rc=True, capture=True)

        if result.returncode != 0:
            err_msg = f"Failed to install package dependencies for {spec_path}\n"
            if result.stdout:
                err_msg += f"{result.stdout.decode()}"
            if result.stderr:
                err_msg += f"\nStderr:\n{result.stderr.decode()}"

            err_exit(err_msg)

        print("Restoring Python package versions after tdnf packge install...")
        self._restore_python_reqs()

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
                    f"for extracted dir {root}!\n"
                    f"Error: {e}"
                )

    # downloads all required sources from .spec file and validates
    # against checksum
    def _download_srcs(
        self,
        output_dir=None,
        alt_src_url="",
        photon_root="",
    ):
        archive = ""
        archive_checksum = ""
        src_url = ""
        local_checksum = ""
        pub_src_url = ""
        rc = 0

        for source in self._config_yaml["sources"]:
            archive = source["archive"]

            if self._used_sources and archive not in self._used_sources:
                print(f"\nWARNING:'{archive}' is not used in spec file ...\n")
                continue

            archive_checksum = source["archive_sha512sum"]
            pub_src_url = f"{common.ph_pub_url}/photon_sources/1.0/{archive}"

            if not common.is_extractable(archive):
                pr_err(
                    f"WARNING: {archive} doesn't appear to have an archive extension, is "
                    "this intentional?"
                )

            # check locally first
            local_path = f"{photon_root}/stage/SOURCES/{archive}"
            output_path = f"{output_dir}/{archive}"
            if os.path.exists(local_path) and not os.path.exists(output_path):
                print(f"LOCAL: Found {archive} at {local_path}, copying...")
                shutil.copy2(local_path, output_path)
            elif not os.path.exists(output_path):
                if alt_src_url:
                    print(f"Trying to download from {alt_src_url} first...")

                    src_url = f"{alt_src_url}/{archive}"
                    rc = common.download_file(src_url, output_path, allow_failure=True)

                if rc < 0 or not alt_src_url:
                    pr_err(
                        f"Failed to download {src_url}, trying published..."
                    )

                    rc = common.download_file(pub_src_url, output_path, allow_failure=True)

                # Finally, try downloading from the outside URL
                if rc < 0 and "url" in source:
                    pr_err(
                        f"Failed to download {pub_src_url}, trying directly from config.yaml URL"
                    )
                    src_url = source["url"]
                    rc = common.download_file(src_url, output_path, allow_failure=True)

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

    def _rpmbuild_prep(self, rpm_build_cmds=None, spec_path=None):
        attempts = 0
        spec_fn = os.path.basename(spec_path)

        if not rpm_build_cmds:
            err_exit(
                "No RPM build command passed to Scanner._rpmbuild_prep()!"
            )

        while attempts < 2:
            attempts += 1
            result = common.run_cmd(
                rpm_build_cmds,
                ignore_rc=True,
                capture=True,
            )

            if result.returncode == 0:
                return

            pr_err(
                f"Failed to build src directory for {spec_fn}:\n{result.stdout.decode()}"
            )

            if result.stderr:
                pr_err(result.stderr.decode())

            if attempts < 2:
                print("Trying to install required packages and trying again...")
                shutil.rmtree(f"{common.rpm_build_root}/BUILD")
                self._install_build_reqs(spec_path)
            else:
                err_exit()

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

        result = common.run_cmd(f"rpm -i {rpm_path} --root {common.rpm_install_root}")
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
            "-D",
            f"_topdir {common.rpm_build_root}",
            "-D",
            "with_check 0",
        ]

        if spec_fn.startswith("linux"):
            src_rpm_basename = os.path.basename(rpm_path)
            dist_tag = re.search(r"\.ph.*\.src", src_rpm_basename).group().split(".")[1]

            rpm_build_cmds += ["-D", f"dist .{dist_tag}"]

        spec_path = f"{common.rpm_build_root}/SPECS/{spec_fn}"

        rpm_build_cmds.append(spec_path)

        self._rpmbuild_prep(rpm_build_cmds, spec_path)

        return f"{common.rpm_build_root}/BUILD"

    def _set_spec_vars(self, spec_path):
        # find build-config.json
        ph_root = os.path.abspath(spec_path)
        while os.path.basename(ph_root) != "SPECS" and ph_root:
            ph_root = os.path.dirname(ph_root)

        if not ph_root:
            err_exit(f"Failed to find the SPECS path for {spec_path}!")

        self._ph_root = os.path.dirname(ph_root)

        with open(f"{self._ph_root}/build-config.json") as build_conf:
            build_config_json = json.load(build_conf)
            self._dist_tag = build_config_json["photon-build-param"][
                "photon-dist-tag"
            ]

    # Build the scan directory from a photon spec file,
    # e.g SPECS/<pkg name>/<pkg.spec>. Similar to extract_src_rpm()
    def _build_scan_dir_from_spec_dir(self, spec_path=None, alt_src_url=None):
        if not spec_path:
            return None

        common.copy_spec_to_rpm_build_root(spec_path)

        spec_fn = os.path.basename(spec_path)

        self._download_srcs(
            f"{common.rpm_build_root}/SOURCES",
            alt_src_url=alt_src_url,
            photon_root=self._ph_root,
        )

        rpm_build_cmds = [
            "rpmbuild",
            "-bp",
            "--nodeps",
            "-D",
            f"_topdir {common.rpm_build_root}",
            "-D",
            "with_check 0",
            "-D",
            f"dist {self._dist_tag}"
        ]

        rpm_build_cmds.append(f"{common.rpm_build_root}/SPECS/{spec_fn}")

        self._rpmbuild_prep(rpm_build_cmds, spec_path)

        return f"{common.rpm_build_root}/BUILD"

    def _get_used_sources(self, path):
        cmd = []

        if not os.path.exists(path):
            raise FileNotFoundError(
                            errno.ENOENT,
                            os.strerror(errno.ENOENT),
                            path
                        )
        elif not path.endswith(".spec"):
            err_exit("_get_used_sources: path must end with .spec")

        cmd = [
                "rpmspec",
                "-D",
                f"%dist {self._dist_tag}",
                "-D",
                f"_sourcedir {os.path.dirname(path)}",
                "-P",
                path
            ]

        result = common.run_cmd(cmd, capture=True)
        for line in result.stdout.decode().splitlines():
            match = re.match(r"Source[0-9]+:", line)
            if match:
                span = match.span()
                src = line[span[1]:].strip()
                src = os.path.basename(src)
                self._used_sources.append(src)

    def _setup_scan_dir(self, path="", build_spec=False, alt_src_url=None):
        scan_dir = ""

        if not path:
            err_exit("No path given to Scanner._setup_scan_dir()")

        # clean out the dir if anything there before
        if os.path.exists(common.ph_scan_dir):
            shutil.rmtree(common.ph_scan_dir)

        os.makedirs(common.ph_scan_dir)

        if path.endswith(".src.rpm"):
            scan_dir = self._extract_src_rpm(path)
            if not scan_dir:
                err_exit(f"Failed to extract {path} as .src.rpm")
        elif build_spec:
            # this is a Photon spec directory, i.e SPECS/<pkg name>
            if not path.endswith(".spec"):
                err_exit(
                    "--build_spec option requires --path to point to a .spec file"
                )

            self._set_spec_vars(path)

            specDir = os.path.dirname(path)
            config_yaml_path = f"{specDir}/config.yaml"
            if not os.path.exists(config_yaml_path):
                pr_err(
                    f"config.yaml for {path} not found at {config_yaml_path}, nothing to scan"
                )
                return scan_dir

            with open(config_yaml_path, "r") as config_yaml_f:
                self._config_yaml = yaml.load(config_yaml_f, Loader=yaml.SafeLoader)

            if "shared_sources" in self._config_yaml:
                for shared_cfg in self._config_yaml['shared_sources']:
                    with open(f"{self._ph_root}/SPECS/{shared_cfg}") as config_yaml_f:
                        shared_cfg_yaml = yaml.load(config_yaml_f, Loader=yaml.SafeLoader)
                        addl_srcs = shared_cfg_yaml['sources']
                        self._config_yaml['sources'].extend(addl_srcs)

            self._get_used_sources(path)

            scan_dir = self._build_scan_dir_from_spec_dir(path, alt_src_url)

            if not scan_dir:
                err_exit(f"Failed to build source directory for {path}")
        elif not os.path.isdir(path):
            shutil.copy2(path, f"{common.ph_scan_dir}")

            input_file = f"{common.ph_scan_dir}/{os.path.basename(path)}"

            # extract with scancode universal extractor
            print(f"Extracting output from {input_file}...")
            res = common.run_cmd(f"extractcode --verbose {input_file} --shallow")
            if res.returncode != 0:
                err_exit(f"ERROR: Extraction of {input_file} failed!")

            if os.path.exists(f"{input_file}-extract"):
                # For .gem files, file_paths in config.yaml are expressed
                # relative to the parent of the gem-extract directory (e.g.
                # "nokogiri-1.18.8.gem-extract/data.tar.gz-extract/..."),
                # so keep scan_dir as ph_scan_dir rather than descending
                # into the gem-extract subdirectory.
                if path.endswith(".gem"):
                    scan_dir = common.ph_scan_dir
                else:
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
            common.copytree(path, f"{common.ph_scan_dir}/{dir_path}")

            scan_dir = os.path.abspath(f"{common.ph_scan_dir}/{dir_path}")

        # extract any latent archives which are not yet extracted
        # do it as a best effort, as it may fail occasionally
        common.run_cmd(f"extractcode --verbose {scan_dir}", ignore_rc=True)
        self._remove_extracted_archives(scan_dir)

        return scan_dir

    # For some packages with multiple sources, there can be multiple subdirectories under BUILD/
    # each corresponding to a different source archive. Only one is the main source/build directory,
    # but to outsiders we can't really tell which one.
    #
    # As in the case of Linux, for example, some files are copied from one BUILD subdirectory to
    # another, resulting in the same file existing in two separate locations, with different paths.
    #
    # We need to grab the manual review licenses AND delete the file in each place where it exists,
    # and to do this we need the relative paths for both the main source/build directory and the
    # archive directory.
    def _parse_manual_review(self, scan_dir):
        spdx_exp = []
        key = "license_manual_review"
        # Check manual review paths relative to the archive directories
        for archive in self._config_yaml["sources"]:
            if key not in archive:
                continue
            archive_name = archive["archive"]
            if self._used_sources and archive_name not in self._used_sources:
                print(
                    f"\nSkipping '{archive_name}' from manual review because it is unused in spec\n"
                )
                continue

            spdx_exp.extend(self.__parse_manual_review(scan_dir, archive[key]))

        return spdx_exp

    def __parse_found_manual_review_file(
        self, reviewed_shasum, reviewed_spdx_exp, path
    ):
        spdx_exp = []

        with open(path, "rb") as check_f:
            checksum = hashlib.file_digest(check_f, "sha256").hexdigest()

        if checksum != reviewed_shasum:
            common.err_exit(
                f"Manual review required for '{path}'. The checksum has changed, "
                "please review and update the checksum/spdx expression accordingly"
            )

        lic_tree = license_tree.create_exp_tree(reviewed_spdx_exp, exception_list=[],
                                                ignore_list=[])
        spdx_exp.extend(license_tree.get_top_lvl_ands(lic_tree))

        os.remove(path)

        return spdx_exp

    def __parse_manual_review(self, scan_dir, manual_review):
        spdx_exp = []
        missing_files = []

        for reviewed_f in manual_review:
            filePaths = reviewed_f.get("file_paths", [])
            if not filePaths:
                common.err_exit("ERROR: file_paths is empty ...")

            # check the path relative to each subdirectory under BUILD/
            # these are all different paths to the same file, and can be different if scanning
            # config.yaml vs --build_spec. So if we find at least one, it's ok for now.
            found_files = False
            for path in filePaths:
                print(
                    f"Searching for manual review file: '{path}' under '{scan_dir}' ..."
                )
                full_path = f"{scan_dir}/{path}"
                if os.path.exists(full_path):
                    print(f"'{path}' found at '{full_path}' ...")
                    found_files = True
                    if not missing_files:
                        spdx_exp.extend(
                            self.__parse_found_manual_review_file(
                                reviewed_f["sha256sum"],
                                reviewed_f.get("spdx_exp", ""),
                                full_path,
                            )
                        )
                else:
                    common.pr_err(
                        f"ERROR: '{os.path.basename(path)}' NOT FOUND at '{full_path}' ..."
                    )

            if not found_files:
                pr_err(f"ERROR: Failed to find any of the manual review files: {filePaths}")
                missing_files.extend(filePaths)

        if missing_files:
            pr_err("\nERROR: Invalid manual review entries found in config.yaml ...")
            pr_err("Entries:\n" + "\n".join(missing_files))
            err_exit()

        return spdx_exp

    def _cleanup_scan(self, scan_dir=""):
        try:
            if scan_dir and os.path.exists(scan_dir):
                shutil.rmtree(scan_dir)

            if os.path.exists(common.ph_scan_dir):
                shutil.rmtree(common.ph_scan_dir)
        except Exception as e:
            pr_err(f"Failed to remove temp dir(s) after scan: {e}")

    def _check_prereqs(self):
        common.check_scancode_ver()

        commands = {
            "scancode": "pip3 install scancode-toolkit",
            "extractcode": "pip3 install extractcode",
            "rpmbuild": "tdnf install -y rpm-build",
            "rpm": "tdnf install -y rpm",
        }

        for cmd, install_hint in commands.items():
            if not shutil.which(cmd):
                print(
                    f"'{cmd}' command not found, please install with '{install_hint}'"
                )
                err_exit("")

    def _export_yaml(
        self, sc_yaml_out_path="", user_yaml_path=None, cache_util=None, cwd=""
    ):
        if not user_yaml_path:
            return

        if user_yaml_path.startswith("/"):
            yaml_output_path = user_yaml_path
        else:
            # local file, relative path
            yaml_output_path = f"{cwd}/{user_yaml_path}"

        shutil.copy(sc_yaml_out_path, yaml_output_path)
        print(f"Detailed scan yaml produced at: {yaml_output_path}")

        # also produce a yaml for the cached results
        if cache_util:
            cache_util.report_cache_results(
                yaml_output_dir=os.path.dirname(yaml_output_path)
            )

    def scan_config_yaml(
        self,
        build_spec=None,
        path=None,
        score=common.default_lic_score,
        yaml_out=None,
        cpus=0,
        docker=False,
        alt_src_url=None,
        extra_repo_urls=None,
        config_yaml=None,
        timeout=None
    ):
        from Comparator import Comparator

        comparator = Comparator()
        from ruamel.yaml import YAML

        yaml_out_dir = ""

        if not config_yaml:
            err_exit("--config_yaml requires a path!")

        docker_util = DockerUtil() if docker else DockerUtil.detect()
        if docker_util is not None:
            mnt_list, cmd = docker_util.build_scan_docker_cmd(
                build_spec=build_spec,
                path=path,
                redis_host=common.redis_host,
                redis_port=common.redis_port,
                redis_ttl=common.redis_ttl,
                score=score,
                yaml_out=yaml_out,
                cpus=cpus,
                alt_src_url=alt_src_url,
                extra_repo_urls=extra_repo_urls,
                config_yaml=config_yaml,
                timeout=timeout
            )
            docker_util.run_docker_cmd(cmd=cmd, mount_list=mnt_list)
            if yaml_out:
                print(f"yaml output can be found at {yaml_out}")
            return

        if not path.endswith("config.yaml"):
            common.err_exit(
                f"--config_yaml requires `config.yaml` not {os.path.basename(path)}"
            )

        if yaml_out:
            if os.path.isdir(yaml_out):
                yaml_out_dir = yaml_out
            elif not os.path.exists(yaml_out):
                os.makedirs(yaml_out)
                yaml_out_dir = yaml_out
            else:
                common.err_exit("ERROR: --yaml must point to a directory for --config_yaml")

            print(
                f"Outputting scancode YAML for each source under parent directory: {yaml_out_dir}"
            )

        ruamel_yaml = YAML()
        with open(path, "r") as cfg_yaml_f:
            self._config_yaml = ruamel_yaml.load(cfg_yaml_f)

        if not os.path.exists(common.ph_srcs_dir):
            os.makedirs(common.ph_srcs_dir)

        self._set_spec_vars(path)

        # download all srcs in the config yaml
        self._download_srcs(
            common.ph_srcs_dir,
            alt_src_url=alt_src_url,
            photon_root=self._ph_root,
        )

        # scan each source and update the license expression
        for i, source in enumerate(self._config_yaml["sources"]):
            archive = source["archive"]
            local_path = f"{common.ph_srcs_dir}/{archive}"

            if not os.path.exists(local_path):
                common.err_exit(f"ERROR: not found: {local_path}")

            yaml_out = f"{common.ph_scan_tool_dir}/{os.path.basename(local_path)}.yaml"
            spdx_exp = self.scan(
                build_spec=build_spec,
                path=local_path,
                score=score,
                yaml_out=yaml_out,
                cpus=cpus,
                docker=False,
                alt_src_url=alt_src_url,
                extra_repo_urls=extra_repo_urls,
                timeout=timeout
            )

            # Only update if different, not just different order
            if (
                comparator.compare_exps(
                    spdx_exp,
                    source["spdx"]["package"]["license_concluded"],
                    quiet=True
                )
                < 0
            ):
                source["spdx"]["package"]["license_concluded"] = spdx_exp

            if (
                comparator.compare_exps(
                    spdx_exp,
                    source["spdx"]["package"]["license_declared"],
                    quiet=True
                )
                < 0
            ):
                source["spdx"]["package"]["license_declared"] = spdx_exp

            self._config_yaml["sources"][i] = source

            if yaml_out_dir:
                shutil.copy2(yaml_out, yaml_out_dir)
            os.remove(yaml_out)

        with open(config_yaml, "w+") as out_cfg_yaml:
            ruamel_yaml.dump(self._config_yaml, out_cfg_yaml)

        if yaml_out_dir:
            print(f"yaml output for each source located under {yaml_out_dir}")

    def __replace_unencodeable(self, string):
        chars = []
        for s in string:
            try:
                chars.append(s.encode('utf-8').decode())
            except UnicodeEncodeError:
                chars.append("<bad char>")
        return "".join(chars)

    # For each file in the scan dir, check if the file path
    # contains some unencodable characters for 'utf-8'.
    # Scancode will fail to cache the resources for such files,
    # because the caching does a md5 hash of the file path, which
    # requires the whole string to be utf-8 encoded first
    def _check_for_unencodeable(self, scan_dir):
        bad_files = []
        for root, _, files in os.walk(scan_dir):
            for f in files:
                try:
                    p = os.path.join(root, f)
                    p.encode('utf-8')
                except UnicodeEncodeError:
                    bad_files.append(self.__replace_unencodeable(os.path.join(root, f)))

        if bad_files:
            pr_err("Scancode may fail with the following utf-8 unencodeable paths")
            pr_err("Note: bad chars replaced with <bad char> for printing.")
            pr_err("Please add these files to manual review section, if using config.yaml")
            for f in bad_files:
                pr_err(f"\t-{f}")

            err_exit()

    def __find_available_memory(self):
        with open("/proc/meminfo", "r") as meminfo_f:
            for line in meminfo_f:
                if "MemAvailable" in line:
                    return int(line.split()[1]) * 1024

        err_exit("Failed to read available memory from /proc/meminfo for thread count calculation, \
                    please specify --cpus to avoid this check")

    # Attempt to limit threads to a manageable level, and avoid OOM issues
    def _determine_thread_count(self, num_cpus=1, scan_dir=""):
        if not scan_dir:
            err_exit("Must pass scan dir to _determine_thread_count()")

        # Find the biggest files in the scan dir
        file_sizes = []
        for root, _, files in os.walk(scan_dir):
            for file in files:
                file_sizes.append(os.path.getsize(os.path.join(root, file)))

        file_sizes.sort(reverse=True)

        available_memory = self.__find_available_memory()

        # Use only 3/4 of the available memory
        available_memory *= 0.75
        # Assume overhead of roughly 1200 MB for one file + scancode
        total_mem_usage = 1258291200  # 1200 MB
        # Thread overhead seems to be about 1000MB per additional thread
        thread_overhead = 1048576000  # 1000 MB

        if available_memory < total_mem_usage + file_sizes[0]:
            err_exit(
                "Available memory is not sufficient, risking OOM error. " +
                "Free memory and try again later"
            )

        i = 0
        total = total_mem_usage
        while total < available_memory and i < len(file_sizes):
            # Assume entire file is loaded into memory, plus thread overhead
            total += file_sizes[i] + thread_overhead
            i += 1

        if i <= num_cpus:
            return i

        return num_cpus

    def _scan(self,
              scan_dir=None,
              build_spec=None,
              path=None,
              score=common.default_lic_score,
              yaml_out=None,
              cpus=0,
              alt_src_url=None,
              extra_repo_urls=None,
              timeout=None
            ):

        cached_spdx_ids = set()
        lic_db = None
        cache_util = None
        yaml_tmp_path = f"{tempfile.mkdtemp()}/scan-results.yaml"
        cwd = os.getcwd()

        if build_spec:
            cached_spdx_ids.update(self._parse_manual_review(scan_dir))

        # If config.yaml is present and the path points to an archive
        # find the archive in the config.yaml and parse any manual review
        if self._config_yaml and common.is_extractable(path):
            archive = {}
            bsname = os.path.basename(path)
            for i, source in enumerate(self._config_yaml['sources']):
                if source['archive'] == bsname:
                    archive = source
                    break

            if archive and 'license_manual_review' in archive:
                cached_spdx_ids.update(
                    self.__parse_manual_review(scan_dir, archive['license_manual_review'])
                )
            else:
                common.pr_err(f"Warning: Failed to find archive {bsname} in config.yaml!")

        if common.redis_host and common.redis_port:
            from CacheUtil import CacheUtil

            cache_util = CacheUtil(
                common.redis_host, common.redis_port, common.redis_ttl
            )
        elif common.redis_host or common.redis_port:
            err_exit(
                "For redis cache, need both the host and the port!"
            )

        if not common.no_trimming:
            from LicDB import LicDB

            lic_db = LicDB()
            print(
                "Trimming license DB to include only valid SPDX licenses "
                "before scan..."
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

        self._check_for_unencodeable(scan_dir)

        if not cpus:
            cpus = multiprocessing.cpu_count()
            cpus = self._determine_thread_count(cpus, scan_dir)
            print(f"Calculated max safe usage of {cpus} simultaneous threads")

        # run the scan
        scan_cmd = [
            "scancode",
            "-v",
            "--license",
            "-n", str(cpus),
            "--license-score", str(score),
            "--timeout", "7200",
            "--yaml",
            yaml_tmp_path,
            scan_dir,
        ]

        result = common.run_cmd(
            scan_cmd,
            ignore_rc=True,
            timeout=timeout
        )

        if result.returncode != 0:
            pr_err("ERROR: scancode failed during scanning process :(")
            pr_err(f"Failed cmd: '{scan_cmd}'")

            if not common.no_trimming:
                lic_db.restore_lic_db()

            if os.path.exists(yaml_tmp_path):
                self._export_yaml(
                    user_yaml_path=yaml_out,
                    cache_util=cache_util,
                    cwd=cwd,
                    sc_yaml_out_path=yaml_tmp_path,
                )

                shutil.rmtree(os.path.dirname(yaml_tmp_path))

            err_exit()

        if not common.no_trimming:
            print("Restoring license DB after scan completion")
            lic_db.restore_lic_db()

        exceptions_list = common.get_exceptions_list()

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

        self._export_yaml(
            user_yaml_path=yaml_out,
            cache_util=cache_util,
            cwd=cwd,
            sc_yaml_out_path=yaml_tmp_path,
        )

        shutil.rmtree(os.path.dirname(yaml_tmp_path))

        return spdx_exp

    # Main scanning function
    def scan(
        self,
        build_spec=None,
        path=None,
        score=common.default_lic_score,
        yaml_out=None,
        cpus=0,
        docker=False,
        alt_src_url=None,
        extra_repo_urls=None,
        timeout=None
    ):
        scan_dir = None
        self._extra_repo_urls = extra_repo_urls
        abs_path = os.path.abspath(path)

        if not path:
            err_exit("ERROR: No input given for scan!")

        if not os.path.exists(abs_path):
            err_exit(f"Path: '{abs_path}' does not exist! Exiting...")

        if not yaml_out:
            yaml_out = "/tmp/%s.yaml" % os.path.splitext(os.path.basename(path))[0]
            print(f"Warning: no output yaml path given, defaulting to: {yaml_out}")

        docker_util = DockerUtil() if docker else DockerUtil.detect()
        if docker_util is not None:
            mnt_list, cmd = docker_util.build_scan_docker_cmd(
                build_spec=build_spec,
                path=path,
                redis_host=common.redis_host,
                redis_port=common.redis_port,
                redis_ttl=common.redis_ttl,
                score=score,
                yaml_out=yaml_out,
                cpus=cpus,
                alt_src_url=alt_src_url,
                extra_repo_urls=extra_repo_urls,
                timeout=timeout
            )
            docker_util.run_docker_cmd(cmd=cmd, mount_list=mnt_list)
            if yaml_out:
                print(f"yaml output can be found at {yaml_out}")
            return

        self._check_prereqs()

        scan_dir = self._setup_scan_dir(path, build_spec, alt_src_url)
        if not scan_dir:
            common.emit_spdx()
            self._cleanup_scan()
            return

        spdx_exp = self._scan(
            scan_dir=scan_dir,
            build_spec=build_spec,
            score=score,
            alt_src_url=alt_src_url,
            timeout=timeout,
            cpus=cpus,
            yaml_out=yaml_out,
            extra_repo_urls=extra_repo_urls,
            path=path,
        )

        common.emit_spdx(spdx_exp)
        self._cleanup_scan(scan_dir)

        return spdx_exp
