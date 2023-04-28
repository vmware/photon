#!/usr/bin/env python3

import os
import sys
import shutil
import imagegenerator

from utils import Utils
from argparse import ArgumentParser
from CommandUtils import CommandUtils

cmdUtils = CommandUtils()


def runInstaller(options, install_config, working_directory):
    try:
        import photon_installer
        from photon_installer.installer import Installer
    except:
        raise ImportError(
            f"Module photon_installer not found!\n"
            f"Run 'pip3 install git+https://github.com/vmware/photon-os-installer.git'"
        )

    # Run the installer
    installer = Installer(working_directory=working_directory,
                          log_path=options.log_path, photon_release_version=options.photon_release_version)
    installer.configure(install_config)
    installer.execute()


def get_file_name_with_last_folder(filename):
    basename = os.path.basename(filename)
    dirname = os.path.dirname(filename)
    lastfolder = os.path.basename(dirname)
    name = os.path.join(lastfolder, basename)
    return name


def create_pkg_list_to_copy_to_iso(build_install_option, output_data_path):
    option_list_json = Utils.jsonread(build_install_option)
    options_sorted = option_list_json.items()
    packages = []
    for install_option in options_sorted:
        if install_option[0] != "iso":
            file_path = os.path.join(output_data_path, os.path.splitext(install_option[1]["packagelist_file"])[0]+"_expanded.json")
            package_list_json = Utils.jsonread(file_path)
            packages = packages + package_list_json["packages"]
    return packages


def create_additional_file_list_to_copy_in_iso(base_path, build_install_option):
    option_list_json = Utils.jsonread(build_install_option)
    options_sorted = option_list_json.items()
    file_list = []
    for install_option in options_sorted:
        if "additional-files" in install_option[1]:
            file_list = file_list + list(map(
                lambda filename: os.path.join(base_path, filename),
                install_option[1].get("additional-files")))
    return file_list


#copy_flags 1: add the rpm file for the package
#           2: add debuginfo rpm file for the package.
#           4: add src rpm file for the package
def create_rpm_list_to_be_copied_to_iso(pkg_to_rpm_map_file, build_install_option, copy_flags,
                                        output_data_path):
    packages = []
    if build_install_option is None:
        packages = []
    else:
        packages = create_pkg_list_to_copy_to_iso(build_install_option, output_data_path)

    rpm_list = []
    pkg_to_rpm_map = Utils.jsonread(pkg_to_rpm_map_file)
    for k in pkg_to_rpm_map:
        if build_install_option is None or k in packages:
            if not pkg_to_rpm_map[k]["rpm"] is None and bool(copy_flags & 1):
                filename = pkg_to_rpm_map[k]["rpm"]
                rpm_list.append(get_file_name_with_last_folder(filename))
            if not pkg_to_rpm_map[k]["debugrpm"] is None and bool(copy_flags & 2):
                filename = pkg_to_rpm_map[k]["debugrpm"]
                rpm_list.append(pkg_to_rpm_map[k]["debugrpm"])
            if not pkg_to_rpm_map[k]["sourcerpm"] is None and bool(copy_flags & 4):
                rpm_list.append(pkg_to_rpm_map[k]["sourcerpm"])
    return rpm_list


def make_debug_iso(working_directory, debug_iso_path, rpm_list):
    if os.path.exists(working_directory) and os.path.isdir(working_directory):
        shutil.rmtree(working_directory)
    cmdUtils.runBashCmd(f"mkdir -p {working_directory}/DEBUGRPMS")
    for rpmfile in rpm_list:
        if os.path.isfile(rpmfile):
            dirname = os.path.dirname(rpmfile)
            lastfolder = os.path.basename(dirname)
            dest_working_directory = os.path.join(working_directory, "DEBUGRPMS", lastfolder)
            cmdUtils.runBashCmd(f"mkdir -p {dest_working_directory}")
            shutil.copy2(rpmfile, dest_working_directory)
    cmdUtils.runBashCmd(f"mkisofs -r -o {debug_iso_path} {working_directory}")
    shutil.rmtree(working_directory)


def make_src_iso(working_directory, src_iso_path, rpm_list):
    if os.path.exists(working_directory) and os.path.isdir(working_directory):
        shutil.rmtree(working_directory)
    cmdUtils.runBashCmd(f"mkdir -p {working_directory}/SRPMS")
    for rpmfile in rpm_list:
        if os.path.isfile(rpmfile):
            shutil.copy2(rpmfile, os.path.join(working_directory, "SRPMS"))
    cmdUtils.runBashCmd(f"mkisofs -r -o {src_iso_path} {working_directory}")
    shutil.rmtree(working_directory)


