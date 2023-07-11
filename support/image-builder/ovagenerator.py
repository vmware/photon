#!/usr/bin/env python3

import os

from utils import Utils
from argparse import ArgumentParser
from CommandUtils import CommandUtils


def create_ova(
    raw_image_names, config, skip_convert=False, image_name=None, eulafile=None
):
    cmdUtils = CommandUtils()

    config_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), config["image_type"]
    )

    if image_name is None:
        image_name = config.get("image_name", "photon-{config['image_type']}")

    if type(raw_image_names) is str:
        raw_image_names = [raw_image_names]
    assert type(raw_image_names) is list

    output_path = os.path.dirname(os.path.realpath(raw_image_names[0]))

    vmdk_paths = []
    for i, raw_img in enumerate(raw_image_names):
        vmdk_paths.append(os.path.join(output_path, f"{image_name}{i}.vmdk"))
        if not skip_convert:
            cmdUtils.runBashCmd(
                f"vmdk-convert -t 2147483647 {raw_img} {vmdk_paths[i]}"
            )

    ova_config_file = os.path.join(config_path, config["ova_config"])
    ova_file = os.path.join(output_path, f"{image_name}.ova")

    compose_cmd = f"ova-compose -i {ova_config_file} -o {ova_file}"
    if eulafile is not None:
        compose_cmd += f" --param eulafile={eulafile}"
    for i, d in enumerate(vmdk_paths):
        compose_cmd += f" --param disk{i}={d}"
    cmdUtils.runBashCmd(compose_cmd)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-r", "--raw-image-path", dest="raw_image_path")
    parser.add_argument("-c", "--config-path", dest="config_path")
    parser.add_argument(
        "-v", "--skip-convert", dest="skip_convert", action="store_true"
    )

    options = parser.parse_args()
    if options.config_path:
        config = Utils.jsonread(options.config_path)
    else:
        raise Exception("No config file defined")

    create_ova(
        options.raw_image_path, config, skip_convert=options.skip_convert
    )
