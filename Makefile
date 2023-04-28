#
# Copyright VMware, Inc. 2015-2022
#

SRCROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
MAKEROOT=$(SRCROOT)/support/make

# do not build these targets as '%'
$(MAKEROOT)/makedefs.mk: ;
Makefile: ;

include $(MAKEROOT)/makedefs.mk

export PATH := $(SRCROOT)/tools/bin:$(PATH)
export PHOTON_BUILD_NUM=$(PHOTON_BUILD_NUMBER)
export PHOTON_RELEASE_VER=$(PHOTON_RELEASE_VERSION)
export PHOTON_BUILDER_TAG=$(PH_BUILDER_TAG)
export PH_BUILD_SRC_RPM=$(BUILD_SRC_RPM)
export PH_BUILD_DBGINFO_RPM=$(BUILD_DBGINFO_RPM)

ifdef PHOTON_CACHE_PATH
PHOTON_PACKAGES_MINIMAL := packages-cached
PHOTON_PACKAGES := packages-cached
else
PHOTON_PACKAGES_MINIMAL := packages-minimal
PHOTON_PACKAGES := packages
endif

ifdef PHOTON_SOURCES_PATH
PHOTON_SOURCES := sources-cached
else
PHOTON_SOURCES ?= sources
endif

FULL_PACKAGE_LIST_FILE := build_install_options_all.json
MINIMAL_PACKAGE_LIST_FILE := build_install_options_minimal.json
RT_PACKAGE_LIST_FILE := build_install_options_rt.json

ifdef PHOTON_PUBLISH_RPMS_PATH
PHOTON_PUBLISH_RPMS := publish-rpms-cached
else
PHOTON_PUBLISH_RPMS := publish-rpms
endif

ifdef PHOTON_PUBLISH_XRPMS_PATH
PHOTON_PUBLISH_XRPMS := publish-x-rpms-cached
else
PHOTON_PUBLISH_XRPMS := publish-x-rpms
endif

# Tri state RPMCHECK:
# 1) RPMCHECK is not specified:  just build
# 2) RPMCHECK=enable: build and run %check section. do not stop on error. will generate report file.
# 3) RPMCHECK=enable_stop_on_error: build and run %check section. stop on first error.
#
# We use 2 parameters:
# -u: enable checking.
# -q: quit on error. if -q is not specified it will keep going

ifeq ($(RPMCHECK),enable)
PHOTON_RPMCHECK_FLAGS := --enable-rpmcheck
else ifeq ($(RPMCHECK),enable_stop_on_error)
PHOTON_RPMCHECK_FLAGS := --enable-rpmcheck --rpmcheck-stop-on-error
else
PHOTON_RPMCHECK_FLAGS :=
endif

# KAT build for FIPS certification
# Use KAT_BUILD=enable to build a kat kernel. By default, KAT_BUILD is disabled.
ifeq ($(KAT_BUILD),enable)
PHOTON_KAT_BUILD_FLAGS := --enable-katbuild
endif

ifeq ($(BUILDDEPS),true)
PUBLISH_BUILD_DEPENDENCIES := --publish-build-dependencies True
else
PUBLISH_BUILD_DEPENDENCIES :=
endif

PACKAGE_WEIGHTS = --package-weights-path $(SRCROOT)/common/data/packageWeights.json

ifdef PKG_BUILD_OPTIONS
PACKAGE_BUILD_OPTIONS = --pkg-build-option-file $(PKG_BUILD_OPTIONS)
else
PACKAGE_BUILD_OPTIONS =
endif

TOOLS_BIN := $(SRCROOT)/tools/bin
CONTAIN := $(TOOLS_BIN)/contain
ifeq ($(ARCH),x86_64)
VIXDISKUTIL := $(TOOLS_BIN)/vixdiskutil
else
VIXDISKUTIL :=
endif

# Marker file indicating if run from container
DOCKER_ENV=/.dockerenv

$(TOOLS_BIN):
	@mkdir -p $(TOOLS_BIN)

$(CONTAIN): $(TOOLS_BIN)
	@./tools/src/contain/make.sh

$(VIXDISKUTIL): $(TOOLS_BIN)
	@./tools/src/vixDiskUtil/make.sh

.PHONY : all iso clean image all-images \
check-tools check-docker check-bison check-g++ check-gawk check-repo-tool check-kpartx check-sanity \
clean-install clean-chroot build-updated-packages check generate-yaml-files

THREADS?=1
LOGLEVEL?=info

# Build targets for rpm build
#-------------------------------------------------------------------------------
packages-minimal: check-tools photon-stage $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) generate-dep-lists
	@echo "Building all minimal RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
	$(PHOTON_PACKAGE_BUILDER) \
		--spec-path $(PHOTON_SPECS_DIR) \
		--rpm-path $(PHOTON_RPMS_DIR) \
		--source-path $(PHOTON_SRCS_DIR) \
		--build-root-path $(PHOTON_CHROOT_PATH) \
		--packages-json-input $(PHOTON_DATA_DIR)/packages_minimal.json \
		--log-path $(PHOTON_LOGS_DIR) \
		--log-level $(LOGLEVEL) \
		--publish-RPMS-path $(PHOTON_PUBLISH_RPMS_DIR) \
		--pullsources-config $(PHOTON_PULLSOURCES_CONFIG) \
		--dist-tag $(PHOTON_DIST_TAG) \
		--build-number $(PHOTON_BUILD_NUMBER) \
		--release-version $(PHOTON_RELEASE_VERSION) \
		--pkginfo-file $(PHOTON_PKGINFO_FILE) \
		$(PHOTON_RPMCHECK_FLAGS) \
		$(PUBLISH_BUILD_DEPENDENCIES) \
		$(PACKAGE_WEIGHTS) \
		--threads ${THREADS}
	$(PHOTON_REPO_TOOL) $(PHOTON_REPO_TOOL_OPT) $(PHOTON_RPMS_DIR)

