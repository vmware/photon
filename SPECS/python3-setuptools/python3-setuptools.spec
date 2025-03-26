%define srcname             setuptools
%define python_wheel_dir    %{_datadir}/python-wheels
%define python_wheel_name   %{srcname}-%{version}-py3-none-any.whl

Summary:        Extensions to the standard Python datetime module
Name:           python3-setuptools
# if you make any security fix in this package, package the whl files
# python3.spec without miss
Version:        69.0.3
Release:        7%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/setuptools

Source0: https://files.pythonhosted.org/packages/5f/36/7374297692bb9dbd7569a0f84887c7e5e314c41d5d9518cb76fbb130620d/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: CVE-2024-6345.patch

BuildRequires: python3-devel
BuildRequires: python3-xml

%define ExtraBuildRequires: python3-wheel

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

%build
%{python3} setup.py bdist_wheel

%install
%{py3_install}
find %{buildroot}%{python3_sitelib} -name '*.exe' -delete
mkdir -p %{buildroot}%{python_wheel_dir}
install -p dist/%{python_wheel_name} -t %{buildroot}%{python_wheel_dir}

%check
%{py3_test}

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
