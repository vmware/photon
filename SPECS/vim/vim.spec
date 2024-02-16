%define debug_package %{nil}
%global maj_ver vim90

Summary:        Text editor
Name:           vim
Version:        9.0.2142
Release:        1%{?dist}
License:        Charityware
URL:            http://www.vim.org
Group:          Applications/Editors
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/vim/vim/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=d5dae309a219c1775e5637f417e72ef164fbc85c77df8e2cad9767c5ba06f9ceb5b647e059b9148ad87ea7835837ede740caaf65e1a4418dd4f3dc190c52bdc2

Source1: vimrc

BuildRequires:  ncurses-devel

%description
The VIM package contains a powerful text editor.

%package    extra
Summary:    Extra files for Vim text editor
Group:      Applications/Editors
Requires:   tcsh
Requires:   python3
Requires:   %{name} = %{version}-%{release}
Conflicts:  toybox < 0.8.2-2

%description extra
The vim extra package contains a extra files for powerful text editor.

%prep
%autosetup -p1
echo '#define SYS_VIMRC_FILE "/etc/vimrc"' >> src/feature.h

%build
%configure \
    --enable-multibyte

%make_build

%install
# make doesn't support _smp_mflags
%make_install
ln -sfv vim %{buildroot}%{_bindir}/vi
install -vdm 755 %{buildroot}%{_sysconfdir}
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/vimrc

%if 0%{?with_check}
%check
sed -i '/source test_recover.vim/d' src/testdir/test_alot.vim
sed -i '916d' src/testdir/test_search.vim
sed -i '454,594d' src/testdir/test_autocmd.vim
sed -i '1,9d' src/testdir/test_modeline.vim
sed -i '133d' ./src/testdir/Make_all.mak
make test %{?_smp_mflags}
%endif

%post
if ! sed -n -e '0,/[[:space:]]*call[[:space:]]\+system\>/p' %{_sysconfdir}/vimrc | \
     grep -q '^[[:space:]]*set[[:space:]]\+shell=/bin/bash'; then
  sed -i -e 's#^\([[:space:]]*\)\(call[[:space:]]\+system.*\)$#\1set shell=/bin/bash\n\1\2#g' %{_sysconfdir}/vimrc
fi

