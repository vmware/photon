import license_tree
import os
import requests
import json
import time
import sys

ignore_list = ["LicenseRef-unknown-spdx", "LicenseRef-scancode-unknown-spdx"]


# Stole this from ../license_validation.py. Easier than configuring the import
# from another directory
def get_exceptions_list():
    exception_list = []
    exceptions_json_loc = "/tmp/exceptions.json"
    exceptions_json = None
    retries = 3

    if os.path.exists(exceptions_json_loc):
        os.remove(exceptions_json_loc)

    while retries > 0:
        # download latest version of exceptions.json from github
        response = requests.get(
            "https://raw.githubusercontent.com/spdx/license-list-data/"
            + "refs/heads/main/json/exceptions.json"
        )

        if response.status_code == 200:
            with open(exceptions_json_loc, "wb") as exc_file:
                exc_file.write(response.content)
            break
        else:
            retries -= 1
            if retries > 0:
                print("Failed to get exceptions list, retrying after delay...")
                time.sleep(5)
            else:
                print("ERROR: Exhausted all retries, couldn't get exceptions list!")
                sys.exit(1)

    with open(exceptions_json_loc, "r") as spdx_exceptions_json:
        exceptions_json = json.load(spdx_exceptions_json)

    for exception in exceptions_json["exceptions"]:
        exception_list.append(exception["licenseExceptionId"])

    os.remove(exceptions_json_loc)

    return exception_list


exception_list = get_exceptions_list()

# add our custom test exception
exception_list.append("TEST_EXC")

# run test
license_tree.__test_exp_tree__(
    input_yaml="exp_tree_tests.yaml",
    exception_list=exception_list,
    ignore_list=ignore_list,
)
