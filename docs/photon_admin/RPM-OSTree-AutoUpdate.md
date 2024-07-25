# Automatic Updates

Automatic updates are disabled by default. 

To verify this, run the status command.

```
root@photon-host-def [ ~ ]# rpm-ostree status
State: idle
AutomaticUpdates: disabled
Deployments:
* ostree://photon-1:photon/3.0/x86_64/minimal
                   Version: 3.0_minimal.1 (2019-09-16T09:51:33Z)
                BaseCommit: 28dc49ecb4604c0bc349e4445adc659491a1874c01198e6253a261f4d59708b7
           LayeredPackages: createrepo_c rpm wget

```

## Enable Automatic Updates

1. Run the following command:

```
$ systemctl restart rpm-ostreed
```

1. To enable automatic background updates, edit the `/etc/rpm-ostreed.conf`, and include the below lines in the `Daemon` section:

    ```
    [Daemon]
    AutomaticUpdatePolicy=stage
    #IdleExitTimeout=60
    ```

1. Run the following commands:

    ```
    $ systemctl reload rpm-ostreed
    $ systemctl enable rpm-ostree-automatic.timer --now  
    $ systemctl restart rpm-ostree-automatic
    ```

1. Verify that the automatic update feature has been enabled:

    ```
    $ rpm-ostree status -v 
          State: idle

          AutomaticUpdates: stage; rpm-ostreed-automatic.timer: last run 16min ago
    ```

1. On the server machine, perform another commit on the base tree. 

Automatic updates are now enabled and will automatically update the host system.

