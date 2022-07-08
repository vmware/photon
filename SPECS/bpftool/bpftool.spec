Name:           bpftool
Version:        5.17.15
Release:        1%{?dist}
Summary:        Inspection and simple manipulation of eBPF programs and maps
Vendor:         VMware, Inc.
Distribution:   Photon
License:        GPLv2
URL:            http://www.kernel.org/
Source0:        https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha512  %{name}=5c4354d8abef3941054256e04f52b770fc952b19b0e3536c893de6119a86af67899f1cca24c78d18aaa9a57d9c015c502bdb840506451997ae59419652d178c4

BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  glibc-devel
BuildRequires:  python3-docutils
BuildRequires:  binutils-devel

%description
This package contains the bpftool, which allows inspection and simple
manipulation of eBPF programs and maps.

%prep

%autosetup -p1 -n linux-%{version}

%build

ln -sfv /usr/bin/rst2man3.py /usr/bin/rst2man
cd tools/bpf/%{name}/
sed -i '/#include <linux\/if.h>/d' net.c
make
make doc

%install

cd tools/bpf/%{name}/
%make_install prefix=/usr  doc-install

mv %{buildroot}/usr/man %{buildroot}%{_mandir}

%files
%defattr(-,root,root)
%{_sbindir}/%{name}
%exclude %{_datadir}/bash-completion/completions/%{name}
%{_mandir}

%changelog
* Fri Jul 8 2022 Benson Kwok <bkwok@vmware.com> 5.17-1
- Initial version

