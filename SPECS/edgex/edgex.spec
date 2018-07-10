%global security_hardening nopie
%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        EdgeX Foundry Go Services
Name:           edgex
Version:        0.6.0
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/edgexfoundry/edgex-go
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
# Wait for official release
# Since we already use "glide install" use "go get" for edgex sources for now.
#Source0:	TBD
#Source1:	TBD
Source2:	edgex-template.service
Source3:	edgex-core-config-seed.service
# Origin https://github.com/edgexfoundry/developer-scripts
Source4:	init_mongo.js

BuildRequires:  git
BuildRequires:  glide
BuildRequires:  go >= 1.9
BuildRequires:  make
BuildRequires:  systemd-devel
BuildRequires:  zeromq-devel
Requires:       systemd
Requires:       mongodb
Requires:       consul

%description
EdgeX Foundry Go Services

%prep
export GOPATH="/go"
export PATH="$PATH:$GOPATH/bin"

%build
go get github.com/edgexfoundry/edgex-go
cd $GOPATH/src/github.com/edgexfoundry/edgex-go
glide install
make build

go get github.com/edgexfoundry/core-config-seed-go
cd $GOPATH/src/github.com/edgexfoundry/core-config-seed-go
glide install
make build

%install
# edgex-go
cd $GOPATH/src/github.com/edgexfoundry/edgex-go

install -d -m755 %{buildroot}%{_bindir}
install -d -m755 %{buildroot}%{_datadir}/%{name}
install -d -m755 %{buildroot}%{_libdir}/systemd/system

# install binary
for srv in core-command core-data core-metadata export-client export-distro support-logging ; do
install -p -m755 cmd/${srv}/${srv} %{buildroot}%{_bindir}/edgex-${srv}
install -d -m755 %{buildroot}%{_datadir}/%{name}/${srv}/res
install -p -m644 cmd/${srv}/res/configuration.toml %{buildroot}%{_datadir}/%{name}/${srv}/res/configuration.toml
# workdir for the service
install -d -m755 %{buildroot}%{_var}/log/%{name}/${srv}
ln -s %{_datadir}/%{name}/${srv}/res %{buildroot}%{_var}/log/%{name}/${srv}/res

sed "s/SERVICE_NAME/${srv}/" %{SOURCE2} > %{buildroot}%{_libdir}/systemd/system/edgex-${srv}.service
done

# core-config-seed-go
cd $GOPATH/src/github.com/edgexfoundry/core-config-seed-go
install -p -m755 core-config-seed-go %{buildroot}%{_bindir}/edgex-core-config-seed
install -d -m755 %{buildroot}%{_datadir}/%{name}/core-config-seed/res
install -p -m644 res/configuration.toml %{buildroot}%{_datadir}/%{name}/core-config-seed/res/configuration.toml
install -p -m644 res/banner.txt %{buildroot}%{_datadir}/%{name}/core-config-seed/res/banner.txt
cp -a config %{buildroot}%{_datadir}/%{name}/core-config-seed/
install -p -m644 %{SOURCE3} %{buildroot}%{_libdir}/systemd/system/`basename %{SOURCE3}`

# init mongo script
install -d -m755 %{buildroot}%{_datadir}/%{name}/scripts/
install -p -m644 %{SOURCE4} %{buildroot}%{_datadir}/%{name}/scripts/`basename %{SOURCE4}`

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%{_libdir}/*
%{_var}/log/*

%changelog
*   Fri Jul 06 2018 Alexey Makhalov <amakhalov@vmware.com> 0.6.0-1
-   Initial version
