#!/usr/bin/env python3

import getopt
import glob
import json
import os
import platform
import shutil
import subprocess
import sys

THIS_ARCH = platform.machine()

RELEASE_VER = "5.0"

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTON_DIR = os.path.abspath(os.path.join(THIS_DIR, "../.."))
EULA_PATH = os.path.join(PHOTON_DIR, "EULA.txt")
STAGE_DIR = os.path.join(PHOTON_DIR, "stage")
REPO_DIR = os.path.join(STAGE_DIR, "RPMS")

ARCH_MAP = {"x86_64": "amd64", "aarch64": "arm64"}

if THIS_ARCH == "x86_64":
    POI_IMAGE = "projects.registry.vmware.com/photon/installer:ob-23999758"
elif THIS_ARCH == "aarch64":
    POI_IMAGE = "projects.registry.vmware.com/photon/installer-arm64:ob-22815437"
else:
    raise Exception(f"unknown arch {THIS_ARCH}")


class Poi(object):

    def __init__(
        self,
        arch=THIS_ARCH,
        release_ver=RELEASE_VER,
        repo_dir=None,
        poi_image=POI_IMAGE,
        photon_dir=PHOTON_DIR,
        stage_dir=STAGE_DIR,
        eula_path=EULA_PATH,
        sha=None,
    ):

        self.arch = arch
        self.release_ver = release_ver
        self.repo_dir = repo_dir
        self.poi_image = poi_image
        self.photon_dir = photon_dir
        self.stage_dir = stage_dir
        self.eula_path = EULA_PATH
        self.sha = sha

        if self.sha is None:
            self.sha = self.get_git_sha()
        if self.repo_dir is None:
            self.repo_dir = os.path.join(self.stage_dir, "RPMS")

        self.docker_arch = ARCH_MAP[self.arch]

    def run_poi(self, command, workdir=None):
        if workdir is None:
            workdir = os.getcwd()

        poi_cmd = [
            "docker",
            "run",
            "--rm",
            "--privileged",
            "-v",
            "/dev:/dev",
            "-v",
            f"{self.repo_dir}:/repo",
            "-v",
            f"{workdir}:/workdir",
            "-v",
            f"{self.photon_dir}:/photon",
            "-v",
            f"{self.stage_dir}:/photon/stage",
            "-w",
            "/workdir",
        ]

        if self.arch != THIS_ARCH:
            poi_cmd.append(f"--platform=linux/{self.docker_arch}")

        poi_cmd.append(self.poi_image)
        poi_cmd.extend(command)

        print(f"running {poi_cmd}")
        out = subprocess.run(poi_cmd, check=True)

    #
    # copy config files from configs/{type} to stage dir
    # packages json from common/data overrides the one from configs, if present
    #
    def create_config(self, type, subtype=None, subdir=None):
        if subdir is None:
            subdir = type
        if subtype is None:
            subtype = type

        stage_cfg_dir = os.path.join(self.stage_dir, subdir)
        os.makedirs(stage_cfg_dir, exist_ok=True)

        cfg_dir = os.path.join(THIS_DIR, "configs", subdir)
        if os.path.isdir(cfg_dir):
            shutil.copytree(cfg_dir, stage_cfg_dir, dirs_exist_ok=True)
        else:
            print(f"{cfg_dir} not found, ignoring")

        pkg_list_file = os.path.join(
            self.photon_dir, "common", "data", f"packages_{subtype}.json"
        )
        if os.path.isfile(pkg_list_file):
            print(f"using pkg_list_file {pkg_list_file}")
            shutil.copy(pkg_list_file, stage_cfg_dir)
        else:
            print(f"{pkg_list_file} not found, ignoring")

    def create_config_from_custom(self, type, custom_file, subtype=None, subdir=None):
        if subdir is None:
            subdir = type
        if subtype is None:
            subtype = type

        image_file = self.image_filename(type)
        stage_cfg_dir = os.path.join(self.stage_dir, subdir)
        os.makedirs(stage_cfg_dir, exist_ok=True)

        ks_file = os.path.join(stage_cfg_dir, f"{type}_ks.yaml")
        print(f"generating {ks_file} from {custom_file}")

        with open(custom_file, "rt") as f:
            custom_config = json.load(f)
        ks_config = custom_config["installer"]
        ks_config["disks"] = {
            "default": {"filename": image_file, "size": custom_config["size"]}
        }
        ks_config["live"] = False

        # remove this code when "../relocate-rpmdb.sh" is removed from
        # build/photon-aarch64.json in photon-cfg
        if "postinstallscripts" in ks_config:
            ks_config["postinstallscripts"] = list(
                filter(
                    lambda item: "relocate-rpmdb.sh" not in item,
                    ks_config["postinstallscripts"],
                )
            )

        # saving with .yaml extension although it's just json because that's
        # what we are going to use in create_image() - but json is a subset
        # of yaml anyway
        with open(ks_file, "wt") as f:
            json.dump(ks_config, f, indent=4)

        pkg_list_file = os.path.join(
            self.photon_dir, "common", "data", ks_config["packagelist_file"]
        )
        if os.path.isfile(pkg_list_file):
            shutil.copy(pkg_list_file, stage_cfg_dir)
        else:
            print(f"{pkg_list_file} not found, ignoring")

    def create_raw_image(self, type, image_file, subdir=None):
        if subdir is None:
            subdir = type

        stage_cfg_dir = os.path.join(self.stage_dir, subdir)
        ks_file = f"{type}_ks.yaml"
        self.run_poi(
            [
                "create-image",
                "-c",
                ks_file,
                "-v",
                self.release_ver,
                "--param",
                f"imgfile={image_file}",
            ],
            workdir=stage_cfg_dir,
        )
        return os.path.join(stage_cfg_dir, image_file)

    def create_ova(self, image_file, subdir="ova", cleanup=True):
        stage_cfg_dir = os.path.join(self.stage_dir, subdir)
        shutil.copy(self.eula_path, stage_cfg_dir)

        # strip the extension:
        ova_name = image_file.rsplit(".", 1)[0]

        self.run_poi(
            [
                "create-ova",
                "--raw-images",
                image_file,
                "--ova-config",
                "photon.yaml",
                "--ova-name",
                ova_name,
                "--param",
                "eulafile=EULA.txt",
            ],
            workdir=stage_cfg_dir,
        )
        if cleanup:
            os.remove(os.path.join(stage_cfg_dir, image_file))

    def create_azure(self, image_file, subdir="azure"):
        stage_cfg_dir = os.path.join(self.stage_dir, subdir)

        self.run_poi(
            [
                "create-azure",
                "--raw-image",
                image_file,
            ],
            workdir=stage_cfg_dir,
        )
        # no cleanup, done by create-azure

    def _create_tar_gz(self, image_file, tarfile, subdir=None, cleanup=True):
        if subdir is None:
            raise Exception("subdir must be set")

        stage_cfg_dir = os.path.join(self.stage_dir, subdir)
        print(f"tarring {image_file} to {tarfile}")
        subprocess.run(["tar", "zcf", tarfile, image_file], cwd=stage_cfg_dir)
        if cleanup:
            os.remove(os.path.join(stage_cfg_dir, image_file))

    def create_ami(self, image_file, subdir=None, cleanup=True):
        if subdir is None:
            raise Exception("subdir must be set")

        stage_cfg_dir = os.path.join(self.stage_dir, subdir)
        # strip the extension:
        basename = image_file.rsplit(".", 1)[0]
        # our scripts expect the extension ".raw":
        image_file_raw = f"{basename}.raw"
        os.rename(
            os.path.join(stage_cfg_dir, image_file),
            os.path.join(stage_cfg_dir, image_file_raw),
        )

        self._create_tar_gz(
            image_file_raw, f"{basename}.tar.gz", subdir=subdir, cleanup=cleanup
        )

    def create_gce(self, image_file, subdir=None, cleanup=True):
        if subdir is None:
            raise Exception("subdir must be set")

        stage_cfg_dir = os.path.join(self.stage_dir, subdir)
        # strip the extension:
        basename = image_file.rsplit(".", 1)[0]
        # gce expects the name "disk.raw":
        image_file_raw = "disk.raw"
        os.rename(
            os.path.join(stage_cfg_dir, image_file),
            os.path.join(stage_cfg_dir, image_file_raw),
        )

        self._create_tar_gz(
            image_file_raw, f"{basename}.tar.gz", subdir=subdir, cleanup=cleanup
        )

    def create_rpi(self, image_file, subdir=None, cleanup=True):
        if subdir is None:
            raise Exception("subdir must be set")

        stage_cfg_dir = os.path.join(self.stage_dir, subdir)
        # strip the extension:
        basename = image_file.rsplit(".", 1)[0]
        image_path_xz = os.path.join(stage_cfg_dir, f"{basename}.xz")
        print(f"compressing {image_file} to {basename}.xz")
        with open(image_path_xz, "w") as fout:
            subprocess.run(["xz", "-c", image_file], stdout=fout, cwd=stage_cfg_dir)
        if cleanup:
            os.remove(os.path.join(stage_cfg_dir, image_file))

    def create_rpm_list(self, iso_file, type=None, subdir="iso"):

        basename = iso_file.rsplit(".", 1)[0]
        stage_cfg_dir = os.path.join(self.stage_dir, subdir)

        rpm_list = []
        pkg_info_json = os.path.join(self.stage_dir, "pkg_info.json")

        if type == "src":
            self.repo_dir = os.path.abspath(os.path.join(self.repo_dir, "../SRPMS"))

        if os.path.isfile(pkg_info_json):
            print("using pkg_info.json for RPM list")

            key = "rpm"
            if type in ["src", "debug"]:
                key = f"{type}rpm"

            with open(pkg_info_json, "rt") as f:
                pkg_info = json.load(f)

            for pkg_name, pkg in pkg_info.items():
                pkg_file = pkg.get(key, None)
                if pkg_file is not None:
                    rpm_list.append(pkg_file.replace(self.repo_dir, "/repo"))
        else:
            print("pkg_info.json not found, shipping all RPMs")
            for arch in ["noarch", self.arch]:
                for p in glob.glob(os.path.join(self.repo_dir, arch, "*.rpm")):
                    if ("-debuginfo-" in p) == (type == "debug"):
                        # replace leading directory path with path as seen
                        # in container
                        rpm_list.append(p.replace(self.repo_dir.rstrip("/"), "/repo"))

        if type is None:
            rpm_list_file = os.path.join(stage_cfg_dir, f"{basename}.rpm-list")
        else:
            rpm_list_file = os.path.join(stage_cfg_dir, f"{basename}.{type}.rpm-list")

        with open(rpm_list_file, "wt") as f:
            for line in rpm_list:
                f.write(f"{line}\n")

    def create_full_iso(self, iso_file, subdir=None):
        if subdir is None:
            subdir = "iso"

        stage_cfg_dir = os.path.join(self.stage_dir, subdir)

        for cfg_file in ["packages_installer_initrd.json", "packages_minimal.json"]:
            cfg_path = os.path.join(self.photon_dir, "common", "data", cfg_file)
            shutil.copy(cfg_path, stage_cfg_dir)

        basename = iso_file.rsplit(".", 1)[0]
        self.run_poi(
            [
                "photon-iso-builder",
                "-f",
                "build-iso",
                "-v",
                self.release_ver,
                "-p",
                "packages_minimal.json",
                "--initrd-pkgs-list-file",
                "packages_installer_initrd.json",
                "--repo-paths=/repo",
                "--rpms-list-file",
                f"{basename}.rpm-list",
                "--config",
                "iso.yaml",
                "--name",
                iso_file,
            ],
            workdir=stage_cfg_dir,
        )

    def create_full_special_iso(self, iso_file, type=None, subdir=None):
        if subdir is None:
            subdir = "iso"

        if type == "debug":
            repo_subdir = "DEBUGRPMS"
        elif type == "src":
            repo_subdir = "SRPMS"
        else:
            raise Exception(f"unknown iso type '{type}'")

        stage_cfg_dir = os.path.join(self.stage_dir, subdir)
        basename = iso_file.rsplit(".", 1)[0]

        rpm_list_file = rpm_list_file = f"{basename}.{type}.rpm-list"

        script = f"""
        cd /workdir && \
        mkdir -p iso/{repo_subdir} && \
        while read f ; do \
            cp ${{f}} /workdir/iso/{repo_subdir}/ ; \
        done < {rpm_list_file} && \
        createrepo /workdir/iso/{repo_subdir}/ && \
        mkisofs -quiet -r -o {iso_file} /workdir/iso/ &&
        rm -rf iso/
        """
        self.run_poi(["bash", "-c", script], workdir=stage_cfg_dir)

    def create_custom_iso(self, iso_file, type=None, subdir=None):
        if subdir is None:
            subdir = f"{type}-iso"

        stage_cfg_dir = os.path.join(self.stage_dir, subdir)

        initrd_pkgs_list_path = os.path.join(
            self.photon_dir, "common", "data", "packages_installer_initrd.json"
        )
        shutil.copy(initrd_pkgs_list_path, stage_cfg_dir)

        self.run_poi(
            [
                "photon-iso-builder",
                "-f",
                "build-iso",
                "-v",
                self.release_ver,
                "-p",
                f"packages_{type}.json",
                "--initrd-pkgs-list-file",
                "packages_installer_initrd.json",
                "--repo-paths=/repo",
                "--name",
                iso_file,
            ],
            workdir=stage_cfg_dir,
        )

    def get_git_sha(self):
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            check=True,
            cwd=self.photon_dir,
        )
        return out.stdout.decode().strip()

    # ova, azure etc. have the type in the name
    def image_filename(self, type, ext="img"):
        return f"photon-{type}-{self.release_ver}-{self.sha}.{self.arch}.{ext}"

    # full ISOs have no special name, but an extension
    def full_iso_name(self, type=None):
        if type is None:
            return f"photon-{self.release_ver}-{self.sha}.{self.arch}.iso"
        else:
            return f"photon-{self.release_ver}-{self.sha}.{self.arch}.{type}.iso"

    # custom ISOs have the type in the name, and just an 'iso' extension
    # (debug/src not supported here)
    def iso_name(self, type=type):
        return f"photon-{type}-{self.release_ver}-{self.sha}.{self.arch}.iso"


