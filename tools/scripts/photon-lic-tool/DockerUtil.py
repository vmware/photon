#!/usr/bin/env python3

import os
import common
import docker
import sys
import json
from contextlib import suppress
from time import sleep
from common import err_exit, script_dir, SignalContext


class DockerUtil:
    _supported_cmds = ["scan", "validate", "clean-exp"]
    # Docker specific constants
    _docker_img_name = "photon-license-scanner"
    # Location of the photon-lic-tool directory within the docker container
    _docker_tool_dir = "/root/photon-lic-tool"
    # Lock file - don't want multiple docker builds at once
    _docker_lock_fn = "/tmp/.docker_lock_lic_tool"

    def __init__(self):
        # docker client
        self.client = docker.from_env(version="auto")

    @staticmethod
    def detect():
        try:
            client = DockerUtil()
        except:
            return None
        return client if client.docker_img_exists() else None

    def _write_list_to_dockerfile(self, dockerfile=None, write_list=None):
        if not dockerfile or not write_list:
            return

        for item in write_list:
            if item != write_list[-1]:
                dockerfile.write(f"{item} \\\n")
            else:
                dockerfile.write(f"{item}\n")

    def docker_img_exists(self):
        return self.client.images.list(self._docker_img_name)

    def ensure_docker_image(self):
        if imgs := self.docker_img_exists():
            print(f"Docker image has already been built: {imgs[0]}")
            return True
        buildargs = {}
        if "BASE_URL" in os.environ:
            buildargs.update({"URL": os.environ["BASE_URL"]})
        try:
            with open(self._docker_lock_fn, 'x'):
                pass
        except FileExistsError:
            print("Docker build already in progress, skipping ...")
            print(f"If you are sure, remove {self._docker_lock_fn} to skip this check.")
            return
        except Exception as e:
            err_exit(f"Failed to create lock file: {e}")
        def handler(sig, frame):
            raise Exception("Interrupted")
        id = None
        with SignalContext(handler):
            try:
                logstream = self.client.api.build(
                    tag=self._docker_img_name,
                    path=os.path.dirname(__file__),
                    rm=True,
                    buildargs=buildargs,
                    network_mode="host",
                    dockerfile="Dockerfile",
                )
                for entry in logstream:
                    resp = json.loads(entry.decode())
                    if 'stream' in resp:
                        sys.stdout.write(resp.pop('stream'))
                    if 'aux' in resp:
                        id = resp['aux'].pop('ID', None)
                        break
                    if 'errorDetail' in resp:
                        raise Exception(resp['errorDetail'].pop('message', 'unknown'))
            except Exception as e:
                os.unlink(self._docker_lock_fn)
                err_exit(f"Docker image build failed: {e}")
        os.unlink(self._docker_lock_fn)
        print(f"Successfully built docker image {self._docker_img_name}: {id}")
        return True

    def clean_docker_image(self):
        with suppress(Exception):
            self.client.images.remove(self._docker_img_name, force=True)

    # Build docker scan command
    def build_scan_docker_cmd(
        self,
        build_spec=None,
        path=None,
        redis_host=None,
        redis_port=None,
        redis_ttl=None,
        score=None,
        yaml_out=None,
        cpus=None,
        alt_src_url=None,
        extra_repo_urls=None,
        config_yaml=None,
    ):
        tool_cmd = []
        docker_scan_mnt = f"{common.ph_scan_tool_dir}/scan-mnt"
        docker_yaml_mnt = f"{common.ph_scan_tool_dir}/yaml-mnt"
        docker_cfg_yaml_mnt = f"{common.ph_scan_tool_dir}/cfg-mnt"
        mount_list = []
        local_scan_path = ""
        docker_scan_mnt_src = ""
        docker_scan_mnt_target = ""

        if not path:
            return (None, None)

        # scan dir needs to be the full photon repo
        if build_spec or config_yaml:
            local_scan_path = os.path.abspath(path)

            if "SPECS" not in path:
                err_exit("--build_spec/--config_yaml must be run within photon repo!")

            relative_path = os.path.basename(local_scan_path)
            while local_scan_path and os.path.basename(local_scan_path) != "SPECS":
                local_scan_path = os.path.dirname(local_scan_path)
                relative_path = f"{os.path.basename(local_scan_path)}/{relative_path}"

            if not local_scan_path:
                err_exit(
                    "Failed to find parent SPECS dir for --build_spec/--config_yaml!"
                )

            local_scan_path = os.path.dirname(local_scan_path)

            docker_scan_mnt_src = local_scan_path
            docker_scan_mnt_target = f"{docker_scan_mnt}"
        else:
            local_scan_path = path
            relative_path = os.path.basename(local_scan_path)

            docker_scan_mnt_src = os.path.abspath(local_scan_path)
            docker_scan_mnt_target = f"{docker_scan_mnt}/{relative_path}"

        mount_list = [
            (docker_scan_mnt_src, docker_scan_mnt_target, "ro"),
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

        if yaml_out:
            yaml_src = os.path.abspath(os.path.dirname(yaml_out))
            yaml_mount = (yaml_src, docker_yaml_mnt, "rw")
            mount_list.append(yaml_mount)

            tool_cmd.append(f"--yaml={docker_yaml_mnt}/{os.path.basename(yaml_out)}")

        if cpus:
            tool_cmd.append(f"--cpus={cpus}")

        if config_yaml:
            cfg_src = os.path.abspath(os.path.dirname(config_yaml))
            cfg_mnt = (cfg_src, docker_cfg_yaml_mnt, "rw")
            mount_list.append(cfg_mnt)

            tool_cmd.append(
                f"--config_yaml={docker_cfg_yaml_mnt}/{os.path.basename(config_yaml)}"
            )

        return (mount_list, tool_cmd)

    def build_validate_docker_cmd(self, file=None, stdin=None):
        if not file and not stdin:
            err_exit("Must pass in expression to validate cmd")

        docker_spec_mnt = f"{common.ph_scan_tool_dir}/spec-mnt"
        file_mnt_path = ""
        docker_mnt_cmd = ""
        tool_cmd = ["validate"]
        docker_mnt = []

        # read from file
        if file and file.endswith(".spec"):
            # scan dir needs to be the full photon repo
            local_scan_path = os.path.abspath(file)

            if "SPECS" not in local_scan_path:
                err_exit(
                    f"Spec file {local_scan_path} must be located inside the photon repo"
                )

            relative_path = os.path.basename(local_scan_path)
            while local_scan_path and os.path.basename(local_scan_path) != "SPECS":
                local_scan_path = os.path.dirname(local_scan_path)
                relative_path = f"{os.path.basename(local_scan_path)}/{relative_path}"

            if not local_scan_path:
                err_exit("Failed to find parent SPECS dir for validator!")

            local_scan_path = os.path.dirname(local_scan_path)
            docker_mnt.append((local_scan_path, docker_spec_mnt, "ro"))
            tool_cmd.extend(["-f", f"{docker_spec_mnt}/{relative_path}"])
        elif file:
            file_mnt_path = f"{docker_spec_mnt}/{os.path.basename(file)}"
            file = os.path.abspath(file)

            docker_mnt.append((file, file_mnt_path, "ro"))
            tool_cmd.extend(["-f", file_mnt_path])
        # read from stdin
        elif stdin:
            tool_cmd.extend(["-i", stdin])
        else:
            err_exit("License expression must be provided!")

        return (docker_mnt, tool_cmd)

    def build_clean_exp_docker_cmd(self, file=None, stdin=None):
        if not file and not stdin:
            err_exit("Must pass in expression to clean cmd")

        docker_spec_mnt = f"{common.ph_scan_tool_dir}/spec-mnt"
        file_mnt_path = ""
        docker_mnt_cmd = ""
        tool_cmd = ["clean-exp"]
        docker_mnt = []

        # read from file
        if file and file.endswith(".spec"):
            # scan dir needs to be the full photon repo
            local_scan_path = os.path.abspath(file)

            if "SPECS" not in local_scan_path:
                err_exit(
                    f"Spec file {local_scan_path} must be located inside the photon repo"
                )

            relative_path = os.path.basename(local_scan_path)
            while local_scan_path and os.path.basename(local_scan_path) != "SPECS":
                local_scan_path = os.path.dirname(local_scan_path)
                relative_path = f"{os.path.basename(local_scan_path)}/{relative_path}"

            if not local_scan_path:
                err_exit("Failed to find parent SPECS dir for validator!")

            local_scan_path = os.path.dirname(local_scan_path)
            docker_mnt.append((local_scan_path, docker_spec_mnt, "ro"))

            tool_cmd.extend(["-f", f"{docker_spec_mnt}/{relative_path}"])
        elif file:
            file_mnt_path = f"{docker_spec_mnt}/{os.path.basename(file)}"
            file = os.path.abspath(file)

            docker_mnt.append((file, file_mnt_path, "ro"))
            tool_cmd.extend(["-f", file_mnt_path])
        # read from stdin
        elif stdin:
            tool_cmd.extend(["-i", stdin])
        else:
            err_exit("License expression must be provided!")

        return (docker_mnt, tool_cmd)

    # Run the command in a docker container
    def run_docker_cmd(self, cmd=None, mount_list=[], **kwargs):
        while True:
            if self.ensure_docker_image():
                break
            # Don't try to build the image if already in the process of building.
            # Also, wait for build to finish before running.
            print("Cannot start container while image build is in progress, wait ...")
            print(f"If you are sure, remove {self._docker_lock_fn} to skip this check.")
            sleep(10)

        if cmd[0] not in self._supported_cmds:
            err_exit(f"Command '{cmd[0]}' not compatible with docker, refusing to run")
        full_cmd = ["python3", f"{self._docker_tool_dir}/{common.tool_filename}"] + cmd

        mounts = {
            hostpath: {"bind": containerpath, "mode": mode} for
            (hostpath, containerpath, mode) in mount_list + [(script_dir, self._docker_tool_dir, "ro")]
        }

        docker_inst = None
        def handler(sig, frame):
            # Try to kill the docker instance.
            with suppress(Exception):
                docker_inst.kill()
            raise Exception("Interrupted")
        with SignalContext(handler):
            try:
                docker_inst = self.client.containers.run(
                    self._docker_img_name,
                    entrypoint="/usr/bin/env",
                    detach=True,
                    auto_remove=True,
                    network_mode="host",
                    volumes=mounts,
                    command=full_cmd,
                    **kwargs,
                )
                logs = docker_inst.logs(stream=True, follow=True)
                for log in logs:
                    sys.stdout.buffer.write(log)
                    sys.stdout.flush()
                exit_code = docker_inst.wait()['StatusCode']
            except Exception as e:
                err_exit(f"Failed to run command in docker container: {e}")
        if exit_code != 0:
            err_exit(
                f'\nCommand {full_cmd} failed inside container with exit code {exit_code}\n'
            )
        print("\nDocker finished successfully\n")
