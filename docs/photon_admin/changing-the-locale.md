# Changing the Locale 

You can change the locale if the default locale does not meet your requirements. 

To find the locale, run the the `localectl` command:  

    localectl
    System Locale: LANG=en_US.UTF-8
       VC Keymap: n/a
      X11 Layout: n/a

To change the locale, choose the languages that you want from `/usr/share/locale/locale.alias`, add them to `/etc/locale-gen.conf`, and then regenerate the locale list by running the following command as root: 

    locale-gen.sh

Finally, run the following command to set the new locale, replacing the example (`en_US.UTF-8`) with the locale that you require: 

    localectl set-locale LANG="de_CH.UTF-8" LC_CTYPE="de_CH.UTF-8"

# Changing the keyboard layout

See which keymaps are currently available on your system:

    localectl list-keymaps
    
If the response to that command is the all-too-common `Couldn't find any console keymaps`, install the key tables files and utilities:

    tdnf install kbd
    
You should now be able to find a keymap matching your keyboard. As an example, here I'm searching for the German keyboard layout (so I'm expecting something with `de` in the name) used in Switzerland:

    localectl list-keymaps | grep de
    
```console
    ...
    de-latin1
    de-latin1-nodeadkeys
    de-mobii
    de_CH-latin1
    de_alt_UTF-8
    ...
```

`de_CH-latin1` seems to be what we're looking for, so change your current layout to that keymap:

    localectl set-keymap de_CH-latin1
    
and confirm that the change has been made:

    localectl
    System Locale: LANG=de_CH.UTF-8
       VC Keymap: de_CH-latin1
      X11 Layout: n/a
