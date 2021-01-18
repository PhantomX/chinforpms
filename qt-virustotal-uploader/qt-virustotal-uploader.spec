%global commit 5ef9e1880c107bbe41b919d26410abc3a8e6ecb9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20160501
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           qt-virustotal-uploader
Version:        1.3
Release:        1%{?gver}%{?dist}
Summary:        VirusTotal uploader

License:        ASL 2.0 
URL:            https://www.virustotal.com/
%if 0%{?with_snapshot}
Source0:        https://github.com/VirusTotal/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/VirusTotal/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  make
BuildRequires:  c-vtapi-devel
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(jansson)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(Qt5) >= 5.3
BuildRequires:  pkgconfig(Qt5Core) >= 5.3
BuildRequires:  pkgconfig(Qt5Gui) >= 5.3
BuildRequires:  pkgconfig(Qt5Network) >= 5.3
BuildRequires:  pkgconfig(zlib)
Requires:       hicolor-icon-theme

%description
%{summary}.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit}
%else
%autosetup -n %{name}-%{version}
%endif

sed \
  -e 's|/usr/local/include/ $$(HOME)/local/include/|%{_includedir}/c-vtapi|g' \
  -e 's|-L/usr/local/lib -L$$(HOME)/local/lib ||g' \
  -i qt-vt-uploader.pro

%build
%qmake_qt5 qt-vt-uploader.pro
%make_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 VirusTotalUploader %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Name=VirusTotal Uploader
Comment=Upload files for VirusTotal analysis
Comment[pt_BR]=Envia arquivos para análise pelo VirusTotal
Exec=VirusTotalUploader
Icon=VirusTotalUploader
Terminal=false
Type=Application
StartupNotify=true
Categories=Qt;Network;
EOF

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -pm0644 vtlogo-sigma.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/VirusTotalUploader.png

for res in 16 22 24 32 36 48 64 72 96 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert vtlogo-sigma.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/VirusTotalUploader.png
done

%files
%license COPYING
%doc AUTHORS ReadMe.md
%{_bindir}/VirusTotalUploader
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Thu Aug 17 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.3-1.20160501git5ef9e18
- Initial spec
