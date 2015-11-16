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
PHOTON_PACKAGES_MICRO := packages-cached
PHOTON_PACKAGES_MINIMAL := packages-cached
PHOTON_PACKAGES := packages-cached
else
PHOTON_PACKAGES_MICRO := packages-micro
PHOTON_PACKAGES_MINIMAL := packages-minimal
PHOTON_PACKAGES := packages
endif

ifdef PHOTON_SOURCES_PATH
PHOTON_SOURCES := sources-cached
else
PHOTON_SOURCES ?= sources
endif

MINIMAL_PACKAGE_LIST_FILE := build_install_options_minimal.json
MICRO_PACKAGE_LIST_FILE := build_install_options_micro.json
FULL_PACKAGE_LIST_FILE := build_install_options_all.json

ifdef PHOTON_PUBLISH_RPMS_PATH
PHOTON_PUBLISH_RPMS := publish-rpms-cached
else
PHOTON_PUBLISH_RPMS := publish-rpms
endif

TOOLS_BIN := $(SRCROOT)/tools/bin
CONTAIN := $(TOOLS_BIN)/contain

.PHONY : all iso clean photon-build-machine photon-vagrant-build photon-vagrant-local cloud-image \
check check-docker check-bison check-g++ check-gawk check-createrepo check-vagrant check-packer check-packer-ovf-plugin check-sanity \
clean-install clean-chroot build-updated-packages

THREADS?=1

all: iso minimal-iso docker-image ostree-host-iso live-iso cloud-image-all

micro: micro-iso
	@:

micro-iso: check $(PHOTON_STAGE) $(PHOTON_PACKAGES_MICRO)
	@echo "Building Photon Micro ISO..."
	@cd $(PHOTON_INSTALLER_DIR) && \
        $(PHOTON_INSTALLER) \
                -i $(PHOTON_STAGE)/photon-micro-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso \
                -w $(PHOTON_STAGE)/photon_iso \
                -l $(PHOTON_STAGE)/LOGS \
                -r $(PHOTON_STAGE)/RPMS \
                -p $(PHOTON_GENERATED_DATA_DIR)/$(MICRO_PACKAGE_LIST_FILE) \
                -o $(PHOTON_STAGE)/common/data \
                -f > \
                $(PHOTON_LOGS_DIR)/installer.log 2>&1

packages-micro: check $(PHOTON_STAGE) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) generate-dep-lists
	@echo "Building all Micro RPMS..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) -o full \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_RPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -j $(PHOTON_GENERATED_DATA_DIR)/$(MICRO_PACKAGE_LIST_FILE) \
                -c $(PHOTON_BINTRAY_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                -t ${THREADS}

minimal: minimal-iso
	@:

minimal-iso: check $(PHOTON_STAGE) $(PHOTON_PACKAGES_MINIMAL)
	@echo "Building Photon Minimal ISO..."
	@cd $(PHOTON_INSTALLER_DIR) && \
        $(PHOTON_INSTALLER) \
                -i $(PHOTON_STAGE)/photon-minimal-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso \
                -w $(PHOTON_STAGE)/photon_iso \
                -l $(PHOTON_STAGE)/LOGS \
                -r $(PHOTON_STAGE)/RPMS \
                -p $(PHOTON_GENERATED_DATA_DIR)/$(MINIMAL_PACKAGE_LIST_FILE) \
                -o $(PHOTON_STAGE)/common/data \
                -f > \
                $(PHOTON_LOGS_DIR)/installer.log 2>&1

ostree-host-iso: check $(PHOTON_STAGE) ostree-repo
	@echo "Building Photon OSTree Host ISO..."
	@cd $(PHOTON_INSTALLER_DIR) && \
        $(PHOTON_INSTALLER) \
                -i $(PHOTON_STAGE)/photon-ostree-host-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso \
                -w $(PHOTON_STAGE)/photon_iso \
                -l $(PHOTON_STAGE)/LOGS \
                -r $(PHOTON_STAGE)/RPMS \
                -p $(PHOTON_GENERATED_DATA_DIR)/build_install_options_ostreehost.json \
                -o $(PHOTON_STAGE)/common/data \
                -f > \
                $(PHOTON_LOGS_DIR)/installer.log 2>&1

