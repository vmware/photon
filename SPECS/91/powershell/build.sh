#!/bin/bash

set -ex

# Powershell related build instructions

# See https://github.com/PowerShell/PowerShell/blob/master/docs/building/internals.md

export DOTNET_NOLOGO=true
export DOTNET_CLI_TELEMETRY_OPTOUT=true

for f in powershell-unix ResGen TypeCatalogGen; do
  dotnet restore src/${f} -s $HOME/.nuget
done

pushd src/ResGen
dotnet run --no-restore
popd

inc_file="$PWD/src/TypeCatalogGen/powershell_linux-x64.inc"

pushd src
cp Microsoft.PowerShell.SDK.csproj.TypeCatalog.targets Microsoft.PowerShell.SDK/obj
dotnet msbuild \
  Microsoft.PowerShell.SDK/Microsoft.PowerShell.SDK.csproj \
  -t:_GetDependencies \
  -p:DesignTimeBuild=true \
  -p:_DependencyFile=$inc_file \
  -nologo
popd

dotnet run \
  --no-restore \
  --project src/TypeCatalogGen \
  src/System.Management.Automation/CoreCLR/CorePsTypeCatalog.cs \
  "$inc_file"

touch DELETE_ME_TO_DISABLE_CONSOLEHOST_TELEMETRY

dotnet publish \
  --no-restore \
  --runtime linux-x64 \
  --no-self-contained \
  --configuration Release \
  --output bin \
  src/powershell-unix/

# Even after powershell rpm built, dotnet processes are alive, following to stop them:
for pid in $(pgrep dotnet); do
  if [ -n "${pid}" ]; then
    kill -0 "${pid}" && kill -TERM "${pid}" || :
  fi
done
