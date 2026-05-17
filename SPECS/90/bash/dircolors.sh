# Setup for /bin/ls and /bin/grep to support color, the alias is in /etc/bashrc.
if [ -f "/etc/dircolors" ]; then
  eval $(dircolors -b /etc/dircolors)

  if [ -f "$HOME/.dircolors" ]; then
    eval $(dircolors -b $HOME/.dircolors)
  fi
fi
alias ls='ls --color=auto'
grep --help | grep color  >/dev/null 2>&1
if [ $? -eq 0 ]; then
  alias grep='grep --color=auto'
fi
