#	Editable variables follow
BUILDDIR=/mnt/photonroot			# where to build toolchain
MKFLAGS="-j $(getconf _NPROCESSORS_ONLN)"	# how many processors on this host
LOGFILE="$(date +%Y-%m-%d).log"			# this is where we log the build to 
BUILD_TGT=$(uname -m)-photon-linux-gnu

