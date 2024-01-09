#!/bin/bash

set -ex

if false; then
  topdir="${PWD}/.."
  cwd="${PWD}"

  ps_linux_ver="7.1.5"
  libmi_tag="v1.6.9-0"

  # Build libmi

  # The default libmi.so file that comes with powershell (for example powershell-7.1.5-linux-x64.tar.gz)
  # needs libcrypto.1.0.0, we need it to be linked with openssl-1.1.1 (what's present in Photon)
  # Hence we need to re-build it.

  # Pre requisites:

  #tdnf install -y build-essential wget git openssl-devel Linux-PAM-devel krb5-devel e2fsprogs-devel which

  cd "${topdir}"

  wget https://raw.githubusercontent.com/OpenMandrivaSoftware/lsb-release/master/lsb_release
  chmod +x lsb_release && mv lsb_release /usr/bin

  ln -sfv /usr/lib/libssl.so.1.1 /usr/lib/libssl.so
  ln -sfv /usr/lib/libcrypto.so.1.1 /usr/lib/libcrypto.so

  # Actual task
  git clone https://github.com/microsoft/omi.git
  cd omi/Unix && git checkout -b "${libmi_tag}" tags/"${libmi_tag}" && ./configure && make -j32
  mv ./output/lib/libmi.so "${topdir}"/powershell-linux-"${ps_linux_ver}"

  cd "${cwd}"
  rm -rf "${topdir}"/omi
fi

# Powershell related build instructions

# See https://github.com/PowerShell/PowerShell/blob/master/docs/building/internals.md

for f in src/powershell-unix src/ResGen src/TypeCatalogGen; do
  dotnet restore $f
done

pushd src/ResGen
dotnet run
popd

pushd src
cp Microsoft.PowerShell.SDK.csproj.TypeCatalog.targets Microsoft.PowerShell.SDK/obj
dotnet msbuild Microsoft.PowerShell.SDK/Microsoft.PowerShell.SDK.csproj /t:_GetDependencies "/property:DesignTimeBuild=true;_DependencyFile=$(pwd)/TypeCatalogGen/powershell.inc" /nologo
popd

pushd src/TypeCatalogGen
dotnet run ../System.Management.Automation/CoreCLR/CorePsTypeCatalog.cs powershell.inc
popd

touch DELETE_ME_TO_DISABLE_CONSOLEHOST_TELEMETRY
dotnet publish /property:GenerateFullPaths=true --configuration Linux --framework net6.0 --runtime linux-x64 src/powershell-unix --output bin

# Even after powershell rpm built, dotnet processes are alive, following to stop them:
killall -15 dotnet