live-iso: check $(PHOTON_STAGE) $(PHOTON_PACKAGES_MINIMAL) minimal-iso
	@echo "Building Photon Minimal LIVE ISO..."
	@cd $(PHOTON_INSTALLER_DIR) && \
        $(PHOTON_INSTALLER) \
                -i $(PHOTON_STAGE)/photon-live-iso-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso \
                -w $(PHOTON_STAGE)/photon_iso \
                -l $(PHOTON_STAGE)/LOGS \
                -r $(PHOTON_STAGE)/RPMS \
                -p $(PHOTON_GENERATED_DATA_DIR)/build_install_options_livecd.json \
                -o $(PHOTON_STAGE)/common/data \
                -f > \
                $(PHOTON_LOGS_DIR)/installer.log 2>&1

packages-minimal: check $(PHOTON_STAGE) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) generate-dep-lists
	@echo "Building all RPMS..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) -o full \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_RPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -j $(PHOTON_GENERATED_DATA_DIR)/$(MINIMAL_PACKAGE_LIST_FILE) \
                -c $(PHOTON_BINTRAY_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                -t ${THREADS}

iso: check $(PHOTON_STAGE) $(PHOTON_PACKAGES) ostree-repo
	@echo "Building Photon Full ISO..."
	@cd $(PHOTON_INSTALLER_DIR) && \
        sudo $(PHOTON_INSTALLER) \
                -i $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso \
                -w $(PHOTON_STAGE)/photon_iso \
                -l $(PHOTON_STAGE)/LOGS \
                -r $(PHOTON_STAGE)/RPMS \
                -p $(PHOTON_GENERATED_DATA_DIR)/$(FULL_PACKAGE_LIST_FILE) \
                -o $(PHOTON_STAGE)/common/data \
                -f > \
                $(PHOTON_LOGS_DIR)/installer.log 2>&1

pkgtree:
	@cd $(PHOTON_SPECDEPS_DIR) && \
		$(PHOTON_SPECDEPS) -s $(PHOTON_SPECS_DIR) -i pkg -p $(pkg)

imgtree:
	@cd $(PHOTON_SPECDEPS_DIR) && \
		$(PHOTON_SPECDEPS) -s $(PHOTON_SPECS_DIR) -i json -f $(PHOTON_DATA_DIR)/build_install_options_$(img).json

who-needs:
	@cd $(PHOTON_SPECDEPS_DIR) && \
		$(PHOTON_SPECDEPS) -s $(PHOTON_SPECS_DIR) -i who-needs -p $(pkg) 

packages: check $(PHOTON_STAGE) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	@echo "Building all RPMS..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) -o full \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_RPMS_DIR) \
                -a $(PHOTON_SRPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -j $(PHOTON_GENERATED_DATA_DIR)/$(FULL_PACKAGE_LIST_FILE) \
                -c $(PHOTON_BINTRAY_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                -t ${THREADS}

updated-packages: check $(PHOTON_STAGE) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	@echo "Building only updated RPMS..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) -o full \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_UPDATED_RPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -j $(PHOTON_GENERATED_DATA_DIR)/$(FULL_PACKAGE_LIST_FILE) \
                -c $(PHOTON_BINTRAY_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                -k $(PHOTON_INPUT_RPMS_DIR) \
                -t ${THREADS}

tool-chain-stage1: check $(PHOTON_STAGE) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	@echo "Building all RPMS..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) -o full \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_RPMS_DIR) \
                -a $(PHOTON_SRPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -j $(PHOTON_GENERATED_DATA_DIR)/$(FULL_PACKAGE_LIST_FILE) \
                -t ${THREADS} \
                -c $(PHOTON_BINTRAY_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                -m stage1

