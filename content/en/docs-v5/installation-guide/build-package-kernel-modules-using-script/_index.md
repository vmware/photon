---
title:  Building Package or Kernel Modules Using a Script
weight: 4
---

You can use a script to build a single Photon OS package without the need to setup a complete Photon build workspace. You just need a `.spec` specification file and the source files. You can place the source files and the specification files in the same folder, or provide a URL for the source file location, and then run the `build_spec.sh` script. 

The script performs the following steps:

- Creates sandbox using docker
- Installs build tools and `.spec` build requirements from the Photon OS repository
- Runs `rpmbuild`

**Result:** You have a native Photon OS RPM package.

The `build-spec.sh` script is located in the `photon/tools/scripts/` folder.

- [Prerequisites](#prerequisites)
- [Procedure](#procedure)

## Prerequisites

Before you run the `build-spec.sh` script, perform the following steps:

- Ensure you have any Linux OS with a docker daemon running.
- Place the source and RPM `.spec` files in the same folder or provide a URL for the source files.

## Procedure

Run the script. Provide the RPM `.spec` file name, including absolute or relative path, as an argument:

```
./photon/tools/scripts/build_spec.sh <path-to-rpm_spec_file.spec> [$STAGEDIR]
```

You can specify the staging directory (`$STAGEDIR`) where you want to store the generated RPM files and build logs. If you do not specify a staging directory, the generated output files are stored in the directory that contains the spec file.


The following topics show examples to build packages based on various use cases. 