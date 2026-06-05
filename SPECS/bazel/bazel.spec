%global build_if %{photon_subrelease} >= 91

%global debug_package %{nil}
%define __os_install_post %{nil}

Summary:        Build software of any size, quickly and reliably, just as engineers do at Google.
Name:           bazel
Version:        9.0.1
Release:        2%{?dist}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://bazel.build/

Source0: https://github.com/bazelbuild/bazel/releases/download/%{version}/%{name}-%{version}-dist.zip

Source1: license.txt
%include %{SOURCE1}

Source2: setup-zip-wrappers.sh

BuildRequires:  openjdk21
BuildRequires:  zlib-devel
BuildRequires:  which
BuildRequires:  findutils
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  gcc
BuildRequires:  python3

Requires: (openjdk21 or openjdk25)

%description
Bazel is Google's own build tool, now publicly available in Beta. Bazel has
built-in support for building both client and server software, including client
applications for both Android and iOS platforms. It also provides an extensible
framework that you can use to develop your own build rules.

%prep
# Using autosetup is not feasible
%setup -c -T -n %{name}-%{version}
python3 - << 'PYEOF'
import zipfile, os
with zipfile.ZipFile("%{SOURCE0}") as zf:
    for info in zf.infolist():
        extracted = zf.extract(info, ".")
        perm = (info.external_attr >> 16) & 0o777
        if perm and os.path.isfile(extracted):
            os.chmod(extracted, perm)
PYEOF
# contains copyleft licenses
rm ./third_party/java/proguard/proguard6.2.2/docs/proguard.appdata.xml

%build
. %{SOURCE2}
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK*)
export TMPDIR="%{_usr}/tmp"

mkdir -p $TMPDIR
export EXTRA_BAZEL_ARGS="--tool_java_runtime_version=local_jdk --subcommands --verbose_failures --sandbox_debug"
./compile.sh

%install
install -vDm 755 output/%{name} %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/bazel

%changelog
* Tue Jun 02 2026 Ajay Kaher <ajay.kaher@broadcom.com> 9.0.1-2
- Replace deprecated zip/unzip with Python zip/unzip wrappers
* Tue May 26 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 9.0.1-1
- Upgrade to 9.0.1
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 5.3.2-10
- Extended to build for subrelease 91 and above
* Mon Apr 13 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 5.3.2-9
- Added openjdk21 and openjdk25 to requires
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.3.2-8
- Bump version as a part of python3.14 upgrade
* Tue Aug 12 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.3.2-7
- Fix copyleft licensing
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 5.3.2-6
- Release bump for SRP compliance
* Fri Jul 26 2024 Harinadh D <Harinadh.Dommaraju@broadcom.com> 5.3.2-5
- Offline build support
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.2-4
- Require jdk11 or jdk17
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.3.2-3
- Bump version as a part of openjdk11 upgrade
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 5.3.2-2
- Update release to compile with python 3.11
* Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 5.3.2-1
- Automatic Version Bump
* Sun Sep 18 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.3.0-1
- Upgrade to latest version
- Use openjdk11
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 4.0.0-1
- Automatic Version Bump
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 3.5.0-2
- GCC-10 support.
* Mon Sep 21 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 3.5.0-1
- Update bazel version
* Fri Apr 24 2020 Ankit Jain <ankitja@vmware.com> 2.0.0-2
- Changed openjdk install directory name
* Fri Feb 7 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 2.0.0-1
- Initial release
