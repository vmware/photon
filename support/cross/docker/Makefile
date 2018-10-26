SRCROOT=$(realpath ../../..)
SRCDIR=$(SRCROOT)/SOURCES
BUILDDIR=$(SRCROOT)/BUILD

RPMBUILD_ROOT=$(SRCROOT)
RPMBUILD_BUILD=$(BUILDDIR)
RPMBUILD_BUILDROOT=$(SRCROOT)/BUILDROOT
RPMBUILD_SPECS=$(SRCROOT)/SPECS
RPMBUILD_RPMS=$(SRCROOT)/RPMS
RPMBUILD_SRCS=$(SRCROOT)/SOURCES
RPMBUILD_SRPMS=$(SRCROOT)/SRPMS
RPMBUILD_TMP=$(SRCROOT)/tmp

RPMBUILD_DIRS= \
	$(RPMBUILD_BUILD) \
	$(RPMBUILD_SPECS) \
	$(RPMBUILD_RPMS) \
	$(RPMBUILD_SRCS) \
	$(RPMBUILD_SRPMS) \
	$(RPMBUILD_TMP)

BINUTILS_VERSION=2.28
GCC_VERSION=6.3.0
KERNEL_VERSION=4.18.11
GLIBC_VERSION=2.26
MPFR_VERSION=3.1.5
GMP_VERSION=6.1.2
GMP_VERSION_X=6.1.2
MPC_VERSION=1.0.3
ISL_VERSION=0.14
CLOOG_VERSION=0.18.1

INSTALL_PATH_ARM32=/opt/cross
INSTALL_PATH_AARCH64=/opt/cross
INSTALL_PATH_X86=/opt/cross

all: package

package-arm: build-arm | $(RPMBUILD_DIRS)

package-aarch64: build-aarch64 | $(RPMBUILD_DIRS)

package-i686: build-i686 | $(RPMBUILD_DIRS)

build-arm: download | build-dir
	@echo "Building cross compile toolchain for ARM32..."
	@rpmbuild -v \
	    --bb \
	    --define "_topdir $(RPMBUILD_ROOT)" \
	    --define "_builddir $(RPMBUILD_BUILD)/usr/src/debug" \
	    --define "_dist .ph2" \
	    --define "_smp_mflags -j8" \
	    --buildroot $(SRCROOT)/stage/cross/arm-photon-linux-gnu \
	    --noclean \
	    --target arm-photon-linux \
	    $(SRCROOT)/SPECS/cross-tools/cross-arm-tools.spec

build-aarch64: download | build-dir
	@echo "Building cross compile toolchain for AARCH64..."
	@rpmbuild -v \
	    --bb \
	    --define "_topdir $(RPMBUILD_ROOT)" \
	    --define "_builddir $(RPMBUILD_BUILD)/usr/src/debug" \
	    --define "_dist .ph2" \
	    --define "_smp_mflags -j8" \
	    --buildroot $(SRCROOT)/stage/cross/aarch64-photon-linux-gnu \
	    --noclean \
	    --target aarch64-photon-linux \
	    $(SRCROOT)/SPECS/cross-tools/cross-aarch64-tools.spec

build-i686: download | build-dir
	@echo "Building cross compile toolchain for i686..."
	@rpmbuild -v \
	    --bb \
	    --define "_topdir $(RPMBUILD_ROOT)" \
	    --define "_builddir $(RPMBUILD_BUILD)/usr/src/debug" \
	    --define "_dist .ph2" \
	    --define "_smp_mflags -j8" \
	    --buildroot $(SRCROOT)/stage/cross/i686-photon-linux-gnu \
	    --noclean \
	    --target x86-photon-linux \
	    $(SRCROOT)/SPECS/cross-tools/cross-i686-tools.spec

download: src-dir
	@echo "Downloading sources..."
	@$(SRCROOT)/support/cross/docker/scripts/download.sh \
	    -s $(SRCDIR) \
	    -b $(BINUTILS_VERSION) \
	    -c $(CLOOG_VERSION) \
	    -g $(GCC_VERSION) \
	    -i $(ISL_VERSION) \
	    -k $(KERNEL_VERSION) \
	    -l $(GLIBC_VERSION) \
	    -m $(MPFR_VERSION) \
	    -n $(GMP_VERSION) \
	    -p $(MPC_VERSION) \
	    -z $(SRCROOT)/SPECS/cross-tools

$(RPMBUILD_DIRS):
	@mkdir -p $@

src-dir:
	@mkdir -p $(SRCDIR)

build-dir:
	@mkdir -p $(BUILDDIR)

clean:
	@rm -rf $(BUILDDIR)
	@rm -rf $(RPMBUILD_BUILDROOT)
	@rm -rf $(RPMBUILD_TMP)
	@rm -rf $(RPMBUILD_SRPMS)
	@rm -rf $(RPMBUILD_RPMS)
	@rm -rf $(SRCROOT)/stage/cross

scrub: clean
	@rm -rf $(SRCDIR)