%files extra
%defattr(-,root,root)
%{_bindir}/vimtutor
%{_bindir}/xxd
%{_mandir}/*/*
%doc %{_datadir}/vim/vim*/doc/*
%{_datadir}/vim/vim*/autoload/*
%{_datadir}/vim/vim*/bugreport.vim
%{_datadir}/vim/vim*/colors/*
%{_datadir}/applications/gvim.desktop
%{_datadir}/applications/vim.desktop
%{_datadir}/icons/hicolor/48x48/apps/gvim.png
%{_datadir}/icons/locolor/16x16/apps/gvim.png
%{_datadir}/icons/locolor/32x32/apps/gvim.png
%{_datadir}/vim/vim*/pack/dist/opt/*
%exclude %{_datadir}/vim/vim*/colors/desert.vim
%exclude %{_datadir}/vim/vim*/colors/lists/default.vim
%{_datadir}/vim/vim*/compiler/*
%{_datadir}/vim/vim*/delmenu.vim
%{_datadir}/vim/vim*/evim.vim
%{_datadir}/vim/vim*/ftoff.vim
%{_datadir}/vim/vim*/ftplugin.vim
%{_datadir}/vim/vim*/ftplugin/*
%{_datadir}/vim/vim*/ftplugof.vim
%{_datadir}/vim/vim*/gvimrc_example.vim
%{_datadir}/vim/vim*/indent.vim
%{_datadir}/vim/vim*/indent/*
%{_datadir}/vim/vim*/indoff.vim
%{_datadir}/vim/vim*/keymap/*
%{_datadir}/vim/vim*/macros/*
%{_datadir}/vim/vim*/menu.vim
%{_datadir}/vim/vim*/mswin.vim
%{_datadir}/vim/vim*/optwin.vim
%{_datadir}/vim/vim*/plugin/*
%{_datadir}/vim/vim*/synmenu.vim
%{_datadir}/vim/vim*/vimrc_example.vim
%{_datadir}/vim/vim*/print/*
%{_datadir}/vim/vim*/scripts.vim
%{_datadir}/vim/%{maj_ver}/import/dist/vimhelp.vim
%{_datadir}/vim/%{maj_ver}/import/dist/vimhighlight.vim
%{_datadir}/vim/vim*/spell/*
%{_datadir}/vim/vim*/syntax/*
%exclude %{_datadir}/vim/%{maj_ver}/syntax/nosyntax.vim
%exclude %{_datadir}/vim/vim*/syntax/syntax.vim
%exclude %{_datadir}/vim/%{maj_ver}/autoload/dist/ft.vim
%{_datadir}/vim/vim*/tools/*
%{_datadir}/vim/vim*/tutor/*
%{_datadir}/vim/vim*/lang/*.vim
%doc %{_datadir}/vim/vim*/lang/*.txt
%lang(af) %{_datadir}/vim/vim*/lang/af/LC_MESSAGES/vim.mo
%lang(ca) %{_datadir}/vim/vim*/lang/ca/LC_MESSAGES/vim.mo
%lang(cs) %{_datadir}/vim/vim*/lang/cs/LC_MESSAGES/vim.mo
%lang(de) %{_datadir}/vim/vim*/lang/de/LC_MESSAGES/vim.mo
%lang(eb_GB) %{_datadir}/vim/vim*/lang/en_GB/LC_MESSAGES/vim.mo
%lang(eo) %{_datadir}/vim/vim*/lang/eo/LC_MESSAGES/vim.mo
%lang(es) %{_datadir}/vim/vim*/lang/es/LC_MESSAGES/vim.mo
%lang(fi) %{_datadir}/vim/vim*/lang/fi/LC_MESSAGES/vim.mo
%lang(fr) %{_datadir}/vim/vim*/lang/fr/LC_MESSAGES/vim.mo
%lang(ga) %{_datadir}/vim/vim*/lang/ga/LC_MESSAGES/vim.mo
%lang(it) %{_datadir}/vim/vim*/lang/it/LC_MESSAGES/vim.mo
%lang(ja) %{_datadir}/vim/vim*/lang/ja/LC_MESSAGES/vim.mo
%lang(ko.UTF-8) %{_datadir}/vim/vim*/lang/ko.UTF-8/LC_MESSAGES/vim.mo
%lang(ko) %{_datadir}/vim/vim*/lang/ko/LC_MESSAGES/vim.mo
%lang(nb) %{_datadir}/vim/vim*/lang/nb/LC_MESSAGES/vim.mo
%lang(no) %{_datadir}/vim/vim*/lang/no/LC_MESSAGES/vim.mo
%lang(pl) %{_datadir}/vim/vim*/lang/pl/LC_MESSAGES/vim.mo
%lang(pt_BR) %{_datadir}/vim/vim*/lang/pt_BR/LC_MESSAGES/vim.mo
%lang(ru) %{_datadir}/vim/vim*/lang/ru/LC_MESSAGES/vim.mo
%lang(sk) %{_datadir}/vim/vim*/lang/sk/LC_MESSAGES/vim.mo
%lang(sv) %{_datadir}/vim/vim*/lang/sv/LC_MESSAGES/vim.mo
%lang(uk) %{_datadir}/vim/vim*/lang/uk/LC_MESSAGES/vim.mo
%lang(da) %{_datadir}/vim/vim*/lang/da/LC_MESSAGES/vim.mo
%lang(lv) %{_datadir}/vim/vim*/lang/lv/LC_MESSAGES/vim.mo
%lang(sr) %{_datadir}/vim/vim*/lang/sr/LC_MESSAGES/vim.mo
%lang(vi) %{_datadir}/vim/vim*/lang/vi/LC_MESSAGES/vim.mo
%lang(tr) %{_datadir}/vim/vim*/lang/tr/LC_MESSAGES/vim.mo
%lang(zh_CN.UTF-8) %{_datadir}/vim/vim*/lang/zh_CN.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_CN) %{_datadir}/vim/vim*/lang/zh_CN/LC_MESSAGES/vim.mo
%lang(zh_TW.UTF-8) %{_datadir}/vim/vim*/lang/zh_TW.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_TW) %{_datadir}/vim/vim*/lang/zh_TW/LC_MESSAGES/vim.mo
%lang(cs.cp1250)  %{_datadir}/vim/vim*/lang/cs.cp1250/LC_MESSAGES/vim.mo
%lang(ja.euc-jp)  %{_datadir}/vim/vim*/lang/ja.euc-jp/LC_MESSAGES/vim.mo
%lang(ja.sjis)    %{_datadir}/vim/vim*/lang/ja.sjis/LC_MESSAGES/vim.mo
%lang(nl)     %{_datadir}/vim/vim*/lang/nl/LC_MESSAGES/vim.mo
%lang(pl.UTF-8)   %{_datadir}/vim/vim*/lang/pl.UTF-8/LC_MESSAGES/vim.mo
%lang(pl.cp1250)  %{_datadir}/vim/vim*/lang/pl.cp1250/LC_MESSAGES/vim.mo
%lang(ru.cp1251)  %{_datadir}/vim/vim*/lang/ru.cp1251/LC_MESSAGES/vim.mo
%lang(sk.cp1250)  %{_datadir}/vim/vim*/lang/sk.cp1250/LC_MESSAGES/vim.mo
%lang(uk.cp1251)  %{_datadir}/vim/vim*/lang/uk.cp1251/LC_MESSAGES/vim.mo
%lang(zh_CN.cp936) %{_datadir}/vim/vim*/lang/zh_CN.cp936/LC_MESSAGES/vim.mo

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/vimrc
%{_datadir}/vim/vim*/syntax/syntax.vim
%{_datadir}/vim/vim*/colors/desert.vim
%{_datadir}/vim/vim*/colors/lists/default.vim
%{_datadir}/vim/vim*/defaults.vim
%{_datadir}/vim/vim*/filetype.vim
%{_datadir}/vim/%{maj_ver}/syntax/nosyntax.vim
%{_datadir}/vim/%{maj_ver}/syntax/syntax.vim
%{_datadir}/vim/%{maj_ver}/autoload/dist/ft.vim
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvim
%{_bindir}/rview
%{_bindir}/vim
%{_bindir}/vimdiff

