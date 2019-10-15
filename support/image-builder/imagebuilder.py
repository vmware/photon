#!/usr/bin/python3

import os
import sys
import shutil
import subprocess
from argparse import ArgumentParser
from utils import Utils
import imagegenerator

def runInstaller(options, install_config, working_directory):
    try:
        sys.path.insert(0, options.installer_path)
        from installer import Installer
    except:
        raise ImportError('Installer path incorrect!')

    # Run the installer
    installer = Installer(working_directory=working_directory, rpm_path=options.rpm_path,
                          log_path=options.log_path)
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
            file_path = os.path.join(output_data_path, install_option[1]["packagelist_file"])
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
            if not pkg_to_rpm_map[k]['rpm'] is None and bool(copy_flags & 1):
                filename = pkg_to_rpm_map[k]['rpm']
                rpm_list.append(get_file_name_with_last_folder(filename))
            if not pkg_to_rpm_map[k]['debugrpm'] is None and bool(copy_flags & 2):
                filename = pkg_to_rpm_map[k]['debugrpm']
                rpm_list.append(pkg_to_rpm_map[k]['debugrpm'])
            if not pkg_to_rpm_map[k]['sourcerpm'] is None and bool(copy_flags & 4):
                rpm_list.append(pkg_to_rpm_map[k]['sourcerpm'])
    return rpm_list

def make_debug_iso(working_directory, debug_iso_path, rpm_list):
    if os.path.exists(working_directory) and os.path.isdir(working_directory):
        shutil.rmtree(working_directory)
    process = subprocess.Popen(['mkdir', '-p', os.path.join(working_directory, "DEBUGRPMS")])
    process.wait()
    for rpmfile in rpm_list:
        if os.path.isfile(rpmfile):
            dirname = os.path.dirname(rpmfile)
            lastfolder = os.path.basename(dirname)
            dest_working_directory = os.path.join(working_directory, "DEBUGRPMS", lastfolder)
            if not os.path.isdir(dest_working_directory):
                process = subprocess.Popen(['mkdir', dest_working_directory])
                process.wait()
            shutil.copy2(rpmfile, dest_working_directory)
    process = subprocess.Popen(['mkisofs', '-r', '-o', debug_iso_path, working_directory])
    process.wait()
    shutil.rmtree(working_directory)

def make_src_iso(working_directory, src_iso_path, rpm_list):
    if os.path.exists(working_directory) and os.path.isdir(working_directory):
        shutil.rmtree(working_directory)
    process = subprocess.Popen(['mkdir', '-p', os.path.join(working_directory, "SRPMS")])
    process.wait()
    for rpmfile in rpm_list:
        if os.path.isfile(rpmfile):
            shutil.copy2(rpmfile, os.path.join(working_directory, "SRPMS"))
    process = subprocess.Popen(['mkisofs', '-r', '-o', src_iso_path, working_directory])
    process.wait()
    shutil.rmtree(working_directory)

def createIso(options):
    working_directory = os.path.abspath(os.path.join(options.stage_path, "photon_iso"))
    script_directory = os.path.dirname(os.path.realpath(__file__))
    # Making the iso if needed
    if options.iso_path:
        # Additional RPMs to copy to ISO's /RPMS/ folder
        rpm_list = " ".join(
            create_rpm_list_to_be_copied_to_iso(
                options.pkg_to_rpm_map_file,
                options.pkg_to_be_copied_conf_file, 1, options.generated_data_path))
        # Additional files to copy to ISO's / folder
        files_to_copy = " ".join(
            create_additional_file_list_to_copy_in_iso(
                os.path.abspath(options.stage_path), options.package_list_file))

        initrd_pkg_list_file = os.path.join(os.path.dirname(options.package_list_file), 'packages_installer_initrd.json')
        initrd_pkgs = " ".join(Utils.jsonread(initrd_pkg_list_file)["packages"])

        retval = subprocess.call([script_directory + '/iso/mk-install-iso.sh',
                                  options.installer_path,
                                  working_directory, options.iso_path,
                                  options.rpm_path, options.package_list_file,
                                  rpm_list, options.stage_path, files_to_copy,
                                  options.generated_data_path, initrd_pkgs])

        if retval:
            raise Exception("Unable to create install ISO")

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
    script = parent_script_dir + '/' + script_name
    if os.path.isfile(script_dir + '/' + img + '/' + script_name):
        script = script_dir + '/' + img + '/' + script_name
    return script

