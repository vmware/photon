Summary:       Convert output of command line tools and others to JSON
Name:          jc
Version:       1.23.6
Release:       3%{?dist}
URL:           https://github.com/kellyjonbrazil/jc
Group:         Development/Languages/Python
Vendor:        VMware, Inc.
Distribution:  Photon
BuildArch:     noarch

Source0: https://github.com/kellyjonbrazil/jc/archive/refs/tags/jc-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-xmltodict
BuildRequires: python3-ruamel-yaml
BuildRequires: python3-Pygments

Requires: python3-%{name} = %{version}-%{release}

%if 0%{?with_check}
BuildRequires: tzdata
BuildRequires: python3-pytest
%endif

%description
CLI tool that converts the output of popular command-line
tools, file-types, and common strings to JSON, YAML, or Dictionaries.

%package -n python3-%{name}
BuildArch: noarch
Summary: Module to convert output of command line tools and others
Requires: python3
Requires: python3-xmltodict
Requires: python3-ruamel-yaml
Requires: python3-Pygments

%description -n python3-%{name}
Module to convert the output of popular command-line
tools, file-types, and common strings to JSON, YAML, or Dictionaries.

%prep
%autosetup -p1

%build
%{py3_build}

%install
%{py3_install}
find %{buildroot}%{python3_sitelib}/%{name} -depth -name __pycache__ -exec rm -rf {} \;
install -m 755 -d %{buildroot}%{_mandir}/man1
install -m 644 -p man/jc.1 %{buildroot}%{_mandir}/man1/
install -m 755 -d %{buildroot}%{_datadir}/bash-completion/completions
install -m 644 -p completions/jc_bash_completion.sh %{buildroot}%{_datadir}/bash-completion/completions/%{name}

%if 0%{?with_check}
%check
# needs Pacific timezone, see https://github.com/kellyjonbrazil/jc/issues/474
TZ=America/Los_Angeles ./runtests.sh
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.md
%doc EXAMPLES.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.*
%{_datadir}/bash-completion/completions/*

%files -n python3-%{name}
%defattr(-,root,root)
%doc README.md
%license LICENSE.md
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.23.6-3
- Release bump for SRP compliance
* Sat Dec 09 2023 Oliver Kurth <oliver.kurth@broadcom.com> 1.23.6-2
- fix requires by moving them to the python package
* Tue Oct 24 2023 Oliver Kurth <okurth@vmware.com> 1.23.6-1
- Initial build
