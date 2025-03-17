%define srcname pytz-deprecation-shim

Name:       python3-pytz-deprecation-shim
Version:    0.1.0.post0
Release:    2%{?dist}
Summary:    Shims to help you safely remove pytz
Group:      Development/Languages/Python
URL:        https://github.com/pganssle/pytz-deprecation-shim
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pganssle/pytz-deprecation-shim/archive/refs/tags/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: tzdata
BuildRequires: python3-wheel
BuildRequires: python3-pip

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-hypothesis
BuildRequires: python3-pytz
%endif

Requires: python3
Requires: python3-dateutil
Requires: tzdata

BuildArch:      noarch

%description
pytz has served the Python community well for many years, but it is no longer
the best option for providing time zones. pytz has a non-standard interface
that is very easy to misuse; this interface was necessary when pytz was
created, because datetime had no way to represent ambiguous datetimes, but this
was solved in Python 3.6, which added a fold attribute to datetimes in PEP 495.
With the addition of the zoneinfo module in Python 3.9 (PEP 615), there has
never been a better time to migrate away from pytz.

However, since pytz time zones are used very differently from a standard
tzinfo, and many libraries have built pytz zones into their standard time zone
interface (and thus may have users relying on the existence of the localize and
normalize methods); this library provides shim classes that are compatible with
both PEP 495 and pytz’s interface, to make it easier for libraries to deprecate
pytz.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
pip3 install tomli
%{pytest}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.1.0.post0-2
- Release bump for SRP compliance
* Sat Aug 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.1.0.post0-1
- New addition, needed by python3-tzlocal
