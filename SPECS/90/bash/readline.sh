# Setup the INPUTRC environment variable.
if [ -z "$INPUTRC" -a ! -f "$HOME/.inputrc" ]; then
  INPUTRC=/etc/inputrc
fi
export INPUTRC
