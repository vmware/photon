#!/usr/bin/env python3

"""
RPM signing utilities: build signing command from config and sign artifacts.
"""

from CommandUtils import CommandUtils

# Key map from option names (e.g. from build config) to internal keys
signingMap = {
    "srp-signing-script": "script",
    "srp-signing-params": "params",
    "srp-signing-auth": "auth",
}

# Mutable state populated from constants / storeScriptsToCopy
signingOptsSandbox = {}
signingOptsHost = {}
rpmSigningCmd = []


def getSigningCmd():
    """Build and return the RPM signing command, or None if signing is disabled.
    Caches the result in rpmSigningCmd.
    """
    if not rpmSigningCmd:
        if len(signingOptsHost) != len(signingMap):
            rpmSigningCmd.append(False)
            return None

        cmd = [
            signingOptsHost["script"],
            "--file_type",
            "rpm",
            "--config_file",
            signingOptsHost["params"],
            "--auth_file",
            signingOptsHost["auth"],
            "--artifact",
        ]
        rpmSigningCmd.clear()
        rpmSigningCmd.extend(cmd)
        return cmd
    elif not rpmSigningCmd[0]:
        return None

    return rpmSigningCmd


def signFile(path):
    """Run the signing command on a single artifact path. No-op if signing disabled."""
    cmd = getSigningCmd()
    if cmd:
        CommandUtils.runCmd(cmd + [path])


def setScriptToCopy(key, val):
    """Record a script path to copy for signing (host and sandbox paths)."""
    signingOpt = signingMap[key]
    src = val.get("src")
    if src:
        signingOptsHost[signingOpt] = src
        signingOptsSandbox[signingOpt] = val.get("dest", "")


def addSigningMacros():
    """Add signing_* macros to the global constants userDefinedMacros if configured."""
    from constants import constants

    if len(signingOptsSandbox) == len(signingMap):
        for k, v in signingOptsSandbox.items():
            constants.addMacro(f"signing_{k}", v)
