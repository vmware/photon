%define debug_package %{nil}

Summary:        Text editor
Name:           vim
Version:        8.2.3408
Release:        1%{?dist}
License:        Charityware
URL:            http://www.vim.org
Group:          Applications/Editors
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    vim=f53626d97b6d57b2579493f2527fdcf275244017

BuildRequires:  ncurses-devel

%description
The Vim package contains a powerful text editor.

%package    extra
Summary:    Extra files for Vim text editor
Group:      Applications/Editors
Requires:   tcsh
Conflicts:  toybox < 0.8.2-2

%description extra
The vim extra package contains a extra files for powerful text editor.

%prep
%autosetup
echo '#define SYS_VIMRC_FILE "/etc/vimrc"' >> src/feature.h
%build

%configure --enable-multibyte
make VERBOSE=1 %{?_smp_mflags}

%install
# make doesn't support _smp_mflags
make DESTDIR=%{buildroot} install
ln -sv vim %{buildroot}%{_bindir}/vi
install -vdm 755 %{buildroot}/etc
cat > %{buildroot}/etc/vimrc << "EOF"
" Begin /etc/vimrc

set shell=/bin/bash
set nocompatible
set backspace=2
set ruler
syntax on
set tags=./tags;/
color desert
if (&term == "iterm") || (&term == "putty")
  set background=dark
endif
" Binds
nmap <F2> :w<CR>
imap <F2> <Esc>:w<CR>
nmap <F10> :q!<CR>
nmap <Esc><Esc> :q<CR>
" Use 4 space characters instead of tab for python files
au BufEnter,BufNew *.py set tabstop=4 shiftwidth=4 expandtab
" Move the swap file location to protect against CVE-2017-1000382
" More information at http://security.cucumberlinux.com/security/details.php?id=120
if ! isdirectory("~/.vim/swap/")
        call system('install -d -m 700 ~/.vim/swap')
endif
set directory=~/.vim/swap//
" End /etc/vimrc
EOF

%check
sed -i '/source test_recover.vim/d' src/testdir/test_alot.vim
sed -i '916d' src/testdir/test_search.vim
sed -i '454,594d' src/testdir/test_autocmd.vim
sed -i '1,9d' src/testdir/test_modeline.vim
sed -i '133d' ./src/testdir/Make_all.mak
make test %{?_smp_mflags}

%post
if ! sed -n -e '0,/[[:space:]]*call[[:space:]]\+system\>/p' %{_sysconfdir}/vimrc | \
     grep -q '^[[:space:]]*set[[:space:]]\+shell=/bin/bash'
then
    sed -i -e 's#^\([[:space:]]*\)\(call[[:space:]]\+system.*\)$#\1set shell=/bin/bash\n\1\2#g' \
        %{_sysconfdir}/vimrc
fi

