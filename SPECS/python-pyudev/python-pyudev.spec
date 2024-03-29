Summary:        Python binding for libudev
Name:           python3-pyudev
Version:        0.23.2
Release:        1%{?dist}
License:        GNU Library or Lesser General Public License (LGPL) (LGPL 2.1+)
Group:          Development/Languages/Python
URL:            https://pypi.org/project/pyudev
Source0:        pyudev-%{version}.tar.gz
%define sha512  pyudev=40b947d363dca73789f5ab77cbda4b48349e28fe04f2f5cafb93d20799d842ebeb2b7d78d1f16dcbcaac5c20aff1b931b372c75852706e731337e6e1d30b8538
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  systemd-devel
Requires:       systemd
Requires:       python3
Requires:       python3-pip
Requires:       python3-six
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  curl-devel
BuildRequires:  python3-six
BuildRequires:  python3-py
BuildRequires:  python3-pytest
BuildRequires:  python3-attrs
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-docutils
%endif

%description
pyudev is a LGPL licensed, pure Python binding for libudev, the device and hardware management and information
library for Linux. It supports almost all libudev functionality. You can enumerate devices, query device properties and
attributes or monitor devices, including asynchronous monitoring with threads, or within the event loops of Qt, Glib
or wxPython.

The binding supports CPython 2 (2.6 or newer) and 3 (3.1 or newer), and PyPy 1.5 or newer. It is tested against udev
151 or newer, earlier versions of udev as found on dated Linux systems may work, but are not officially supported.

%prep
%autosetup -n pyudev-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install pluggy more_itertools hypothesis mock
python3 setup.py test

%files
%defattr(-,root,root)
%doc COPYING README.rst
%{python3_sitelib}/*

%changelog
*   Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.23.2-1
-   Automatic Version Bump
*   Thu Mar 19 2020 Tapas Kundu <tkundu@vmware.com> 0.22.0-1
-   Initial release.
