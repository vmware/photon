%define migrate_vmw_repo_url() \
prefix_match='^baseurl\\s*=\\s*' \
vmw_url_match='https://packages\\.vmware\\.com/' \
brcm_old_url_match='https://packages-prod\\.broadcom\\.com/' \
brcm_new_url='https://packages.broadcom.com/' \
cd /etc/yum.repos.d \
for repo in %* ; do  \
  repof=/etc/yum.repos.d/${repo}.repo \
  if command -v grep > /dev/null; then \
    grep -q "${prefix_match}${vmw_url_match}" ${repof} || grep -q "${prefix_match}${brcm_old_url_match}" ${repof} || continue \
  fi \
  if command -v sed > /dev/null; then \
    echo "migrating vmware/old broadcom URLs (if any) in ${repo}.repo" >&2 \
    sed -i "s|${prefix_match}${vmw_url_match}|baseurl=${brcm_new_url}|g" ${repof} || : \
    sed -i "s|${prefix_match}${brcm_old_url_match}|baseurl=${brcm_new_url}|g" ${repof} || : \
  fi \
done
