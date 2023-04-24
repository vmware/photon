---
title:  Automatic Updates
weight: 8
---

Automatic updates are disabled by default. 

To verify this, run the status command.

    root@photon-7c2d910d79e9 [ ~ ]# rpm-ostree status 
    State: idle
    Deployments:
    ● ostree://photon:photon/4.0/x86_64/minimal
       Version: 4.0_minimal (2021-02-20T07:15:43Z)
    Commit: 965c1abeb048e1a8ff77e9cd34ffccc5e3356176cda3332b4ff0e7a6c66b661f
    


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

