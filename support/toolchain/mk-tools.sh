#!/bin/bash
#################################################
#	Title:	mk-tools			#
#        Date:	2015-01-14			#
#     Version:	1.0				#
#      Author:	dthaluru@vmware.com     	#
#     Options:					#
#################################################
set -o errexit		# exit if error...insurance ;)
set -o nounset		# exit if variable not initalized
set +h			# disable hashall
source config.inc
source function.inc
KERNEL_VERSION=$(head -n 1 kernel-version.txt)
PRGNAME=${0##*/}	# script name minus the path

if [ $# -lt 3 ]; then
   echo "Usage: $PRGNAME <source_path> <log_path> <dest path>"
   exit 1
fi

SOURCE_PATH=$1
SPECS_PATH=$2
LOG_PATH=$3
DESTDIR=$4
LOGFILE=${LOG_PATH}/"${PRGNAME}-${LOGFILE}"	#	set log file name
[ ${EUID} -eq 0 ]	|| die "${PRGNAME}: Need to be root user: FAILURE"
[ -z ${BUILDDIR} ]		&& die "${PRGNAME}: Build path: not set"
[ -z ${BUILD_TGT} ]     && die "${PRGNAME}: Environment not set: FAILURE"
> ${LOGFILE}		#	clear/initialize logfile

[ -d ${BUILDDIR} ]	        || build "Creating directory: ${BUILDDIR}" "install -vdm 755 ${BUILDDIR}" "${LOGFILE}"
[ -d ${BUILDDIR} ]		&& build "Clean directory: ${BUILDDIR}" "rm -rf ${BUILDDIR}/* " "${LOGFILE}"
[ -d ${BUILDDIR} ]		|| build "Setting directory permissions: ${BUILDDIR}" "chmod 755 ${BUILDDIR}" "${LOGFILE}"
[ -d /tools ]			&& build "Removing directory: /tools" "rm -rf /tools " "${LOGFILE}"
[ -h /tools ]			&& build "Removing existing symlink: /tools" "rm /tools " "${LOGFILE}"
[ -d ${BUILDDIR}/tools ]	|| build "Creating directory: ${BUILDDIR}/tools" "install -vdm 755 ${BUILDDIR}/tools" "${LOGFILE}"
build "Symlink: ${BUILDDIR}/tools to /tools" "ln -vs ${BUILDDIR}/tools /" "${LOGFILE}"

PATH=/tools/bin:/bin:/usr/bin
msg "Install build system: "
build "	Installing directories" "install -vdm 755 ${BUILDDIR}/{BUILD,SOURCES,PATCHES,LOGS,SCRIPTS}" "${LOGFILE}"
build "	Copying files" "cp -var ${SOURCE_PATH} ${BUILDDIR}/" "${LOGFILE}"
build "	Copying files" "find -L ${SPECS_PATH} -name ""*.patch"" -exec cp ""{}"" ${BUILDDIR}/PATCHES \;" "${LOGFILE}"
build "	Copying files" "cp -var SCRIPTS ${BUILDDIR}/" "${LOGFILE}"
cd ${BUILDDIR}

build-binutils1() {
	local	_pkgname="binutils"
	local	_pkgver="2.25"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Create work directory" "install -vdm 755 ../build" ${_logfile}
	build "	Change directory: ../build" "pushd ../build" ${_logfile}
	build "	Configure" "../${_pkgname}-${_pkgver}/configure --prefix=/tools --with-sysroot=${BUILDDIR} --with-lib-path=/tools/lib --target=${BUILD_TGT} --disable-nls --disable-werror" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	[ "x86_64" == $(uname -m) ] && build "		Create symlink for amd64" "install -vdm 755 /tools/lib;ln -vfs lib /tools/lib64" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}

build-gcc1() {
	local	_pkgname="gcc"
	local	_pkgver="4.8.2"
	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	local	_pwd=${PWD}/BUILD
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	build "	Create work directory" "install -vdm 755 build" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	unpack "${PWD}" "mpfr-3.1.2"
	unpack "${PWD}" "gmp-5.1.3"
	unpack "${PWD}" "mpc-1.0.2"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Symlinking gmp" " ln -vs ../gmp-5.1.3  gmp" ${_logfile}
	build "	Symlinking mpc" " ln -vs ../mpc-1.0.2  mpc" ${_logfile}
	build "	Symlinking mpfr" "ln -vs ../mpfr-3.1.2 mpfr" ${_logfile}
	build "	Fixing headers" 'for file in $(find gcc/config -name linux64.h -o -name linux.h -o -name sysv4.h); do cp -uv $file{,.orig};sed -e "s@/lib\(64\)\?\(32\)\?/ld@/tools&@g" -e "s@/usr@/tools@g" $file.orig > $file;printf "\n%s\n%s\n%s\n%s\n\n" "#undef STANDARD_STARTFILE_PREFIX_1" "#undef STANDARD_STARTFILE_PREFIX_2" "#define STANDARD_STARTFILE_PREFIX_1 \"/tools/lib/\"" "#define STANDARD_STARTFILE_PREFIX_2 \"\" ">> $file;touch $file.orig;done' ${_logfile}
	build "	sed -i '/k prot/agcc_cv_libc_provides_ssp=yes' gcc/configure" "sed -i '/k prot/agcc_cv_libc_provides_ssp=yes' gcc/configure" ${_logfile}
	build "	Change directory: ../build" "pushd ../build" ${_logfile}
	build "	Configure" "../${_pkgname}-${_pkgver}/configure --target=${BUILD_TGT} --prefix=/tools --with-sysroot=${BUILDDIR} --with-newlib --without-headers --with-local-prefix=/tools --with-native-system-header-dir=/tools/include --disable-nls --disable-shared --disable-multilib --disable-decimal-float --disable-threads --disable-libatomic --disable-libgomp --disable-libitm --disable-libmudflap --disable-libquadmath --disable-libsanitizer --disable-libssp --disable-libstdc++-v3 --enable-languages=c,c++ --with-mpfr-include=${_pwd}/${_pkgname}-${_pkgver}/mpfr/src --with-mpfr-lib=${_pwd}/build/mpfr/src/.libs" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Symlinking libgcc_eh.a" 'ln -vs libgcc.a $(${BUILD_TGT}-gcc -print-libgcc-file-name | sed "s/libgcc/&_eh/")' ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-linux-api-headers() {
	local	_pkgname="linux"
	local	_pkgver=${KERNEL_VERSION}
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	make mrproper" "make mrproper" ${_logfile}
	build "	make headers_check" "make headers_check" ${_logfile}
	build "	make INSTALL_HDR_PATH=dest headers_install" "make INSTALL_HDR_PATH=dest headers_install" ${_logfile}
	build "	cp -rv dest/include/* /tools/include" "cp -rv dest/include/* /tools/include" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-glibc() {
	local	_pkgname="glibc"
	local	_pkgver="2.21"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	[ ! -r /usr/include/rpc/types.h ] && build "	Copying rpc headers to host system" \
		"su -c 'mkdir -pv /usr/include/rpc' && su -c 'cp -v sunrpc/rpc/*.h /usr/include/rpc'"  ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Create work directory" "install -vdm 755 ../build" ${_logfile}
	build "	Change directory: ../build" "pushd ../build" ${_logfile}
	build "	Configure" "../${_pkgname}-${_pkgver}/configure --prefix=/tools --host=${BUILD_TGT} --build=$(../${_pkgname}-${_pkgver}/scripts/config.guess) --disable-profile --enable-kernel=2.6.32 --with-headers=/tools/include libc_cv_forced_unwind=yes libc_cv_ctors_header=yes libc_cv_c_cleanup=yes" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	msg_line "       Checking glibc for sanity: "
	echo 'main(){}' > dummy.c
	${BUILD_TGT}-gcc dummy.c
	retval=$(readelf -l a.out | grep ': /tools')
	rm dummy.c a.out
	retval=${retval##*: }	# strip [Requesting program interpreter: 
	retval=${retval%]}	# strip ]
	case "${retval}" in
		"/tools/lib/ld-linux.so.2")		msg_success ;;
		"/tools/lib64/ld-linux-x86-64.so.2")	msg_success ;;
		*)					msg_line "       Glibc is insane: "msg_failure ;;
	esac
	>  ${_complete}
	return 0
}
build-libstdc++() {
	local	_pkgname="gcc"
	local	_pkgver="4.8.2"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Create work directory" "install -vdm 755 ../build" ${_logfile}
	build "	Change directory: ../build" "pushd ../build" ${_logfile}
	build "	Configure" "../${_pkgname}-${_pkgver}/libstdc++-v3/configure --host=${BUILD_TGT} --prefix=/tools --disable-multilib --disable-shared --disable-nls --disable-libstdcxx-threads --disable-libstdcxx-pch --with-gxx-include-dir=/tools/${BUILD_TGT}/include/c++/${_pkgver}" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-binutils2() {
	local	_pkgname="binutils"
	local	_pkgver="2.25"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Create work directory" "install -vdm 755 ../build" ${_logfile}
	build "	Change directory: ../build" "pushd ../build" ${_logfile}
	build "	Configure" "CC=${BUILD_TGT}-gcc AR=${BUILD_TGT}-ar RANLIB=${BUILD_TGT}-ranlib ../${_pkgname}-${_pkgver}/configure --prefix=/tools --disable-nls --with-lib-path=/tools/lib --with-sysroot" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	make -C ld clean" "make -C ld clean" ${_logfile}
	build "	make -C ld LIB_PATH=/usr/lib:/lib" "make -C ld LIB_PATH=/usr/lib:/lib" ${_logfile}
	build "	cp -v ld/ld-new /tools/bin" "cp -v ld/ld-new /tools/bin" ${_logfile}
	build "	Restore directory" "popd " /dev/nullPWD
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-gcc2() {
	local	_pkgname="gcc"
	local	_pkgver="4.8.2"
	local	_pwd=${PWD}/BUILD
	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	unpack "${PWD}" "mpfr-3.1.2"
	unpack "${PWD}" "gmp-5.1.3"
	unpack "${PWD}" "mpc-1.0.2"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Symlinking gmp" " ln -vs ../gmp-5.1.3  gmp" ${_logfile}
	build "	Symlinking mpc" " ln -vs ../mpc-1.0.2  mpc" ${_logfile}
	build "	Symlinking mpfr" "ln -vs ../mpfr-3.1.2 mpfr" ${_logfile}
	build "	Fixing limits.h" 'cat gcc/limitx.h gcc/glimits.h gcc/limity.h > $(dirname $( ${BUILD_TGT}-gcc -print-libgcc-file-name))/include-fixed/limits.h' ${_logfile}
	[ "x86_64" == $(uname -m) ] || build "	Adding -fomit-frame-pointer to CFLAGS" 'sed -i "s/^T_CFLAGS =$/& -fomit-frame-pointer/" gcc/Makefile.in' ${_logfile}
	build "	Fixing headers" 'for file in $(find gcc/config -name linux64.h -o -name linux.h -o -name sysv4.h); do cp -uv $file{,.orig};sed -e "s@/lib\(64\)\?\(32\)\?/ld@/tools&@g" -e "s@/usr@/tools@g" $file.orig > $file;printf "\n%s\n%s\n%s\n%s\n\n" "#undef STANDARD_STARTFILE_PREFIX_1" "#undef STANDARD_STARTFILE_PREFIX_2" "#define STANDARD_STARTFILE_PREFIX_1 \"/tools/lib/\"" "#define STANDARD_STARTFILE_PREFIX_2 \"\" ">> $file;touch $file.orig;done' ${_logfile}
	build "	Create work directory" "install -vdm 755 ../build" ${_logfile}
	build "	Change directory: ../build" "pushd ../build" ${_logfile}
	build "	Configure" "CC=${BUILD_TGT}-gcc CXX=${BUILD_TGT}-g++ AR=${BUILD_TGT}-ar RANLIB=${BUILD_TGT}-ranlib ../${_pkgname}-${_pkgver}/configure --prefix=/tools --with-local-prefix=/tools --with-native-system-header-dir=/tools/include --enable-clocale=gnu --enable-shared --enable-threads=posix --enable-__cxa_atexit --enable-languages=c,c++ --disable-libstdcxx-pch --disable-multilib --disable-bootstrap --disable-libgomp --with-mpfr-include=${_pwd}/${_pkgname}-${_pkgver}/mpfr/src --with-mpfr-lib=${_pwd}/build/mpfr/src/.libs" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	ln -sv gcc /tools/bin/cc" "ln -sv gcc /tools/bin/cc" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	msg_line "       Checking glibc for sanity: "
	echo 'main(){}' > dummy.c
	${BUILD_TGT}-gcc dummy.c
	retval=$(readelf -l a.out | grep ': /tools')
	rm dummy.c a.out
	retval=${retval##*: }	# strip [Requesting program interpreter: 
	retval=${retval%]}	# strip ]
	case "${retval}" in
		"/tools/lib/ld-linux.so.2")	     msg_success ;;
		"/tools/lib64/ld-linux-x86-64.so.2") msg_success ;;
		*)					msg_line "       GCC is insane: "msg_failure ;;
	esac
	>  ${_complete}
	return 0
}
build-tcl() {
	local	_pkgname="tcl"
	local	_pkgver="8.6.1"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}${_pkgver}-src"
	build "	Change directory: ${_pkgname}${_pkgver}/unix" "pushd ${_pkgname}${_pkgver}/unix" ${_logfile}
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Installing Headers" "make install-private-headers" ${_logfile}
	build "	chmod -v u+w /tools/lib/libtcl8.6.so" "chmod -v u+w /tools/lib/libtcl8.6.so" ${_logfile}
	build "	ln -sv tclsh8.6 /tools/bin/tclsh" " ln -sv tclsh8.6 /tools/bin/tclsh" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-expect() {
	local	_pkgname="expect"
	local	_pkgver="5.45"
	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}${_pkgver}"
	build "	Change directory: ${_pkgname}${_pkgver}" "pushd ${_pkgname}${_pkgver}" ${_logfile}
	build "	cp -v configure{,.orig}" "cp -v configure{,.orig}" ${_logfile}
	build "	sed 's:/usr/local/bin:/bin:' configure.orig > configure" "sed 's:/usr/local/bin:/bin:' configure.orig > configure" ${_logfile}
	build "	Configure" "./configure --prefix=/tools --with-tcl=/tools/lib --with-tclinclude=/tools/include" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" 'make SCRIPTS="" install' ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-dejagnu() {
	local	_pkgname="dejagnu"
	local	_pkgver="1.5.1"
	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-check() {
	local	_pkgname="check"
	local	_pkgver="0.9.14"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Configure" "PKG_CONFIG= ./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-ncurses() {
	local	_pkgname="ncurses"
	local	_pkgver="5.9"
	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Configure" "./configure --prefix=/tools --with-shared --without-debug --without-ada --enable-widec --enable-overwrite" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-bash() {
	local	_pkgname="bash"
	local	_pkgver="4.3"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Patch" "patch -Np1 -i ../../PATCHES/bash-4.3-upstream_fixes-7.patch" ${_logfile}
	build "	Configure" "./configure --prefix=/tools --without-bash-malloc" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	ln -sv bash /tools/bin/sh" "ln -sv bash /tools/bin/sh" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-bzip2() {
local	_pkgname="bzip2"
	local	_pkgver="1.0.6"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Make" "make ${MKFLAGS} CFLAGS='-fPIC -O2 -g -pipe'" ${_logfile}
	build "	Install" "make  PREFIX=/tools install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-coreutils() {
	local	_pkgname="coreutils"
	local	_pkgver="8.22"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Configure" "FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=/tools --enable-install-program=hostname " ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-diffutils() {
	local	_pkgname="diffutils"
	local	_pkgver="3.3"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-file() {
	local	_pkgname="file"
	local	_pkgver="5.22"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-findutils() {
	local	_pkgname="findutils"
	local	_pkgver="4.4.2"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-gawk() {
	local	_pkgname="gawk"
	local	_pkgver="4.1.0"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-gettext() {
	local	_pkgname="gettext"
	local	_pkgver="0.18.3.2"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}/gettext-tools" "pushd ${_pkgname}-${_pkgver}/gettext-tools" ${_logfile}
	build "	Configure" "EMACS="no" ./configure --prefix=/tools --disable-shared" ${_logfile}
	build "	make -C gnulib-lib" "make -C gnulib-lib" ${_logfile}
	build "	make -C src msgfmt" "make -C src msgfmt" ${_logfile}
	build "	make -C src msgmerge" "make -C src msgmerge" ${_logfile}
	build "	make -C src xgettext" "make -C src xgettext" ${_logfile}
	build "	cp -v src/{msgfmt,msgmerge,xgettext} /tools/bin" "cp -v src/{msgfmt,msgmerge,xgettext} /tools/bin" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-grep() {
	local	_pkgname="grep"
	local	_pkgver="2.21"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-gzip() {
	local	_pkgname="gzip"
	local	_pkgver="1.6"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-m4() {
	local	_pkgname="m4"
	local	_pkgver="1.4.17"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-make() {
	local	_pkgname="make"
	local	_pkgver="4.0"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Configure" "./configure --prefix=/tools --without-guile" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-patch() {
	local	_pkgname="patch"
	local	_pkgver="2.7.1"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-perl() {
	local	_pkgname="perl"
	local	_pkgver="5.18.2"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Patch" "patch -Np1 -i ../../PATCHES/perl-5.18.2-libc-1.patch" ${_logfile}
	build "	Configure" "sh Configure -des -Dprefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile} 
	build "	cp -v perl cpan/podlators/pod2man /tools/bin" "cp -v perl cpan/podlators/pod2man /tools/bin" ${_logfile}
	build "	mkdir -pv /tools/lib/perl5/5.18.2" "mkdir -pv /tools/lib/perl5/5.18.2" ${_logfile}
	build "	cp -Rv lib/* /tools/lib/perl5/5.18.2" "cp -Rv lib/* /tools/lib/perl5/5.18.2" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-sed() {
	local	_pkgname="sed"
	local	_pkgver="4.2.2"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-tar() {
	local	_pkgname="tar"
	local	_pkgver="1.27.1"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Configure" "FORCE_UNSAFE_CONFIGURE=1 ./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-texinfo() {
	local	_pkgname="texinfo"
	local	_pkgver="5.2"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-util-linux() {
	local	_pkgname="util-linux"
	local	_pkgver="2.24.1"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Configure" "./configure --prefix=/tools --disable-makeinstall-chown --without-systemdsystemunitdir PKG_CONFIG=''" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-xz() {
	local	_pkgname="xz"
	local	_pkgver="5.0.5"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
strip-ToolChain() {
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build 'strip --strip-debug /tools/lib/*' 'strip --strip-debug /tools/lib/* || true' ${_logfile}
	build '/usr/bin/strip --strip-unneeded /tools/{,s}bin/*' '/usr/bin/strip --strip-unneeded /tools/{,s}bin/* || true' ${_logfile}
	build 'rm -rf /tools/{,share}/{info,man,doc}' 'rm -rf /tools/{,share}/{info,man,doc}' ${_logfile}
	>  ${_complete}
	return 0
}
change-ownership() {
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	chown -R root:root $BUILD/tools" "su -c 'chown -R root:root /tools'" ${_logfile}
	>  ${_complete}
	return 0
}
#
#	Add rpm to tool chain
#
build-zlib() {
	local	_pkgname="zlib"
	local	_pkgver="1.2.8"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Configure" "./configure --prefix=/tools" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-nspr() {
	local _pkgname="nspr"
	local _pkgver="4.10.3"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	cd nspr
	sed -ri 's#^(RELEASE_BINS =).*#\1#' pr/src/misc/Makefile.in  || die "${FUNCNAME}: sed: FAILURE"
	sed -i 's#$(LIBRARY) ##' config/rules.mk  || die "${FUNCNAME}: sed: FAILURE"
	build "	Configure" "PKG_CONFIG_PATH="/tools/lib/pkgconfig" ./configure --prefix=/tools --with-mozilla --with-pthreads $([ "$(uname -m)" = "x86_64" ] && echo --enable-64bit)" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-nss() {
	local _pkgname="nss"
	local _pkgver="3.15.4"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Patch" "patch -Np1 -i ../../PATCHES/nss-3.15.4-standalone-1.patch" ${_logfile}
	cd nss
	build "	Make" "make BUILD_OPT=1 NSPR_INCLUDE_DIR=/tools/include/nspr USE_SYSTEM_ZLIB=1 ZLIB_LIBS=-lz $([ "$(uname -m)" = "x86_64" ] && echo USE_64=1) -j1" ${_logfile}
	cd ../dist
	build "	install -vdm 755 /tools/bin" "install -vdm 755 /tools/bin" ${_logfile}
	build "	install -vdm 755 /tools/lib/pkgconfig" "install -vdm 755 /tools/lib/pkgconfig" ${_logfile}
	build "	install -vdm 755 /tools/include" "install -vdm 755 /tools/include" ${_logfile}
	build "	install -v -m755 Linux*/lib/*.so /tools/lib" "install -v -m755 Linux*/lib/*.so /tools/lib" ${_logfile}
	build "	install -v -m644 Linux*/lib/{*.chk,libcrmf.a} /tools/lib" "install -v -m644 Linux*/lib/{*.chk,libcrmf.a} /tools/lib" ${_logfile}
	build "	cp -v -RL {public,private}/nss/* /tools/include" "cp -v -RL {public,private}/nss/* /tools/include" ${_logfile}
	build "	install -v -m755 Linux*/bin/{certutil,nss-config,pk12util} /tools/bin" "install -v -m755 Linux*/bin/{certutil,nss-config,pk12util} /tools/bin" ${_logfile}
	build "	install -v -m644 Linux*/lib/pkgconfig/nss.pc  /tools/lib/pkgconfig" "install -v -m644 Linux*/lib/pkgconfig/nss.pc  /tools/lib/pkgconfig" ${_logfile}
	build "	sed -i 's|usr|tools|' /tools/lib/pkgconfig/nss.pc" "sed -i 's|usr|tools|' /tools/lib/pkgconfig/nss.pc" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-popt() {
	local _pkgname="popt"
	local _pkgver="1.16"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}	
	build "	Configure" "./configure --prefix=/tools --disable-static" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-readline() {
	local _pkgname="readline"
	local _pkgver="6.3"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	sed -i '/MV.*old/d' Makefile.in" "sed -i '/MV.*old/d' Makefile.in" ${_logfile}
	build "	sed -i '/{OLDSUFF}/c:' support/shlib-install" "sed -i '/{OLDSUFF}/c:' support/shlib-install" ${_logfile}
	build "	Patch" "patch -Np1 -i ../../PATCHES/readline-6.3-upstream_fixes-3.patch" ${_logfile}
	build "	Configure" "PKG_CONFIG_PATH='/tools/lib/pkgconfig' ./configure --prefix=/tools --libdir=/tools/lib --with-curses=/tools/lib" ${_logfile}
	build "	Make" "make ${MKFLAGS} SHLIB_LIBS=-lncursesw" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-elfutils() {
	local _pkgname="elfutils"
	local _pkgver="0.158"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build "	Configure" 'PKG_CONFIG_PATH="/tools/lib/pkgconfig" ./configure --prefix=/tools --program-prefix="eu-" --with-bzlib=no' ${_logfile}
	build "	Make" "make ${MKFLAGS} SHLIB_LIBS=-lncursesw" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}
build-rpm() {
	local _pkgname="rpm"
	local _pkgver="4.11.2"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	unpack "${PWD}" "db-5.3.28"
	build "	ln -vs db-5.3.28 db" "ln -vs db-5.3.28 db" ${_logfile}
	build "	Configure" "PKG_CONFIG_PATH=/tools/lib/pkgconfig CPPFLAGS='-I/tools/include -I/tools/include/nspr' ./configure --prefix=/tools --disable-static --disable-dependency-tracking --without-lua" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	install -dm 755 /tools/etc/rpm" "install -dm 755 /tools/etc/rpm" ${_logfile}
	build "	rm -v/tools/bin/{rpmquery,rpmverify}" "rm -v /tools/bin/{rpmquery,rpmverify}" ${_logfile}
	build "	ln -vsf rpm /tools/bin/rpmquery" "ln -vsf rpm /tools/bin/rpmquery" ${_logfile}
	build "	ln -vsf rpm /tools/bin/rpmverify" "ln -vsf rpm /tools/bin/rpmverify" ${_logfile}
	build "	install -vm 755 ${BUILDDIR}/SCRIPTS/macros /tools/etc/rpm" "install -vm 755 ${BUILDDIR}/SCRIPTS/macros /tools/etc/rpm" ${_logfile}
	build "	install -vm 755 ${BUILDDIR}/SCRIPTS/brp-strip-debug-symbols /tools/lib/rpm" "install -vm 755 ${BUILDDIR}/SCRIPTS/brp-strip-debug-symbols /tools/lib/rpm" ${_logfile}
	build "	install -vm 755 ${BUILDDIR}/SCRIPTS/brp-strip-unneeded /tools/lib/rpm" "install -vm 755 ${BUILDDIR}/SCRIPTS/brp-strip-unneeded /tools/lib/rpm" ${_logfile}
	build " sed -i 's@/usr/lib/rpm/debugedit@/tools/lib/rpm/debugedit@g' /tools/lib/rpm/find-debuginfo.sh" "sed -i 's@/usr/lib/rpm/debugedit@/tools/lib/rpm/debugedit@g' /tools/lib/rpm/find-debuginfo.sh" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}

build-cpio() {
	local _pkgname="cpio"
	local _pkgver="2.11"
      	local	_complete="${PWD}/LOGS/${FUNCNAME}.completed"
	local	_logfile="${PWD}/LOGS/${FUNCNAME}.log"
	[ -e ${_complete} ] && { msg "${FUNCNAME}: SKIPPING";return 0; } || msg "${FUNCNAME}: Building"
	> ${_logfile}
	build "	Clean build directory" 'rm -rf BUILD/*' ${_logfile}
	build "	Change directory: BUILD" "pushd BUILD" ${_logfile}
	unpack "${PWD}" "${_pkgname}-${_pkgver}"
	build "	Change directory: ${_pkgname}-${_pkgver}" "pushd ${_pkgname}-${_pkgver}" ${_logfile}
	build " sed -i -e '/gets is a/d' gnu/stdio.in.h" "sed -i -e '/gets is a/d' gnu/stdio.in.h" ${_logfile}
	build "	Configure" "PKG_CONFIG_PATH=/tools/lib/pkgconfig CPPFLAGS='-I/tools/include -I/tools/include/nspr' ./configure --prefix=/tools --enable-mt --with-rmt=/usr/libexec/rmt" ${_logfile}
	build "	Make" "make ${MKFLAGS}" ${_logfile}
	build "	Install" "make install" ${_logfile}
	build "	Restore directory" "popd " /dev/null
	build "	Restore directory" "popd " /dev/null
	>  ${_complete}
	return 0
}

#
#	Main line	
#
msg "Building Tool chain"
build-binutils1	
build-gcc1
build-linux-api-headers
build-glibc
build-libstdc++
build-binutils2
build-gcc2
build-tcl
#build-expect
#build-dejagnu
build-check
build-ncurses
build-bash
build-bzip2
build-coreutils
build-diffutils
build-file
build-findutils
build-gawk
build-gettext
build-grep
build-gzip
build-m4
build-make
build-patch
build-perl
build-sed
build-tar
build-texinfo
build-util-linux
build-xz
#	The following packages comprise the package management system RPM
build-zlib
build-nspr
build-nss
build-popt
build-readline
build-elfutils
build-rpm
build-cpio
#	The following are not used
strip-ToolChain
#	change-ownership
msg "Creating tools tar ball"
tar -cf $DESTDIR/tools-build.tar -C ${BUILDDIR} tools
rm -rf ${BUILDDIR}
rm /tools
msg "Successfully built the Toolchain"
exit 0
