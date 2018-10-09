#
# Copyright VMware, Inc 2015
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
PHOTON_RPMCHECK_FLAGS := -u
else ifeq ($(RPMCHECK),enable_stop_on_error)
PHOTON_RPMCHECK_FLAGS := -u -q
else
PHOTON_RPMCHECK_FLAGS :=
endif

# KAT build for FIPS certification
ifdef KAT_BUILD
PHOTON_KAT_BUILD_FLAGS := -F $(KAT_BUILD)
endif

ifeq ($(BUILDDEPS),true)
PUBLISH_BUILD_DEPENDENCIES := -bd True
else
PUBLISH_BUILD_DEPENDENCIES :=
endif

ifdef WEIGHTS
PACKAGE_WEIGHTS_PATH = -pw $(WEIGHTS)
else
PACKAGE_WEIGHTS_PATH =
endif

TOOLS_BIN := $(SRCROOT)/tools/bin
CONTAIN := $(TOOLS_BIN)/contain
ifeq ($(ARCH),x86_64)
VIXDISKUTIL := $(TOOLS_BIN)/vixdiskutil
IMGCONVERTER := $(TOOLS_BIN)/imgconverter
else
VIXDISKUTIL :=
IMGCONVERTER :=
endif

$(TOOLS_BIN):
	mkdir -p $(TOOLS_BIN)