def main():
    config = None
    poi_image = POI_IMAGE
    stage_dir = STAGE_DIR
    repo_dir = None
    arch = THIS_ARCH
    sha = None

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "c:",
            longopts=[
                "config=",
                "docker-image=",
                "arch=",
                "stage-dir=",
                "repo-dir=",
                "sha=",
            ],
        )
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)

    for o, a in opts:
        if o == "--arch":
            arch = a
        elif o in ["-c", "--config"]:
            config = a
        elif o == "--docker-image":
            poi_image = a
        elif o == "--stage-dir":
            stage_dir = a
        elif o == "--repo-dir":
            repo_dir = a
        elif o == "--sha":
            sha = a
        else:
            assert False, f"unhandled option {o}"

    assert arch in ARCH_MAP, "unsupported arch {arch}"

    target = args[0]

    poi = Poi(
        arch=arch, poi_image=poi_image, stage_dir=stage_dir, repo_dir=repo_dir, sha=sha
    )

    if target in ["ova", "ova-stig", "azure", "ami", "gce", "rpi"]:
        assert (
            target != "rpi" or arch == "aarch64"
        ), "arch must be aarch64 to build RPi image"

        poi.create_config(target)
        if config is not None:
            poi.create_config_from_custom(target, config)

        raw_image_file = poi.image_filename(target, "img")
        raw_image_path = poi.create_raw_image(target, raw_image_file)
        assert os.path.isfile(raw_image_path)

        if target == "ova":
            poi.create_ova(raw_image_file)
        if target == "ova-stig":
            poi.create_ova(raw_image_file, subdir="ova-stig")
        elif target == "azure":
            poi.create_azure(raw_image_file)
        elif target == "ami":
            poi.create_ami(raw_image_file, subdir="ami")
        elif target == "gce":
            poi.create_gce(raw_image_file, subdir="gce")
        elif target == "rpi":
            poi.create_rpi(raw_image_file, subdir="rpi")

    elif target in ["iso", "debug-iso", "src-iso"]:
        poi.create_config("iso")

        # type is None indicates the 'normal' full ISO
        # otherwise it's 'special' (src or debug)
        type = None
        if target.startswith("debug-"):
            type = "debug"
        elif target.startswith("src-"):
            type = "src"
        iso_file = poi.full_iso_name(type=type)
        poi.create_rpm_list(iso_file, type=type)

        if type is None:
            poi.create_full_iso(iso_file)
        else:
            poi.create_full_special_iso(iso_file, type=type)

    elif target in ["basic-iso", "minimal-iso", "rt-iso"]:
        # strip "-iso" from the end:
        type = target[:-4]
        poi.create_config(target, subtype=type)
        iso_file = poi.iso_name(type=type)
        poi.create_custom_iso(iso_file, type=type)

    else:
        assert False, f"unknown target {target}"


if __name__ == "__main__":
    main()
