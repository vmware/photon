#!/usr/bin/env python3

"""
Simple tool for validating SPDX license expression using the Python SPDX
tools package.

To install: pip3 install spdx-tools
Arguments:
  -i: Direct input. Following should be the full license expression.
       Should be quoted, i.e: "<lic exp>".
  -f: File input. Reads license expression from file. Should work with
      SPECS/<pkg>/license.txt, or even .spec files themselves. Reads the
      license expression from the line that matches "License: <lic exp>".
"""

import os
import sys

from spdx_tools.spdx.validation.license_expression_validator import (
    validate_license_expression,
)

from spdx_tools.common.spdx_licensing import spdx_licensing

from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    CreationInfo,
    Document,
)

from datetime import datetime

license_exp = None

script_fn = sys.argv[0]


def pr_err(msg):
    print(f"\n{msg}\n", file=sys.stderr)


def usage():
    msg = f"""
Usage:

  {script_fn} [ -i <license-str> || -f <license-file> ]


  -i: Direct input. Following should be the full license expression.
      Should be quoted, i.e: "<lic exp>".

  -f: File input. Reads license expression from file. Should work with
      SPECS/<pkg>/license.txt, or even .spec files themselves. Reads the
      license expression from the line that matches "License: <lic exp>".
"""
    pr_err(msg)
    exit(1)


if len(sys.argv) != 3:
    usage()

opt = sys.argv[1]

if opt not in ["-i", "-f"]:
    usage()

license_exp = sys.argv[2]

if opt == "-f":
    if not os.path.exists(license_exp):
        pr_err(f"ERROR: Invalid file path: {license_exp}")
        exit(1)

    lic_f = open(license_exp, "r")
    for line in lic_f:
        if line.startswith("License:"):
            license_exp = line.split(":")[1].strip()
    lic_f.close()

if not license_exp:
    pr_err("ERROR: No valid license expression received!")
    exit(1)

"""
Because SPDX is really a full document format, the license expression
validation can't be done on its' own, at least with the available official
SPDX tools. So, create a dummy document object, and use that.
"""
creation_info = CreationInfo(
    spdx_version="SPDX-3.0",
    spdx_id="SPDXRef-DOCUMENT",
    name="document name",
    data_license="Dummy License",
    document_namespace="https://some.namespace",
    creators=[Actor(ActorType.PERSON, "Jane Doe", "jane.doe@example.com")],
    created=datetime(2024, 1, 1),
)
document = Document(creation_info)

try:
    # create license expression object
    license_exp = spdx_licensing.parse(license_exp)

    # returns List[ValidateMessage]
    validation_messages = validate_license_expression(
        license_exp, document, parent_id="SPDXRef-File"
    )

    if validation_messages:
        pr_err("ERROR: Failed to validate SPDX expression! Please see error(s) below:")
        for msg in validation_messages:
            pr_err(msg.validation_message)
        exit(1)
    print("SPDX license validation successful")
except Exception as e:
    pr_err(f"ERROR: Caught exception while attempting to validate the given expression: {e}")
