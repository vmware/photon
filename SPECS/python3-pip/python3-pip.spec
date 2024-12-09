%define srcname             pip
%define python_wheel_dir    %{_datadir}/python-wheels
%define python_wheel_name   %{srcname}-%{version}-py3-none-any.whl

Summary:        The PyPA recommended tool for installing Python packages.
Name:           python3-pip
# if you make any security fix in this package, package the whl files
# python3.spec without miss
Version:        24.0
Release:        2%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pip/

Source0: https://files.pythonhosted.org/packages/6b/8b/0b16094553ecc680e43ded8f920c3873b01b1da79a54274c98f08cb29fca/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=b687d9e7e2b0348a1c3355610bcf4e194dd157dc6e79638f8a0a383cf1ba7c4253be4b145e9a5029e089807d1feec9e444976f34f77a732f3ef527d9bc6bcebf

Source1: license.txt
%include %{SOURCE1}

Patch0: dummy-certifi.patch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-wheel

Requires:       python3
Requires:       python3-setuptools
Requires:       python3-xml
Requires:       %{name}-wheel = %{version}-%{release}

BuildArch:      noarch

%description
Pip is the package installer for Python.
You can use pip to install packages from the Python Package Index and
other indexes.

%package        wheel
Summary:        The pip wheel
Requires:       ca-certificates

%description wheel
A Python wheel of pip to use with venv.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%{python3} setup.py bdist_wheel

%install
%{python3} dist/%{python_wheel_name}/pip install \
    --root %{buildroot} \
    --no-deps \
    --disable-pip-version-check \
    --progress-bar off \
    --verbose \
    --ignore-installed \
    --no-warn-script-location \
    --no-index \
    --no-cache-dir \
    --find-links dist \
    'pip==%{version}'

find %{buildroot}%{python3_sitelib} -name '*.exe' | xargs rm -vf

mkdir -p %{buildroot}%{python_wheel_dir}
install -p dist/%{python_wheel_name} -t %{buildroot}%{python_wheel_dir}

%check
%{py3_test}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,755)
%{python3_sitelib}/*
%{_bindir}/pip*

%files wheel
%defattr(-,root,root,755)
%dir %{python_wheel_dir}
%{python_wheel_dir}/%{python_wheel_name}

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 24.0-2
- Release bump for SRP compliance
* Thu Jul 25 2024 Tapas Kundu <tapas.kundu@broadom.com> 24.0-1
- Update to 24.0
* Wed Feb 28 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 23.3.2-1
- Initial addition. Seperated from python3 spec.
