die() {	local _red="\\033[1;31m"
	local _normal="\\033[0;39m"
	[ -n "$*" ] && printf "${_red}$*${_normal}\n"
	exit 1
}
msg() {
	printf "%s\n" "${1}"
}
msg_line() {
	printf "%s" "${1}"
}
msg_failure() {
	local _red="\\033[1;31m"
	local _normal="\\033[0;39m"
	printf "${_red}%s${_normal}\n" "FAILURE"
	exit 2
}
msg_success() {
	local _green="\\033[1;32m"
	local _normal="\\033[0;39m"
	printf "${_green}%s${_normal}\n" "SUCCESS"
	return 0
}
build() {
	# $1 = message 
	# $2 = command
	# $3 = log file
	local _start=$(date +%s)
	local _msg="${1}"
	local _cmd="${2}"
	local _logfile="${3}"
	if [ "/dev/null" == "${_logfile}" ]; then
		msg_line "${_msg}: "
		eval ${_cmd} >> ${_logfile} 2>&1 && msg_success || msg_failure 
	else
		msg_line "${_msg}: "
		printf "\n%s\n\n" "###       ${_msg}       ###" >> ${_logfile} 2>&1
		eval ${_cmd} >> ${_logfile} 2>&1 && msg_success || msg_failure 
		fi

	local _end=$(date +%s)
	local _elapsed=$((_end-_start))
	echo "Elapsed time: ${_elapsed} seconds" >> ${_logfile} 2>&1
	return 0
}
unpack() {	# $1 = directory
	# $2 = source package name I'll find the suffix thank you
	local _dir=${1%%/BUILD*} # remove BUILD from path
	local i=${2}
	local p=$(echo ${_dir}/SOURCES/${i}*.tar.*)
	[ -e ${p} ] || p=$(echo ${_dir}/SOURCES/${i}*.gz)
	msg_line "	Unpacking: ${i}: "
	[ -e ${p} ] || die " File not found: FAILURE"
	tar xf ${p} && msg_success || msg_failure
	return 0
}