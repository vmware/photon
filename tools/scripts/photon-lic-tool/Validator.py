#!/usr/bin/env python3

import common
import json
import os

from DockerUtil import DockerUtil
from common import (
    get_official_spdx_list,
    get_exceptions_list,
    err_exit,
    pr_err,
    read_license_from_file,
    config_path,
)


class Validator:
    def validate(self, file=None, stdin=None, srp_policy_controls=None):
        license_expressions = {}

        docker_util = DockerUtil.detect()
        if docker_util:
            mount_list, cmd = docker_util.build_validate_docker_cmd(
                file=file, stdin=stdin, srp_policy_controls=srp_policy_controls
            )
            docker_util.run_docker_cmd(cmd=cmd, mount_list=mount_list)
            return

        try:
            import license_expression
        except ImportError:
            print(
                "license_expression import failed, do 'pip3 install license_expression'"
            )
            raise

        license_exp = ""
        bad_ids = ["unknown-spdx", "LicenseRef", "scancode"]
        spdx_licensing = license_expression.get_spdx_licensing()
        spdx_list = []
        exceptions_list = []
        errors = 0
        warnings = 0

        # TODO: Cache these inside the docker image? Downside is may be outdated.
        spdx_list = get_official_spdx_list()
        exceptions_list = get_exceptions_list()
        if srp_policy_controls:
            network_copyleft, other_non_permissive = self.get_disallowed_licenses(srp_policy_controls)
            srp_known_licenses = self.get_srp_known_licenses(srp_policy_controls)
        else:
            network_copyleft = common.disallowed_licenses["network_copyleft"]
            other_non_permissive = common.disallowed_licenses["other_non_permissive"]
            srp_known_licenses = common.srp_known_licenses

        # read from file
        if file:
            license_expressions = read_license_from_file(file)
        # read from stdin
        elif stdin:
            license_expressions["stdin"] = stdin
        else:
            err_exit("License expression must be provided!")

        for license_exp in license_expressions:
            print(f"Validating license for {license_exp}")
            license_exp = license_expressions[license_exp]
            print(f"License found:\n{common.emit_spdx(license_exp)}\n")

            # for some reason, the license_expression package, which is used by the
            # official spdx-tools package, returns/uses the same database for both
            # spdx and scancode licenses. So let's do our own filtering here.
            for bad_id in bad_ids:
                if bad_id in license_exp:
                    pr_err(f"Bad/unofficial identifier {bad_id} in license expression!")
                    errors += 1
            try:
                # create license expression object - throws an exception for any
                # validation errors
                spdx_licensing.parse(license_exp, validate=True, strict=True)
            except Exception as e:
                err_exit(f"Caught exception while attempting to validate license: {e}")

            # Check for disallowed licenses
            for key in spdx_licensing.license_keys(license_exp):
                if key in network_copyleft:
                    pr_err(
                        f"ERROR: {key} is not allowed according to Broadcom "
                        + "legal policy!"
                    )
                    errors += 1
                elif key in other_non_permissive:
                    pr_err(
                        f"WARNING: {key} is currently only permitted by Broadcom legal "
                        + "by an exception to standard legal policy for Photon"
                    )
                    warnings += 1

                if key not in spdx_list and key not in exceptions_list:
                    pr_err(
                        f"Unofficial license/exception {key} found in license "
                        + "expression! This license is not in the SPDX database."
                    )
                    errors += 1

                # This will check approved exception combinations as well, e.g 'A WITH B'
                if key not in srp_known_licenses:
                    pr_err(
                        f"ERROR: {key} has not been reviewed by Broadcom SRP team."
                    )
                    errors += 1

        if errors == 0 and warnings == 0:
            print("SPDX license validation successful")
        elif errors == 0 and warnings > 0:
            print(f"SPDX license validation successful - with {warnings} warning(s)")
        else:
            err_exit(
                f"Failed to validate SPDX license - "
                f"found {errors} error(s) and {warnings} warning(s)\n"
                f"If srp_known_licenses in {os.path.basename(config_path)} is out of sync, "
                "please update it."
            )

    # Get list of known licenses from SRP policy controls repo, if present.
    # The license-exception combination must be explicitly reviewed
    # (exception cannot be used for other licenses)
    def get_srp_known_licenses(self, srp_policy_controls=None):

        if not os.path.exists(srp_policy_controls):
            err_exit(f"SRP policy controls not found: {srp_policy_controls}")

        srp_known_licenses_file = os.path.join(
                srp_policy_controls,
                "data/legal/osc/vcf_9.1/licenses/data.json"
            )

        srp_known_licenses = set()

        if not os.path.exists(srp_known_licenses_file):
            err_exit(f"SRP Policy Controls repo is missing {srp_known_licenses_file}")

        with open(srp_known_licenses_file, "r") as f:
            json_data = json.load(f)

            for lic_key, lic_data in json_data.items():
                srp_known_licenses.add(json_data[lic_key]['spdx_id'])

        return srp_known_licenses

    def get_disallowed_licenses(self, srp_policy_controls=None):
        if not os.path.exists(srp_policy_controls):
            err_exit(f"SRP policy controls not found: {srp_policy_controls}")

        srp_disallowed_licenses_file = os.path.join(
            srp_policy_controls,
            "data/legal/osc/vcf_9.1/license_family_to_license_map/data.json"
        )

        if not os.path.exists(srp_disallowed_licenses_file):
            err_exit(f"SRP Policy Controls repo is missing {srp_disallowed_licenses_file}")

        network_copyleft = set()
        other_non_permissive = set()

        with open(srp_disallowed_licenses_file, "r") as f:
            json_data = json.load(f)

            for lic in json_data["network_copyleft"]:
                network_copyleft.add(lic)

            for lic in json_data["other_non_permissive"]:
                other_non_permissive.add(lic)

        return network_copyleft, other_non_permissive