packages-rt: check-tools photon-stage $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) generate-dep-lists
	@echo "Building minimal RPMS for Real Time..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
	$(PHOTON_PACKAGE_BUILDER) \
		--spec-path $(PHOTON_SPECS_DIR) \
		--rpm-path $(PHOTON_RPMS_DIR) \
		--source-path $(PHOTON_SRCS_DIR) \
		--build-root-path $(PHOTON_CHROOT_PATH) \
		--packages-json-input $(PHOTON_DATA_DIR)/packages_rt.json \
		--log-path $(PHOTON_LOGS_DIR) \
		--log-level $(LOGLEVEL) \
		--publish-RPMS-path $(PHOTON_PUBLISH_RPMS_DIR) \
		--pullsources-config $(PHOTON_PULLSOURCES_CONFIG) \
		--dist-tag $(PHOTON_DIST_TAG) \
		--build-number $(PHOTON_BUILD_NUMBER) \
		--release-version $(PHOTON_RELEASE_VERSION) \
		--pkginfo-file $(PHOTON_PKGINFO_FILE) \
		$(PHOTON_RPMCHECK_FLAGS) \
		$(PUBLISH_BUILD_DEPENDENCIES) \
		$(PACKAGE_WEIGHTS) \
		--threads ${THREADS}
	$(PHOTON_REPO_TOOL) $(PHOTON_REPO_TOOL_OPT) $(PHOTON_RPMS_DIR)

packages-initrd: check-tools photon-stage $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) generate-dep-lists
	@echo "Building all initrd package RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
	$(PHOTON_PACKAGE_BUILDER) \
		--spec-path $(PHOTON_SPECS_DIR) \
		--rpm-path $(PHOTON_RPMS_DIR) \
		--source-path $(PHOTON_SRCS_DIR) \
		--build-root-path $(PHOTON_CHROOT_PATH) \
		--packages-json-input $(PHOTON_DATA_DIR)/packages_installer_initrd.json \
		--log-path $(PHOTON_LOGS_DIR) \
		--log-level $(LOGLEVEL) \
		--publish-RPMS-path $(PHOTON_PUBLISH_RPMS_DIR) \
		--pullsources-config $(PHOTON_PULLSOURCES_CONFIG) \
		--dist-tag $(PHOTON_DIST_TAG) \
		--build-number $(PHOTON_BUILD_NUMBER) \
		--release-version $(PHOTON_RELEASE_VERSION) \
		--pkginfo-file $(PHOTON_PKGINFO_FILE) \
		$(PHOTON_RPMCHECK_FLAGS) \
		$(PUBLISH_BUILD_DEPENDENCIES) \
		$(PACKAGE_WEIGHTS) \
		--threads ${THREADS}
	$(PHOTON_REPO_TOOL) $(PHOTON_REPO_TOOL_OPT) $(PHOTON_RPMS_DIR)

packages: check-tools photon-stage $(PHOTON_PUBLISH_XRPMS) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) check-spec-files generate-dep-lists
	@echo "Building all RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
	$(PHOTON_PACKAGE_BUILDER) \
		--build-type $(PHOTON_BUILD_TYPE) \
		--spec-path $(PHOTON_SPECS_DIR) \
		--rpm-path $(PHOTON_RPMS_DIR) \
		--source-rpm-path $(PHOTON_SRPMS_DIR) \
		--source-path $(PHOTON_SRCS_DIR) \
		--build-root-path $(PHOTON_CHROOT_PATH) \
		--log-path $(PHOTON_LOGS_DIR) \
		--log-level $(LOGLEVEL) \
		--publish-RPMS-path $(PHOTON_PUBLISH_RPMS_DIR) \
		--publish-XRPMS-path $(PHOTON_PUBLISH_XRPMS_DIR) \
		--pullsources-config $(PHOTON_PULLSOURCES_CONFIG) \
		--dist-tag $(PHOTON_DIST_TAG) \
		--build-number $(PHOTON_BUILD_NUMBER) \
		--release-version $(PHOTON_RELEASE_VERSION) \
		--pkginfo-file $(PHOTON_PKGINFO_FILE) \
		$(PACKAGE_BUILD_OPTIONS) \
		$(PHOTON_RPMCHECK_FLAGS) \
		$(PHOTON_KAT_BUILD_FLAGS) \
		$(PUBLISH_BUILD_DEPENDENCIES) \
		$(PACKAGE_WEIGHTS) \
		--threads ${THREADS}
	@$(PHOTON_REPO_TOOL) $(PHOTON_REPO_TOOL_OPT) $(PHOTON_RPMS_DIR)

