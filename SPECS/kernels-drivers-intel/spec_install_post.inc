%define __modules_install_post\
  find %{buildroot}%{_modulesdir} -name *.ko -type f -print0 | xargs -0 xz\
%{nil}

# Extra step is added to default __spec_install_post to compress the module file
%define __spec_install_post\
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__modules_install_post}\
%{nil}
