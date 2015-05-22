#
# Copyright VMware, Inc 2015
#

SRCROOT := .
MAKEROOT=$(SRCROOT)/support/make
include $(MAKEROOT)/makedefs.mk

ifdef PHOTON_CACHE_PATH
PHOTON_PACKAGES := packages-cached
else
PHOTON_PACKAGES := packages
endif

ifdef PHOTON_SOURCES_PATH
PHOTON_SOURCES := sources-cached
else
PHOTON_SOURCES := sources
endif

.PHONY : all iso clean toolchain toolchain-minimal photon-build-machine photon-vagrant-build photon-vagrant-local \
check check-bison check-g++ check-gawk check-createrepo check-vagrant check-packer check-packer-ovf-plugin

all: iso

iso: check $(PHOTON_PACKAGES) $(PHOTON_TOOLCHAIN_MINIMAL)
	@echo "Building Photon ISO..."
	@cd $(PHOTON_INSTALLER_DIR) && \
    $(PHOTON_INSTALLER) -i $(PHOTON_STAGE)/photon.iso \
                        -w $(PHOTON_STAGE)/photon_iso \
                        -t $(PHOTON_STAGE) \
                        -f > \
        $(PHOTON_LOGS_DIR)/installer.log 2>&1

packages: check $(PHOTON_TOOLCHAIN_MINIMAL) $(PHOTON_SOURCES)
	@echo "Building all RPMS..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
    $(PHOTON_PACKAGE_BUILDER) -a \
                              -b $(PHOTON_CHROOT_PATH) \
                              -s $(PHOTON_SPECS_DIR) \
                              -r $(PHOTON_RPMS_DIR) \
                              -o $(PHOTON_SRCS_DIR) \
                              -p $(PHOTON_STAGE) \
                              -l $(PHOTON_LOGS_DIR)