packages-docker: check-tools photon-stage $(PHOTON_PUBLISH_XRPMS) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	@echo "Building all RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
	$(PHOTON_PACKAGE_BUILDER) \
		--build-type $(PHOTON_BUILD_TYPE) \
		--spec-path $(PHOTON_SPECS_DIR) \
		--rpm-path $(PHOTON_RPMS_DIR) \
		--source-rpm-path $(PHOTON_SRPMS_DIR) \
		--source-path $(PHOTON_SRCS_DIR) \
		--build-root-path $(PHOTON_CHROOT_PATH) \
		--log-path $(PHOTON_LOGS_DIR) \
		--log-level $(LOGLEVEL) \
		--publish-RPMS-path $(PHOTON_PUBLISH_RPMS_DIR) \
		--publish-XRPMS-path $(PHOTON_PUBLISH_XRPMS_DIR) \
		--pullsources-config $(PHOTON_PULLSOURCES_CONFIG) \
		--dist-tag $(PHOTON_DIST_TAG) \
		--build-number $(PHOTON_BUILD_NUMBER) \
		--release-version $(PHOTON_RELEASE_VERSION) \
		--pkginfo-file $(PHOTON_PKGINFO_FILE) \
		$(PACKAGE_BUILD_OPTIONS) \
		$(PHOTON_RPMCHECK_FLAGS) \
		$(PUBLISH_BUILD_DEPENDENCIES) \
		$(PACKAGE_WEIGHTS) \
		--threads ${THREADS}
	$(PHOTON_REPO_TOOL) $(PHOTON_REPO_TOOL_OPT) $(PHOTON_RPMS_DIR)

updated-packages: check-tools photon-stage $(PHOTON_PUBLISH_XRPMS) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	@echo "Building only updated RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
	$(PHOTON_PACKAGE_BUILDER) \
		--spec-path $(PHOTON_SPECS_DIR) \
		--rpm-path $(PHOTON_UPDATED_RPMS_DIR) \
		--source-path $(PHOTON_SRCS_DIR) \
		--build-root-path $(PHOTON_CHROOT_PATH) \
		--log-path $(PHOTON_LOGS_DIR) \
		--log-level $(LOGLEVEL) \
		--publish-RPMS-path $(PHOTON_PUBLISH_RPMS_DIR) \
		--publish-XRPMS-path $(PHOTON_PUBLISH_XRPMS_DIR) \
		--pullsources-config $(PHOTON_PULLSOURCES_CONFIG) \
		--dist-tag $(PHOTON_DIST_TAG) \
		--build-number $(PHOTON_BUILD_NUMBER) \
		--release-version $(PHOTON_RELEASE_VERSION) \
		--input-RPMS-path $(PHOTON_INPUT_RPMS_DIR) \
		$(PHOTON_KAT_BUILD_FLAGS) \
		$(PHOTON_RPMCHECK_FLAGS) \
		$(PUBLISH_BUILD_DEPENDENCIES) \
		$(PACKAGE_WEIGHTS) \
		--threads ${THREADS}

tool-chain-stage1: check-tools photon-stage $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	@echo "Building all RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
	$(PHOTON_PACKAGE_BUILDER) \
		--spec-path $(PHOTON_SPECS_DIR) \
		--rpm-path $(PHOTON_RPMS_DIR) \
		--source-rpm-path $(PHOTON_SRPMS_DIR) \
		--source-path $(PHOTON_SRCS_DIR) \
		--build-root-path $(PHOTON_CHROOT_PATH) \
		--log-path $(PHOTON_LOGS_DIR) \
		--log-level $(LOGLEVEL) \
		--publish-RPMS-path $(PHOTON_PUBLISH_RPMS_DIR) \
		--threads ${THREADS} \
		--pullsources-config $(PHOTON_PULLSOURCES_CONFIG) \
		--dist-tag $(PHOTON_DIST_TAG) \
		--build-number $(PHOTON_BUILD_NUMBER) \
		--release-version $(PHOTON_RELEASE_VERSION) \
		$(PHOTON_RPMCHECK_FLAGS) \
		--tool-chain-stage stage1

tool-chain-stage2: check-tools photon-stage $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	@echo "Building all RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
	$(PHOTON_PACKAGE_BUILDER) \
		--spec-path $(PHOTON_SPECS_DIR) \
		--rpm-path $(PHOTON_RPMS_DIR) \
		--source-rpm-path $(PHOTON_SRPMS_DIR) \
		--source-path $(PHOTON_SRCS_DIR) \
		--build-root-path $(PHOTON_CHROOT_PATH) \
		--log-path $(PHOTON_LOGS_DIR) \
		--log-level $(LOGLEVEL) \
		--publish-RPMS-path $(PHOTON_PUBLISH_RPMS_DIR) \
		--threads ${THREADS} \
		--pullsources-config $(PHOTON_PULLSOURCES_CONFIG) \
		--dist-tag $(PHOTON_DIST_TAG) \
		--build-number $(PHOTON_BUILD_NUMBER) \
		--release-version $(PHOTON_RELEASE_VERSION) \
		$(PHOTON_RPMCHECK_FLAGS) \
		--tool-chain-stage stage2

