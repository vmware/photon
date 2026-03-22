%global build_if %{photon_subrelease} >= 92

Name:           python3-legacy-cgi
Version:        2.6.4
Release:        1%{?dist}
Summary:        Fork of the standard library cgi and cgitb modules
URL:            https://github.com/jackrosenthal/python-cgi
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0: legacy_cgi-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-hatchling
BuildRequires: python3-pip

Requires: python3

%description
Python CGI This is a fork of the standard library modules cgi and cgitb.
They are slated to be removed from the Python standard library in
Python 3.13. The purpose of this fork is to support existing CGI
scripts using these modules.

%prep
%autosetup -p1 -n legacy_cgi-%{version}
sed -i '1s|^#!.*|#!/usr/bin/env python3|' cgi.py

%build
%pyproject_wheel

%install
%pyproject_install

%files
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sun Mar 22 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.6.4-1
- Initial version, needed by python3-webob
