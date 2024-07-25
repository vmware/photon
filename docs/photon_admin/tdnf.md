# Introduction to `tdnf`

On Photon OS, tdnf is the default package manager for installing new packages. It is a C implementation of the DNF package manager without Python dependencies. DNF is the next upcoming major version of yum. 

Tdnf appears in the minimal and full versions of Photon OS. Tdnf reads yum repositories and works like yum. The full version of Photon OS also includes yum, and you can install packages by using yum if you want. 

In the minimal version of Photon OS, you can manage packages by using yum, but you must install it first by running the following `tdnf` command as root: 

	tdnf install yum

Tdnf implements a subset of the `dnf` commands as listed in the [dnf guide](http://dnf.readthedocs.org/en/latest/).