%: check-tools $(PHOTON_PUBLISH_RPMS) $(PHOTON_PUBLISH_XRPMS) $(PHOTON_SOURCES) $(CONTAIN) check-spec-files $(eval PKG_NAME = $@)
	$(eval PKG_NAME = $@)
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
	$(PHOTON_PACKAGE_BUILDER) --install-package $(PKG_NAME) \
		--build-type $(PHOTON_BUILD_TYPE) \
		--build-root-path $(PHOTON_CHROOT_PATH) \
		--spec-path $(PHOTON_SPECS_DIR) \
		--rpm-path $(PHOTON_RPMS_DIR) \
		--source-rpm-path $(PHOTON_SRPMS_DIR) \
		--source-path $(PHOTON_SRCS_DIR) \
		--publish-RPMS-path $(PHOTON_PUBLISH_RPMS_DIR) \
		--publish-XRPMS-path $(PHOTON_PUBLISH_XRPMS_DIR) \
		--pullsources-config $(PHOTON_PULLSOURCES_CONFIG) \
		--log-level $(LOGLEVEL) \
		--dist-tag $(PHOTON_DIST_TAG) \
		--build-number $(PHOTON_BUILD_NUMBER) \
		--release-version $(PHOTON_RELEASE_VERSION) \
		$(PACKAGE_BUILD_OPTIONS) \
		$(PHOTON_RPMCHECK_FLAGS) \
		$(PHOTON_KAT_BUILD_FLAGS) \
		--log-path $(PHOTON_LOGS_DIR) \
		--threads ${THREADS}

check: packages
	ifeq ($(RPMCHECK),enable_stop_on_error)
		$(eval rpmcheck_stop_on_error = -q)
	endif
	@echo "Testing all RPMS ..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
	$(PHOTON_PACKAGE_BUILDER) \
		--build-type $(PHOTON_BUILD_TYPE) \
		--spec-path $(PHOTON_SPECS_DIR) \
		--rpm-path $(PHOTON_RPMS_DIR) \
		--source-rpm-path $(PHOTON_SRPMS_DIR) \
		--source-path $(PHOTON_SRCS_DIR) \
		--build-root-path $(PHOTON_CHROOT_PATH) \
		--log-path $(PHOTON_LOGS_DIR) \
		--log-level $(LOGLEVEL) \
		--publish-RPMS-path $(PHOTON_PUBLISH_RPMS_DIR) \
		--publish-XRPMS-path $(PHOTON_PUBLISH_XRPMS_DIR) \
		--pullsources-config $(PHOTON_PULLSOURCES_CONFIG) \
		--dist-tag $(PHOTON_DIST_TAG) \
		--build-number $(PHOTON_BUILD_NUMBER) \
		--release-version $(PHOTON_RELEASE_VERSION) \
		--pkginfo-file $(PHOTON_PKGINFO_FILE) \
		$(PACKAGE_BUILD_OPTIONS) \
		--enable-rpmcheck \
		$(rpmcheck_stop_on_error) \
		--threads ${THREADS}

#-------------------------------------------------------------------------------

# The targets listed under "all" are the installer built artifacts
#===============================================================================
all: check-tools iso photon-docker-image k8s-docker-images all-images src-iso

iso: check-tools photon-stage $(PHOTON_PACKAGES) ostree-repo
	@echo "Building Photon Full ISO..."
	@cd $(PHOTON_IMAGE_BUILDER_DIR) && \
	$(PHOTON_IMAGE_BUILDER) \
		--iso-path $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso \
		--debug-iso-path $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).debug.iso \
		--log-path $(PHOTON_STAGE)/LOGS \
		--log-level $(LOGLEVEL) \
		--rpm-path $(PHOTON_STAGE)/RPMS \
		--srpm-path $(PHOTON_STAGE)/SRPMS \
		--package-list-file $(PHOTON_DATA_DIR)/$(FULL_PACKAGE_LIST_FILE) \
		--generated-data-path $(PHOTON_STAGE)/common/data \
		--pkg-to-rpm-map-file $(PHOTON_PKGINFO_FILE) \
		--photon-docker-image $(PHOTON_DOCKER_IMAGE) \
		--photon-release-version $(PHOTON_RELEASE_VERSION)

minimal-iso: check-tools photon-stage $(PHOTON_PUBLISH_XRPMS) packages-minimal packages-initrd
	@echo "Building Photon Minimal ISO..."
	@$(CP) -f $(PHOTON_DATA_DIR)/$(MINIMAL_PACKAGE_LIST_FILE) $(PHOTON_GENERATED_DATA_DIR)/
	@cd $(PHOTON_IMAGE_BUILDER_DIR) && \
	$(PHOTON_IMAGE_BUILDER) \
		--iso-path $(PHOTON_STAGE)/photon-minimal-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUM).iso \
		--debug-iso-path $(PHOTON_STAGE)/photon-minimal-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).debug.iso \
		--log-path $(PHOTON_STAGE)/LOGS \
		--log-level $(LOGLEVEL) \
		--rpm-path $(PHOTON_STAGE)/RPMS \
		--srpm-path $(PHOTON_STAGE)/SRPMS \
		--package-list-file $(PHOTON_DATA_DIR)/$(MINIMAL_PACKAGE_LIST_FILE) \
		--generated-data-path $(PHOTON_STAGE)/common/data \
		--pkg-to-rpm-map-file $(PHOTON_PKGINFO_FILE) \
		--pkg-to-be-copied-conf-file $(PHOTON_GENERATED_DATA_DIR)/$(MINIMAL_PACKAGE_LIST_FILE) \
		--photon-docker-image $(PHOTON_DOCKER_IMAGE) \
		--photon-release-version $(PHOTON_RELEASE_VERSION)

