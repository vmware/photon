if [ -d /usr/local/lib/pkgconfig ]; then
  pathappend /usr/local/lib/pkgconfig PKG_CONFIG_PATH
fi
if [ -d /usr/local/bin ]; then
  pathprepend /usr/local/bin
fi
if [ -d /usr/local/sbin -a $EUID -eq 0 ]; then
  pathprepend /usr/local/sbin
fi
