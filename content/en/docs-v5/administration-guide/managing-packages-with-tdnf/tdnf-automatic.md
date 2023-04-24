---
title:  tdnf-automatic
weight: 6
---

`tdnf-automatic` is an alternative Command Line Interface (CLI) to `tdnf upgrade/tdnf update` with specific features so that it is suitable to be executed automatically and regularly from `systemd` timers, cron jobs, and so on.

The operation of the tool is usually controlled by the configuration file or the function-specific timer units. The command only accepts a single optional argument pointing to the config file, and some control arguments intended for use by the services that back the timer units. If no configuration file is passed from the command line,then  `/etc/tdnf/automatic.conf` is used.

The tool synchronizes package metadata as needed and then checks for the updates available for the given system and then either exits or shows available updates or downloads and installs the packages.

The outcome of the operation is then reported through `stdio`.

The `systemd` timer unit `tdnf-automatic.timer` behaves as the configuration file specifies whether to download and apply updates. Some other timer units are provided which override the configuration file with some standard behaviors:

    * tdnf-automatic-notifyonly

    * tdnf-automatic-install

Irrespective of the configuration file settings, the first only notifies of available updates. The second one downloads and installs the updates.

### Run tdnf-automatic ###

You can select one that most closely fits your needs, customize /etc/tdnf/automatic.conf for any specific behaviors, and enable the timer unit.

For example: systemctl enable --now tdnf-automatic-notifyonly.timer

### Configuration file format ###

The configuration file is separated into two sections. This basically gives info on what can be put in /etc/tdnf/automatic.conf. 'automatic.conf' is a configuration INI file.

### Format ###

    tdnf-automatic help:
    
    tdnf-automatic [{-c|--conf config-file}(optional)] [{-i|--install}] [{-n|--notify}] [{-h|--help}] [{-v|--version}]
    
    
    
    -c, --conftdnf-automatic configuration file (Optional argument)
    
    -i, --installOverride automatic.conf apply_updates and install updates
    
    -n, --notifyShow available updates
    
    -h, --helpShow this help message
    
    -v, --versionShow tdnf-automatic version information

### Commands ###

To set the mode of the operation of the program:



- `apply_updates (boolean, default: no)`
Whether packages comprising the available updates should be applied by tdnf-automatic.timer, i.e. installed via RPM. Note that the other timer units override this setting.



- `show_updates (boolean, default: yes)`
To just receive updates use tdnf-automatic-notifyonly.timer



- `network_online_timeout (time in seconds, default: 60)`
Maximum time tdnf-automatic will wait until the system is online. 0 means that network availability detection will be skipped.



- `random_sleep (time in seconds, default: 0)`
Maximum random delay before downloading. Note that, by default, the systemd timers also apply a random delay of up to 1 hour.



- `upgrade_type (either one of all or security. default: `all`)`
Looks at the kind of upgrades. `all` signals looking for all available updates. `security` indicates only those with an issued security advisory.



- `tdnf_conf (string, default: /etc/tdnf/tdnf.conf)`
Configurations to override default tdnf configuration. 

 
### Reports ###

To select how the results should be reported:



- emit_to_stdio (boolean, default: yes)
Report the results through stdio. If no, no report will be shown.



- system_name (string, default: hostname of the given system)
How the system is called in the reports.



- emit_to_file  (string, absolute path of file)
If we want to capture the logs in a file
