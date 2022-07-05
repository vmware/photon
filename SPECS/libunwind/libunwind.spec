Summary:        Portable and efficient C programming interface (API) to determine the call-chain of a program.
Name:           libunwind
Version:        1.6.2
Release:        1%{?dist}
License:        X11
URL:            http://www.nongnu.org/libunwind/
Source0:        http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz
%define sha512    libunwind=1d17dfb14f99a894a6cda256caf9ec481c14068aaf8f3a85fa3befa7c7cca7fca0f544a91a3a7c2f2fc55bab19b06a67ca79f55ac9081151d94478c7f611f8f7
Group:          Utilities/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

%description
Portable and efficient C programming interface (API) to determine the call-chain of a program.
The API additionally provides the means to manipulate the preserved (callee-saved) state of each call-frame,
and to resume execution at any point in the call-chain (non-local goto).
The API supports both local (same-process) and remote (across-process) operation.
As such, the API is useful in a number of applications.

%package        devel
Summary:        libunwind devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description    devel
This contains development tools and libraries for libunwind.

%prep
%autosetup

%build
%configure \
	--disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_libdir}/libunwind*.so.*

%files devel
%{_includedir}/*unwind*
%{_libdir}/libunwind*.a
%{_libdir}/libunwind*.so
%{_libdir}/pkgconfig/libunwind*

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.6.2-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.5.0-1
-   Automatic Version Bump
*   Wed Jan 13 2021 Alexey Makhalov <amakhalov@vmware.com> 1.4.0-2
-   GCC-10 support
*   Wed Aug 12 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
-   Automatic Version Bump
*   Sun Sep 29 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.2-3
-   libunwind-devel needs libunwind.
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.2-2
-   Use standard configure macros
*   Mon Feb 06 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.2-1
-   Initial version of libunwind package for Photon.
