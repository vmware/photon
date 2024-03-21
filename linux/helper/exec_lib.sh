#!/bin/bash
#
# Execution helper library
#

CURDIR=$(basename $PWD)

if [ x"$CURDIR" = x"tests" ]
then
	_LIB_EXEC="../acvp-parser"
else
	_LIB_EXEC="./acvp-parser"
fi

_LIB_IUT_USER="$1"
_LIB_IUT="testvectors"
_LIB_IUT_PROD="testvectors-production"
_LIB_REQ="testvector-request.json"
_LIB_RESP="testvector-response.json"
_LIB_EXPECTED="testvector-expected.json"
#_LIB_OE="operational_environment.json"

failures=0
local_failures=0

# EBITS can be set as an environment variable to remove 32 bits
EBITS=${EBITS:-"64 32"}
ABITS=()
for B in ${EBITS}; do
    ABITS+=("_${B}_bit___ ")
done
EXEC_TYPES=${ABITS[@]}

EXEC_TYPES__64_bit___=""
EXEC_TYPES__32_bit___="CFLAGS=-m32 LDFLAGS=-m32"


color()
{
	bg=0
	echo -ne "\033[0m"
	while [[ $# -gt 0 ]]; do
		code=0
		case $1 in
			black) code=30 ;;
			red) code=31 ;;
			green) code=32 ;;
			yellow) code=33 ;;
			blue) code=34 ;;
			magenta) code=35 ;;
			cyan) code=36 ;;
			white) code=37 ;;
			background|bg) bg=10 ;;
			foreground|fg) bg=0 ;;
			reset|off|default) code=0 ;;
			bold|bright) code=1 ;;
		esac
		[[ $code == 0 ]] || echo -ne "\033[$(printf "%02d" $((code+bg)))m"
		shift
	done
}

pass_name="GENERATED"
echo_pass()
{
 	echo $(color "green")[$pass_name]$(color off) $@
}

echo_fail()
{
	echo $(color "red")[FAILED]$(color off) $@
	failures=$(($failures+1))
	local_failures=$(($local_failures+1))
}

echo_deact()
{
	echo $(color "yellow")[DEACTIVATED]$(color off) $@
}

echo_warn()
{
	echo $(color "blue")[WARNING]$(color off) $@
}

clean_tool()
{
	if [ x"$CURDIR" = x"tests" ]
	then
		make -C ../ clean
	else
		make clean
	fi
	ret=$?
	if [ $ret -ne 0 ]
	then
		echo "Cleaning failed"
		exit $ret
	fi
}

build_tool()
{
	local target=$1

	if [ -z "$target" ]
	then
		echo "No module name provided, skipping"
		return
	fi

	clean_tool

	if [ x"$CURDIR" = x"tests" ]
	then
		make -C ../ -s $target
	else
		make -s $target
	fi
	ret=$?
	if [ $ret -ne 0 ]
	then
		echo "Build failed"
		exit $ret
	fi
}

get_proc_family() {
	local file=$1

	if [ -z "$file" ]
	then
		return
	fi

	if [ ! -f $file ]
	then
		return
	fi

	family=$(grep family $file | cut -d ":" -f 2 | cut -d"\"" -f 2)

	echo $family
}

# List of JSON keyword:value pairs to search for JSON test vectors known
# to be no known answer test and thus are unfit for regression testing
REGRESSION_VECTOR_SKIP="
	algorithm:KTS-IFC
"

# List of JSON search_keyword:search_value:replace_keyword:replace_value set to
# search for JSON vectors know to be no known answer tests but can be turned
# into known answer tests for regression testing
REGRESSION_VECTOR_REPLACE="
	mode:keyGen:mode:keyVer
	mode:sigGen:mode:sigVer
	mode:pqgGen:mode:pqgVer
	ivGen:internal:ivGen:external
	algorithm:KAS-FFC:testType:VAL
	algorithm:KAS-ECC:testType:VAL
	algorithm:KAS-ECC-SSC:testType:VAL
	kdfMode:counter:algorithm:KDF
	kdfMode:feedback:algorithm:KDF
	kdfMode:double:algorithm:KDF
"

