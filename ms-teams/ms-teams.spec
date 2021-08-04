# DO NOT DISTRIBUTE PACKAGED RPMS FROM THIS

%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true

%global pkgname teams
%global pkgrel 1

Name:           ms-%{pkgname}
Version:        1.4.00.13653
Release:        1%{?dist}
Summary:        Chat-centered workspace in Office 365

License:        Microsoft End User License Agreement
URL:            https://teams.microsoft.com/

Source0:        https://packages.microsoft.com/yumrepos/%{name}/%{pkgname}-%{version}-%{pkgrel}.x86_64.rpm

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  ImageMagick
BuildRequires:  desktop-file-utils
Requires:       libappindicator-gtk3%{?_isa}
Requires:       libdbusmenu%{?_isa}
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*

%global __requires_exclude ^libffmpeg.so
%global __requires_exclude %__requires_exclude|^libEGL.so
%global __requires_exclude %__requires_exclude|^libGLESv2.so
%global __requires_exclude %__requires_exclude|^libVkICD_mock_icd.so


%description
Microsoft Teams is your hub for teamwork in Office 365. All your team
conversations, files, meetings, and apps live together in a single shared
workspace, and you can take it with you on your favorite mobile device.


%prep
%setup -c -T
rpm2cpio %{SOURCE0} | cpio -imdv --no-absolute-filenames

find usr/share/%{pkgname}/ -name '*.so*' | xargs chmod +x

chrpath --delete usr/share/%{pkgname}/%{pkgname}

sed -e '/^OnlyShowIn=/d' -i usr/share/applications/%{pkgname}.desktop


%build


%install
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{pkgname} <<'EOF'
#!/usr/bin/sh
APP_PATH=%{_libdir}/%{name}
export APP_PATH
LD_LIBRARY_PATH="${APP_PATH}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH
exec ${APP_PATH}/%{pkgname} "$@" --disable-namespace-sandbox --disable-setuid-sandbox
EOF
chmod 0755 %{buildroot}%{_bindir}/%{pkgname}

mkdir -p %{buildroot}%{_libdir}/%{name}
cp -rp usr/share/%{pkgname}/{%{pkgname},locales,resources,*.{bin,dat,pak,so}} \
  %{buildroot}%{_libdir}/%{name}/

chmod 0755 %{buildroot}%{_libdir}/%{name}/%{pkgname}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="%{pkgname} %U" \
  usr/share/applications/%{pkgname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -pm0644 usr/share/pixmaps/%{pkgname}.png \
  %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/

for res in 16 24 32 48 64 72 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert usr/share/pixmaps/%{pkgname}.png -filter Lanczos -resize ${res}x${res}  \
    ${dir}/%{pkgname}.png
done


%files
%license usr/share/%{pkgname}/LICENSE*
%{_bindir}/%{pkgname}
%{_libdir}/%{name}/
%{_datadir}/applications/%{pkgname}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Tue Aug 03 2021 - 1.4.00.13653-1
- 1.4.00.13653

* Fri Apr 16 2021 - 1.4.00.7556-2
- Sync wrapper command line with upstream

* Wed Apr 07 2021 - 1.4.00.7556-1
- 1.4.00.7556

* Wed Dec 02 2020 - 1.3.00.30857-1
- 1.3.00.30857

* Wed Oct 28 2020 - 1.3.00.25560-1
- 1.3.00.25560

* Wed Jun 17 2020 - 1.3.00.5153-1
- Initial spec