packages-cached: check $(PHOTON_TOOLCHAIN_MINIMAL)
	@echo "Using cached RPMS..."
	@$(RM) -f $(PHOTON_RPMS_DIR_NOARCH)/* && \
     $(RM) -f $(PHOTON_RPMS_DIR_X86_64)/* && \
     $(CP) -f $(PHOTON_CACHE_PATH)/RPMS/noarch/* $(PHOTON_RPMS_DIR_NOARCH)/ && \
     $(CP) -f $(PHOTON_CACHE_PATH)/RPMS/x86_64/* $(PHOTON_RPMS_DIR_X86_64)/

package: check $(PHOTON_TOOLCHAIN_MINIMAL) $(PHOTON_SOURCES)
	@if [ -z $(PKG_NAME) ]; then \
		echo "Error: PKG_NAME is undefined"; \
        exit 1; \
	fi
	@echo "Building package $(PKG_NAME) ..."
	@cd $(PHOTON_PKG_BUILDER_DIR) && \
    $(PHOTON_PACKAGE_BUILDER) -i \
                              -b $(PHOTON_CHROOT_PATH) \
                              -s $(PHOTON_SPECS_DIR) \
                              -r $(PHOTON_RPMS_DIR) \
                              -o $(PHOTON_SRCS_DIR) \
                              -p $(PHOTON_STAGE) \
                              -l $(PHOTON_LOGS_DIR) \
                              $(PKG_NAME)

sources:
	@echo "Pulling sources from bintary..."
	@cd $(PHOTON_PULL_SOURCES_DIR) && \
	$(PHOTON_PULL_SOURCES) $(PHOTON_SRCS_DIR)

sources-cached:
	@echo "Using cached SOURCES..."
	@$(MKDIR) -p $(PHOTON_SRCS_DIR) && \
	 $(CP) -rf $(PHOTON_SOURCES_PATH)/* $(PHOTON_SRCS_DIR)/

toolchain-minimal : $(PHOTON_TOOLCHAIN_MINIMAL)

$(PHOTON_TOOLCHAIN_MINIMAL) : $(PHOTON_TOOLCHAIN) $(PHOTON_TOOLCHAIN_MIN_LIST)
	echo "Building minimal toolchain..."
	@$(RMDIR) $(PHOTON_TOOLS_DIR) && \
	cd $(PHOTON_STAGE) && \
	$(TAR) xvf $(PHOTON_TOOLCHAIN) > $(PHOTON_LOGS_DIR)/toolchain-minimal.log 2>&1 && \
    $(TAR) cvfz \
           $@ \
           -T $(PHOTON_TOOLCHAIN_MIN_LIST) >> \
              $(PHOTON_LOGS_DIR)/toolchain-minimal.log 2>&1 && \
	$(RMDIR) $(PHOTON_TOOLS_DIR)

toolchain : $(PHOTON_TOOLCHAIN)

ifdef PHOTON_CACHE_PATH

$(PHOTON_TOOLCHAIN): check $(PHOTON_STAGE)
	@echo "Using cached toolchain..."
	@$(RM) -f $(PHOTON_TOOLCHAIN) && \
	 $(CP) -f $(PHOTON_CACHE_PATH)/tools-build.tar $(PHOTON_TOOLCHAIN)

else

$(PHOTON_TOOLCHAIN): $(PHOTON_STAGE) $(PHOTON_SOURCES)
	@if [ -a $(PHOTON_TOOLCHAIN) ] ; then \
		echo "Using already built toolchain"; \
	else \
		echo "Building toolchain..."; \
		cd $(PHOTON_TOOLCHAIN_DIR) && \
				$(PHOTON_TOOLCHAIN_BUILDER) \
					$(PHOTON_SRCS_DIR) \
					$(PHOTON_SPECS_DIR) \
					$(PHOTON_LOGS_DIR) \
					$(PHOTON_STAGE) ;\
	fi

endif

$(PHOTON_STAGE):
	@echo "Creating staging folder..."
	$(MKDIR) -p $(PHOTON_STAGE)
	@echo "Creating chroot path..."
	$(MKDIR) -p $(PHOTON_CHROOT_PATH)
	@echo "Building RPMS folders..."
	@test -d $(PHOTON_RPMS_DIR_NOARCH) || $(MKDIR) -p $(PHOTON_RPMS_DIR_NOARCH)
	@test -d $(PHOTON_RPMS_DIR_X86_64) || $(MKDIR) -p $(PHOTON_RPMS_DIR_X86_64)
	@echo "Building SOURCES folder..."
	@test -d $(PHOTON_SRCS_DIR) || $(MKDIR) -p $(PHOTON_SRCS_DIR)
	@echo "Building LOGS folder..."
	@test -d $(PHOTON_LOGS_DIR) || $(MKDIR) -p $(PHOTON_LOGS_DIR)

clean: clean-install clean-chroot
	@echo "Deleting Photon ISO..."
	@$(RM) -f $(PHOTON_STAGE)/photon.iso
	@echo "Deleting stage dir..."
	@$(RMDIR) $(PHOTON_STAGE)
	@echo "Deleting chroot path..."
	@$(RMDIR) $(PHOTON_CHROOT_PATH)

clean-install:
	@echo "Cleaning installer working directory..."
	@if [ -d $(PHOTON_STAGE)/photon_iso ]; then \
		cd $(PHOTON_INSTALLER_DIR) && \
		$(PHOTON_INSTALLER_DIR)/mk-unmount-disk.sh -w $(PHOTON_STAGE)/photon_iso && \
		$(RMDIR) $(PHOTON_STAGE)/photon_iso; \
	fi

clean-chroot:
	@echo "Cleaning chroot path..."
	@if [ -d $(PHOTON_CHROOT_PATH) ]; then \
		cd $(PHOTON_PKG_BUILDER_DIR) && \
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
	@if [ -e $(PHOTON_STAGE)/photon.iso ]; then \
		cd $(PHOTON_PACKER_TEMPLATES) && \
		$(SED) -i "" -e "s#\"iso_checksum_value\":.*#\"iso_checksum_value\": \"$$($(SHASUM) ../../stage/photon.iso | cut -f 1 -d ' ')\",#" photon.json && \
		$(PACKER) build $(PACKER_ARGS) photon.json && \
		$(SED) -i "" -e "s#\"iso_checksum_value\":.*#\"iso_checksum_value\": \"\",#" photon.json; \
		echo "Moving boxes to $(PHOTON_STAGE)..." && \
		$(MV) *.box $(PHOTON_STAGE); \
	else \
		echo "Unable to find $(PHOTON_STAGE)/photon.iso ... aborting build"; \
	fi

check: check-bison check-g++ check-gawk check-createrepo check-texinfo

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
