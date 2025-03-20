# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%ifarch x86_64
%global parch x86_64
%else
%global parch i386
%endif

%global pkgver 2024
%global pkgrel 1224
%global repo https://shop.softmaker.com/repo
%global pkgdir office%{pkgver}
%global dist %{?dist}

Name:           softmaker-office
Version:        %{pkgver}.%{pkgrel}
Release:        2%{?dist}
Epoch:          1
Summary:        SoftMaker Office %{pkgver} for Linux

License:        Proprietary
URL:            https://www.softmaker.de
Source0:        %{repo}/rpm/%{parch}/RPMS/%{name}-%{pkgver}-%{pkgrel}.%{parch}.rpm
Source1:        %{repo}/linux-repo-public.key

ExclusiveArch:  %{ix86} x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       google-noto-sans-fonts
Requires:       google-noto-sans-cjk-ttc-fonts
Requires:       open-sans-fonts

%global __provides_exclude_from ^%{_libdir}/%{name}/.*

%global __requires_exclude ^libCSegmentation\\.so.*$
%global __requires_exclude %__requires_exclude|^libCTokenizer\\.so.*$
%global __requires_exclude %__requires_exclude|^libDpfDict\\.so.*$
%global __requires_exclude %__requires_exclude|^libdpf\\.so.*$
%global __requires_exclude %__requires_exclude|^libgamorphDpf\\.so.*$
%global __requires_exclude %__requires_exclude|^libSGAnalyseSP\\.so.*$
%global __requires_exclude %__requires_exclude|^libsprt4-7-0.*\\.so.*$
%global __requires_exclude %__requires_exclude|^libsx\\.so.*$

%description
SoftMaker Office is a powerful, fast and Microsoft Office-compatible office
suite.
It comes with the TextMaker word processor, the spreadsheet program PlanMaker
and the presentations software Presentations.


%prep
%setup -c -T
rpm2cpio %{S:0} | cpio -imd --no-absolute-filenames

tar xf usr/share/%{pkgdir}/dwr.tar.lzma -C usr/share/%{pkgdir}/
rm -f usr/share/%{pkgdir}/dwr.tar.lzma
rm -f usr/share/%{pkgdir}/add_rpm_repo.sh
rm -f usr/share/%{pkgdir}/fonts/Noto*
rm -f usr/share/%{pkgdir}/fonts/OpenSans*

find usr/share/%{pkgdir}/ -name '*.so*' | xargs chmod +x
find usr/share/%{pkgdir}/ -name '*.dwr*' | xargs chmod -x
find usr/share/%{pkgdir}/ -name '*.iwr*' | xargs chmod -x

mv usr/share/%{pkgdir}/icons .
mv usr/share/%{pkgdir}/mime .

sed -e 's|glob pattern=|glob weight="40" pattern=|g' -i mime/%{name}-%{pkgver}.xml

mv mime/*.desktop .
rename -- '-%{pkgver}' '' *.desktop
for i in *.desktop ;do
  mv $i %{name}-$i
done
sed \
  -e '/^ $/d' \
  -e '/Name=/s| %{pkgver}||g' \
  -e 's|12;application/vnd.openxmlformats-officedocument.spreadsheetml.template;|12;|' \
  -i *.desktop


%build

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
mv usr/share/%{pkgdir}/* %{buildroot}%{_libdir}/%{name}/

chrpath --delete %{buildroot}%{_libdir}/%{name}/planmaker
chrpath --delete %{buildroot}%{_libdir}/%{name}/presentations
chrpath --delete %{buildroot}%{_libdir}/%{name}/textmaker
chrpath -k --delete %{buildroot}%{_libdir}/%{name}/dpf3/*.so*

mkdir -p %{buildroot}%{_bindir}
for file in planmaker textmaker ;do
cat > %{buildroot}%{_bindir}/${file} <<EOF
#!/usr/bin/bash
LD_LIBRARY_PATH="%{_libdir}/%{name}/dpf3\${LD_LIBRARY_PATH:+:\$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec %{_libdir}/%{name}/${file} "\$@"
EOF
done

cat > %{buildroot}%{_bindir}/presentations <<'EOF'
#!/usr/bin/bash
# A script to run Presentations.

shopt -s nocasematch
presentationsbin=%{_libdir}/%{name}/presentations
LD_LIBRARY_PATH="%{_libdir}/%{name}/dpf3${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
case "$@" in
  *.prs|*.pps|*.ppsx)
    exec ${presentationsbin} -S\""$*"\"
    ;;
  *)
    exec ${presentationsbin} "$@"
    ;;
esac
EOF

chmod 0755 %{buildroot}%{_bindir}/*

mkdir -p %{buildroot}%{_datadir}/applications
desktopinstall() {
  desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    --remove-category=Application \
    --remove-key=Encoding \
    --remove-key=Path \
    --remove-key=TryExec \
    --set-icon=%{name}-$1 \
    --set-key=Exec \
    --set-value="$2 %F" \
  %{name}-$2.desktop
}

desktopinstall pml planmaker
desktopinstall prl presentations
desktopinstall tml textmaker

for res in 16 24 32 48 64 128 256 512 1024;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}
  mkdir -p ${dir}/{apps,mimetypes}
  for icon in pml prl tml ;do
    install -pm0644 icons/${icon}_${res}.png \
      ${dir}/apps/%{name}-${icon}.png
  done
  for icon in pmd pmd_mso pmd_oth prd prd_mso prd_oth tmd tmd_mso tmd_oth ;do
    install -pm0644 icons/${icon}_${res}.png \
      ${dir}/mimetypes/application-x-${icon//_/-}.png
  done
done

mkdir -p %{buildroot}%{_datadir}/mime/packages
install -pm0644 mime/%{name}-%{pkgver}.xml \
  %{buildroot}%{_datadir}/mime/packages/%{name}.xml


%files
%license mime/copyright
%{_bindir}/planmaker
%{_bindir}/presentations
%{_bindir}/textmaker
%{_libdir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/mime/packages/*.xml

%changelog
* Thu Mar 20 2025 - 1:2024.1224-2
- 2024.1224

* Thu Aug 08 2024 - 1:2024.1214-1
- 2024.1214

* Thu Mar 28 2024 - 1:2024.1210-1
- 2024.1204

* Mon Oct 02 2023 - 1:2024.1204-1
- 2024-1204

* Tue Jul 18 2023 - 1:2024-1.1200
- 2024-1200

* Mon Jan 23 2023 - 1:2021-1.1060
- 2021-1060

* Fri Dec 02 2022 - 1:2021-1.1058
- 2021-1058

* Mon Jan 10 2022 - 1:2021-1.1042
- 2021-1042

* Mon Nov 15 2021 - 1:2021-1.1038
- Initial spec
