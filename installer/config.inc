#	Editable variables follow
BUILDROOT=/mnt/photon-root	# where to build photon
#	Edit partition and mnt_point for the correct values.
#	Failing to do so will cause you grief as in overwriting your host system.
#	You have been warned!
LOGFILE="$(date +%Y-%m-%d).log"	#	this is where we log the build to 
HDD=/dev/sdb			# 	Hard drive to prepare for photon mount.
PARTITION=/dev/sdb2			#	Partition to create filesystem for photon build
SWAPPARTITION=/dev/sdb3			# 	Partition where swap partition is created

#Check if the BUILDROOT parameter is passed
if [[ $# > 1 ]]; then
		if [[ "$1" =~ ^(-w|--working-directory)$ ]]; then
				BUILDROOT="$2"
				shift 2
		fi
fi
