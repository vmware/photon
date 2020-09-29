%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Run a subprocess in a pseudo terminal.
Name:           python3-ptyprocess
Version:        0.6.0
Release:        6%{?dist}
License:        ISC
Url:            https://github.com/pexpect/ptyprocess
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://files.pythonhosted.org/packages/source/p/ptyprocess/ptyprocess-%{version}.tar.gz
%define sha1    ptyprocess=39622a2ff2cb456f17db542d60e5a0782e354128

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-xml
BuildRequires:  python3-pip
%endif
Requires:       python3
Requires:       python3-libs

BuildArch:      noarch

%description
Launch a subprocess in a pseudo terminal (pty), and interact with both the
process and its pty.


%prep
%setup -q -n ptyprocess-%{version}

%build
python3 setup.py build


%install
rm -rf %{buildroot}
python3 setup.py install --root=%{buildroot}

%check
pip3 install pathlib2 funcsigs pluggy more_itertools
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python3_sitelib} \
py.test3

%files
%{python3_sitelib}/*

%changelog
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.6.0-6
-   openssl 1.1.1
*   Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 0.6.0-5
-   Mass removal python2
*   Wed Feb 26 2020 Tapas Kundu <tkundu@vmware.com> 0.6.0-4
-   Fix make check
*   Mon Sep 09 2019 Tapas Kundu <tkundu@vmware.com> 0.6.0-3
-   Fix make check
*   Thu Dec 06 2018 Ashwin H <ashwinh@vmware.com> 0.6.0-2
-   Add %check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.6.0-1
-   Update to version 0.6.0
*   Tue Sep 19 2017 Kumar Kaushik <kaushikk@vmware.com> 0.5.2-1
-   Initial packaging for Photon

