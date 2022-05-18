%define debug_package %{nil}
%global maj_ver vim82

Summary:        Text editor
Name:           vim
Version:        8.2.4925
Release:        1%{?dist}
License:        Charityware
URL:            http://www.vim.org
Group:          Applications/Editors
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=0b11344bc505c76aa5853effca7959eb997635c3815b0d9cb0bc58c306246306a6b37bcddcaf07104e773f05972a5ec9f397818ca45f3fed6ca95f2cfca6783d
Source1:        vimrc

BuildRequires:  ncurses-devel

%description
The VIM package contains a powerful text editor.

%package    extra
Summary:    Extra files for Vim text editor
Group:      Applications/Editors
Requires:   tcsh
Requires:   %{name} = %{version}-%{release}
Conflicts:  toybox < 0.8.2-2

%description extra
The vim extra package contains a extra files for powerful text editor.

%prep
%autosetup -p1
echo '#define SYS_VIMRC_FILE "/etc/vimrc"' >> src/feature.h

%build
%configure --enable-multibyte
make VERBOSE=1 %{?_smp_mflags}

%install
# make doesn't support _smp_mflags
make DESTDIR=%{buildroot} install
ln -sfv vim %{buildroot}%{_bindir}/vi
install -vdm 755 %{buildroot}%{_sysconfdir}
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/vimrc