rt-iso: check-tools photon-stage $(PHOTON_PUBLISH_XRPMS) packages-rt packages-initrd
	@echo "Building Photon Real Time ISO..."
	@$(CP) -f $(PHOTON_DATA_DIR)/$(RT_PACKAGE_LIST_FILE) $(PHOTON_GENERATED_DATA_DIR)/
	@cd $(PHOTON_IMAGE_BUILDER_DIR) && \
	$(PHOTON_IMAGE_BUILDER) \
		--iso-path $(PHOTON_STAGE)/photon-rt-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUM).iso \
		--debug-iso-path $(PHOTON_STAGE)/photon-rt-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).debug.iso \
		--log-path $(PHOTON_STAGE)/LOGS \
		--log-level $(LOGLEVEL) \
		--rpm-path $(PHOTON_STAGE)/RPMS \
		--srpm-path $(PHOTON_STAGE)/SRPMS \
		--package-list-file $(PHOTON_DATA_DIR)/$(RT_PACKAGE_LIST_FILE) \
		--generated-data-path $(PHOTON_STAGE)/common/data \
		--pkg-to-rpm-map-file $(PHOTON_PKGINFO_FILE) \
		--pkg-to-be-copied-conf-file $(PHOTON_GENERATED_DATA_DIR)/$(RT_PACKAGE_LIST_FILE) \
		--photon-docker-image $(PHOTON_DOCKER_IMAGE) \
		--photon-release-version $(PHOTON_RELEASE_VERSION)

src-iso: check-tools photon-stage $(PHOTON_PACKAGES)
	@echo "Building Photon Full Source ISO..."
	@cd $(PHOTON_IMAGE_BUILDER_DIR) && \
	$(PHOTON_IMAGE_BUILDER) \
		--src-iso-path $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).src.iso \
		--log-path $(PHOTON_STAGE)/LOGS \
		--log-level $(LOGLEVEL) \
		--rpm-path $(PHOTON_STAGE)/RPMS \
		--srpm-path $(PHOTON_STAGE)/SRPMS \
		--package-list-file $(PHOTON_GENERATED_DATA_DIR)/$(FULL_PACKAGE_LIST_FILE) \
		--generated-data-path $(PHOTON_STAGE)/common/data \
		--pkg-to-rpm-map-file $(PHOTON_PKGINFO_FILE) \
		--photon-docker-image $(PHOTON_DOCKER_IMAGE) \
		--photon-release-version $(PHOTON_RELEASE_VERSION) > \
		$(PHOTON_LOGS_DIR)/sourceiso-installer.log 2>&1

image: check-tools check-kpartx photon-stage $(VIXDISKUTIL) $(PHOTON_PACKAGES)
	@echo "Building image using $(CONFIG)..."
	@cd $(PHOTON_IMAGE_BUILDER_DIR)
	$(PHOTON_IMAGE_BUILDER) \
		--config-file=$(CONFIG) \
		--img-name=$(IMG_NAME) \
		--src-root=$(SRCROOT) \
		--generated-data-path=$(PHOTON_DATA_DIR) \
		--stage-path=$(PHOTON_STAGE) \
		--rpm-path $(PHOTON_STAGE)/RPMS \
		--photon-docker-image $(PHOTON_DOCKER_IMAGE) \
		--photon-release-version $(PHOTON_RELEASE_VERSION)

all-images: check-tools check-kpartx photon-stage $(VIXDISKUTIL) $(PHOTON_PACKAGES)
	@echo "Building all images - gce, ami, azure, ova..."
	@cd $(PHOTON_IMAGE_BUILDER_DIR)
	$(PHOTON_IMAGE_BUILDER) \
		--src-root=$(SRCROOT) \
		--generated-data-path=$(PHOTON_DATA_DIR) \
		--stage-path=$(PHOTON_STAGE) \
		--rpm-path $(PHOTON_STAGE)/RPMS \
		--photon-docker-image $(PHOTON_DOCKER_IMAGE) \
		--photon-release-version $(PHOTON_RELEASE_VERSION) \
		--img-name=ami
	$(PHOTON_IMAGE_BUILDER) \
		--src-root=$(SRCROOT) \
		--generated-data-path=$(PHOTON_DATA_DIR) \
		--stage-path=$(PHOTON_STAGE) \
		--rpm-path $(PHOTON_STAGE)/RPMS \
		--photon-docker-image $(PHOTON_DOCKER_IMAGE) \
		--photon-release-version $(PHOTON_RELEASE_VERSION) \
		--img-name=gce
	$(PHOTON_IMAGE_BUILDER) \
		--src-root=$(SRCROOT) \
		--generated-data-path=$(PHOTON_DATA_DIR) \
		--stage-path=$(PHOTON_STAGE) \
		--rpm-path $(PHOTON_STAGE)/RPMS \
		--photon-docker-image $(PHOTON_DOCKER_IMAGE) \
		--photon-release-version $(PHOTON_RELEASE_VERSION) \
		--img-name=azure
	$(PHOTON_IMAGE_BUILDER) \
		--src-root=$(SRCROOT) \
		--generated-data-path=$(PHOTON_DATA_DIR) \
		--stage-path=$(PHOTON_STAGE) \
		--rpm-path $(PHOTON_STAGE)/RPMS \
		--photon-docker-image $(PHOTON_DOCKER_IMAGE) \
		--photon-release-version $(PHOTON_RELEASE_VERSION) \
		--img-name=ova
	$(PHOTON_IMAGE_BUILDER) \
		--src-root=$(SRCROOT) \
		--generated-data-path=$(PHOTON_DATA_DIR) \
		--stage-path=$(PHOTON_STAGE) \
		--rpm-path $(PHOTON_STAGE)/RPMS \
		--photon-docker-image $(PHOTON_DOCKER_IMAGE) \
		--photon-release-version $(PHOTON_RELEASE_VERSION) \
		--img-name=ova_uefi

