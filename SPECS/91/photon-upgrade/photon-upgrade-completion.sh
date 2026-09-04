# bash completion for photon-upgrade.sh

_photon_upgrade_complete() {
  local cur prev opts
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"

  opts="--help --repos= --upgrade-os --to-ver= --assume-yes --skip-update --install-all --rm-pkgs-pre= --rm-pkgs-post= --precheck-only"

  COMPREPLY=($(compgen -W "${opts}" -- "${cur}"))
}

complete -F _photon_upgrade_complete photon-upgrade.sh
