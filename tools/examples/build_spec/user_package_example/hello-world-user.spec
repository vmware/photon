Summary:        Hello World User Package
Name:           hello-world-user
Version:        1.0
Release:        1%{?dist}
License:    	GPLv2
Group:        	System Environment/Kernel
Vendor:         VMware, Inc.
Distribution: 	Photon
Source0:        hello-world-user.tar.gz
BuildRequires:  hello-world-user1
BuildRequires:  git
Requires:       hello-world-user1

%description
Example of building User Package for Photon OS

%prep
%autosetup -n hello-world-user

%build
make %{?_smp_mflags}

%install
pwd
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
/usr/bin/*

%changelog
*   Wed Oct 19 2022 User <user@example.org> 1.0-1
-   Initial build. First version
