%global build_if %{photon_subrelease} >= 92
%global srcname vcs-versioning

Summary:        setuptools-scm VCS versioning backend
Name:           python3-vcs-versioning
Version:        1.1.1
Release:        1%{?dist}
URL:            https://github.com/pypa/setuptools-scm
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pypa/setuptools-scm/archive/refs/tags/%{srcname}-v%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-setuptools
BuildRequires:  python3-build
BuildRequires:  python3-installer

Requires:       python3
Requires:       python3-packaging

%description
VCS metadata integration for setuptools-scm (Git, Mercurial, fallbacks). Packaged so
other builds do not need pip or network during %%py3_build_wheel.

%prep
%autosetup -n setuptools-scm-vcs-versioning-v%{version}

%build
# No git in the minimal chroot: archival tags like vcs-versioning-v1.1.1 are not
# git-describe shaped; vcs_versioning's parser then fails. Pin the sdist version.
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
cd %{srcname}
%py3_build_wheel

%install
cd %{srcname}
%py3_install_wheel

%{py_byte_compile_and_ghost}

%check
%{__python3} -c "import vcs_versioning"

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/vcs-versioning

%changelog
* Tue Apr 07 2026 Mukul Sikka <mukul.sikka@broadcom.com> 1.1.1-1
- Initial packaging for offline setuptools-scm