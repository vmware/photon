import os
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


class KernelSpecProcessor:
    def __init__(self, driver_info_file, spec_paths):
        self.kvers = defaultdict(list)
        self.krels = defaultdict(list)
        self.build_for = defaultdict(list)
        self.spec_paths = spec_paths
        self.__load_data(driver_info_file)
        self.__extract_kernel_data()

    # Load the JSON data from the given file
    def __load_data(self, driver_info_file):
        with open(driver_info_file, "r") as file:
            data = json.load(file)

        if "linux_flavour" not in data or "linux_dep_package" not in data:
            print("Error: Missing required keys in JSON data.")
            sys.exit(1)

        # Store the entire JSON structure for easy access
        self.linux_flavours = data["linux_flavour"]
        self.spec_map = data["linux_dep_package"]

    def __find_spec_files(self, pattern, template=False):
        k_specs = []
        pattern = f"*/{pattern}.spec"
        if template is True:
            pattern = f'{pattern}.in'
        for spec_path in self.spec_paths:
            directory_path = Path(spec_path).resolve()
            if directory_path.is_dir():
                # Recursively find files matching the pattern
                k_specs.extend(directory_path.rglob(pattern))
        return k_specs

    def __delete_older_specs(self):
        for pattern, value in  self.spec_map.items():
            k_specs = []
            if 'kernels' in pattern:
                pattern = "*drivers-intel-*"
            else:
                pattern = f"*{pattern}*"
            k_specs = self.__find_spec_files(pattern)
            for spec_file in k_specs:
                spec_file.unlink()

    def __extract_kernel_data(self):
        # # Extract kernel versions, releases, and build targets
        for linux_flavour in self.linux_flavours:
            spec_paths = self.__find_spec_files(linux_flavour)
            for spec_path in spec_paths:
                with open(spec_path, 'r') as spec_file:
                    spec_content = spec_file.read()

                version_match = re.search(r"^Version:\s*(\S+)",
                                          spec_content, re.MULTILINE).group(1)
                release_match = re.search(r"^Release:\s*(\S+)",
                                          spec_content, re.MULTILINE).group(1)
                build_for_match = re.search(r"^\s*%global\s+build_for\s+(.*)",
                                            spec_content, re.MULTILINE)

                if build_for_match:
                    build_for_value = build_for_match.group(1).strip()
                else:
                    build_for_value = "all"

                self.kvers[linux_flavour].append(version_match)
                self.krels[linux_flavour].append(release_match)
                self.build_for[linux_flavour].extend([build_for_value])

    # Process spec file by replacing placeholders with actual values
    def __process_spec_file(self, spec_file, kver, krel, ksubrel,
                          build_for_value, target_fn,
                          linux_flavour, pkg_version):
        spec_file = self.__find_spec_files(spec_file, template=True)
        with open(spec_file[0], "r") as file:
            content = file.read()
        linux_flavour = linux_flavour.replace('linux', '')

        content = content.replace("%{KERNEL_VERSION}", kver) \
                         .replace("%{KERNEL_RELEASE}", krel) \
                         .replace("%{?kernelsubrelease}", ksubrel) \
                         .replace("%{BUILD_FOR}", build_for_value) \
                         .replace("%{KERNEL_FLAVOUR}", linux_flavour) \
                         .replace("%{PKG_VERSION}", pkg_version)

        target_dir = os.path.dirname(spec_file[0])
        target_file = os.path.join(target_dir, target_fn)
        with open(target_file, "w") as file:
            file.write(content)

    # Create specs based on the provided package name
    def create_specs(self):
        self.__delete_older_specs()
        for linux_flavour in self.linux_flavours:
            # Get kernel versions, releases, and build targets
            kver_arr = self.kvers.get(linux_flavour, [])
            krel_arr = self.krels.get(linux_flavour, [])
            build_for_arr = self.build_for.get(linux_flavour, [])
            # Loop through all kernel versions
            for i in range(len(kver_arr)):
                kver = kver_arr[i]
                build_for_value = build_for_arr[i]

                # Kernel subrelease format
                a, b, *c = map(int, kver.split("."))
                c = c[0] if c else 0
                d = int(''.join(re.findall(r'\d+', krel_arr[i])))
                major_linux_version = f"v{a}.{b}"
                ksubrel = f".{a:02d}{b:02d}{c:03d}{d:03d}"
                # Process each spec file
                for sp, value in  self.spec_map.items():
                    spec_name = sp
                    spec_name = spec_name.replace("kernels", linux_flavour)

                    target_fn = f"{spec_name.replace('.spec.in', '')}-{kver}.spec"
                    # Check if driver-specific processing is required
                    if major_linux_version in value:
                        if linux_flavour in value[major_linux_version]:
                            supported_linux_version = set(value[major_linux_version][linux_flavour])
                            for sp_version in supported_linux_version:
                                target_fn = f"{spec_name}-{sp_version}-{kver}.spec"
                                self.__process_spec_file(sp, kver, krel_arr[i], ksubrel, build_for_value,
                                                       target_fn, linux_flavour, sp_version)


# Main logic for processing specs
def main(driver_info_file, spec_paths):
    processor = KernelSpecProcessor(driver_info_file,
                                    spec_paths)
    processor.create_specs()


if __name__ == "__main__":
    # Provide the path to the JSON file containing kernel driver data
    spec_paths = sys.argv[1:-1]
    driver_info_file = sys.argv[-1]
    main(driver_info_file, spec_paths)
