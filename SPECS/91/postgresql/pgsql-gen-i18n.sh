# Create file lists, for --enable-nls and i18n
localeDirActual="%{_pgbaseinstdir}/share/locale"
localeDir="%{buildroot}${localeDirActual}"

moFiles=($(find ${localeDir} -type f -name '*.mo' \
  | sed "s/-%{pgmajorversion}\.mo$//" \
  | xargs -n1 basename \
  | sort -u))

for m in ${moFiles[@]}; do
  %find_lang "${m}-%{pgmajorversion}"
done

cat *.lang > %{name}.lst

i18nLstPath="$(realpath %{name}.lst)"
pushd ${localeDir}
find . -type d | sed 's|^\.||' | sed "s|^|%dir ${localeDirActual}|" >> ${i18nLstPath}
popd