def createIso(options):
    working_directory = os.path.abspath(os.path.join(options.stage_path, "photon_iso"))
    script_directory = os.path.dirname(os.path.realpath(__file__))
    # Making the iso if needed
    if options.iso_path:
        # Additional RPMs to copy to ISO"s /RPMS/ folder
        rpm_list = " ".join(
            create_rpm_list_to_be_copied_to_iso(
                options.pkg_to_rpm_map_file,
                options.pkg_to_be_copied_conf_file, 1, options.generated_data_path))
        # Additional files to copy to ISO"s / folder
        files_to_copy = " ".join(
            create_additional_file_list_to_copy_in_iso(
                os.path.abspath(options.stage_path), options.package_list_file))

        initrd_pkg_list_file = f"{options.generated_data_path}/packages_installer_initrd_expanded.json"
        initrd_pkgs = " ".join(Utils.jsonread(initrd_pkg_list_file)["packages"])

        cmdUtils.runBashCmd(
            f"{script_directory}/iso/mk-install-iso.sh"
            f" \"{working_directory}\" \"{options.iso_path}\""
            f" \"{options.rpm_path}\" \"{options.package_list_file}\""
            f" \"{rpm_list}\" \"{options.stage_path}\""
            f" \"{files_to_copy}\" \"{options.generated_data_path}\""
            f" \"{initrd_pkgs}\" \"{options.ph_docker_image}\""
            f" \"{options.ph_builder_tag}\" \"{options.photon_release_version}\""
        )

    if options.debug_iso_path:
        debug_rpm_list = create_rpm_list_to_be_copied_to_iso(
            options.pkg_to_rpm_map_file, options.pkg_to_be_copied_conf_file, 2,
            options.generated_data_path)
        make_debug_iso(working_directory, options.debug_iso_path, debug_rpm_list)

    if options.src_iso_path:
        rpm_list = create_rpm_list_to_be_copied_to_iso(options.pkg_to_rpm_map_file,
                                                       options.pkg_to_be_copied_conf_file, 4,
                                                       options.generated_data_path)
        make_src_iso(working_directory, options.src_iso_path, rpm_list)
    if os.path.exists(working_directory) and os.path.isdir(working_directory):
        shutil.rmtree(working_directory)


def replaceScript(script_dir, img, script_name, parent_script_dir=None):
    if not parent_script_dir:
        parent_script_dir = script_dir
    script = f"{parent_script_dir}/{script_name}"
    if os.path.isfile(f"{script_dir}/{img}/{script_name}"):
        script = f"{script_dir}/{img}/{script_name}"
    return script


def verifyImageTypeAndConfig(config_file, img_name):
    # All of the below combinations are supported
    # 1. make image IMG_NAME=<name>
    # 2. make image IMG_NAME=<name> CONFIG=<config_file_path>
    # 3. make image CONFIG=<config_file_path>
    config = None
    if img_name and img_name != "":
        # Verify there is a directory corresponding to image
        if img_name not in next(os.walk(os.path.dirname(__file__)))[1]:
            return (False, config)
        if config_file and config_file != "" and os.path.isfile(config_file):
            config = Utils.jsonread(config_file)
            if "image_type" in config and config["image_type"] != img_name:
                return (False, config)
        else:
            config_file = os.path.dirname(__file__) + f"/{img_name}/config_{img_name}.json"
            if os.path.isfile(config_file):
                config = Utils.jsonread(config_file)
                if "image_type" not in config:
                    config["image_type"] = img_name
            else:
                return (False, config)
        return (True, config)
    if not config_file or config_file == "":
        return (False, config)

    config = Utils.jsonread(config_file)
    return ("image_type" in config, config)


# Detach loop device and remove raw image
def cleanup(loop_devices, raw_image):
    for i,loop_dev in enumerate(loop_devices):
        cmdUtils.runBashCmd(f"losetup -d {loop_dev}")
        os.remove(raw_image[i])


