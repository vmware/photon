Summary:        Hello World User Package
Name:           hello-world-user1
Version:        1.0
Release:        1%{?dist}
License:    	GPLv2
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        hello-world-user1.tar.gz

%description
Example of building User Package for Photon OS

%prep
%autosetup -n hello-world-user1

%build
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
/usr/bin/*

%changelog
*   Wed Oct 19 2022 User <user@example.org> 1.0-1
-   Initial build. First version