def verifyImageTypeAndConfig(config_file, img_name):
    # All of the below combinations are supported
    # 1. make image IMG_NAME=<name>
    # 2. make image IMG_NAME=<name> CONFIG=<config_file_path>
    # 3. make image CONFIG=<config_file_path>
    config = None
    if img_name and img_name != '':
        # Verify there is a directory corresponding to image
        if img_name not in next(os.walk('.'))[1]:
            return (False, config)
        if config_file and config_file != '' and os.path.isfile(config_file):
            config = Utils.jsonread(config_file)
            if 'image_type' in config and config['image_type'] != img_name:
                return (False, config)
        else:
            config_file = img_name + "/config_" + img_name + ".json"
            if os.path.isfile(config_file):
                config = Utils.jsonread(config_file)
                if 'image_type' not in config:
                    config['image_type'] = img_name
            else:
                return (False, config)
        return (True, config)
    if not config_file or config_file == '':
        return (False, config)

    config = Utils.jsonread(config_file)
    return ('image_type' in config, config)

def createImage(options):
    (validImage, config) = verifyImageTypeAndConfig(options.config_file, options.img_name)
    if not validImage:
        raise Exception("Image type/config not supported")

    if 'ova' in config['artifacttype'] and shutil.which("ovftool") is None:
        raise Exception("ovftool is not available")

    install_config = config['installer']

    image_type = config['image_type']
    workingDir = os.path.abspath(options.stage_path + "/" + image_type)
    if os.path.exists(workingDir) and os.path.isdir(workingDir):
        shutil.rmtree(workingDir)
    os.mkdir(workingDir)
    script_dir = os.path.dirname(os.path.realpath(__file__))

    grub_script = replaceScript(script_dir, image_type, "mk-setup-grub.sh", options.installer_path)
    install_config['setup_grub_script'] = grub_script

    # Set absolute path for 'packagelist_file'
    if 'packagelist_file' in install_config:
        plf = install_config['packagelist_file']
        if not plf.startswith('/'):
            plf = os.path.join(options.generated_data_path, plf)
        install_config['packagelist_file'] = plf

    os.chdir(workingDir)
    image_file = workingDir + "/photon-" + image_type + ".raw"

    # Create disk image
    Utils.runshellcommand(
        "dd if=/dev/zero of={} bs=1024 seek={} count=0".format(image_file, config['size'] * 1024))
    Utils.runshellcommand(
        "chmod 755 {}".format(image_file))

    if 'log_level' not in install_config:
        install_config['log_level'] = options.log_level

    install_config['search_path'] = [
        os.path.abspath(os.path.join(script_dir, image_type)),
        os.path.abspath(script_dir),
    ]

    # Associating loopdevice to raw disk and save the name as a target's 'disk'
    install_config['disk'] = (Utils.runshellcommand(
        "losetup --show -f {}".format(image_file))).rstrip('\n')

    # No return value, it throws exception on error.
    runInstaller(options, install_config, workingDir)

    # Detaching loop device from vmdk
    Utils.runshellcommand("losetup -d {}".format(install_config['disk']))

    os.chdir(script_dir)
    imagegenerator.createOutputArtifact(
                                image_file,
                                config,
                                options.src_root,
                                options.src_root + '/tools/bin/'
                              )

if __name__ == '__main__':
    parser = ArgumentParser()

    # Common args
    parser.add_argument("-e", "--src-root", dest="src_root", default="../..")
    parser.add_argument("-f", "--installer-path", dest="installer_path", default="../../installer")
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

    options = parser.parse_args()
    if options.config_file and options.config_file != '':
        options.config_file = os.path.abspath(options.config_file)
    # Create ISO
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    if options.iso_path or options.debug_iso_path or options.src_iso_path:
        createIso(options)
    elif options.config_file or options.img_name:
        createImage(options)
    else:
        raise Exception("No supported image type defined")
