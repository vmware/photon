%global major_version 8.2

# If you are incrementing major_version, enable bootstrapping and adjust accordingly.
# Version should be the latest prior build. If you don't do this, build will break.
# once bootstrapped rpm is built, keep it in PUBLISHRPMS & build other dependent publish rpms
# And once done, bootstrap can be set to 0.
%global bootstrap 0
%global bootstrap_major_version 7.0
%global bootstrap_version %{bootstrap_major_version}

Summary:        Command-line editing and history capabilities
Name:           readline
Version:        8.2
Release:        2%{?dist}
License:        GPLv3+
URL:            http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/readline/%{name}-%{version}.tar.gz
%define sha512 %{name}=0a451d459146bfdeecc9cdd94bda6a6416d3e93abd80885a40b334312f16eb890f8618a27ca26868cebbddf1224983e631b1cbc002c1a4d1cd0d65fba9fea49a

%if 0%{?bootstrap}
Source1: http://ftp.gnu.org/gnu/readline/%{name}-%{bootstrap_major_version}.tar.gz
%define sha512 readline-%{bootstrap_major_version}=18243189d39bf0d4c8a76cddcce75243c1bae8824c686e9b6ba352667607e5b10c5feb79372a1093c1c388d821841670702e940df12eae94bcebdeed90047870
%endif

BuildRequires:  ncurses-devel

Requires:       ncurses-libs

%description
The Readline package is a set of libraries that offers command-line
editing and history capabilities.

%package        devel
Summary:        Header and development files for readline
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%prep
tar xf %{SOURCE0} --no-same-owner
%if 0%{?bootstrap}
tar xf %{SOURCE1} --no-same-owner
%endif

pushd %{name}-%{major_version}
sed -i '/MV.*old/d' Makefile.in
sed -i '/{OLDSUFF}/c:' support/shlib-install
popd

%if 0%{?bootstrap}
pushd %{name}-%{bootstrap_major_version}
sed -i '/MV.*old/d' Makefile.in
sed -i '/{OLDSUFF}/c:' support/shlib-install
popd
%endif

%build
pushd %{name}-%{major_version}
%configure --disable-silent-rules
%make_build SHLIB_LIBS=-lncurses
popd

%if 0%{?bootstrap}
pushd %{name}-%{bootstrap_major_version}
%configure --disable-silent-rules
%make_build SHLIB_LIBS=-lncurses shared
popd
%endif

%install
%if 0%{?bootstrap}
pushd %{name}-%{bootstrap_major_version}
%make_install -C shlib %{?_smp_mflags}
popd
%endif

pushd %{name}-%{major_version}
%make_install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_lib}
ln -sfv ../..%{_lib}/$(readlink %{buildroot}%{_libdir}/libreadline.so) %{buildroot}%{_libdir}/libreadline.so
ln -sfv ../..%{_lib}/$(readlink %{buildroot}%{_libdir}/libhistory.so) %{buildroot}%{_libdir}/libhistory.so
install -vdm 755 %{buildroot}%{_docdir}/%{name}-%{version}
install -v -m644 doc/*.{ps,pdf,html,dvi} %{buildroot}%{_docdir}/%{name}-%{version}
rm -rf %{buildroot}%{_infodir}
popd

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libreadline.so.*
%{_libdir}/libhistory.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/keymaps.h
%{_includedir}/%{name}/history.h
%{_includedir}/%{name}/rlstdc.h
%{_includedir}/%{name}/chardefs.h
%{_includedir}/%{name}/readline.h
%{_includedir}/%{name}/rlconf.h
%{_includedir}/%{name}/rltypedefs.h
%{_includedir}/%{name}/tilde.h
%{_libdir}/libreadline.a
%{_libdir}/libhistory.a
%{_libdir}/libhistory.so
%{_libdir}/libreadline.so
%{_libdir}/pkgconfig/readline.pc
%{_libdir}/pkgconfig/history.pc
%{_datadir}/%{name}/hist_purgecmd.c
%{_datadir}/%{name}/rlbasic.c
%{_datadir}/%{name}/rltest.c
%{_datadir}/%{name}/rlversion.c
%{_datadir}/%{name}/rlptytest.c
%{_datadir}/%{name}/rlevent.c
%{_datadir}/%{name}/rl-callbacktest.c
%{_datadir}/%{name}/rlcat.c
%{_datadir}/%{name}/histexamp.c
%{_datadir}/%{name}/rl-fgets.c
%{_datadir}/%{name}/rl.c
%{_datadir}/%{name}/excallback.c
%{_datadir}/%{name}/manexamp.c
%{_datadir}/%{name}/hist_erasedups.c
%{_datadir}/%{name}/fileman.c
%{_datadir}/%{name}/rlkeymaps.c
%{_datadir}/%{name}/rl-timeout.c
%{_docdir}/%{name}/INSTALL
%{_docdir}/%{name}/README
%{_docdir}/%{name}/CHANGES
%{_docdir}/%{name}-%{version}/readline.html
%{_docdir}/%{name}-%{version}/readline.dvi
%{_docdir}/%{name}-%{version}/history.pdf
%{_docdir}/%{name}-%{version}/rluserman.html
%{_docdir}/%{name}-%{version}/rluserman.dvi
%{_docdir}/%{name}-%{version}/history.dvi
%{_docdir}/%{name}-%{version}/readline.ps
%{_docdir}/%{name}-%{version}/history.ps
%{_docdir}/%{name}-%{version}/rluserman.ps
%{_docdir}/%{name}-%{version}/readline.pdf
%{_docdir}/%{name}-%{version}/history_3.ps
%{_docdir}/%{name}-%{version}/readline_3.ps
%{_docdir}/%{name}-%{version}/history.html
%{_docdir}/%{name}-%{version}/rluserman.pdf
%{_mandir}/man3/history.3.gz
%{_mandir}/man3/readline.3.gz

%changelog
* Fri Jun 09 2023 Nitesh Kumar <kunitesh@vmware.com> 8.2-2
- Bump version as a part of ncurses upgrade to v6.4
* Thu Dec 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 8.2-1
- Upgrade to v8.2
* Wed Nov 07 2018 Alexey Makhalov <amakhalov@vmware.com> 7.0-3
- Use %configure
* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 7.0-2
- Fix dependency
* Fri Jan 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 7.0-1
- Updated to version 7.0
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 6.3-6
- Move docs and man to the devel package
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 6.3-5
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.3-4
- GA - Bump release of all rpms
* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> 6.3-3
- Adding ncurses to run time require package
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 6.3-2
- Update according to UsrMove.
* Wed Oct 22 2014 Divya Thaluru <dthaluru@vmware.com> 6.3-1
- Initial build. First version
