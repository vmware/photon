#!/usr/bin/env python3

import os
import sys
import subprocess


logger = None


def initLogger():
    global logger

    if logger:
        return

    from Logger import Logger
    from constants import constants

    logPath = constants.logPath
    if not logPath:
        return

    logLevel = constants.logLevel

    logger = Logger.getLogger(
        "CommandUtils", logpath=logPath, loglevel=logLevel
    )


class CommandUtils:
    @staticmethod
    def findFile(filename, sourcePath):
        ret = subprocess.run(
            [
                "find",
                "-L",
                sourcePath,
                "-name",
                filename,
                "-not",
                "-type",
                "d",
                "-print0",
            ],
            capture_output=True,
            check=False,
        )
        """
        We don't check the return val here because find could return 1 but
        still be able to find the result. We shouldn't blindly return None
        without even checking the result.
        The reason we want to suppress this is because for built RPMs,
        we first copy it to the location with a random name and move it to
        the real name. find will complain our action and return 1.
        find's flag ignore_readdir_race can suppress this but it isn't
        working.
        https://bugs.centos.org/view.php?id=13685
        """

        return [f.decode() for f in ret.stdout.split(b"\x00") if f]

    @staticmethod
    def runCmd(
        args,
        logfile=None,
        logfn=None,
        cwd=None,
        capture=False,
        ignore_rc=False,
        env=None,
        clean_env=False,
        shell=False,
    ):
        global logger
        if logger:
            logger.debug(f"Running {args}")
        else:
            initLogger()
            print(f"Running {args}", file=sys.stderr)

        fp = None
        if logfn is not None:
            capture = True

        if capture:
            fp = subprocess.PIPE

        if logfile is not None:
            if capture:
                raise Exception(
                    "Cannot specify both logfn/capture and logfile"
                )
            fp = logfile

        new_env = None
        if env is not None:
            new_env = env if clean_env else {**os.environ, **env}

        sp = subprocess.Popen(
            args, cwd=cwd, env=new_env, shell=shell, stdout=fp, stderr=fp
        )

        out, err = sp.communicate()
        rc = sp.wait()

        out = out.decode() if out else ""
        err = err.decode() if err else ""

        if logfn:
            logfn(out)

        if rc and not ignore_rc:
            print(f"Stdout: {out}\nStderr: {err}")
            raise Exception(f"Error while running: {args}")

        return out, err, rc

    @staticmethod
    def strtobool(val):
        val = val.lower()

        if val in ("y", "yes", "t", "true", "on", "1", "enable"):
            return 1

        if val in ("n", "no", "f", "false", "off", "0", "disable"):
            return 0

        raise ValueError("invalid truth value {!r}".format(val))

    @staticmethod
    def splitlines(output):
        return [line for line in output.split("\n") if line]
