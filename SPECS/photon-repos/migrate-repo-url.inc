%define migrate_vmw_repo_url() \
prefix_match='^baseurl\\s*=\\s*' \
vmw_url_match='https://packages\\.vmware\\.com/' \
brcm_url='https://packages-prod.broadcom.com/' \
cd /etc/yum.repos.d \
for repo in %* ; do  \
  repof=/etc/yum.repos.d/${repo}.repo \
  if command -v grep > /dev/null; then \
    grep -q "${prefix_match}${vmw_url_match}" ${repof} || continue \
  fi \
  if command -v sed > /dev/null; then \
    echo "migrating vmware URLs (if any) in ${repo}.repo" >&2 \
    sed -i "s|${prefix_match}${vmw_url_match}|baseurl=${brcm_url}|g" ${repof} || : \
  fi \
done