def createImage(options):
    (validImage, config) = verifyImageTypeAndConfig(options.config_file, options.img_name)
    if not validImage:
        raise Exception("Image type/config not supported")

    if "ova" in config["artifacttype"] and shutil.which("ovftool") is None:
        raise Exception("ovftool is not available")

    install_config = config["installer"]

    image_type = config["image_type"]
    image_name = config.get("image_name", f"photon-{image_type}")
    workingDir = os.path.abspath(f"{options.stage_path}/{image_type}")
    if os.path.exists(workingDir) and os.path.isdir(workingDir):
        shutil.rmtree(workingDir)
    os.mkdir(workingDir)
    script_dir = os.path.dirname(os.path.realpath(__file__))

    grub_script = replaceScript(script_dir, image_type, "mk-setup-grub.sh")
    if os.path.isfile(grub_script):
        install_config["setup_grub_script"] = grub_script

    # Set absolute path for "packagelist_file"
    if "packagelist_file" in install_config:
        plf = install_config["packagelist_file"]
        if not plf.startswith("/"):
            plf = os.path.join(options.generated_data_path, plf)
        install_config["packagelist_file"] = plf

    os.chdir(workingDir)

    if "log_level" not in install_config:
        install_config["log_level"] = options.log_level

    install_config["search_path"] = [
        os.path.abspath(os.path.join(script_dir, image_type)),
        os.path.abspath(script_dir),
    ]

    # if "photon_docker_image" is defined in config_<img>.json then ignore
    # commandline param "PHOTON_DOCKER_IMAGE" and "config.json" value
    if "photon_docker_image" not in install_config:
        install_config["photon_docker_image"] = options.ph_docker_image

    # Take default "repo" baseurl as options.rpm_path if not specified in config_<img>.json
    if "repos" not in install_config:
        install_config["repos"] = {"photon-local": { "name": "VMware Photon OS Installer",
                                                     "baseurl": f"file://{os.path.abspath(options.rpm_path)}",
                                                     "gpgcheck": 0,
                                                     "enabled": 1 }}

    if "size" in config and "disks" in config:
        raise Exception(
            f"Both 'size' and 'disks' key should not be defined together."
            f"\nPlease use 'disks' for defining multidisks only."
        )
    elif "size" in config:
        # "BOOTDISK" key name doesn"t matter. It is just a name given for better understanding
        config["disks"] = {"BOOTDISK": config["size"]}
    elif "disks" not in config:
        raise Exception("Disk size not defined!!")

    image_file = []
    loop_device = {}
    # Create disk image
    for ndisk, k in enumerate(config["disks"]):
        image_file.append(f"{workingDir}/{image_name}-{ndisk}.raw")
        cmdUtils.runBashCmd(
            "dd if=/dev/zero of={} bs=1024 seek={} count=0".format(image_file[ndisk], config["disks"].get(k) * 1024))
        cmdUtils.runBashCmd(
            "chmod 755 {}".format(image_file[ndisk]))
        # Associating loopdevice to raw disk and save the name as a target"s "disk"
        out, _, _ = cmdUtils.runBashCmd("losetup --show -f {}".format(image_file[ndisk]), capture=True)
        loop_device[k] = out.rstrip("\n")

    # Assigning first loop device as BOOTDISK
    install_config["disk"] = loop_device[next(iter(loop_device))]

    # Mapping the given disks to the partition table disk
    # Assigning the appropriate loop device to the partition "disk"
    if "partitions" in install_config:
        for partition in install_config["partitions"]:
            if len(loop_device) == 1:
                partition["disk"] = install_config["disk"]
            elif "disk" in partition:
                if partition["disk"] in loop_device.keys():
                    partition["disk"] = loop_device[partition["disk"]]
                else:
                    cleanup(loop_device.values(), image_file)
                    raise Exception("disk name:{} defined in partition table not found in list of 'disks'!!".format(partition["disk"]))
            else:
                cleanup(loop_device.values(), image_file)
                raise Exception("disk name must be defined in partition table for multidisks!!")

    # No return value, it throws exception on error.
    runInstaller(options, install_config, workingDir)

    # Detaching loop device from vmdk
    for loop_dev in loop_device.values():
        cmdUtils.runBashCmd(f"losetup -d {loop_dev}")

    os.chdir(script_dir)
    imagegenerator.createOutputArtifact(
                image_file,
                config,
                options.src_root,
                f"{options.src_root}/tools/bin/"
            )


if __name__ == "__main__":
    parser = ArgumentParser()

    # Common args
    parser.add_argument("-e", "--src-root", dest="src_root", default="../..")
    parser.add_argument("-g", "--generated-data-path", dest="generated_data_path", default="../../stage/common/data")
    parser.add_argument("-s", "--stage-path", dest="stage_path", default="../../stage")
    parser.add_argument("-l", "--log-path", dest="log_path", default="../../stage/LOGS")
    parser.add_argument("-y", "--log-level", dest="log_level", default="debug")
    # Image builder args for ami, gce, azure, ova, rpi3 etc.
    parser.add_argument("-c", "--config-file", dest="config_file")
    parser.add_argument("-i", "--img-name", dest="img_name")
    # ISO builder args
    parser.add_argument("-j", "--iso-path", dest="iso_path")
    parser.add_argument("-k", "--debug-iso-path", dest="debug_iso_path")
    parser.add_argument("-m", "--src-iso-path", dest="src_iso_path")
    parser.add_argument("-r", "--rpm-path", dest="rpm_path", default="../../stage/RPMS")
    parser.add_argument("-x", "--srpm-path", dest="srpm_path", default="../../stage/SRPMS")
    parser.add_argument("-p", "--package-list-file", dest="package_list_file", default="../../common/data/build_install_options_all.json")
    parser.add_argument("-d", "--pkg-to-rpm-map-file", dest="pkg_to_rpm_map_file", default="../../stage/pkg_info.json")
    parser.add_argument("-z", "--pkg-to-be-copied-conf-file", dest="pkg_to_be_copied_conf_file")
    parser.add_argument("-q", "--photon-docker-image", dest="ph_docker_image", default="photon:latest")
    parser.add_argument("-v", "--photon-release-version", dest="photon_release_version")

    options = parser.parse_args()
    if options.config_file and options.config_file != "":
        options.config_file = os.path.abspath(options.config_file)
    # Create ISO
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    if options.iso_path or options.debug_iso_path or options.src_iso_path:
        createIso(options)
    elif options.config_file or options.img_name:
        createImage(options)
    else:
        raise Exception("No supported image type defined")
