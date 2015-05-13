fail() {	
    local _red="\\033[1;31m"
	local _normal="\\033[0;39m"
	[ -n "$*" ] && printf "${_red}$*${_normal}\n"
	exit 1
}
print_message() {
     printf "%s" "${1}"
}
print_failed_in_red() {
     local _red="\\033[1;31m"
     local _normal="\\033[0;39m"
     printf "${_red}%s${_normal}\n" "FAILED"
     exit 2
}
print_succeeded_in_green() {
     local _green="\\033[1;32m"
     local _normal="\\033[0;39m"
     printf "${_green}%s${_normal}\n" "SUCCEEDED"
     return 0
}

run_command() {
	# $1 = message 
	# $2 = command
	# $3 = log file
	local _msg="${1}"
	local _cmd="${2}"
	local _logfile="${3}"
	if [ "/dev/null" == "${_logfile}" ]; then
		print_message "${_msg}: "
		eval ${_cmd} >> ${_logfile} 2>&1 && print_succeeded_in_green || print_failed_in_red
	else
		print_message "${_msg}: "
		printf "\n%s\ncmd: %s\n\n" "###       ${_msg}       ###" "${_cmd}" >> ${_logfile} 2>&1
		eval ${_cmd} >> ${_logfile} 2>&1 && print_succeeded_in_green || print_failed_in_red
		fi
	return 0
}
