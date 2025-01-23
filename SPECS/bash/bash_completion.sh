# check for interactive bash and only bash
if [ -n "$BASH_VERSION" -a -n "$PS1" ]; then

  # enable bash completion in interactive shells
  if ! shopt -oq posix; then
    if [ -f /usr/share/bash-completion/bash_completion ]; then
      . /usr/share/bash-completion/bash_completion
    fi
  fi
fi
