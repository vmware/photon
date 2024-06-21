# __debug_package won't work if files don't have exec permission
# So, we set exec permission for all .ko files
# Then __debug_install_post will run which will collect data for creating debuginfo package
# Then we remove this exec permission while signing in sign_and_compress.sh

%define __spec_install_post\
  find %{buildroot}%{_modulesdir} -name '*.ko' -print0 | xargs -0 chmod a+x\
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  bash sign_and_compress.sh %{buildroot}%{_modulesdir} ${PWD}\
%{nil}
