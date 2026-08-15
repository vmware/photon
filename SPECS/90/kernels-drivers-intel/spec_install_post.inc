# Module signing
%define sign_module() \
  %{signing_script} --file_type ko \\\
        --config_file %{signing_params} \\\
        --auth_file %{signing_auth} \\\
        --artifact \\\
%{nil}

%define __modules_install_post\
  find %{buildroot}%{_modulesdir} -name *.ko -type f -print0 | while IFS= read -r -d '' file; do \
    if [ -n "%{?signing_script}" ]; then \
      %{sign_module} "$file" \
    fi \
    xz "$file"\
  done\
%{nil}

# Extra step is added to default __spec_install_post to sign and compress the module file
%define __spec_install_post\
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__modules_install_post}\
%{nil}