tool-chain-stage2: check $(PHOTON_STAGE) $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	@echo "Building all RPMS..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) -o full \
                -s $(PHOTON_SPECS_DIR) \
                -r $(PHOTON_RPMS_DIR) \
                -a $(PHOTON_SRPMS_DIR) \
                -x $(PHOTON_SRCS_DIR) \
                -b $(PHOTON_CHROOT_PATH) \
                -l $(PHOTON_LOGS_DIR) \
                -p $(PHOTON_PUBLISH_RPMS_DIR) \
                -j $(PHOTON_GENERATED_DATA_DIR)/$(FULL_PACKAGE_LIST_FILE) \
                -t ${THREADS} \
                -c $(PHOTON_BINTRAY_CONFIG) \
                -d $(PHOTON_DIST_TAG) \
                -n $(PHOTON_BUILD_NUMBER) \
                -v $(PHOTON_RELEASE_VERSION) \
                -m stage2


packages-cached:
	@echo "Using cached RPMS..."
	@$(RM) -f $(PHOTON_RPMS_DIR_NOARCH)/* && \
     $(RM) -f $(PHOTON_RPMS_DIR_X86_64)/* && \
     $(CP) -f $(PHOTON_CACHE_PATH)/RPMS/noarch/* $(PHOTON_RPMS_DIR_NOARCH)/ && \
     $(CP) -f $(PHOTON_CACHE_PATH)/RPMS/x86_64/* $(PHOTON_RPMS_DIR_X86_64)/

sources:
	@echo "Pulling sources from bintray...(nothing to do)"
	@$(MKDIR) -p $(PHOTON_SRCS_DIR)

sources-cached:
	@echo "Using cached SOURCES..."
	@$(MKDIR) -p $(PHOTON_SRCS_DIR) && \
	 $(CP) -rf $(PHOTON_SOURCES_PATH)/* $(PHOTON_SRCS_DIR)/

publish-rpms:
	@echo "Pulling publish rpms from bintray..."
	@cd $(PHOTON_PULL_PUBLISH_RPMS_DIR) && \
	$(PHOTON_PULL_PUBLISH_RPMS) $(PHOTON_PUBLISH_RPMS_DIR)

publish-rpms-cached:
	@echo "Using cached publish rpms..."
	@$(MKDIR) -p $(PHOTON_PUBLISH_RPMS_DIR) && \
	 $(CP) -rf $(PHOTON_PUBLISH_RPMS_PATH)/* $(PHOTON_PUBLISH_RPMS_DIR)/

$(PHOTON_STAGE):
	@echo "Creating staging folder..."
	$(MKDIR) -p $(PHOTON_STAGE)
	@echo "Creating chroot path..."
	$(MKDIR) -p $(PHOTON_CHROOT_PATH)
	@echo "Building RPMS folders..."
	@test -d $(PHOTON_RPMS_DIR_NOARCH) || $(MKDIR) -p $(PHOTON_RPMS_DIR_NOARCH)
	@test -d $(PHOTON_RPMS_DIR_X86_64) || $(MKDIR) -p $(PHOTON_RPMS_DIR_X86_64)
	@echo "Building SRPMS folders..."
	@test -d $(PHOTON_SRPMS_DIR) || $(MKDIR) -p $(PHOTON_SRPMS_DIR)
	@echo "Building UPDATED_RPMS folders..."
	@test -d $(PHOTON_UPDATED_RPMS_DIR_NOARCH) || $(MKDIR) -p $(PHOTON_UPDATED_RPMS_DIR_NOARCH)
	@test -d $(PHOTON_UPDATED_RPMS_DIR_X86_64) || $(MKDIR) -p $(PHOTON_UPDATED_RPMS_DIR_X86_64)
	@echo "Building SOURCES folder..."
	@test -d $(PHOTON_SRCS_DIR) || $(MKDIR) -p $(PHOTON_SRCS_DIR)
	@echo "Building LOGS folder..."
	@test -d $(PHOTON_LOGS_DIR) || $(MKDIR) -p $(PHOTON_LOGS_DIR)
	@echo "Creating data folder for generated files..."

generate-dep-lists:
	$(RMDIR) $(PHOTON_GENERATED_DATA_DIR)
	$(MKDIR) -p $(PHOTON_GENERATED_DATA_DIR)
	@for f in $$(ls $(PHOTON_DATA_DIR)/build_install_options*.json) ; \
	do \
		cp $$f $(PHOTON_GENERATED_DATA_DIR); \
		echo "Generating the install time dependency list for " $$f; \
		cd $(PHOTON_SPECDEPS_DIR) && \
		$(PHOTON_SPECDEPS) \
		-s $(PHOTON_SPECS_DIR) \
		-t $(PHOTON_STAGE) \
		--input-type=json --file $$f -d json -a $(PHOTON_DATA_DIR); \
	done

docker-image:
	sudo docker run \
		-it \
		--rm \
		--privileged \
		--net=host \
		-e PHOTON_BUILD_NUMBER=$(PHOTON_BUILD_NUMBER) \
		-e PHOTON_RELEASE_VERSION=$(PHOTON_RELEASE_VERSION) \
		-v `pwd`:/workspace \
		vmware/build-photon \
		./support/dockerfiles/photon/make-docker-image.sh tdnf

install-docker-image: docker-image
	sudo docker build -t photon:tdnf .

ostree-repo: $(PHOTON_PACKAGES)
	@echo "Creating OSTree repo from local PRMs in ostree-repo.tar.gz..."
	@if [ -f  $(PHOTON_STAGE)/ostree-repo.tar.gz ]; then \
		echo "ostree-repo.tar.gz already present, not creating again..."; \
	else \
		$(SRCROOT)/support/ostree-tools/make-ostree-image.sh $(SRCROOT); \
	fi

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

photon-build-machine: check-packer check-vagrant
	@echo "Building photon-build-machine with Packer..."
	@cd $(PHOTON_PACKER_TEMPLATES) && \
	$(PACKER) build photon-build-machine.json
	@echo "Adding box to Vagrant boxes..."
	@$(VAGRANT) box add $(PHOTON_PACKER_TEMPLATES)/photon-build-machine.box --name photon-build-machine --force && \
	$(RM) $(PHOTON_PACKER_TEMPLATES)/photon-build-machine.box

photon-vagrant-build: check-vagrant
	@echo "Starting Photon build using Vagrant..."
	@cd $(SRCROOT) && \
	$(VAGRANT) up && \
	$(VAGRANT) destroy -f

ifeq ($(VAGRANT_BUILD),all)
PACKER_ARGS=""
else
PACKER_ARGS="-only=$(VAGRANT_BUILD)"
endif

photon-vagrant-local: check-packer check-vagrant
	@echo "Building a Photon Vagrant box with Packer..."
	@if [ -e $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso ]; then \
		cd $(PHOTON_PACKER_TEMPLATES) && \
		$(SED) -i "" -e "s#\"iso_checksum_value\":.*#\"iso_checksum_value\": \"$$($(SHASUM) ../../stage/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso | cut -f 1 -d ' ')\",#" photon.json && \
		$(PACKER) build $(PACKER_ARGS) photon.json && \
		$(SED) -i "" -e "s#\"iso_checksum_value\":.*#\"iso_checksum_value\": \"\",#" photon.json; \
		echo "Moving boxes to $(PHOTON_STAGE)..." && \
		$(MV) *.box $(PHOTON_STAGE); \
	else \
		echo "Unable to find $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso ... aborting build"; \
	fi

cloud-image: $(PHOTON_STAGE) iso
	@echo "Building cloud image $(IMG_NAME)..."
	@cd $(PHOTON_CLOUD_IMAGE_BUILDER_DIR)
	$(PHOTON_CLOUD_IMAGE_BUILDER) $(PHOTON_CLOUD_IMAGE_BUILDER_DIR) $(IMG_NAME) $(SRCROOT) $(PHOTON_GENERATED_DATA_DIR) $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso $(ADDITIONAL_RPMS_PATH)


cloud-image-all: $(PHOTON_STAGE) iso
	@echo "Building cloud images - gce, ami, azure and ova..."
	@cd $(PHOTON_CLOUD_IMAGE_BUILDER_DIR)
	$(PHOTON_CLOUD_IMAGE_BUILDER) $(PHOTON_CLOUD_IMAGE_BUILDER_DIR) gce $(SRCROOT) $(PHOTON_GENERATED_DATA_DIR) $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso $(ADDITIONAL_RPMS_PATH)
	$(PHOTON_CLOUD_IMAGE_BUILDER) $(PHOTON_CLOUD_IMAGE_BUILDER_DIR) ami $(SRCROOT) $(PHOTON_GENERATED_DATA_DIR) $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso $(ADDITIONAL_RPMS_PATH)
	$(PHOTON_CLOUD_IMAGE_BUILDER) $(PHOTON_CLOUD_IMAGE_BUILDER_DIR) azure $(SRCROOT) $(PHOTON_GENERATED_DATA_DIR) $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso $(ADDITIONAL_RPMS_PATH)
	$(PHOTON_CLOUD_IMAGE_BUILDER) $(PHOTON_CLOUD_IMAGE_BUILDER_DIR) ova $(SRCROOT) $(PHOTON_GENERATED_DATA_DIR) $(PHOTON_STAGE)/photon-$(PHOTON_RELEASE_VERSION)-$(PHOTON_BUILD_NUMBER).iso $(ADDITIONAL_RPMS_PATH)


check: check-bison check-g++ check-gawk check-createrepo check-texinfo check-sanity check-docker

check-docker:
	@command -v docker >/dev/null 2>&1 || { echo "Package docker not installed. Aborting." >&2; exit 1; }

check-bison:
	@command -v bison >/dev/null 2>&1 || { echo "Package bison not installed. Aborting." >&2; exit 1; }

check-texinfo:
	@command -v makeinfo >/dev/null 2>&1 || { echo "Package texinfo not installed. Aborting." >&2; exit 1; }

check-g++:
	@command -v g++ >/dev/null 2>&1 || { echo "Package g++ not installed. Aborting." >&2; exit 1; }

check-gawk:
	@command -v gawk >/dev/null 2>&1 || { echo "Package gawk not installed. Aborting." >&2; exit 1; }

check-createrepo:
	@command -v createrepo >/dev/null 2>&1 || { echo "Package createrepo not installed. Aborting." >&2; exit 1; }

check-vagrant: check-packer
	@command -v $(VAGRANT) >/dev/null 2>&1 || { echo "Vagrant not installed or wrong path, expecting $(VAGRANT). Aborting" >&2; exit 1; }

check-sanity:
	$(SRCROOT)/support/sanity_check.sh

ifeq ($(VAGRANT_BUILD),vcloudair)
check-packer: check-packer-ovf-plugin
else ifeq ($(VAGRANT_BUILD),all)
check-packer: check-packer-ovf-plugin
else
check-packer:
endif
	@command -v $(PACKER) >/dev/null 2>&1 || { echo "Packer not installed or wrong path, expecting $(PACKER). Aborting" >&2; exit 1; }

check-packer-ovf-plugin:
	@[[ -e ~/.packer.d/plugins/packer-post-processor-vagrant-vmware-ovf ]] || { echo "Packer OVF post processor not installed. Aborting" >&2; exit 1; }

%: check $(PHOTON_PUBLISH_RPMS) $(PHOTON_SOURCES) $(CONTAIN) generate-dep-lists
	$(eval PKG_NAME = $@)
	@echo "Building package $(PKG_NAME) ..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
        $(PHOTON_PACKAGE_BUILDER) -i $(PKG_NAME)\
                              -b $(PHOTON_CHROOT_PATH) \
                              -s $(PHOTON_SPECS_DIR) \
                              -r $(PHOTON_RPMS_DIR) \
                              -a $(PHOTON_SRPMS_DIR) \
                              -x $(PHOTON_SRCS_DIR) \
                              -p $(PHOTON_PUBLISH_RPMS_DIR) \
                              -c $(PHOTON_BINTRAY_CONFIG) \
                              -d $(PHOTON_DIST_TAG) \
                              -n $(PHOTON_BUILD_NUMBER) \
                              -v $(PHOTON_RELEASE_VERSION) \
                              -l $(PHOTON_LOGS_DIR)

$(TOOLS_BIN):
	mkdir -p $(TOOLS_BIN)

$(CONTAIN): $(TOOLS_BIN)
	gcc -O2 -std=gnu99 -Wall -Wextra $(SRCROOT)/tools/src/contain/*.c -o $@_unpriv
	sudo install -o root -g root -m 4755 $@_unpriv $@