#
# Execute testing
# $1 module name to be executed
# $2 if present, apply a regression test
# $3 if present, requested processor family
# $4 if present, search criteria for regression test (commonly an array of
#    vsIds)
exec_module()
{
	local module=$1
	shift
	local regression=$1
	shift
	local req_proc=$1
	shift
	local vsid=${@}

	local testvalidation=""
	local vendordir
	local i
	local j
	local lib_iut_dir=${_LIB_IUT}

	# If the script name contains "_regression" we switch into regression
	# mode transparently
	if $(echo $0 | grep -q "_regression")
	then
	       regression="regression"
	       pass_name="VALIDATED"
	fi

	# If the script name contains "_validation" we switch into validation
	# mode transparently
	if $(echo $0 | grep -q "_validation")
       	then
	       testvalidation="validation"
	       regression="regression"
	       pass_name="VALIDATED"
	fi

	if [ -z "$module" ]
	then
		echo "No module name provided, skipping"
		return
	fi

	if [ ! -z "${_LIB_IUT_USER}" ]
	then
		lib_iut_dir=${_LIB_IUT_USER}
	elif [ ! -d "${_LIB_IUT}" ]
	then
		if [ -d "${_LIB_IUT_PROD}" ]
		then
			lib_iut_dir=${_LIB_IUT_PROD}
		else
			echo "Test vector base directory ${_LUB_IUT} / ${_LIB_IUT_PROD} not found"
			return
		fi
	fi

	# Iterate over all directories
	for vendordir in ${lib_iut_dir}/*
	do
		if [ ! -d "$vendordir" ]
		then
			continue
		fi

		local iutdir="$vendordir/$module"

		if [ ! -d "${iutdir}" ]
		then
			echo "No test vectors found for module $iutdir"
			continue
		fi

		# Iterate over all request files
		for i in $(find ${iutdir} -name ${_LIB_REQ})
		do
			local dir=$(dirname $i)
			local vsid_dir=$(basename $dir)
			local testid_dir=$(dirname $dir)
			local found=0
			local respfile=$_LIB_RESP

			for j in $vsid
			do
				if [ "$j" = "$vsid_dir" ]
				then
					found=1
					break
				fi
			done

			# If no search vsids are given, execute testing
			if [ -z "$vsid" ]
			then
				found=1
			fi

			if [ $found -eq 0  ]
			then
				echo_deact "Skipping vsId $vsid_dir as it does not match search criteria"
				continue
			fi

#			if [ -n "$req_proc" -a x"$req_proc" != x"X" ]
#			then
#				local proc_family=$(get_proc_family "${testid_dir}/${_LIB_OE}")
#
#				if [ x"$req_proc" != x"$proc_family" ]
#				then
#					echo_deact "Skipping vsId $vsid_dir as requested processor type does not match defined processor"
#					continue
#				fi
#			fi

			# Sanity checking - no regular testing if response file exists
			if [ -f $dir/$_LIB_RESP -a -z "$regression" ]
			then
				echo_deact "Response file exists - skipping $dir"
				continue
			fi

			# Sanity checking - no regular testing if response file exists
			if [ -f $dir/$_LIB_RESP -a x"$regression" = x"X" ]
			then
				echo_deact "Response file exists - skipping $dir"
				continue
			fi

			# Regression testing: if no test response is there, use expected vector
			if [ ! -f $dir/$_LIB_RESP -a -n "$regression" -a x"$regression" != x"X" ]
			then
				if [ -f $dir/$_LIB_EXPECTED ]
				then
					respfile=$_LIB_EXPECTED
				else
					echo_deact "Response file missing but regression testing requested - skipping $dir"
					continue
				fi
			fi

			# Sanity checking: validation requires response and expected data
			if [ x"$testvalidation" != x ]
			then
				if [ ! -f $dir/$_LIB_RESP ]
				then
					echo_deact "Response file missing but validation testing requested - skipping $dir"
					continue
				fi

				if [ ! -f $dir/$_LIB_EXPECTED ]
				then
					echo_deact "Expected file missing but validation testing requested - skipping $dir"
					continue
				fi
			fi

			# Sanity checking: we need the request data
			if [ ! -f $dir/$_LIB_REQ ]
			then
				echo_deact "Request file missing - skipping $dir"
				continue
			fi

			# Sanity checking: does the request file contain valid data?
			if (grep -q status $dir/$_LIB_REQ)
			then
				echo_deact "Request contains status information - skipping $dir"
				continue
			fi

			if [ -z "$regression" -o x"$regression" = x"X" ]
			then
				# Do real testing

				$_LIB_EXEC $dir/$_LIB_REQ $dir/$_LIB_RESP
				local ret=$?
				if [ $ret -eq 95 ]	#EOPNOTSUPP
				then
					echo_deact "Operation not supported for $dir"
				elif [ $ret -ne 0 ]
				then
					echo_fail "Execution for $dir failed (error code $ret) - executed command:"
					echo "$_LIB_EXEC $dir/$_LIB_REQ $dir/$_LIB_RESP"
				else
					echo_pass "Processed $dir"
				fi
			else
				# Do regression testing / validation

				local testname=""

				# Skip vectors known to generate random numbers and
				# thus will not work as KAT
				local skip=0
				for j in ${REGRESSION_VECTOR_SKIP}
				do
					keyword=${j%%:*}
					value=${j##*:}

					if [ -z "$keyword" -o -z "$value" ]
					then
						echo "Empty keyword ($keyword) or value ($value)"
						continue
					fi

					if (grep -i \"$keyword\" $dir/$_LIB_REQ | grep -iq $value > /dev/null)
					then
						echo_deact "Key $keyword and value $value found in $dir/$_LIB_REQ"
						skip=1
						break
					fi
				done

				# Invoke replace operation for the following
				# vectors
				local replaceop=""
				for j in $REGRESSION_VECTOR_REPLACE
				do
					local OLDIFS=$IFS
					IFS=":"

					local tokens=( $j )
					keyword=${tokens[0]}
					value=${tokens[1]}
					r_keyword=${tokens[2]}
					replace=${tokens[3]}

					IFS=$OLDIFS

					if [ -z "$keyword" -o -z "$value" -o -z "$r_keyword" -o -z "$replace" ]
					then
						echo "Empty keyword ($keyword) or value ($value) or replace keyword ($r_keyword) or replace ($replace)"
						continue
					fi

					if (grep -i \"$keyword\" $dir/$_LIB_REQ | grep -iq $value > /dev/null)
					then
						replaceop="--replace $r_keyword:$replace"
						break
					fi
				done

				if [ $skip -ne 0 ]
				then
					continue
				fi

				if [ -n "$replaceop" ]
				then
					# Perform regression testing
					testname="Regression testing of no-known-answer test"
					$_LIB_EXEC $replaceop $dir/$_LIB_REQ $dir/$respfile
				elif [ -x"$testvalidation" != x ]
				then
					# Perform regression testing
					testname="Regression testing"
					$_LIB_EXEC -r $dir/$_LIB_REQ $dir/$respfile
				else
					# Perform test matching
					testname="Vector validation"
					$_LIB_EXEC -e $dir/$_LIB_RESP $dir/$_LIB_EXPECTED
				fi

				local ret=$?
				if [ $ret -eq 95 ]	#EOPNOTSUPP
				then
					echo_deact "Operation not supported for $dir"
				elif [ $ret -ne 0 ]
				then
					echo_fail "${testname} for $dir"
				else
					echo_pass "${testname} for $dir"
				fi
			fi
		done
	done

	if [ -n "$regression" -a x"$regression" != x"X" ]
	then
		echo "=========================================================="
		if [ $local_failures -gt 0 ]
		then
			echo $(color "red")[FAILED]$(color off) $@ "$local_failures failures for module $module"

		else
			echo_pass "no failures for module $module"
		fi
	fi

	local_failures=0
}

#
# Execute testing
# $1 module name to be executed
# $2 if present, search criteria for regression test (commonly an array of
#    vsIds)
regression_test()
{
	local module=$1
	shift

	exec_module "$module" "regression" ${@}
}

cleanup()
{
	echo > /dev/null
	# Do not call make clean here
#	clean_tool
}

trap "cleanup; exit $failures" 0 1 2 3 15