$(CONTAIN): $(TOOLS_BIN)
	gcc -O2 -std=gnu99 -Wall -Wextra $(SRCROOT)/tools/src/contain/*.c -o $@_unpriv
	sudo install -o root -g root -m 4755 $@_unpriv $@

$(VIXDISKUTIL): $(TOOLS_BIN)
	@cd $(SRCROOT)/tools/src/vixDiskUtil && \
	make

$(IMGCONVERTER): $(TOOLS_BIN)
	@cd $(SRCROOT)/tools/src/imgconverter && \
	make

.PHONY : all iso clean cloud-image \
check-tools check-docker check-bison check-g++ check-gawk check-repo-tool check-kpartx check-sanity \
clean-install clean-chroot build-updated-packages check generate-yaml-files

THREADS?=1
LOGLEVEL?=info

# Build targets for rpm build
#-------------------------------------------------------------------------------
packages-minimal: check-tools $(PHOTON_STAGE) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) generate-dep-lists
	@echo "Building all minimal RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_RPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -y $(LOGLEVEL) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -c $(PHOTON_PULLSOURCES_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                $(PHOTON_RPMCHECK_FLAGS) \
		$(PUBLISH_BUILD_DEPENDENCIES) \
		$(PACKAGE_WEIGHTS_PATH) \
                -t ${THREADS}

packages: check-docker-py check-tools $(PHOTON_STAGE) $(PHOTON_PUBLISH_XRPMS) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) check-spec-files generate-dep-lists
	@echo "Building all RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) \
                -bt $(PHOTON_BUILD_TYPE) \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_RPMS_DIR) \
                -a $(PHOTON_SRPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -y $(LOGLEVEL) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -e $(PHOTON_PUBLISH_XRPMS_DIR) \
                -c $(PHOTON_PULLSOURCES_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                -w $(PHOTON_STAGE)/pkg_info.json \
                -g $(PHOTON_DATA_DIR)/pkg_build_options.json \
                $(PHOTON_RPMCHECK_FLAGS) \
		$(PHOTON_KAT_BUILD_FLAGS) \
		$(PUBLISH_BUILD_DEPENDENCIES) \
		$(PACKAGE_WEIGHTS_PATH) \
                -t ${THREADS}

packages-docker: check-docker-py check-docker-service check-tools $(PHOTON_STAGE) $(PHOTON_PUBLISH_XRPMS) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	@echo "Building all RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) \
                -bt $(PHOTON_BUILD_TYPE) \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_RPMS_DIR) \
                -a $(PHOTON_SRPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -y $(LOGLEVEL) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -e $(PHOTON_PUBLISH_XRPMS_DIR) \
                -c $(PHOTON_PULLSOURCES_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                -w $(PHOTON_STAGE)/pkg_info.json \
                -g $(PHOTON_DATA_DIR)/pkg_build_options.json \
                $(PHOTON_RPMCHECK_FLAGS) \
		$(PUBLISH_BUILD_DEPENDENCIES) \
		$(PACKAGE_WEIGHTS_PATH) \
                -t ${THREADS}

updated-packages: check-tools $(PHOTON_STAGE) $(PHOTON_PUBLISH_XRPMS) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	@echo "Building only updated RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_UPDATED_RPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -y $(LOGLEVEL) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -e $(PHOTON_PUBLISH_XRPMS_DIR) \
                -c $(PHOTON_PULLSOURCES_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                -k $(PHOTON_INPUT_RPMS_DIR) \
		$(PHOTON_KAT_BUILD_FLAGS) \
                $(PHOTON_RPMCHECK_FLAGS) \
		$(PUBLISH_BUILD_DEPENDENCIES) \
		$(PACKAGE_WEIGHTS_PATH) \
                -t ${THREADS}

tool-chain-stage1: check-tools $(PHOTON_STAGE) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	@echo "Building all RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_RPMS_DIR) \
                -a $(PHOTON_SRPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -y $(LOGLEVEL) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -t ${THREADS} \
                -c $(PHOTON_PULLSOURCES_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                $(PHOTON_RPMCHECK_FLAGS) \
                -m stage1

tool-chain-stage2: check-tools $(PHOTON_STAGE) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	@echo "Building all RPMS..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_RPMS_DIR) \
                -a $(PHOTON_SRPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -y $(LOGLEVEL) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -t ${THREADS} \
                -c $(PHOTON_PULLSOURCES_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                $(PHOTON_RPMCHECK_FLAGS) \
                -m stage2

%: check-tools $(PHOTON_PUBLISH_RPMS) $(PHOTON_PUBLISH_XRPMS) $(PHOTON_SOURCES) $(CONTAIN) check-spec-files $(eval PKG_NAME = $@)
	$(eval PKG_NAME = $@)
	@echo ""
	@echo "Building package $(PKG_NAME) ..."
	@echo ""
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) -i $(PKG_NAME)\
                              -bt $(PHOTON_BUILD_TYPE) \
                              -b $(PHOTON_CHROOT_PATH) \
                              -s $(PHOTON_SPECS_DIR) \
                              -r $(PHOTON_RPMS_DIR) \
                              -a $(PHOTON_SRPMS_DIR) \
                              -x $(PHOTON_SRCS_DIR) \
                              -p $(PHOTON_PUBLISH_RPMS_DIR) \
                              -e $(PHOTON_PUBLISH_XRPMS_DIR) \
                              -c $(PHOTON_PULLSOURCES_CONFIG) \
                              -y $(LOGLEVEL) \
                              -d $(PHOTON_DIST_TAG) \
                              -n $(PHOTON_BUILD_NUMBER) \
                              -v $(PHOTON_RELEASE_VERSION) \
                              -g $(PHOTON_DATA_DIR)/pkg_build_options.json \
                              $(PHOTON_RPMCHECK_FLAGS) \
				$(PHOTON_KAT_BUILD_FLAGS) \
                              -l $(PHOTON_LOGS_DIR) \
			      -t ${THREADS}
#-------------------------------------------------------------------------------

# The targets listed under "all" are the installer built artifacts
#===============================================================================
all: iso photon-docker-image k8s-docker-images cloud-image-all src-iso

iso: check-tools $(PHOTON_STAGE) $(PHOTON_PACKAGES)
	@echo "Building Photon Full ISO..."
	@cd $(PHOTON_INSTALLER_DIR) && \
        sudo $(PHOTON_INSTALLER) \
                -i $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso \
                -k $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).debug.iso \
                -w $(PHOTON_STAGE)/photon_iso \
                -l $(PHOTON_STAGE)/LOGS \
                -y $(LOGLEVEL) \
                -r $(PHOTON_STAGE)/RPMS \
                -x $(PHOTON_STAGE)/SRPMS \
                -p $(PHOTON_GENERATED_DATA_DIR)/$(FULL_PACKAGE_LIST_FILE) \
                -o $(PHOTON_STAGE)/common/data \
                -d $(PHOTON_STAGE)/pkg_info.json \
                -s $(PHOTON_DATA_DIR) \
                -f > \
                $(PHOTON_LOGS_DIR)/installer.log 2>&1

src-iso: check-tools $(PHOTON_STAGE) $(PHOTON_PACKAGES)
	@echo "Building Photon Full Source ISO..."
	@cd $(PHOTON_INSTALLER_DIR) && \
        sudo $(PHOTON_INSTALLER) \
                -j $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).src.iso \
                -w $(PHOTON_STAGE)/photon_iso \
                -l $(PHOTON_STAGE)/LOGS \
                -y $(LOGLEVEL) \
                -r $(PHOTON_STAGE)/RPMS \
                -x $(PHOTON_STAGE)/SRPMS \
                -p $(PHOTON_GENERATED_DATA_DIR)/$(FULL_PACKAGE_LIST_FILE) \
                -o $(PHOTON_STAGE)/common/data \
                -d $(PHOTON_STAGE)/pkg_info.json \
                -s $(PHOTON_DATA_DIR) \
                -f > \
                $(PHOTON_LOGS_DIR)/sourceiso-installer.log 2>&1

cloud-image: check-kpartx $(PHOTON_STAGE) $(VIXDISKUTIL) $(IMGCONVERTER) $(PHOTON_PACKAGES)
	@echo "Building cloud image $(IMG_NAME)..."
	@cd $(PHOTON_CLOUD_IMAGE_BUILDER_DIR)
	$(PHOTON_CLOUD_IMAGE_BUILDER) $(PHOTON_CLOUD_IMAGE_BUILDER_DIR) $(IMG_NAME) $(SRCROOT) $(PHOTON_GENERATED_DATA_DIR) $(PHOTON_STAGE) $(ADDITIONAL_RPMS_PATH)


cloud-image-all: check-kpartx $(PHOTON_STAGE) $(VIXDISKUTIL) $(IMGCONVERTER) $(PHOTON_PACKAGES)
	@echo "Building cloud images - gce, ami, azure and ova..."
	@cd $(PHOTON_CLOUD_IMAGE_BUILDER_DIR)
	$(PHOTON_CLOUD_IMAGE_BUILDER) $(PHOTON_CLOUD_IMAGE_BUILDER_DIR) gce $(SRCROOT) $(PHOTON_GENERATED_DATA_DIR) $(PHOTON_STAGE) $(ADDITIONAL_RPMS_PATH)
	$(PHOTON_CLOUD_IMAGE_BUILDER) $(PHOTON_CLOUD_IMAGE_BUILDER_DIR) ami $(SRCROOT) $(PHOTON_GENERATED_DATA_DIR) $(PHOTON_STAGE) $(ADDITIONAL_RPMS_PATH)
	$(PHOTON_CLOUD_IMAGE_BUILDER) $(PHOTON_CLOUD_IMAGE_BUILDER_DIR) azure $(SRCROOT) $(PHOTON_GENERATED_DATA_DIR) $(PHOTON_STAGE) $(ADDITIONAL_RPMS_PATH)
	$(PHOTON_CLOUD_IMAGE_BUILDER) $(PHOTON_CLOUD_IMAGE_BUILDER_DIR) ova $(SRCROOT) $(PHOTON_GENERATED_DATA_DIR) $(PHOTON_STAGE) $(ADDITIONAL_RPMS_PATH)
	$(PHOTON_CLOUD_IMAGE_BUILDER) $(PHOTON_CLOUD_IMAGE_BUILDER_DIR) ova_micro $(SRCROOT) $(PHOTON_GENERATED_DATA_DIR) $(PHOTON_STAGE) $(ADDITIONAL_RPMS_PATH)

photon-docker-image:
	$(PHOTON_REPO_TOOL) $(PHOTON_RPMS_DIR)
	sudo docker build --no-cache --tag photon-build ./support/dockerfiles/photon
	sudo docker run \
		-it \
		--rm \
		--privileged \
		--net=host \
		-e PHOTON_BUILD_NUMBER=$(PHOTON_BUILD_NUMBER) \
		-e PHOTON_RELEASE_VERSION=$(PHOTON_RELEASE_VERSION) \
		-v `pwd`:/workspace \
		photon-build \
		./support/dockerfiles/photon/make-docker-image.sh tdnf

k8s-docker-images: start-docker photon-docker-image
	mkdir -p $(PHOTON_STAGE)/docker_images && \
	cd ./support/dockerfiles/k8s-docker-images && \
	./build-k8s-base-image.sh $(PHOTON_RELEASE_VERSION) $(PHOTON_BUILD_NUMBER) $(PHOTON_STAGE)  && \
	./build-k8s-docker-images.sh $(PHOTON_DIST_TAG) $(PHOTON_RELEASE_VERSION) $(PHOTON_SPECS_DIR) $(PHOTON_STAGE) && \
	./build-k8s-metrics-server-image.sh $(PHOTON_DIST_TAG) $(PHOTON_RELEASE_VERSION) $(PHOTON_SPECS_DIR) $(PHOTON_STAGE)  && \
	./build-k8s-coredns-image.sh $(PHOTON_DIST_TAG) $(PHOTON_RELEASE_VERSION) $(PHOTON_SPECS_DIR) $(PHOTON_STAGE)  && \
	./build-k8s-dns-docker-images.sh $(PHOTON_DIST_TAG) $(PHOTON_RELEASE_VERSION) $(PHOTON_SPECS_DIR) $(PHOTON_STAGE) && \
	./build-k8s-dashboard-docker-images.sh $(PHOTON_DIST_TAG) $(PHOTON_RELEASE_VERSION) $(PHOTON_SPECS_DIR) $(PHOTON_STAGE) && \
	./build-flannel-docker-image.sh $(PHOTON_DIST_TAG) $(PHOTON_RELEASE_VERSION) $(PHOTON_SPECS_DIR) $(PHOTON_STAGE) && \
	./build-calico-docker-images.sh $(PHOTON_DIST_TAG) $(PHOTON_RELEASE_VERSION) $(PHOTON_SPECS_DIR) $(PHOTON_STAGE) && \
	./build-k8s-heapster-image.sh $(PHOTON_DIST_TAG) $(PHOTON_RELEASE_VERSION) $(PHOTON_SPECS_DIR) $(PHOTON_STAGE) && \
	./build-k8s-nginx-ingress.sh $(PHOTON_DIST_TAG) $(PHOTON_RELEASE_VERSION) $(PHOTON_SPECS_DIR) $(PHOTON_STAGE)  && \
	./build-wavefront-proxy-docker-image.sh $(PHOTON_DIST_TAG) $(PHOTON_RELEASE_VERSION) $(PHOTON_SPECS_DIR) $(PHOTON_STAGE)
#===============================================================================

# Set up Build environment
#_______________________________________________________________________________
packages-cached:
	@echo "Using cached RPMS..."
	@$(RM) -f $(PHOTON_RPMS_DIR_NOARCH)/* && \
     $(RM) -f $(PHOTON_RPMS_DIR_ARCH)/* && \
     $(CP) -f $(PHOTON_CACHE_PATH)/RPMS/noarch/* $(PHOTON_RPMS_DIR_NOARCH)/ && \
     $(CP) -f $(PHOTON_CACHE_PATH)/RPMS/$(ARCH)/* $(PHOTON_RPMS_DIR_ARCH)/

sources:
	@$(MKDIR) -p $(PHOTON_SRCS_DIR)

sources-cached:
	@echo "Using cached SOURCES..."
	@ln -sf $(PHOTON_SOURCES_PATH) $(PHOTON_SRCS_DIR)

publish-rpms:
	@echo "Pulling toolchain rpms from bintray..."
	@cd $(PHOTON_PULL_PUBLISH_RPMS_DIR) && \
	$(PHOTON_PULL_PUBLISH_RPMS) $(PHOTON_PUBLISH_RPMS_DIR)

publish-x-rpms:
	@echo "Pulling X toolchain rpms from bintray..."
	@cd $(PHOTON_PULL_PUBLISH_RPMS_DIR) && \
	$(PHOTON_PULL_PUBLISH_X_RPMS) $(PHOTON_PUBLISH_XRPMS_DIR)

publish-rpms-cached:
	@echo "Using cached publish rpms..."
	@$(MKDIR) -p $(PHOTON_PUBLISH_RPMS_DIR)/{$(ARCH),noarch} && \
	cd $(PHOTON_PULL_PUBLISH_RPMS_DIR) && \
        $(PHOTON_PULL_PUBLISH_RPMS) $(PHOTON_PUBLISH_RPMS_DIR) $(PHOTON_PUBLISH_RPMS_PATH)

publish-x-rpms-cached:
	@echo "Using ..."
	@$(MKDIR) -p $(PHOTON_PUBLISH_XRPMS_DIR)/{$(ARCH),noarch} && \
	cd $(PHOTON_PULL_PUBLISH_RPMS_DIR) && \
        $(PHOTON_PULL_PUBLISH_X_RPMS) $(PHOTON_PUBLISH_XRPMS_DIR) $(PHOTON_PUBLISH_XRPMS_PATH)

$(PHOTON_STAGE):
	@echo "Creating staging folder..."
	$(MKDIR) -p $(PHOTON_STAGE)
	@echo "Creating chroot path..."
	$(MKDIR) -p $(PHOTON_CHROOT_PATH)
	@echo "Building RPMS folders..."
	@test -d $(PHOTON_RPMS_DIR_NOARCH) || $(MKDIR) -p $(PHOTON_RPMS_DIR_NOARCH)
	@test -d $(PHOTON_RPMS_DIR_ARCH) || $(MKDIR) -p $(PHOTON_RPMS_DIR_ARCH)
	@echo "Building SRPMS folders..."
	@test -d $(PHOTON_SRPMS_DIR) || $(MKDIR) -p $(PHOTON_SRPMS_DIR)
	@echo "Building UPDATED_RPMS folders..."
	@test -d $(PHOTON_UPDATED_RPMS_DIR_NOARCH) || $(MKDIR) -p $(PHOTON_UPDATED_RPMS_DIR_NOARCH)
	@test -d $(PHOTON_UPDATED_RPMS_DIR_ARCH) || $(MKDIR) -p $(PHOTON_UPDATED_RPMS_DIR_ARCH)
	@echo "Building SOURCES folder..."
	@test -d $(PHOTON_SRCS_DIR) || $(MKDIR) -p $(PHOTON_SRCS_DIR)
	@echo "Building LOGS folder..."
	@test -d $(PHOTON_LOGS_DIR) || $(MKDIR) -p $(PHOTON_LOGS_DIR)
	@echo "Creating COPYING file..."
	install -m 444 $(SRCROOT)/COPYING $(PHOTON_STAGE)/COPYING
	@echo "Creating open_source_license.txt file..."
	install -m 444 $(SRCROOT)/installer/open_source_license.txt $(PHOTON_STAGE)/open_source_license.txt
	@echo "Creating NOTICE file..."
	install -m 444 $(SRCROOT)/NOTICE $(PHOTON_STAGE)/NOTICE
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

#==================================================================

# Targets to check for tools support in build environment
#__________________________________________________________________________________
check-tools: check-bison check-g++ check-gawk check-repo-tool check-texinfo check-sanity check-docker

check-docker:
	@command -v docker >/dev/null 2>&1 || { echo "Package docker not installed. Aborting." >&2; exit 1; }

check-docker-service:
	@docker ps >/dev/null 2>&1 || { echo "Docker service is not running. Aborting." >&2; exit 1; }

check-docker-py:
	@python3 -c "import docker; assert docker.__version__ == '$(PHOTON_DOCKER_PY_VER)'" >/dev/null 2>&1 || { echo "Error: Python3 package docker-py3 2.3.0 not installed.\nPlease use: pip3 install docker==2.3.0" >&2; exit 1; }

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
	@$(SRCROOT)/support/sanity_check.sh
	@echo ""

start-docker: check-docker
	systemctl start docker

install-photon-docker-image: photon-docker-image
	sudo docker build -t photon:tdnf .
#__________________________________________________________________________________

check: packages
    ifeq ($(RPMCHECK),enable_stop_on_error)
	    $(eval rpmcheck_stop_on_error = -q)
    endif
	@echo "Testing all RPMS ..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) \
                -bt $(PHOTON_BUILD_TYPE) \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_RPMS_DIR) \
                -a $(PHOTON_SRPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -y $(LOGLEVEL) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -e $(PHOTON_PUBLISH_XRPMS_DIR) \
                -c $(PHOTON_PULLSOURCES_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                -w $(PHOTON_DATA_DIR)/pkg_info.json \
                -g $(PHOTON_DATA_DIR)/pkg_build_options.json \
                -u \
                $(rpmcheck_stop_on_error) \
                -t ${THREADS}

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
		-s $(PHOTON_SPECS_DIR) \
		-t $(PHOTON_STAGE) \
		-l $(PHOTON_LOGS_DIR) \
	        -y $(LOGLEVEL) \
		-p $(PHOTON_GENERATED_DATA_DIR) \
		--input-type=json \
		--file "$$(ls $(PHOTON_DATA_DIR)/build_install_options*.json)" \
		-d json \
		-a $(PHOTON_DATA_DIR)
	@echo ""
pkgtree:
	@cd $(PHOTON_SPECDEPS_DIR) && \
		$(PHOTON_SPECDEPS) -s $(PHOTON_SPECS_DIR) -y $(LOGLEVEL) -i pkg -p $(pkg)

imgtree:
	@cd $(PHOTON_SPECDEPS_DIR) && \
		$(PHOTON_SPECDEPS) -s $(PHOTON_SPECS_DIR) -y $(LOGLEVEL) -i json -f $(PHOTON_DATA_DIR)/build_install_options_$(img).json

who-needs:
	@cd $(PHOTON_SPECDEPS_DIR) && \
		$(PHOTON_SPECDEPS) -s $(PHOTON_SPECS_DIR) -y $(LOGLEVEL) -i who-needs -p $(pkg)

print-upward-deps:
	@cd $(PHOTON_SPECDEPS_DIR) && \
		$(PHOTON_SPECDEPS) -s $(PHOTON_SPECS_DIR) -i print-upward-deps -p $(pkg)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

generate-yaml-files: check-tools $(PHOTON_STAGE) $(PHOTON_PACKAGES)
	@echo "Generating yaml files for packages ..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_GENERATE_OSS_FILES) -y \
                              -s $(PHOTON_SPECS_DIR) \
                              -a $(PHOTON_SRPMS_DIR) \
                              -l $(PHOTON_LOGS_DIR) \
                              -z $(LOGLEVEL) \
                              -c $(PHOTON_PULLSOURCES_CONFIG) \
                              -f $(PHOTON_PKG_BLACKLIST_FILE)

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
	@test -n "$$(git diff --name-only $(BASE_COMMIT) @ | grep SPECS)" && $(PHOTON_SPECDEPS) -s $(PHOTON_SPECS_DIR) -i remove-upward-deps -p $$(echo `git diff --name-only $(BASE_COMMIT) @ | grep .spec | xargs -n1 basename 2>/dev/null` | tr ' ' :) ||:
	@test -n "$$(git diff --name-only $(BASE_COMMIT) @ | grep support)" && $(RM) -rf $(PHOTON_RPMS_DIR) ||:

