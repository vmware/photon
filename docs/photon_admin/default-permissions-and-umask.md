# Default Permissions and umask

The `umask` on Photon OS is set to `0027`.

When you create a new file with the `touch` command as root, the default on Photon OS is to set the permissions to `0640`--which translates to `read-write` for user, `read` for group, and no access for others. Here's an example: 

    touch newfile.md
    stat newfile.md
      File: 'newfile.md'
      Size: 0               Blocks: 0          IO Block: 4096   regular empty file
    Device: 801h/2049d      Inode: 316454      Links: 1
    Access: (0640/-rw-r-----)  Uid: (    0/    root)   Gid: (    0/    root)

When you create a directory as root, Photon OS sets the permissions to `0750`:

    mkdir newdir
    stat newdir
      File: 'newdir'
      Size: 4096            Blocks: 8          IO Block: 4096   directory
    Device: 801h/2049d      Inode: 316455      Links: 2
    Access: (0750/drwxr-x---)  Uid: (    0/    root)   Gid: (    0/    root)

Because the `mkdir` command uses the umask to modify the permissions placed on newly created files or directories, you can see `umask` at work in the permissions of the new directory. Its default permissions are set at `0750` after the umask subtracts `0027` from the full set of open permissions, `0777`.

Similarly, a new file begins as `0666` if you were to set umask to `0000`. But because umask is set by default to `0027`, a new file's permissions are set to `0640`. 

So be aware of the default permissions on the directories and files that you create. Some system services and applications might require permissions other than the default. The `systemd` network service, for example, requires user-defined configuration files to be set to `644`, not the default of `640`. Thus, after you create a network configuration file with a `.network` extension, you must run the `chmod` command to set the new file's mode bits to `644`. For example: 

    chmod 644 10-static-en.network 

For more information on permissions, see the man pages for `stat`, `umask`, and `acl`.