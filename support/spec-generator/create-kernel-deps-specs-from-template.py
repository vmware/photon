import operator
import os
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

_BUILD_IF_OPS = {
    "<=": operator.le,
    ">=": operator.ge,
    "<": operator.lt,
    ">": operator.gt,
    "==": operator.eq,
}


class KernelSpecProcessor:
    def __init__(self, driver_info_file, spec_paths):
        self.kvers = defaultdict(list)
        self.krels = defaultdict(list)
        self.build_for = defaultdict(list)
        self.spec_paths = spec_paths
        self.__template_active_cache = {}
        self.current_subrelease = self.__load_current_subrelease()
        self.__load_data(driver_info_file)
        self.__extract_kernel_data()

    # Same precedence as build.py: PHOTON_SUBRELEASE env var, else build-config.json.
    def __load_current_subrelease(self):
        env_value = os.environ.get("PHOTON_SUBRELEASE")
        if env_value is not None:
            try:
                return int(env_value)
            except ValueError:
                pass

        for spec_path in self.spec_paths:
            config_path = Path(spec_path).resolve().parent / "build-config.json"
            if not config_path.is_file():
                continue
            try:
                with open(config_path, "r") as file:
                    build_config = json.load(file)
            except (json.JSONDecodeError, OSError):
                continue
            value = build_config.get("photon-build-param", {}).get("photon-subrelease")
            if value is not None:
                try:
                    return int(value)
                except ValueError:
                    continue
        return None

    # Evaluate a "%{photon_subrelease} <op> N" build_if expression; unparseable defaults to active.
    def __is_build_if_active(self, build_for_value):
        if self.current_subrelease is None:
            return True
        match = re.match(
            r"%\{photon_subrelease\}\s*(<=|>=|<|>|==)\s*(\d+)", build_for_value.strip()
        )
        if not match:
            return True
        op, num = match.group(1), int(match.group(2))
        return _BUILD_IF_OPS[op](self.current_subrelease, num)

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

    def __read_build_if(self, path):
        with open(path, "r") as file:
            content = file.read()
        match = re.search(r"^\s*%(?:global|define)\s+build_if\s+(.*)", content, re.MULTILINE)
        return match.group(1).strip() if match else "1"

    def __template_dir_label(self, candidate):
        for spec_path in self.spec_paths:
            root = Path(spec_path).resolve()
            try:
                parts = candidate.resolve().relative_to(root).parts
            except ValueError:
                continue
            return parts[0] if parts and parts[0].isdigit() else None
        return None

    # Pick among duplicate templates (base + subrelease overrides) by build_if
    # truth, not directory name -- prefer the named override, else any active
    # override, else the base template.
    def __resolve_template_match(self, matches):
        if not matches:
            return None
        if self.current_subrelease is None or len(matches) == 1:
            return matches[0]

        current = str(self.current_subrelease)
        overrides, base_match = [], None
        for candidate in matches:
            label = self.__template_dir_label(candidate)
            if label is None:
                base_match = base_match or candidate
            else:
                overrides.append((label, candidate))

        overrides.sort(key=lambda pair: pair[0] != current)
        for _, candidate in overrides:
            if self.__is_build_if_active(self.__read_build_if(candidate)):
                return candidate

        return base_match or matches[0]

    def __delete_older_specs(self):
        for pattern, value in  self.spec_map.items():
            k_specs = []
            if 'kernels' in pattern:
                pattern = "*drivers-intel-*"
            else:
                # Only match our own generated output, not a hand-written "<pattern>.spec".
                pattern = f"{pattern}-*"
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
                build_for_match = re.search(r"^\s*%(?:global|define)\s+build_if\s+(.*)", spec_content, re.MULTILINE)

                if build_for_match:
                    build_for_value = build_for_match.group(1).strip()
                else:
                    build_for_value = "1"

                if not self.__is_build_if_active(build_for_value):
                    continue

                self.kvers[linux_flavour].append(version_match)
                self.krels[linux_flavour].append(release_match)
                self.build_for[linux_flavour].extend([build_for_value])

    # Skip a package entirely if its template's own build_if is inactive.
    def __is_template_active(self, spec_file):
        if spec_file not in self.__template_active_cache:
            active = True
            match_path = self.__resolve_template_match(
                self.__find_spec_files(spec_file, template=True)
            )
            if match_path:
                active = self.__is_build_if_active(self.__read_build_if(match_path))
            self.__template_active_cache[spec_file] = active
        return self.__template_active_cache[spec_file]

    # Process spec file by replacing placeholders with actual values
    def __process_spec_file(self, spec_file, kver, krel, ksubrel,
                          build_for_value, target_fn,
                          linux_flavour, pkg_version):
        spec_file = self.__resolve_template_match(
            self.__find_spec_files(spec_file, template=True)
        )
        with open(spec_file, "r") as file:
            content = file.read()
        linux_flavour = linux_flavour.replace('linux', '')

        content = content.replace("%{KERNEL_VERSION}", kver) \
                         .replace("%{KERNEL_RELEASE}", krel) \
                         .replace("%{?kernelsubrelease}", ksubrel) \
                         .replace("%{BUILD_FOR}", build_for_value) \
                         .replace("%{KERNEL_FLAVOUR}", linux_flavour) \
                         .replace("%{PKG_VERSION}", pkg_version)

        target_dir = os.path.dirname(spec_file)
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
                    if not self.__is_template_active(sp):
                        continue

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