%check
sed -i '/source test_recover.vim/d' src/testdir/test_alot.vim
sed -i '916d' src/testdir/test_search.vim
sed -i '454,594d' src/testdir/test_autocmd.vim
sed -i '1,9d' src/testdir/test_modeline.vim
sed -i '133d' ./src/testdir/Make_all.mak
make test %{?_smp_mflags}

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
%doc %{_datarootdir}/vim/vim*/doc/*
%{_datarootdir}/vim/vim*/autoload/*
%{_datarootdir}/vim/vim*/bugreport.vim
%{_datarootdir}/vim/vim*/colors/*
%{_datarootdir}/applications/gvim.desktop
%{_datarootdir}/applications/vim.desktop
%{_datarootdir}/icons/hicolor/48x48/apps/gvim.png
%{_datarootdir}/icons/locolor/16x16/apps/gvim.png
%{_datarootdir}/icons/locolor/32x32/apps/gvim.png
%{_datarootdir}/vim/vim*/pack/dist/opt/*
%exclude %{_datarootdir}/vim/vim*/colors/desert.vim
%exclude %{_datarootdir}/vim/vim*/colors/lists/default.vim
%{_datarootdir}/vim/vim*/compiler/*
%{_datarootdir}/vim/vim*/delmenu.vim
%{_datarootdir}/vim/vim*/evim.vim
%{_datarootdir}/vim/vim*/ftoff.vim
%{_datarootdir}/vim/vim*/ftplugin.vim
%{_datarootdir}/vim/vim*/ftplugin/*
%{_datarootdir}/vim/vim*/ftplugof.vim
%{_datarootdir}/vim/vim*/gvimrc_example.vim
%{_datarootdir}/vim/vim*/indent.vim
%{_datarootdir}/vim/vim*/indent/*
%{_datarootdir}/vim/vim*/indoff.vim
%{_datarootdir}/vim/vim*/keymap/*
%{_datarootdir}/vim/vim*/macros/*
%{_datarootdir}/vim/vim*/menu.vim
%{_datarootdir}/vim/vim*/mswin.vim
%{_datarootdir}/vim/vim*/optwin.vim
%{_datarootdir}/vim/vim*/plugin/*
%{_datarootdir}/vim/vim*/synmenu.vim
%{_datarootdir}/vim/vim*/vimrc_example.vim
%{_datarootdir}/vim/vim*/print/*
%{_datarootdir}/vim/vim*/scripts.vim
%{_datarootdir}/vim/%{maj_ver}/import/dist/vimhelp.vim
%{_datarootdir}/vim/vim*/spell/*
%{_datarootdir}/vim/vim*/syntax/*
%exclude %{_datarootdir}/vim/%{maj_ver}/syntax/nosyntax.vim
%exclude %{_datarootdir}/vim/vim*/syntax/syntax.vim
%exclude %{_datarootdir}/vim/%{maj_ver}/autoload/dist/ft.vim
%{_datarootdir}/vim/vim*/tools/*
%{_datarootdir}/vim/vim*/tutor/*
%{_datarootdir}/vim/vim*/lang/*.vim
%doc %{_datarootdir}/vim/vim*/lang/*.txt
%lang(af) %{_datarootdir}/vim/vim*/lang/af/LC_MESSAGES/vim.mo
%lang(ca) %{_datarootdir}/vim/vim*/lang/ca/LC_MESSAGES/vim.mo
%lang(cs) %{_datarootdir}/vim/vim*/lang/cs/LC_MESSAGES/vim.mo
%lang(de) %{_datarootdir}/vim/vim*/lang/de/LC_MESSAGES/vim.mo
%lang(eb_GB) %{_datarootdir}/vim/vim*/lang/en_GB/LC_MESSAGES/vim.mo
%lang(eo) %{_datarootdir}/vim/vim*/lang/eo/LC_MESSAGES/vim.mo
%lang(es) %{_datarootdir}/vim/vim*/lang/es/LC_MESSAGES/vim.mo
%lang(fi) %{_datarootdir}/vim/vim*/lang/fi/LC_MESSAGES/vim.mo
%lang(fr) %{_datarootdir}/vim/vim*/lang/fr/LC_MESSAGES/vim.mo
%lang(ga) %{_datarootdir}/vim/vim*/lang/ga/LC_MESSAGES/vim.mo
%lang(it) %{_datarootdir}/vim/vim*/lang/it/LC_MESSAGES/vim.mo
%lang(ja) %{_datarootdir}/vim/vim*/lang/ja/LC_MESSAGES/vim.mo
%lang(ko.UTF-8) %{_datarootdir}/vim/vim*/lang/ko.UTF-8/LC_MESSAGES/vim.mo
%lang(ko) %{_datarootdir}/vim/vim*/lang/ko/LC_MESSAGES/vim.mo
%lang(nb) %{_datarootdir}/vim/vim*/lang/nb/LC_MESSAGES/vim.mo
%lang(no) %{_datarootdir}/vim/vim*/lang/no/LC_MESSAGES/vim.mo
%lang(pl) %{_datarootdir}/vim/vim*/lang/pl/LC_MESSAGES/vim.mo
%lang(pt_BR) %{_datarootdir}/vim/vim*/lang/pt_BR/LC_MESSAGES/vim.mo
%lang(ru) %{_datarootdir}/vim/vim*/lang/ru/LC_MESSAGES/vim.mo
%lang(sk) %{_datarootdir}/vim/vim*/lang/sk/LC_MESSAGES/vim.mo
%lang(sv) %{_datarootdir}/vim/vim*/lang/sv/LC_MESSAGES/vim.mo
%lang(uk) %{_datarootdir}/vim/vim*/lang/uk/LC_MESSAGES/vim.mo
%lang(da) %{_datarootdir}/vim/vim*/lang/da/LC_MESSAGES/vim.mo
%lang(lv) %{_datarootdir}/vim/vim*/lang/lv/LC_MESSAGES/vim.mo
%lang(sr) %{_datarootdir}/vim/vim*/lang/sr/LC_MESSAGES/vim.mo
%lang(vi) %{_datarootdir}/vim/vim*/lang/vi/LC_MESSAGES/vim.mo
%lang(tr) %{_datarootdir}/vim/vim*/lang/tr/LC_MESSAGES/vim.mo
%lang(zh_CN.UTF-8) %{_datarootdir}/vim/vim*/lang/zh_CN.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_CN) %{_datarootdir}/vim/vim*/lang/zh_CN/LC_MESSAGES/vim.mo
%lang(zh_TW.UTF-8) %{_datarootdir}/vim/vim*/lang/zh_TW.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_TW) %{_datarootdir}/vim/vim*/lang/zh_TW/LC_MESSAGES/vim.mo
%lang(cs.cp1250)  %{_datarootdir}/vim/vim*/lang/cs.cp1250/LC_MESSAGES/vim.mo
%lang(ja.euc-jp)  %{_datarootdir}/vim/vim*/lang/ja.euc-jp/LC_MESSAGES/vim.mo
%lang(ja.sjis)    %{_datarootdir}/vim/vim*/lang/ja.sjis/LC_MESSAGES/vim.mo
%lang(nl)     %{_datarootdir}/vim/vim*/lang/nl/LC_MESSAGES/vim.mo
%lang(pl.UTF-8)   %{_datarootdir}/vim/vim*/lang/pl.UTF-8/LC_MESSAGES/vim.mo
%lang(pl.cp1250)  %{_datarootdir}/vim/vim*/lang/pl.cp1250/LC_MESSAGES/vim.mo
%lang(ru.cp1251)  %{_datarootdir}/vim/vim*/lang/ru.cp1251/LC_MESSAGES/vim.mo
%lang(sk.cp1250)  %{_datarootdir}/vim/vim*/lang/sk.cp1250/LC_MESSAGES/vim.mo
%lang(uk.cp1251)  %{_datarootdir}/vim/vim*/lang/uk.cp1251/LC_MESSAGES/vim.mo
%lang(zh_CN.cp936) %{_datarootdir}/vim/vim*/lang/zh_CN.cp936/LC_MESSAGES/vim.mo

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/vimrc
%{_datarootdir}/vim/vim*/syntax/syntax.vim
%{_datarootdir}/vim/vim*/colors/desert.vim
%{_datarootdir}/vim/vim*/colors/lists/default.vim
%{_datarootdir}/vim/vim*/defaults.vim
%{_datarootdir}/vim/vim*/filetype.vim
%{_datarootdir}/vim/%{maj_ver}/syntax/nosyntax.vim
%{_datarootdir}/vim/%{maj_ver}/syntax/syntax.vim
%{_datarootdir}/vim/%{maj_ver}/autoload/dist/ft.vim
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvim
%{_bindir}/rview
%{_bindir}/vim
%{_bindir}/vimdiff

%changelog
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
