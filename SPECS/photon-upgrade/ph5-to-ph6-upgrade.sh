# set the next Photon OS version to upgrade to
TO_VERSION=''    # Photon OS 5.0 is the latest and hence left empty

declare -a deprecated_packages_arr=(
  # Deprecated package names will be populated on next Photon OS release
)

# This hashtable maps package name changes
# we do not expect any core packages here
declare -A replaced_pkgs_map=(
  # Replaced and Replacing Package names map will be populated on next
  # Photon OS release
)

# Residual pkgs to remove post upgrade
declare -a residual_pkgs_arr=(
  # libmetalink libdb libdb-docs
)

# Take care of pre upgrade config changes
function fix_pre_upgrade_config() {
  return 0
}

# Take care of post upgrade config changes
function fix_post_upgrade_config() {
  return 0
}