%changelog
* Fri Feb 16 2024 Srish Srinivasan <srish.srinivasan@broadcom.com> 9.0.2142-1
- Update to v9.0.2142 to fix CVE-2024-22667
* Sat Dec 16 2023 Srish Srinivasan <ssrish@vmware.com> 9.0.2121-1
- Update to v9.0.2121 to fix CVE-2023-48706
* Thu Nov 23 2023 Srish Srinivasan <ssrish@vmware.com> 9.0.2112-1
- Update to v9.0.2112 to fix multiple CVEs
* Thu Nov 02 2023 Srish Srinivasan <ssrish@vmware.com> 9.0.2068-1
- Update to v9.0.2068 to fix CVE-2023-46246
* Tue Oct 10 2023 Srish Srinivasan <ssrish@vmware.com> 9.0.2010-1
- Update to v9.0.2010 to fix multiple CVEs
* Wed Sep 06 2023 Mukul Sikka <msikka@vmware.com> 9.0.1876-1
- Update to v9.0.1876 to fix multiple CVEs
* Fri Aug 11 2023 Srish Srinivasan <ssrish@vmware.com> 9.0.1664-1
- Update to v9.0.1664 to fix CVE-2023-3896
- Keeping it in sync with branch 5.0
* Wed Mar 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.0.1298-3
- Add python3 requires to vim-extra
* Tue Feb 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.0.1298-2
- Fix sh file syntax issue
* Fri Feb 10 2023 Gerrit Photon <photon-checkins@vmware.com> 9.0.1298-1
- Automatic Version Bump
* Mon Jan 16 2023 Shreenidhi Shedi <sshedi@vmware.com> 9.0.1055-2
- Handle E145 exception in vimrc when vim opened in restricted mode
* Wed Dec 14 2022 Gerrit Photon <photon-checkins@vmware.com> 9.0.1055-1
- Automatic Version Bump
* Tue Jun 14 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.5037-1
- Update to 8.2.5037 to fix CVE-2022-1927
* Fri Jun 10 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.5024-1
- Update to 8.2.5024 to fix several CVEs
* Wed May 18 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.4925-1
- Update to 8.2.4925 to fix several CVEs
* Tue Apr 26 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.4827-1
- Update to 8.2.4827
* Wed Apr 06 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.4647-1
- Update to 8.2.4647
* Tue Feb 22 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.2.4436-1
- Update to 8.2.4436
* Thu Dec 02 2021 Shreenidhi Shedi <sshedi@vmware.com> 8.2.3428-3
- Enable skip_defaults_vim in vimrc
* Tue Nov 30 2021 Shreenidhi Shedi <sshedi@vmware.com> 8.2.3428-2
- Move vimrc to source file and add 'set mouse-=a' to /etc/vimrc
* Tue Oct 05 2021 Tapas Kundu <tkundu@vmware.com> 8.2.3428-1
- Update to 8.2.3428 to fix CVE-2021-3796
* Thu Sep 23 2021 Dweep Advani <davani@vmware.com> 8.2.3408-1
- Fix vim startup errors E216, E1187 and E484
- vim-extra requires vim
* Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 8.2.2831-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 8.2.1361-1
- Automatic Version Bump
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 8.2.0190-1
- Automatic Version Bump
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 8.1.0388-5
- Do not conflict with toybox >= 0.8.2-2
* Thu Feb 20 2020 Prashant Singh Chauhan <psinghchauha@vmware.com> 8.1.0388-4
- Fix make check failure
* Tue Jan 29 2019 Dweep Advani <dadvani@vmware.com> 8.1.0388-3
- Fixed swap file creation error for custom login shell
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 8.1.0388-2
- Add conflicts toybox for vim-extra.
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 8.1.0388-1
- Update to version 8.1.0388.
* Tue Jul 10 2018 Tapas Kundu <tkundu@vmware.com> 8.0.0533-4
- Fix for CVE-2017-17087 and CVE-2017-1000382.
* Mon Aug 14 2017 Chang Lee <changlee@vmware.com>  8.0.0533-3
- Disabled Test_recover_root_dir in %check.
* Tue May 02 2017 Anish Swaminathan <anishs@vmware.com>  8.0.0533-2
- Remove tcsh requires.
* Fri Apr 14 2017 Xiaolin Li <xiaolinl@vmware.com> 8.0.0533-1
- Updated to version 8.0.0533.
* Tue Feb 28 2017 Anish Swaminathan <anishs@vmware.com>  7.4-10
- Fix for CVE-2017-6349 and CVE-2017-6350.
* Fri Feb 17 2017 Anish Swaminathan <anishs@vmware.com>  7.4-9
- Fix for CVE-2017-5953.
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  7.4-8
- Fix for CVE-2016-1248.
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 7.4-7
- Modified %check.
* Wed Aug 24 2016 Alexey Makhalov <amakhalov@vmware.com> 7.4-6
- vimrc: Added tags search, tab->spaces and some bindings.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.4-5
- GA - Bump release of all rpms.
* Thu Jul 16 2015 Touseef Liaqat <tliaqat@vmware.com> 7.4-3
- Added profile related files in minimal vim package.
* Tue Jun 30 2015 Touseef Liaqat <tliaqat@vmware.com> 7.4-3
- Pack extra files separately, to make vim package small.
* Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> 7.4-2
- Disable debug package. Use 'desert' colorscheme.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 7.4-1
- Initial build First version.
