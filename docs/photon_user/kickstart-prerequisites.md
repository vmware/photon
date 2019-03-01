# Prerequisites

Before you kick start a build, verify that you have the following resources:

- Packer 0.8 or later version.
- VMware Fusion or Workstation
- VirtualBox (optional)
- Photon Packer template. The template contains the following artifacts:
    - `packer-photon.json` file
    - `scripts` folder. The folder that contains the scripts you require to kickstart photon
    - `vars` folder. The folder that contains the Photon OS 3.0 ISO URL.
- `packages_minimal.json` file. The JSON file that contains the install profile you require.