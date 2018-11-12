# Changing the Locale 

You can change the locale if the default locale, shown below by running the `localectl` command, fails to fulfill your requirements: 

    localectl
    System Locale: LANG=en_US.UTF-8
       VC Keymap: n/a
      X11 Layout: n/a

To change the locale, choose the languages that you want from `/usr/share/locale/locale.alias`, add them to `/etc/locale-gen.conf`, and then regenerate the locale list by running the following command as root: 

    locale-gen.sh

Finally, run the following command to set the new locale, replacing the example (`en_US.UTF-8`) with the locale that you want: 

    localectl set-locale LANG="en_US.UTF-8" LC_CTYPE="en_US.UTF-8"