---
title: Setting grub password in PhotonOS
weight: 2
---

GRUB 2 supports both plain-text and encrypted passwords in the GRUB 2 template files.

## Prerequisites

To make use of grub password feature in PhotonOS we need to `grub2` package.
```console
tdnf install -y grub2
```

`
Warning:
If you do not use the correct format for the menu, or modify the configuration in an incorrect way, you might be unable to boot your system.
`

## Procedure

To specify a user, who can access the grub menu edit access:

1. Create file `01_users` under `/etc/grub.d/` directory.
2. Follow the below template to enable user access to grub edit menu(which will be the content of /etc/grub.d/01_users file)

```
cat <<EOF
set superusers="<user-name>"
password <user-name> <plain-text-password>
EOF
```

```
Note:
You can also use /etc/grub.d/40_custom for setting grub password, the template if you use /etc/grub.d/40_custom is:

set superusers="<user-name>"
password <user-name> <plain-text-password>

Observe there is no cat <<EOF ... EOF here.
It's a good idea to make a backup of 40_custom file after modification, as it might get overwritten if you update grub version.
Change permission of password files using `chmod 755 /etc/grub.d/40_custom /etc/grub.d/01_users`.
```

Example: To give grub menu edit access to user john
```
cat <<EOF
set superusers="john"
password john johnspassword
EOF
```

3. To allow more users to access the menu entries, add additional lines per user at the end of the /etc/grub.d/01_users file.

Example:
```
cat <<EOF
set superusers="john jane"
password john johnspassword
password jane janespassword
EOF
```

4. Now run `grub2-mkconfig -o /boot/grub2/grub.cfg` for the changes to get applied and make sure there are no errors.

5. Reboot. You should see a password prompt to see grub boot menu.
Give the corresponding user name and password you used before to continue booting.


Note:
Now once you do this, grub  will ask for a supervisor password every time you want to boot any menu item.
So you need to add `--unrestricted` to all `menuentries` that any user shall be able to boot.
You can edit the `linux_entry ()` function in `/etc/grub/10_linux` file so that the 'echo "menuentry ..."' lines include --unrestricted by default:

`
    [...]

    echo "menuentry '$(echo "$title" | grub_quote)' --unrestricted ${CLASS} \$menuentry_id_option 'gnulinux-$version-$type-$boot_device_id' {" | sed "s/^/$submenu_indentation/"

    else

    echo "menuentry '$(echo "$os" | grub_quote)' --unrestricted ${CLASS} \$menuentry_id_option 'gnulinux-simple-$boot_device_id' {" | sed "s/^/$submenu_indentation/"

    [...]
`

This is highly recommended. In case if you forget grub password, your system becomes unusable and rescuing from this point is real hard.
Also it's a good idea to keep a backup of `/etc/grub/10_linux` as well as it might get overwritten upon upgrading grub version.

## Password Encryption

By default, passwords are saved in plain text in GRUB 2 scripts.
Although the files cannot be accessed on boot without the correct password, security can be improved by encrypting the password using `grub2-mkpasswd-pbkdf2` command.

Steps:
1. To generate an encrypted password, run the following command on the as root.
```console
grub2-mkpasswd-pbkdf2
```

2. Enter the desired password when prompted and repeat it. The command then outputs your password in an encrypted form.

3. Copy the hash, and paste it in the template file where you configured the users, that is, either in `/etc/grub.d/01_users or /etc/grub.d/40_custom`.

The following format applies for the `01_users` file: (example only, your hash value may differ)
```
cat <<EOF
set superusers="john"
password_pbkdf2 john grub.pbkdf2.sha512.10000.19074739ED80F115963D984BDCB35AA671C24325755377C3E9B014D862DA6ACC77BC110EED41822800A87FD3700C037320E51E9326188D53247EC0722DDF15FC.C56EC0738911AD86CEA55546139FEBC366A393DF9785A8F44D3E51BF09DB980BAFEF85281CBBC56778D8B19DC94833EA8342F7D73E3A1AA30B205091F1015A85
EOF
```

The following format applies for the `40_custom` file:
```
set superusers="john"
password_pbkdf2 john grub.pbkdf2.sha512.10000.19074739ED80F115963D984BDCB35AA671C24325755377C3E9B014D862DA6ACC77BC110EED41822800A87FD3700C037320E51E9326188D53247EC0722DDF15FC.C56EC0738911AD86CEA55546139FEBC366A393DF9785A8F44D3E51BF09DB980BAFEF85281CBBC56778D8B19DC94833EA8342F7D73E3A1AA30B205091F1015A85
```

4. Run `grub2-mkconfig -o /boot/grub2/grub.cfg` as root.

Note:

- If you want to restrict only certain partitions in the system, you can specify the
menu entries that should be password-protected in the `/etc/grub.d/40_custom` file in a similar fashion to the following:
```
menuentry 'Sample entry name'  {
  set root=(hd0,gpt3)
  ... and so on
}
```

For example if this is password configuration:
```
cat <<EOF
set superusers="john"
password john johnspassword
password jane janespassword
EOF
```

When the users and passwords are set up, specify the menu entries that should be password-protected
in the `/etc/grub.d/40_custom` file in a similar fashion to the following:

```
menuentry 'OS-1' --unrestricted {
  set root=(hd0,gpt1)
  ...
}

menuentry 'OS-2' --users jane {
  set root=(hd0,gpt2)
  ...
}

menuentry 'OS-3' {
  set root=(hd0,gpt3)
  ...
}
```

In the above example:
    - john is the superuser and can therefore boot any menu entry, use the GRUB 2 command line, and edit items of the GRUB 2 menu during boot. In this case, john can access OS-1, OS-2 and OS-3. Note that only john can access OS-3 because neither the `--users` nor `--unrestricted` options have been used.
    - User jane can boot OS-2 since she was granted the permission in the configuration.
    - Anyone can boot OS1, because of the `--unrestricted` option, but only john can edit the menu entry as a superuser has been defined. When a superuser is defined then all records are protected against unauthorized changes and all records are protected for booting if they do not have the `--unrestricted` parameter.

- If you do not specify a user for a menu entry, or make use of the `--unrestricted` option, then only the
superuser will have access to the system.
