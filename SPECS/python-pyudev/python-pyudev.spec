%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python binding for libudev
Name:           python3-pyudev
Version:        0.22.0
Release:        1%{?dist}
License:        GNU Library or Lesser General Public License (LGPL) (LGPL 2.1+)
Group:          Development/Languages/Python
URL:            https://pypi.org/project/pyudev
Source0:        pyudev-%{version}.tar.gz
%define         sha1 pyudev=1826db6e768153548df20bfd0a3149f5db9f80e7
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
%setup -q -n pyudev-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
pip3 install pluggy more_itertools hypothesis mock
python3 setup.py test

%files
%defattr(-,root,root)
%doc COPYING README.rst
%{python3_sitelib}/*

%changelog
*   Thu Mar 19 2020 Tapas Kundu <tkundu@vmware.com> 0.22.0-1
-   Initial release.
