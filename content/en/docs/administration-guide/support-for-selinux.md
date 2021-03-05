---
title:  Support for SELinux
weight: 10
---

SELinux is a labelling system to implement MAC(mandatory access control) for subjects(user, process) over objects (files, dirs, sockets) and to protect the confidentiality of objects. It is a policy driven system where rules can be mapped to the labels which have been given to subjects, objects. It is an extra level of security provided on top of Linux normal file ownership/permissions.

Photon OS 4.0 offersx support for SELinux. The support covers a minimal set of policies for the container runtime case and it is referred to as the default policy. It is a Multi-Category Security (MCS) policy. So the files on the filesystem can be labeled with multiple categories.The MCS policy is actively used by container runtime as `runc/containerd/docker/kubernetes` to assign the `per-container` category.

The default policy in Photon OS does not use `user`, `role` (RBAC) and `level` (MLS) fields of the file labels.It operates only with the context and category fields. It consists of several modules loaded with priority as `100`. The user-defined policy can overwrite default modules by using the higher priority.

## Enabling SELinux ##

To enable SELinux on Photon OS:

1. Install default policy and its dependencies. Initial filesystem labeling will be done as RPM post action.

    `tdnf install -y selinux-policy`

1. Enable SELinux security model in kernel by adding 2 kernel parameters:

- `security=selinux`
- `selinux=1`

 Ensure that you reboot after adding the kernel parameters.

1. After reboot, the system runs in SELinux permissive mode. To confirm, check the journal:

        journalctl -b0 | grep -i selinux

        Feb 26 21:42:09 photon-machine kernel: SELinux:  Initializing.
        Feb 26 21:42:09 photon-machine kernel: SELinux:  policy capability ...
        Feb 26 21:42:09 photon-machine kernel: audit: type=1403 audit(1589406128.920:2): auid=4294967295 ses=4294967295 lsm=selinux res=1
        Feb 26 21:42:09 photon-machine systemd[1]: Successfully loaded SELinux policy in 322.475ms.

## Switch SELinux to enforcing mode ##

The three methods to toggle enforcing mode are as follows:
1. Run the `setenforce 1` command (libselinux-utils rpm), Enforcing mode will be set timmediately, but it is not preserved on reboot.
2. Edit the `/etc/selinux/config` file to set `SELINUX=enforcing` and reboot.
3. Add the `enforcing=1` kernel parameter and reboot.


## Developing Customized Policy ##

Photon OS provides an ability to develop customized additional policy on top of existing default policy.
The following example is for adding the sys_admin capability policy:

1. Install policy development packages
    tdnf install -y selinux-policy-devel semodule-utils

2. Create .te file
    cat getty_local.te
    policy_module(getty_local, 1.0)

    gen_require(`
        type getty_t;
          ')

    allow getty_t self:capability sys_admin;

3. Compile it into .pp file
    make -f /usr/share/selinux/devel/Makefile getty_local.pp

4. Load it with priority 200. It will permanently alter default policy. And this change will survive reboot cycle.
    semodule -i getty_local.pp -X 200

5. Check result
    sesearch -A -s getty_t -t getty_t -c capability
    allow getty_t getty_t:capability { chown dac_override dac_read_search fowner fsetid setgid sys_admin sys_resource sys_tty_config };

6. List of loaded modules and their priorities
    semodule -lfull

## Debugging SELinux ##

Install the debugging tools as follows:

    tdnf install -y setools python3-pip

    pip3 install networkx

List all actions denied by Selinux using the following command:

    journalctl _TRANSPORT=audit -b 0 | grep denied

    Feb 26 21:42:43 photon-machine audit[445]: AVC avc:  denied  { sys_admin } for  pid=445 comm="agetty" capability=21
    scontext=system_u:system_r:getty_t:s0-s0:c0.c1023 tcontext=system_u:system_r:getty_t:s0-s0:c0.c1023 tclass=capability permissive=0

You can see that the agetty process running in the getty_t context tries to change the capability of getty_t target to obtain `sys_admin`. To view the capability that getty_t can obtain:

    sesearch -A -s getty_t -t getty_t -c capability

    allow getty_t getty_t:capability { chown dac_override dac_read_search fowner fsetid setgid sys_resource sys_tty_config };

Note: `sys_admind` is not listed there and can be added. 


## Important SELinux Files ##

Here are some of the important SELinux files:


- SELinux config
    /etc/selinux/config


- default policy folder
    /etc/selinux/default/


- Binary policy blob to be loaded to kernel on every boot
    /etc/selinux/default/policy/policy.32


- List of file labels used by the policy
    /etc/selinux/default/contexts/files/file_contexts

## Troubleshooting Compilation Error ##

If compilation fails by any reason and it complains on some line number in the `.cil` file. You can run the pp compiler to get the plain text cil output.

    /usr/libexec/selinux/hll/pp getty_local.pp
    (roleattributeset cil_gen_require system_r)
    (typeattributeset cil_gen_require getty_t)
    (allow getty_t self (capability (sys_admin)))