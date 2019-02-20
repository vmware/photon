Summary:	BACnet open source protocol stack for embedded systems
Name:		bacnet-stack
Version:	0.8.6
Release:	1%{?dist}
License:	GPLv2
URL:		http://bacnet.sourceforge.net
Group:		Development/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://sourceforge.net/projects/bacnet/files/%{name}/%{name}-%{version}/%{name}-%{version}.tgz
%define sha1 bacnet-stack=1994254fff89687b3ab23d3bb823cba0955790fc

%description
This provides BACnet appliction, network and MAC layers as a 
library for embeded systems

%global debug_package %{nil}

%prep
%setup -q

%build
make library %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_libdir}
install -m 644 lib/libbacnet.a  %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_datadir}/doc/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}/bin
cp doc/README.* %{buildroot}%{_datadir}/doc/%{name}
cp -r doc/man %{buildroot}%{_datadir}/doc/%{name}
cp doc/code-standard.txt %{buildroot}%{_datadir}/doc/%{name}
cp -r demo %{buildroot}%{_datadir}/%{name}
cp -r include %{buildroot}%{_datadir}/%{name}
cp -r ports %{buildroot}%{_datadir}/%{name}
cp -r src %{buildroot}%{_datadir}/%{name}

%check
./unittest.sh


%files
%defattr(-,root,root)
%{_libdir}/libbacnet.a
%{_datadir}/*

%changelog
*    Thu Feb 14 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.8.6-1
-    Initial build added for Photon.
