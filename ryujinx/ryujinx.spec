%global _build_id_links none
%undefine _debugsource_packages

%global appname Ryujinx
%global vc_id   28ba55598df384c4b1e6892c49e95376d2b582fb
%global vc_url  https://github.com/%{appname}

Name:           ryujinx
Version:        1.1.328
Release:        1%{?dist}
Summary:        Experimental Nintendo Switch Emulator

License:        MIT
URL:            https://ryujinx.org/

Source0:        %{vc_url}/release-channel-master/releases/download/%{version}/%{name}-%{version}-linux_x64.tar.gz
Source1:        %{vc_url}/%{appname}/raw/%{vc_id}/LICENSE.txt
Source2:        %{vc_url}/%{appname}/raw/%{vc_id}/README.md
Source3:        %{vc_url}/%{appname}/raw/%{vc_id}/distribution/linux/%{name}.desktop
Source4:        %{vc_url}/%{appname}/raw/%{vc_id}/distribution/linux/%{name}-logo.svg
Source5:        %{appname}.sh

ExclusiveArch:  x86_64

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  librsvg2-tools
Requires:       SDL2%{?_isa}
Requires:       sdl_gamecontrollerdb
Requires:       hicolor-icon-theme

%global __provides_exclude_from ^%{_libdir}/%{name}/.*.so


%description
Ryujinx is an open-source Nintendo Switch emulator, written in C#. This emulator
aims at providing excellent accuracy and performance, a user-friendly interface
and consistent builds.


%prep
%autosetup -n publish

cp -p %{S:1} %{S:2} %{S:3} %{S:4} .

cat > %{appname}.sh <<'EOF'
#!/usr/bin/bash
exec "%{_libdir}/%{name}/%{appname}" "$@"
EOF

chrpath --delete %{appname}


%build

%install
mkdir -p %{buildroot}%{_libdir}/%{name}
install -pm0755 %{appname} libsoundio.so %{buildroot}%{_libdir}/%{name}/

install -pm0644 Ryujinx.SDL2.Common.dll.config %{buildroot}%{_libdir}/%{name}/

# Ugly hack to use system SDL2
ln -sf ../libSDL2-2.0.so.0 %{buildroot}%{_libdir}/%{name}/libSDL2.so

ln -sf ../../share/SDL_GameControllerDB/gamecontrollerdb.txt \
  %{buildroot}%{_libdir}/%{name}/SDL_GameControllerDB.txt

ln -sf ../../../tmp %{buildroot}%{_libdir}/%{name}/Logs

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{appname}.sh %{buildroot}%{_bindir}/%{appname}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm0644 %{name}-logo.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

for res in 16 22 24 32 36 48 64 72 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert %{name}-logo.svg -h ${res} -w ${res} \
    -o ${dir}/%{name}.png
done


%files
%license LICENSE.txt THIRDPARTY.md
%doc README.md
%{_bindir}/%{appname}
%{_libdir}/%{name}/%{appname}
%{_libdir}/%{name}/*.so
%{_libdir}/%{name}/*.config
%{_libdir}/%{name}/*.txt
%{_libdir}/%{name}/Logs
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*


%changelog
* Thu Oct 27 2022 Phantom X <megaphantomx at hotmail dot com> - 1.1.328-1
- Initial spec

