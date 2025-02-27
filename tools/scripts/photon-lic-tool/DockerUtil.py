import os
import common
from common import run_cmd, err_exit
import shutil
from time import sleep


class DockerUtil:

    def __init__(self):
        # Docker specific constants
        self._docker_img_name = "photon-license-scanner"
        # Location of the photon-lic-tool directory within the docker container
        self._docker_tool_dir = "/root/photon-lic-tool"

        # check for docker command existence
        if not shutil.which("docker"):
            err_exit(
                "'docker' command not found, please install with "
                + "'tdnf install -y docker'"
            )

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
        docker_lock = ".docker_lock"

        # Don't try to build the image if already in the process of building
        if os.path.exists(".docker_lock"):
            print("Docker build already in progress somewhere else, skipping")
            return

        # indicate build is ongoing
        with open(docker_lock, "w") as docker_lock_f:
            docker_lock_f.write("1")

        cwd = os.getcwd()

        if not os.path.exists(dockerfile_local_path):
            err_exit(f"ERROR: No dockerfile found at {dockerfile_local_path}")

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

        result = run_cmd(build_cmd, ignore_rc=True)
        os.chdir(cwd)

        if result.returncode != 0:
            err_exit(f"Docker image build failed\n{result.stdout.decode()}")

        print(f"Successfully built docker image {self._docker_img_name}")

        if os.path.exists(docker_lock):
            os.remove(docker_lock)

    def clean_docker_image(self):
        docker_clean_cmd = ["docker", "image", "rm", self._docker_img_name]

        # Handles errors internally
        run_cmd(docker_clean_cmd)

    # Build docker scan command
    def _build_scan_docker_cmd(
        self,
        build_spec=None,
        path=None,
        redis_host=None,
        redis_port=None,
        redis_ttl=None,
        score=None,
        yaml=None,
        cpus=None,
    ):
        full_cmd = ""
        tool_cmd = ""
        docker_scan_mnt = f"{common.ph_scan_tool_dir}/scan-mnt"
        docker_yaml_mnt = f"{common.ph_scan_tool_dir}/yaml-mnt"
        mount_list = []
        local_scan_path = ""
        docker_scan_mnt_src = ""
        docker_scan_mnt_target = ""

        if not path:
            return (None, None)

        relative_path = os.path.basename(path)

        # scan dir needs to be the full photon repo
        if build_spec:
            local_scan_path = os.path.abspath(path)

            if "SPECS" not in path:
                err_exit("--build_spec must be run within photon repo!")

            relative_path = os.path.basename(local_scan_path)
            while local_scan_path and os.path.basename(local_scan_path) != "SPECS":
                local_scan_path = os.path.dirname(local_scan_path)
                relative_path = f"{os.path.basename(local_scan_path)}/{relative_path}"

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

        # mount the scan dir
        scan_mnt = "--mount "
        scan_mnt += ",".join(
            [
                "type=bind",
                f"src={docker_scan_mnt_src}",
                f"target={docker_scan_mnt_target}",
                "readonly",
            ]
        )

        mount_list.append(scan_mnt)

        tool_cmd = f"python3 -u {self._docker_tool_dir}/{common.tool_filename}"
        tool_cmd += f" scan --path={docker_scan_mnt}/{relative_path}"

        if redis_host:
            tool_cmd += f" --redis_host={redis_host}"
            tool_cmd += f" --redis_port={redis_port}"
            tool_cmd += f" --redis_ttl={redis_ttl}"

        if score:
            tool_cmd += f" --score={score}"

        if build_spec:
            tool_cmd += " --build_spec"

        if yaml:
            # Mount yaml directory so we can write directly out to the location
            yaml_mnt = "--mount "
            yaml_mnt += ",".join(
                [
                    "type=bind",
                    f"src={os.path.abspath(os.path.dirname(yaml))}",
                    f"target={docker_yaml_mnt}",
                ]
            )

            mount_list.append(yaml_mnt)

            tool_cmd += f" --yaml={docker_yaml_mnt}/{os.path.basename(yaml)}"

        if cpus:
            tool_cmd += f" --cpus={cpus}"

        # docker image is pre-trimmed, no trimming needed here
        tool_cmd += " --no_trim"

        full_cmd = "docker run --detach --network=host"
        for mnt_cmd in mount_list:
            full_cmd += f" {mnt_cmd}"

        full_cmd += f" {self._docker_img_name} {tool_cmd}"

        return full_cmd

    # Run the command in a docker container
    def run_docker_cmd(
        self,
        cmd=None,
        build_spec=None,
        path=None,
        redis_host=None,
        redis_port=None,
        redis_ttl=None,
        score=None,
        yaml=None,
        cpus=None,
    ):
        new_cmd = ""

        if not cmd:
            return

        # Don't try to build the image if already in the process of building.
        # Also, wait for build to finish before running.
        while os.path.exists(".docker_lock"):
            print("Docker build already in progress somewhere else, waiting...")
            sleep(10)

        # Check if need to create docker image
        result = run_cmd(f"docker images -q {self._docker_img_name}")
        if not result.stdout:
            self.create_docker_image()

        if cmd == "scan":
            new_cmd = self._build_scan_docker_cmd(
                build_spec=build_spec,
                path=path,
                redis_host=redis_host,
                redis_port=redis_port,
                redis_ttl=redis_ttl,
                score=score,
                yaml=yaml,
                cpus=cpus,
            )
        else:
            err_exit(f'Command "{cmd}" not compatible with docker, not running.')

        print("\nRunning command inside docker container...\n")

        result = run_cmd(new_cmd, ignore_rc=False)
        container_id = result.stdout.decode().strip()

        # Watch the logs...
        run_cmd(f"docker container logs --follow {container_id}", capture=False)

        # Check for exit code
        result = run_cmd(f"docker wait {container_id}", ignore_rc=True)
        if result.returncode != 0:
            err_exit(f"Failed to check return code from {container_id}...")

        exit_code = result.stdout.decode().strip()
        if exit_code != "0":
            run_cmd(f"docker container rm {container_id}")

            err_exit(
                f'\nCommand "{new_cmd}" failed inside container {container_id} '
                + f"with exit code {exit_code}\n"
            )
        else:
            print("\nDocker finished successfully\n")

        if yaml:
            print(
                f"yaml output can be found at {yaml} and/or "
                + f"{os.path.dirname(yaml)}/{common.cached_yaml_fn}"
            )

        # Clean the container on exit
        run_cmd(f"docker container rm {container_id}")