%global commit 24ac4f2a2e36bd937971c87dc56c7acf249f0d1e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211214
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname PCSX2_MultiConfigTool
%global ver     %%(echo %{version} | tr '~' '-' | tr '_' '-')

Name:           pcsx2-multiconfigtool
Version:        0.7~beta
Release:        1%{?gver}%{?dist}
Summary:        A Manager for multiple Configs with PCSX2

License:        GPLv3
URL:            https://github.com/XXXBold/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{ver}/%{pkgname}-%{ver}.tar.gz
%endif

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  meson
# for xxd
BuildRequires:  vim-common
BuildRequires:  wxGTK3-devel
Requires:       hicolor-icon-theme
Recommends:     pcsx2


%description
%{pkgname} can be used to manage diffrent configs and create Shortcuts for
direct starting games with PCSX2.


%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{ver}} -p1

sed \
  -e 's|/usr/games/PCSX2-linux.sh|%{_bindir}/pcsx2|g' \
  -i src/pcsx2_multiconfigtool.h src/UI_wx/wxwin_selectpaths.h

sed \
  -e 's|/usr/games|%{_bindir}|g' \
  -i resources/PCSX2Tool.fbp

cat > %{name}.desktop <<'EOF'
[Desktop Entry]
Name=%{pkgname}
Comment=Manager for multiple Configs with PCSX2
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;GTK;
EOF


%build
%meson
%meson_build


%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{_vpath_builddir}/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir  %{buildroot}%{_datadir}/applications \
  %{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -pm0644 resources/pcsx2tool_logo.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png

for res in 16 24 32 48 64 96 128 192 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert resources/pcsx2tool_logo.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license LICENSE
%doc README.md manual.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}.png


%changelog
* Thu Feb 17 2022 Phantom X <megaphantomx at hotmail dot com> - 0.7~beta-1
- Initial spec
