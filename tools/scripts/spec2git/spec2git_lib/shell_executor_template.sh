#!/bin/bash
# Shell execution template for spec2git prep section execution
# This script handles state restoration between command blocks
set -e

# Set RPM environment variables that rpmspec injects
__RPM_ENV_VARS_PLACEHOLDER__

# User commands will be inserted here
# Directory stack restoration is handled by prepending commands to this block
__COMMANDS_PLACEHOLDER__
