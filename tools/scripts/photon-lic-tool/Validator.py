import common
from common import get_official_spdx_list, get_exceptions_list, err_exit, pr_err

try:
    import license_expression
except ImportError:
    print("license_expression import failed, do 'pip3 install license_expression'")
    raise


class Validator:
    def validate(self, license_expressions={}):
        license_exp = ""
        bad_ids = ["unknown-spdx", "LicenseRef", "scancode"]
        spdx_licensing = license_expression.get_spdx_licensing()
        spdx_list = []
        exceptions_list = []
        warnings = 0
        errors = 0

        spdx_list = get_official_spdx_list()
        exceptions_list = get_exceptions_list()

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
                if key in common.disallowed_licenses:
                    pr_err(
                        f"WARNING: {key} is not allowed according to Broadcom "
                        + "legal policy!"
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
            print(f"SPDX validation successful - with {warnings} warnings")
        else:
            err_exit(f"Failed to validate SPDX license - found {errors} error(s)")
