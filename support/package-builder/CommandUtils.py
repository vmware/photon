#!/usr/bin/env python3

import subprocess


class CommandUtils:
    @staticmethod
    def findFile(filename, sourcePath):
        (out, _, _) = CommandUtils.runBashCmd(
            f"find -L {sourcePath} -name {filename} -not -type d",
            capture=True,
            ignore_rc=True,
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

        return out.split() if out else None

    @staticmethod
    def runBashCmd(cmd, logfile=None, logfn=None, capture=False, ignore_rc=False):
        fp = None
        if logfile:
            fp = open(logfile, "w")
        elif capture or logfn:
            fp = subprocess.PIPE

        stdout = fp

        sp = subprocess.Popen(
            cmd,
            shell=True,
            executable="/bin/bash",
            stdout=stdout,
            stderr=stdout,
        )

        out, err = sp.communicate()
        rc = sp.wait()

        out = out.decode() if out else ""
        err = err.decode() if err else ""

        if logfn:
            logfn(out)

        if logfile:
            fp.close()

        if rc and not ignore_rc:
            print(f"Stdout: {out}\nStderr: {err}")
            raise Exception(f"Error while running:\n{cmd}")

        return out, err, rc

    @staticmethod
    def strtobool(val):
        val = val.lower()

        if val in ("y", "yes", "t", "true", "on", "1", "enable"):
            return 1

        if val in ("n", "no", "f", "false", "off", "0", "disable"):
            return 0

        raise ValueError("invalid truth value {!r}".format(val))
