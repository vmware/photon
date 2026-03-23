%global build_if %{photon_subrelease} >= 92

%define srcname             setuptools
%define python_wheel_dir    %{_datadir}/python-wheels
%define python_wheel_name   %{srcname}-%{version}-py3-none-any.whl

Summary:        Extensions to the standard Python datetime module
Name:           python3-setuptools
# if you make any security fix in this package, package the whl files
# python3.spec without miss
Version:        80.9.0
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/setuptools

Source0: https://files.pythonhosted.org/packages/18/5d/3bf57dcd21979b887f014ea83c24ae194cfcd12b9e0fda66b957c69d1fca/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-xml

Requires:       python3
Requires:       python3-xml
Requires(post): findutils

BuildArch:      noarch

Provides:       python%{python3_version}dist(setuptools)

%description
Setuptools is a fully-featured, actively-maintained, and stable library
designed to facilitate packaging Python projects.
It helps developers to easily share reusable code (in the form of a library) and programs
(e.g., CLI/GUI tools implemented in Python), that can be installed with pip and uploaded to PyPI.

%package wheel
Summary:        The setuptools wheel

%description wheel
A Python wheel of setuptools to use with venv.

%prep
%autosetup -p1 -n %{srcname}-%{version}
%if 0%{?with_check} == 0
rm -r setuptools/tests/
%endif

%build
%{python3} setup.py bdist_wheel

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build
find %{buildroot}%{python3_sitelib} -name '*.exe' -delete
mkdir -p %{buildroot}%{python_wheel_dir}
install -p dist/%{python_wheel_name} -t %{buildroot}%{python_wheel_dir}

%if 0%{?with_check}
%check
%{py3_test}
%endif

%post
find %{python3_sitelib}/%{srcname}-* -type d -empty -delete

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,755)
%{python3_sitelib}/*

%files wheel
%defattr(-,root,root,755)
%dir %{python_wheel_dir}
%{python_wheel_dir}/%{python_wheel_name}

%changelog
* Mon Mar 23 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 80.9.0-2
- Remove test dir while building
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 80.9.0-1
- Bump up release as part of python3 upgrade
* Wed May 28 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 69.0.3-8
- Fix CVE-2025-47273
* Fri Jan 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 69.0.3-7
- Add findutils to post requires
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 69.0.3-6
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 69.0.3-5
- Release bump for SRP compliance
* Tue Jul 23 2024 Prashant S Chauhan <prashant.singhj-chauhan@broadcom.com> 69.0.3-4
- Fix CVE-2024-6345
* Thu May 02 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 69.0.3-3
- Remove leftover empty setuptools dirs from install location
* Wed Mar 06 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 69.0.3-2
- Remove wheel dependency
* Wed Feb 28 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 69.0.3-1
- Initial addition. Seperated from python3 spec.
