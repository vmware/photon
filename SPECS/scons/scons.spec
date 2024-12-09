Name:           scons
Version:        4.1.0
Release:        3%{?dist}
Summary:        An Open Source software construction tool
Group:          Development/Tools
URL:            https://sourceforge.net/projects/scons
Source0:        https://sourceforge.net/projects/scons/files/scons/%{version}/%{name}-%{version}.tar.gz
%define sha512  scons=f79b86bb09783767b3872cfb8efb665372714a604af2aaf3adc66eee63d3afe27bc6b2aab83813743c83f71c81c800d42842e916501787ba402ce2726dda9b44

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3-xml
Requires:       python3
BuildArch:      noarch

%description
SCons is an Open Source software construction tool—that is, a next-generation build tool.
Think of SCons as an improved, cross-platform substitute for the classic Make utility
with integrated functionality similar to autoconf/automake and compiler caches such as ccache.
In short, SCons is an easier, more reliable and faster way to build software.

%prep
%autosetup -n %{name}-%{version}

%build
python3 scripts/scons.py --help

%install
python3 setup.py install \
    --root=%{buildroot} \
    --prefix=%{_prefix} \
    --install-data=%{_datadir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/*
%{_datadir}/*.1

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.1.0-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 4.1.0-2
- Update release to compile with python 3.11
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 4.1.0-1
- Automatic Version Bump
* Fri Sep 18 2020 Susant Sahani <ssahani@vmware.com> 4.0.1-2
- Add requires python3-xml
* Wed Jul 29 2020 Gerrit Photon <photon-checkins@vmware.com> 4.0.1-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 3.0.1-3
- Build with python3
- Mass removal python2
* Mon Jan 07 2019 Alexey Makhalov <amakhalov@vmware.com> 3.0.1-2
- BuildRequires: python2
* Tue Sep 18 2018 Srinidhi Rao <srinidhir@vmware.com> 3.0.1-1
- Upgraded to version 3.0.1
* Sun Oct 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5.1-1
- Initial build. First version
