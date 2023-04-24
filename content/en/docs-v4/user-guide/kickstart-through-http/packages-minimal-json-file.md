---
title:  packages_minimal.json File
weight: 4
---

The `packages_minimal.json` file contains the install profile that you require.

The contents of the file are as follows:

```json
{
    "packages": [
                 "minimal",
                 "linux",
                 "initramfs"
                 ]
}
```

'minimal` is a meta package contains a number of default packages.

For more imformation, see [4.0 minimal.spec](https://github.com/vmware/photon/blob/4.0/SPECS/minimal/minimal.spec)