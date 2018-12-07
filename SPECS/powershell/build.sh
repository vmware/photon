#!/bin/bash
#See https://github.com/PowerShell/PowerShell/blob/master/docs/building/internals.md

set -e

pushd src/powershell-unix
dotnet restore
popd

pushd src/ResGen
dotnet restore
dotnet run
popd

pushd src

targetFile="Microsoft.PowerShell.SDK/obj/Microsoft.PowerShell.SDK.csproj.TypeCatalog.targets"
cat > $targetFile <<-"EOF"
<Project>
    <Target Name="_GetDependencies"
            DependsOnTargets="ResolveAssemblyReferencesDesignTime">
        <ItemGroup>
            <_RefAssemblyPath Include="%(_ReferencesFromRAR.HintPath)%3B"  Condition=" '%(_ReferencesFromRAR.NuGetPackageId)' != 'Microsoft.Management.Infrastructure' "/>
        </ItemGroup>
        <WriteLinesToFile File="$(_DependencyFile)" Lines="@(_RefAssemblyPath)" Overwrite="true" />
    </Target>
</Project>
EOF
dotnet msbuild Microsoft.PowerShell.SDK/Microsoft.PowerShell.SDK.csproj /t:_GetDependencies "/property:DesignTimeBuild=true;_DependencyFile=$(pwd)/TypeCatalogGen/powershell.inc" /nologo
popd

pushd src/TypeCatalogGen
dotnet restore
dotnet run ../System.Management.Automation/CoreCLR/CorePsTypeCatalog.cs powershell.inc
popd

#build libpsl
pushd src/libpsl-native
cmake -DCMAKE_BUILD_TYPE=Debug .
make -j
popd

#
touch DELETE_ME_TO_DISABLE_CONSOLEHOST_TELEMETRY
dotnet publish /property:GenerateFullPaths=true --configuration Linux --framework netcoreapp2.1 --runtime linux-x64 src/powershell-unix --output bin
