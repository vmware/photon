#!/usr/bin/env python3

import os
import common
import shutil
import signal

from time import sleep
from common import run_cmd, err_exit, script_dir


class DockerUtil:
    _supported_cmds = ["scan", "validate", "clean-exp"]

    def __init__(self):
        # Docker specific constants
        self._docker_img_name = "photon-license-scanner"
        # Location of the photon-lic-tool directory within the docker container
        self._docker_tool_dir = "/root/photon-lic-tool"

        # Lock file - don't want multiple docker builds at once
        self._docker_lock_fn = "/tmp/.docker_lock_lic_tool"

        # check for docker command existence - only if not inside a container already
        if not common.running_in_container() and not shutil.which("docker"):
            err_exit(
                "'docker' command not found, please install with "
                "'tdnf install -y docker'"
            )

    def docker_img_exists(self):
        # For all intents and purposes, if the docker daemon isn't running,
        # we can't use the image anyways, even if it exists.
        result = run_cmd("systemctl is-active --quiet docker", ignore_rc=True)
        if result.returncode != 0:
            return False

        result = run_cmd(
            f"docker images -q {self._docker_img_name}", ignore_rc=True
        )
        if result.stdout:
            return True

        return False

    def _build_mount(self, src, target, readonly=True):
        parts = f"type=bind,src={src},target={target}"
        if readonly:
            parts = f"{parts},readonly"
        return f"--mount {parts}"

    def _write_list_to_dockerfile(self, dockerfile=None, write_list=None):
        if not dockerfile or not write_list:
            return

        for item in write_list:
            if item != write_list[-1]:
                dockerfile.write(f"{item} \\\n")
            else:
                dockerfile.write(f"{item}\n")

    def create_docker_image(self):
        build_cmd = ""
        dockerfile_local_path = "Dockerfile"

        # Don't try to build the image if already in the process of building
        if os.path.exists(self._docker_lock_fn):
            print("Docker build already in progress, skipping ...")
            print(
                f"If you are sure, remove {self._docker_lock_fn} to skip this check."
            )
            return

        cwd = os.getcwd()

        if not os.path.exists(dockerfile_local_path):
            err_exit(f"ERROR: No dockerfile found at {dockerfile_local_path}")

        # indicate build is ongoing
        with open(self._docker_lock_fn, "w") as docker_lock_f:
            docker_lock_f.write("1")

        def cleanup_lock(*_):
            if not os.path.exists(self._docker_lock_fn):
                return

            try:
                os.remove(self._docker_lock_fn)
                print(f"Removed lock file: {self._docker_lock_fn}")
            except OSError as e:
                print(
                    f"WARNING: Could not remove lock file {self._docker_lock_fn}: {e}"
                )

        signal.signal(signal.SIGINT, cleanup_lock)
        signal.signal(signal.SIGTERM, cleanup_lock)

        # build the docker image
        print("Building docker image...")

        os.chdir(common.tool_dir_path)
        build_cmd = [
            "docker",
            "build",
            "-t",
            self._docker_img_name,
            "--network=host",
            ".",
        ]

        url = os.environ.get("BASE_URL")
        if url:
            build_cmd += ["--build-arg", f"URL={url}"]

        result = run_cmd(build_cmd, ignore_rc=True)
        os.chdir(cwd)

        if os.path.exists(self._docker_lock_fn):
            os.remove(self._docker_lock_fn)

        if result.returncode != 0:
            msg = "Docker image build failed:\n"
            if result.stdout:
                msg += f"Stdout:\n{result.stdout.decode()}\n"
            if result.stderr:
                msg += f"Stderr:\n{result.stderr.decode()}\n"

            err_exit(msg)

        print(f"Successfully built docker image {self._docker_img_name}")

    def clean_docker_image(self):
        docker_clean_cmd = ["docker", "image", "rm", self._docker_img_name]

        # Handles errors internally
        run_cmd(docker_clean_cmd)

    # Build docker scan command
    def build_scan_docker_cmd(
        self,
        build_spec=None,
        path=None,
        redis_host=None,
        redis_port=None,
        redis_ttl=None,
        score=None,
        yaml=None,
        cpus=None,
        alt_src_url=None,
        extra_repo_urls=None,
    ):
        tool_cmd = []
        docker_scan_mnt = f"{common.ph_scan_tool_dir}/scan-mnt"
        docker_yaml_mnt = f"{common.ph_scan_tool_dir}/yaml-mnt"
        local_scan_path = ""
        docker_scan_mnt_src = ""
        docker_scan_mnt_target = ""

        if not path:
            return (None, None)

        # scan dir needs to be the full photon repo
        if build_spec:
            local_scan_path = os.path.abspath(path)

            if "SPECS" not in path:
                err_exit("--build_spec must be run within photon repo!")

            relative_path = os.path.basename(local_scan_path)
            while (
                local_scan_path
                and os.path.basename(local_scan_path) != "SPECS"
            ):
                local_scan_path = os.path.dirname(local_scan_path)
                relative_path = (
                    f"{os.path.basename(local_scan_path)}/{relative_path}"
                )

            if not local_scan_path:
                err_exit("Failed to find parent SPECS dir for --build_spec!")

            local_scan_path = os.path.dirname(local_scan_path)

            docker_scan_mnt_src = local_scan_path
            docker_scan_mnt_target = f"{docker_scan_mnt}"
        else:
            local_scan_path = path
            relative_path = os.path.basename(local_scan_path)

            docker_scan_mnt_src = os.path.abspath(local_scan_path)
            docker_scan_mnt_target = f"{docker_scan_mnt}/{relative_path}"

        mount_list = [
            self._build_mount(docker_scan_mnt_src, docker_scan_mnt_target),
        ]

        tool_cmd = [
            "scan",
            f"--path={docker_scan_mnt}/{relative_path}",
            "--no_trim",
        ]

        if redis_host:
            tool_cmd += [
                f"--redis_host={redis_host}",
                f"--redis_port={redis_port}",
                f"--redis_ttl={redis_ttl}",
            ]

        if score:
            tool_cmd.append(f"--score={score}")

        if build_spec:
            tool_cmd.append("--build_spec")

        if alt_src_url:
            tool_cmd.append(f"--alt_src_url={alt_src_url}")

        if extra_repo_urls:
            tool_cmd.append(f"--extra_repo_urls={extra_repo_urls}")

        if yaml:
            yaml_src = os.path.abspath(os.path.dirname(yaml))
            yaml_mount = self._build_mount(
                yaml_src, docker_yaml_mnt, readonly=False
            )
            mount_list.append(yaml_mount)

            tool_cmd.append(
                f"--yaml={docker_yaml_mnt}/{os.path.basename(yaml)}"
            )

        if cpus:
            tool_cmd.append(f"--cpus={cpus}")

        return (mount_list, tool_cmd)

    def build_validate_docker_cmd(self, file=None, stdin=None):
        if not file and not stdin:
            err_exit("Must pass in expression to validate cmd")

        docker_spec_mnt = f"{common.ph_scan_tool_dir}/spec-mnt"
        file_mnt_path = ""
        docker_mnt_cmd = ""
        tool_cmd = ["validate"]

        # read from file
        if file and file.endswith(".spec"):
            # scan dir needs to be the full photon repo
            local_scan_path = os.path.abspath(file)

            if "SPECS" not in local_scan_path:
                err_exit(
                    f"Spec file {local_scan_path} must be located inside the photon repo"
                )

            relative_path = os.path.basename(local_scan_path)
            while (
                local_scan_path
                and os.path.basename(local_scan_path) != "SPECS"
            ):
                local_scan_path = os.path.dirname(local_scan_path)
                relative_path = (
                    f"{os.path.basename(local_scan_path)}/{relative_path}"
                )

            if not local_scan_path:
                err_exit("Failed to find parent SPECS dir for validator!")

            local_scan_path = os.path.dirname(local_scan_path)
            docker_mnt_cmd = self._build_mount(local_scan_path, docker_spec_mnt)
            tool_cmd.extend(["-f", f"{docker_spec_mnt}/{relative_path}"])
        elif file:
            file_mnt_path = f"{docker_spec_mnt}/{os.path.basename(file)}"
            file = os.path.abspath(file)

            docker_mnt_cmd = self._build_mount(file, file_mnt_path)
            tool_cmd.extend(["-f", file_mnt_path])
        # read from stdin
        elif stdin:
            tool_cmd.extend(["-i", stdin])
        else:
            err_exit("License expression must be provided!")

        return ([docker_mnt_cmd], tool_cmd)

    def build_clean_exp_docker_cmd(self, file=None, stdin=None):
        if not file and not stdin:
            err_exit("Must pass in expression to clean cmd")

        docker_spec_mnt = f"{common.ph_scan_tool_dir}/spec-mnt"
        file_mnt_path = ""
        docker_mnt_cmd = ""
        tool_cmd = ["clean-exp"]

        # read from file
        if file and file.endswith(".spec"):
            # scan dir needs to be the full photon repo
            local_scan_path = os.path.abspath(file)

            if "SPECS" not in local_scan_path:
                err_exit(
                    f"Spec file {local_scan_path} must be located inside the photon repo"
                )

            relative_path = os.path.basename(local_scan_path)
            while (
                local_scan_path
                and os.path.basename(local_scan_path) != "SPECS"
            ):
                local_scan_path = os.path.dirname(local_scan_path)
                relative_path = (
                    f"{os.path.basename(local_scan_path)}/{relative_path}"
                )

            if not local_scan_path:
                err_exit("Failed to find parent SPECS dir for validator!")

            local_scan_path = os.path.dirname(local_scan_path)
            docker_mnt_cmd = self._build_mount(local_scan_path, docker_spec_mnt)

            tool_cmd.extend(["-f", f"{docker_spec_mnt}/{relative_path}"])
        elif file:
            file_mnt_path = f"{docker_spec_mnt}/{os.path.basename(file)}"
            file = os.path.abspath(file)

            docker_mnt_cmd = self._build_mount(file, file_mnt_path)
            tool_cmd.extend(["-f", file_mnt_path])
        # read from stdin
        elif stdin:
            tool_cmd.extend(["-i", stdin])
        else:
            err_exit("License expression must be provided!")

        return ([docker_mnt_cmd], tool_cmd)

    # Run the command in a docker container
    def run_docker_cmd(self, cmd=None, mount_list=[]):
        docker_prefix = "docker run --detach --network=host"
        tool_prefix = (
            f"python3 -u {self._docker_tool_dir}/{common.tool_filename}"
        )

        if cmd[0] not in self._supported_cmds:
            err_exit(
                f"Command '{cmd[0]}' not compatible with docker, refusing to run"
            )

        mount_list += [
            self._build_mount(script_dir, self._docker_tool_dir)
        ]

        full_cmd = (
            f"{docker_prefix} "
            f"{' '.join(mount_list)} "
            f"{self._docker_img_name} "
            f"{tool_prefix}"
        ).split()

        full_cmd.extend(cmd)

        # Don't try to build the image if already in the process of building.
        # Also, wait for build to finish before running.
        while os.path.exists(self._docker_lock_fn):
            print(
                "Cannot start container while image build is in progress, wait ..."
            )
            print(
                f"If you are sure, remove {self._docker_lock_fn} to skip this check."
            )
            sleep(10)

        # Check if need to create docker image
        if not self.docker_img_exists():
            self.create_docker_image()

        print("\nRunning command inside docker container...\n")

        result = run_cmd(full_cmd)
        container_id = result.stdout.decode().strip()

        # Watch the logs...
        run_cmd(
            f"docker container logs --follow {container_id}", capture=False
        )

        # Check for exit code
        result = run_cmd(f"docker wait {container_id}", ignore_rc=True)
        if result.returncode != 0:
            run_cmd(f"docker container rm {container_id}")
            err_exit(f"Failed to check return code from {container_id}...")

        exit_code = result.stdout.decode().strip()
        run_cmd(f"docker container rm {container_id}")
        if int(exit_code) != 0:
            err_exit(
                f'\nCommand "{full_cmd}" failed inside container {container_id} '
                f"with exit code {exit_code}\n"
            )
        else:
            print("\nDocker finished successfully\n")