%files extra
%defattr(-,root,root)
%{_bindir}/vimtutor
%{_bindir}/xxd
%{_mandir}/*/*
%doc %{_datarootdir}/vim/vim82/doc/*
%{_datarootdir}/vim/vim82/autoload/*
%{_datarootdir}/vim/vim82/bugreport.vim
%{_datarootdir}/vim/vim82/colors/*
%{_datarootdir}/applications/gvim.desktop
%{_datarootdir}/applications/vim.desktop
%{_datarootdir}/icons/hicolor/48x48/apps/gvim.png
%{_datarootdir}/icons/locolor/16x16/apps/gvim.png
%{_datarootdir}/icons/locolor/32x32/apps/gvim.png
%{_datarootdir}/vim/vim82/defaults.vim
%{_datarootdir}/vim/vim82/pack/dist/opt/*
%exclude %{_datarootdir}/vim/vim82/colors/desert.vim
%{_datarootdir}/vim/vim82/compiler/*
%{_datarootdir}/vim/vim82/delmenu.vim
%{_datarootdir}/vim/vim82/evim.vim
%{_datarootdir}/vim/vim82/filetype.vim
%{_datarootdir}/vim/vim82/ftoff.vim
%{_datarootdir}/vim/vim82/ftplugin.vim
%{_datarootdir}/vim/vim82/ftplugin/*
%{_datarootdir}/vim/vim82/ftplugof.vim
%{_datarootdir}/vim/vim82/gvimrc_example.vim
%{_datarootdir}/vim/vim82/indent.vim
%{_datarootdir}/vim/vim82/indent/*
%{_datarootdir}/vim/vim82/indoff.vim
%{_datarootdir}/vim/vim82/keymap/*
%{_datarootdir}/vim/vim82/macros/*
%{_datarootdir}/vim/vim82/menu.vim
%{_datarootdir}/vim/vim82/mswin.vim
%{_datarootdir}/vim/vim82/optwin.vim
%{_datarootdir}/vim/vim82/plugin/*
%{_datarootdir}/vim/vim82/synmenu.vim
%{_datarootdir}/vim/vim82/vimrc_example.vim
%{_datarootdir}/vim/vim82/print/*
%{_datarootdir}/vim/vim82/scripts.vim
%{_datarootdir}/vim/vim82/spell/*
%{_datarootdir}/vim/vim82/syntax/*
%exclude %{_datarootdir}/vim/vim82/syntax/syntax.vim
%{_datarootdir}/vim/vim82/tools/*
%{_datarootdir}/vim/vim82/tutor/*
%{_datarootdir}/vim/vim82/lang/*.vim
%doc %{_datarootdir}/vim/vim82/lang/*.txt
%lang(af) %{_datarootdir}/vim/vim82/lang/af/LC_MESSAGES/vim.mo
%lang(ca) %{_datarootdir}/vim/vim82/lang/ca/LC_MESSAGES/vim.mo
%lang(cs) %{_datarootdir}/vim/vim82/lang/cs/LC_MESSAGES/vim.mo
%lang(de) %{_datarootdir}/vim/vim82/lang/de/LC_MESSAGES/vim.mo
%lang(eb_GB) %{_datarootdir}/vim/vim82/lang/en_GB/LC_MESSAGES/vim.mo
%lang(eo) %{_datarootdir}/vim/vim82/lang/eo/LC_MESSAGES/vim.mo
%lang(es) %{_datarootdir}/vim/vim82/lang/es/LC_MESSAGES/vim.mo
%lang(fi) %{_datarootdir}/vim/vim82/lang/fi/LC_MESSAGES/vim.mo
%lang(fr) %{_datarootdir}/vim/vim82/lang/fr/LC_MESSAGES/vim.mo
%lang(ga) %{_datarootdir}/vim/vim82/lang/ga/LC_MESSAGES/vim.mo
%lang(it) %{_datarootdir}/vim/vim82/lang/it/LC_MESSAGES/vim.mo
%lang(ja) %{_datarootdir}/vim/vim82/lang/ja/LC_MESSAGES/vim.mo
%lang(ko.UTF-8) %{_datarootdir}/vim/vim82/lang/ko.UTF-8/LC_MESSAGES/vim.mo
%lang(ko) %{_datarootdir}/vim/vim82/lang/ko/LC_MESSAGES/vim.mo
%lang(nb) %{_datarootdir}/vim/vim82/lang/nb/LC_MESSAGES/vim.mo
%lang(no) %{_datarootdir}/vim/vim82/lang/no/LC_MESSAGES/vim.mo
%lang(pl) %{_datarootdir}/vim/vim82/lang/pl/LC_MESSAGES/vim.mo
%lang(pt_BR) %{_datarootdir}/vim/vim82/lang/pt_BR/LC_MESSAGES/vim.mo
%lang(ru) %{_datarootdir}/vim/vim82/lang/ru/LC_MESSAGES/vim.mo
%lang(sk) %{_datarootdir}/vim/vim82/lang/sk/LC_MESSAGES/vim.mo
%lang(sv) %{_datarootdir}/vim/vim82/lang/sv/LC_MESSAGES/vim.mo
%lang(uk) %{_datarootdir}/vim/vim82/lang/uk/LC_MESSAGES/vim.mo
%lang(da) %{_datarootdir}/vim/vim82/lang/da/LC_MESSAGES/vim.mo
%lang(lv) %{_datarootdir}/vim/vim82/lang/lv/LC_MESSAGES/vim.mo
%lang(sr) %{_datarootdir}/vim/vim82/lang/sr/LC_MESSAGES/vim.mo
%lang(vi) %{_datarootdir}/vim/vim82/lang/vi/LC_MESSAGES/vim.mo
%lang(tr) %{_datarootdir}/vim/vim82/lang/tr/LC_MESSAGES/vim.mo
%lang(zh_CN.UTF-8) %{_datarootdir}/vim/vim82/lang/zh_CN.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_CN) %{_datarootdir}/vim/vim82/lang/zh_CN/LC_MESSAGES/vim.mo
%lang(zh_TW.UTF-8) %{_datarootdir}/vim/vim82/lang/zh_TW.UTF-8/LC_MESSAGES/vim.mo
%lang(zh_TW) %{_datarootdir}/vim/vim82/lang/zh_TW/LC_MESSAGES/vim.mo
%lang(cs.cp1250)  %{_datarootdir}/vim/vim82/lang/cs.cp1250/LC_MESSAGES/vim.mo
%lang(ja.euc-jp)  %{_datarootdir}/vim/vim82/lang/ja.euc-jp/LC_MESSAGES/vim.mo
%lang(ja.sjis)    %{_datarootdir}/vim/vim82/lang/ja.sjis/LC_MESSAGES/vim.mo
%lang(nl)     %{_datarootdir}/vim/vim82/lang/nl/LC_MESSAGES/vim.mo
%lang(pl.UTF-8)   %{_datarootdir}/vim/vim82/lang/pl.UTF-8/LC_MESSAGES/vim.mo
%lang(pl.cp1250)  %{_datarootdir}/vim/vim82/lang/pl.cp1250/LC_MESSAGES/vim.mo
%lang(ru.cp1251)  %{_datarootdir}/vim/vim82/lang/ru.cp1251/LC_MESSAGES/vim.mo
%lang(sk.cp1250)  %{_datarootdir}/vim/vim82/lang/sk.cp1250/LC_MESSAGES/vim.mo
%lang(uk.cp1251)  %{_datarootdir}/vim/vim82/lang/uk.cp1251/LC_MESSAGES/vim.mo
%lang(zh_CN.cp936) %{_datarootdir}/vim/vim82/lang/zh_CN.cp936/LC_MESSAGES/vim.mo

%files
%defattr(-,root,root)
%config(noreplace) /etc/vimrc
%{_datarootdir}/vim/vim82/syntax/syntax.vim
%{_datarootdir}/vim/vim82/rgb.txt
%{_datarootdir}/vim/vim82/colors/desert.vim
%{_bindir}/ex
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/rvim
%{_bindir}/rview
%{_bindir}/vim
%{_bindir}/vimdiff

%changelog
*   Wed Sep 15 2021 Tapas Kundu <tkundu@vmware.com> 8.2.3408-1
-   Fix CVE-2021-3770
*   Fri Jul 03 2020 Prashant S Chauhan <psinghchauha@vmware.com> 8.1.1365-2
-   Do not conflict with toybox >= 0.8.2-2
*   Thu Jun 04 2020 Tapas Kundu <tkundu@vmware.com> 8.1.1365-1
-   Update to 8.1.1365 to take Ex command changes along with CVE-2019-20807
*   Mon Jun 1 2020 Anisha Kumari <kanisha@vmware.com> 8.1.0388-7
-   Fix for CVE-2019-20807.
*   Thu Feb 20 2020 Prashant Singh Chauhan <psinghchauha@vmware.com> 8.1.0388-6
-   Fix make check failure
*   Wed Sep 25 2019 Prashant Singh Chauhan <psinghchauha@vmware.com> 8.1.0388-5
-   Removed tests since make-check job was getting stuck on that test
*   Wed Aug 14 2019 Anisha Kumari <kanisha@vmware.com> 8.1.0388-4
-   Fix for CVE-2019-12735.
*   Tue Jan 29 2019 Dweep Advani <dadvani@vmware.com> 8.1.0388-3
-   Fixed swap file creation error for custom login shell
*   Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 8.1.0388-2
-   Add conflicts toybox for vim-extra.
*   Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 8.1.0388-1
-   Update to version 8.1.0388.
*   Tue Jul 10 2018 Tapas Kundu <tkundu@vmware.com> 8.0.0533-4
-   Fix for CVE-2017-17087 and CVE-2017-1000382.
*   Mon Aug 14 2017 Chang Lee <changlee@vmware.com>  8.0.0533-3
-   Disabled Test_recover_root_dir in %check.
*   Tue May 02 2017 Anish Swaminathan <anishs@vmware.com>  8.0.0533-2
-   Remove tcsh requires.
*   Fri Apr 14 2017 Xiaolin Li <xiaolinl@vmware.com> 8.0.0533-1
-   Updated to version 8.0.0533.
*   Tue Feb 28 2017 Anish Swaminathan <anishs@vmware.com>  7.4-10
-   Fix for CVE-2017-6349 and CVE-2017-6350.
*   Fri Feb 17 2017 Anish Swaminathan <anishs@vmware.com>  7.4-9
-   Fix for CVE-2017-5953.
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  7.4-8
-   Fix for CVE-2016-1248.
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 7.4-7
-   Modified %check.
*   Wed Aug 24 2016 Alexey Makhalov <amakhalov@vmware.com> 7.4-6
-   vimrc: Added tags search, tab->spaces and some bindings.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.4-5
-   GA - Bump release of all rpms.
*   Thu Jul 16 2015 Touseef Liaqat <tliaqat@vmware.com> 7.4-3
-   Added profile related files in minimal vim package.
*   Tue Jun 30 2015 Touseef Liaqat <tliaqat@vmware.com> 7.4-3
-   Pack extra files separately, to make vim package small.
*   Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> 7.4-2
-   Disable debug package. Use 'desert' colorscheme.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 7.4-1
-   Initial build First version.