photon-docker-image: check-tools $(PHOTON_PACKAGES)
	@if [ -f $(PHOTON_STAGE)/photon-rootfs-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).tar.gz ]; then \
		echo "Photon docker image already present, not creating again..."; \
	else \
		DOCKER_BUILDKIT=0 \
                docker build --ulimit nofile=1024:1024 --no-cache --tag photon-build ./support/dockerfiles/photon && \
		docker run \
			--ulimit nofile=1024:1024 \
			--rm \
			--privileged \
			--net=host \
			-e PHOTON_BUILD_NUMBER=$(PHOTON_BUILD_NUMBER) \
			-e PHOTON_RELEASE_VERSION=$(PHOTON_RELEASE_VERSION) \
			-v `pwd`:/workspace \
			photon-build \
			./support/dockerfiles/photon/make-docker-image.sh; \
	fi

k8s-docker-images: photon-docker-image check-tools $(PHOTON_PACKAGES)
	mkdir -p $(PHOTON_STAGE)/docker_images && cd ./support/dockerfiles/k8s-docker-images && \
	./build-k8s-base-image.sh $(PHOTON_RELEASE_VERSION) $(PHOTON_BUILD_NUMBER) $(PHOTON_STAGE) && \
	for script_fn in build-k8s-docker-images.sh build-k8s-metrics-server-image.sh \
					build-k8s-coredns-image.sh build-k8s-dns-docker-images.sh \
					build-k8s-dns-docker-images.sh build-k8s-dashboard-docker-images.sh \
					build-flannel-docker-image.sh build-calico-docker-images.sh \
					build-k8s-heapster-image.sh build-k8s-nginx-ingress.sh \
					build-wavefront-proxy-docker-image.sh; do \
		./$$script_fn $(PHOTON_DIST_TAG) $(PHOTON_RELEASE_VERSION) $(PHOTON_SPECS_DIR) $(PHOTON_STAGE); \
	done

ostree-repo: check-tools $(PHOTON_PACKAGES)
	@if [ -f $(PHOTON_STAGE)/ostree-repo.tar.gz ]; then \
		echo "ostree-repo.tar.gz already present, not creating again..."; \
	else \
		echo "Creating OSTree repo from local RPMs in ostree-repo.tar.gz..."; \
		$(SRCROOT)/support/image-builder/ostree-tools/make-ostree-image.sh $(SRCROOT) $(PHOTON_DOCKER_IMAGE); \
	fi
#===============================================================================

