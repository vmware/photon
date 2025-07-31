import common
from DockerUtil import DockerUtil
from common import (
    get_official_spdx_list,
    get_exceptions_list,
    err_exit,
    pr_err,
    read_license_from_file,
)


class Validator:
    def validate(self, file=None, stdin=None):
        license_expressions = {}

        docker_util = DockerUtil()
        if not common.running_in_container() and docker_util.docker_img_exists():
            mount_list, cmd = docker_util.build_validate_docker_cmd(
                file=file, stdin=stdin
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
            print(f"License found:\n{license_exp}\n")

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
                if key in common.disallowed_licenses["network_copyleft"]:
                    pr_err(
                        f"ERROR: {key} is not allowed according to Broadcom "
                        + "legal policy!"
                    )
                    errors += 1
                elif key in common.disallowed_licenses["other_non_permissive"]:
                    pr_err(
                        f"WARNING: {key} is currently only permitted by Broadcom legal "
                        + "by an exception to standard legal policy for Photon"
                    )
                    warnings += 1

                if key not in spdx_list and key not in exceptions_list:
                    pr_err(
                        f"Unofficial license/exception {key} found in license "
                        + "expression!"
                    )
                    errors += 1

        if errors == 0 and warnings == 0:
            print("SPDX license validation successful")
        elif errors == 0 and warnings > 0:
            print(f"SPDX license validation successful - with {warnings} warning(s)")
        else:
            err_exit(
                    f"Failed to validate SPDX license - "
                    + f"found {errors} error(s) and {warnings} warning(s)")
