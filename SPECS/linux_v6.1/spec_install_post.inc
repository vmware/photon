%define __modules_install_post\
  find %{buildroot}%{_modulesdir} -name *.ko -type f -print0 |\
    xargs -t -0 -r -P$(nproc) -n1 sh -c '\
      ./scripts/sign-file sha512 certs/signing_key.pem certs/signing_key.x509 $0\
      xz -T $(nproc) $0\
      rm -f $0.{sig,dig}'\
%{nil}

# __os_install_post strips signature from modules. We need to re-sign & recompress.
# Extra step is added to default __spec_install_post.
%define __spec_install_post\
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__modules_install_post}\
%{nil}