# Set up Build environment
#_______________________________________________________________________________
packages-cached:
	@echo "Using cached RPMS..."
	@$(RM) -f $(PHOTON_RPMS_DIR_NOARCH)/* && \
	$(RM) -f $(PHOTON_RPMS_DIR_ARCH)/* && \
	$(CP) -f $(PHOTON_CACHE_PATH)/RPMS/noarch/* $(PHOTON_RPMS_DIR_NOARCH)/ && \
	$(CP) -f $(PHOTON_CACHE_PATH)/RPMS/$(ARCH)/* $(PHOTON_RPMS_DIR_ARCH)/
	$(PHOTON_REPO_TOOL) $(PHOTON_REPO_TOOL_OPT) $(PHOTON_RPMS_DIR)

sources:
	@$(MKDIR) -p $(PHOTON_SRCS_DIR)

sources-cached:
	@echo "Using cached SOURCES..."
	@ln -sf $(PHOTON_SOURCES_PATH) $(PHOTON_SRCS_DIR)

publish-rpms:
	@echo "Pulling toolchain rpms..."
	@cd $(PHOTON_PULL_PUBLISH_RPMS_DIR) && \
	$(PHOTON_PULL_PUBLISH_RPMS) $(PHOTON_PUBLISH_RPMS_DIR) $(PHOTON_PUBLISH_RPMS_URL) rpmfilelist

publish-x-rpms:
	@echo "Pulling X toolchain rpms..."
	@cd $(PHOTON_PULL_PUBLISH_RPMS_DIR) && \
	$(PHOTON_PULL_PUBLISH_RPMS) $(PHOTON_PUBLISH_XRPMS_DIR) $(PHOTON_PUBLISH_X_RPMS_URL) xrpmfilelist

publish-rpms-cached:
	@echo "Using cached toolchain rpms..."
	cd $(PHOTON_PULL_PUBLISH_RPMS_DIR) && \
	$(PHOTON_PULL_PUBLISH_RPMS_CACHED) $(PHOTON_PUBLISH_RPMS_DIR) $(PHOTON_PUBLISH_RPMS_PATH) rpmfilelist

publish-x-rpms-cached:
	@echo "Using cached X toolchain rpms..."
	cd $(PHOTON_PULL_PUBLISH_RPMS_DIR) && \
	$(PHOTON_PULL_PUBLISH_RPMS_CACHED) $(PHOTON_PUBLISH_XRPMS_DIR) $(PHOTON_PUBLISH_XRPMS_PATH) xrpmfilelist

photon-stage:
	@echo "Creating staging folder and subitems..."
	@test -d $(PHOTON_STAGE) || $(MKDIR) -p $(PHOTON_STAGE)
	@test -d $(PHOTON_CHROOT_PATH) || $(MKDIR) -p $(PHOTON_CHROOT_PATH)
	@test -d $(PHOTON_RPMS_DIR_NOARCH) || $(MKDIR) -p $(PHOTON_RPMS_DIR_NOARCH)
	@test -d $(PHOTON_RPMS_DIR_ARCH) || $(MKDIR) -p $(PHOTON_RPMS_DIR_ARCH)
	@test -d $(PHOTON_SRPMS_DIR) || $(MKDIR) -p $(PHOTON_SRPMS_DIR)
	@test -d $(PHOTON_UPDATED_RPMS_DIR_NOARCH) || $(MKDIR) -p $(PHOTON_UPDATED_RPMS_DIR_NOARCH)
	@test -d $(PHOTON_UPDATED_RPMS_DIR_ARCH) || $(MKDIR) -p $(PHOTON_UPDATED_RPMS_DIR_ARCH)
	@test -d $(PHOTON_SRCS_DIR) || $(MKDIR) -p $(PHOTON_SRCS_DIR)
	@test -d $(PHOTON_LOGS_DIR) || $(MKDIR) -p $(PHOTON_LOGS_DIR)
	@install -m 444 $(SRCROOT)/COPYING $(PHOTON_STAGE)/COPYING
	@install -m 444 $(SRCROOT)/NOTICE-GPL2.0 $(PHOTON_STAGE)/NOTICE-GPL2.0
	@install -m 444 $(SRCROOT)/NOTICE-Apachev2 $(PHOTON_STAGE)/NOTICE-Apachev2
#_______________________________________________________________________________

# Clean build environment
#==================================================================
clean: clean-install clean-chroot
	@echo "Deleting Photon ISO..."
	@$(RM) -f $(PHOTON_STAGE)/photon-*.iso
	@echo "Deleting stage dir..."
	@$(RMDIR) $(PHOTON_STAGE)
	@echo "Deleting chroot path..."
	@$(RMDIR) $(PHOTON_CHROOT_PATH)
	@echo "Deleting tools/bin..."
	@$(RMDIR) $(TOOLS_BIN)

clean-install:
	@echo "Cleaning installer working directory..."
	@if [ -d $(PHOTON_STAGE)/photon_iso ]; then \
		$(PHOTON_CHROOT_CLEANER) $(PHOTON_STAGE)/photon_iso; \
	fi

clean-chroot:
	@echo "Cleaning chroot path..."
	@if [ -d $(PHOTON_CHROOT_PATH) ]; then \
		$(PHOTON_CHROOT_CLEANER) $(PHOTON_CHROOT_PATH); \
	fi

# Targets to check for tools support in build environment
check-tools: check-bison check-g++ check-gawk check-repo-tool check-texinfo check-sanity check-docker check-pyopenssl ph3-docker-img-import check-git-hooks

ph3-docker-img-import: check-docker
	@echo ""
	@$(SRCROOT)/tools/scripts/ph3-docker-img-import.sh $(PH3_DOCKER_IMG_URL) $(PHOTON_DOCKER_IMAGE) $(PHOTON_BUILDER_TAG) || exit 1

check-git-hooks:
	@$(SRCROOT)/tools/scripts/check_git_hooks.sh "$(SRCROOT)"

check-docker:
ifeq (,$(wildcard $(DOCKER_ENV)))
	@command -v docker >/dev/null 2>&1 || { echo "Package docker not installed. Aborting." >&2; exit 1; }
endif

	@systemctl start docker

ifeq (,$(wildcard $(DOCKER_ENV)))
	@docker ps >/dev/null 2>&1 || { echo "Docker service is not running. Aborting." >&2; exit 1; }
endif

ifeq (,$(wildcard $(DOCKER_ENV)))
	@python3 -c "import docker; assert docker.__version__ >= '$(PHOTON_DOCKER_PY_VER)'" >/dev/null 2>&1 || { echo "Error: Python3 package docker-py3 $(PHOTON_DOCKER_PY_VER) not installed.\nPlease use: pip3 install docker==$(PHOTON_DOCKER_PY_VER)" >&2; exit 1; }
endif

check-pyopenssl:
	@python3 -c "import OpenSSL" > /dev/null 2>&1 || { echo "Error pyOpenSSL package not installed.\nPlease use: pip3 install pyOpenSSL" >&2; exit 1; }

check-bison:
	@command -v bison >/dev/null 2>&1 || { echo "Package bison not installed. Aborting." >&2; exit 1; }

check-texinfo:
	@command -v makeinfo >/dev/null 2>&1 || { echo "Package texinfo not installed. Aborting." >&2; exit 1; }

check-g++:
	@command -v g++ >/dev/null 2>&1 || { echo "Package g++ not installed. Aborting." >&2; exit 1; }

check-gawk:
	@command -v gawk >/dev/null 2>&1 || { echo "Package gawk not installed. Aborting." >&2; exit 1; }

check-repo-tool:
	@command -v $(PHOTON_REPO_TOOL) >/dev/null 2>&1 || { echo "Package $(PHOTON_REPO_TOOL) not installed. Aborting." >&2; exit 1; }

check-kpartx:
	@command -v kpartx >/dev/null 2>&1 || { echo "Package kpartx not installed. Aborting." >&2; exit 1; }

check-sanity:
	@$(SRCROOT)/tools/scripts/sanity_check.sh
	@echo ""

install-photon-docker-image: photon-docker-image
	docker build -t photon:tdnf .
#__________________________________________________________________________________

# Spec file checker and utilities
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
check-spec-files:
	@echo ""
	@./tools/scripts/check_spec_files.sh $(BASE_COMMIT)

generate-dep-lists:
	@echo ""
	@$(RMDIR) $(PHOTON_GENERATED_DATA_DIR)
	@$(MKDIR) -p $(PHOTON_GENERATED_DATA_DIR)
	@cd $(PHOTON_SPECDEPS_DIR) && \
	$(PHOTON_SPECDEPS) \
		--spec-path $(PHOTON_SPECS_DIR) \
		--stage-dir $(PHOTON_STAGE) \
		--log-path $(PHOTON_LOGS_DIR) \
		--log-level $(LOGLEVEL) \
		--pkg $(PHOTON_GENERATED_DATA_DIR) \
		--input-type=json \
		--file "$$(ls $(PHOTON_DATA_DIR)/packages_*.json)" \
		--display-option json \
		--input-data-dir $(PHOTON_DATA_DIR)
	@echo ""

pkgtree:
	@cd $(PHOTON_SPECDEPS_DIR) && \
		$(PHOTON_SPECDEPS) \
			--spec-path $(PHOTON_SPECS_DIR) \
			--log-level $(LOGLEVEL) \
			--input-type pkg \
			--pkg $(pkg)

imgtree:
	@cd $(PHOTON_SPECDEPS_DIR) && \
		$(PHOTON_SPECDEPS) \
			--spec-path $(PHOTON_SPECS_DIR) \
			--log-level $(LOGLEVEL) \
			--input-type json \
			--file $(PHOTON_DATA_DIR)/packages_$(img).json

who-needs:
	@cd $(PHOTON_SPECDEPS_DIR) && \
		$(PHOTON_SPECDEPS) \
			--spec-path $(PHOTON_SPECS_DIR) \
			--log-level $(LOGLEVEL) \
			--input-type who-needs \
			--pkg $(pkg)

print-upward-deps:
	@cd $(PHOTON_SPECDEPS_DIR) && \
		$(PHOTON_SPECDEPS) \
			--spec-path $(PHOTON_SPECS_DIR) \
			--input-type print-upward-deps \
			--pkg $(pkg)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

generate-yaml-files: check-tools photon-stage $(PHOTON_PACKAGES)
	@echo "Generating yaml files for packages ..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
	$(PHOTON_GENERATE_OSS_FILES) --generate-yaml-files \
		--spec-path $(PHOTON_SPECS_DIR) \
		--source-rpm-path $(PHOTON_SRPMS_DIR) \
		--log-path $(PHOTON_LOGS_DIR) \
		--dist-tag $(PHOTON_DIST_TAG) \
		--log-level $(LOGLEVEL) \
		--pullsources-config $(PHOTON_PULLSOURCES_CONFIG) \
		--pkg-blacklist-file $(PHOTON_PKG_BLACKLIST_FILE)

# Input args: BASE_COMMIT= (optional)
#
# This target removes staged RPMS that can be affected by change(s) and should
# be rebuilt as part of incremental build support
# For every spec file touched - remove all upward dependent packages (rpms)
# If support folder was touched - do full build
#
# The analyzed changes are:
# - commits from BASE_COMMIT to HEAD (if BASE_COMMIT= parameter is specified)
# - local changes (if no commits specified)

clean-stage-for-incremental-build:
	@test -n "$$(git diff --name-only @~1 @ | grep '^support/\(make\|package-builder\|pullpublishrpms\)')" && { echo "Remove all staged RPMs"; $(RM) -rf $(PHOTON_RPMS_DIR); } || :
	@if [ -d "$(PHOTON_RPMS_DIR)" ]; then \
		$(eval PKG_LIST := $$(shell echo `git diff --name-only $(BASE_COMMIT) @ | grep '\.spec' | xargs -n1 basename 2>/dev/null` | tr ' ' :)) \
		if [ -n "$(PKG_LIST)" ]; then \
			$(PHOTON_SPECDEPS) --spec-path $(PHOTON_SPECS_DIR) -i remove-upward-deps -p $(PKG_LIST); \
		fi; \
	else \
		echo "$(PHOTON_RPMS_DIR) does not exist, return ..."; \
	fi

clean-stage-rpms:
	@python3 $(SRCROOT)/tools/scripts/clean-stage-rpms.py --top-dir $(SRCROOT)
