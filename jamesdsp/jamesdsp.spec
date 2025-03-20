%if 0%{?fedora} >= 40
%global build_type_safety_c 0
%endif

%global commit 9826536c05207211ac187b7ef391ab8fd24123ca
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250202
%bcond_without snapshot

%global commit1 b2f392480e00ca232c397610f42688b165b87640
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 EELEditor

%global commit2 ba63ad32682b20e2d4fde4c8a4aafe4da3423cc5
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 GraphicEQWidget

%global commit3 06509713d85dc336c4a3b089ef9d265003aaf48e
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 FlatTabWidget

%global commit4 013055c360c66a08325208065211ffba1f5bc192
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 LiquidEqualizerWidget

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url  https://github.com/ThePBone

%global pkgname JDSP4Linux

Name:           jamesdsp
Version:        2.7.0
Release:        2%{?dist}
Summary:        An audio effect processor for PipeWire clients

# asyncplusplus: MIT
# http-flaviotordini: MIT
# qcustomplot: GPLv3
# qtcsv: MIT
# qtpromise: MIT
License:        GPL-3.0-only AND MIT
URL:            https://github.com/Audio4Linux/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source11:       %{vc_url}/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source12:       %{vc_url}/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source13:       %{vc_url}/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source14:       %{vc_url}/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz

Patch0:         0001-use-shared-libraries.patch
Patch1:         0001-pipewire-1.4-build-fix.patch


BuildRequires:  desktop-file-utils
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(glibmm-2.4)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6DBus)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6Network)
BuildRequires:  pkgconfig(Qt6Svg)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  pkgconfig(Qt6Xml)

BuildRequires:  qt6-qtbase-private-devel

Requires:       %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       %{name}-pipewire = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-pipewire%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       bundle(asyncplusplus) = 0~git
Provides:       bundle(http-flaviotordini) = 0~git
Provides:       bundle(libqtadvanceddocking) = 0~git
Provides:       bundle(qtpromise) = 0~git
Provides:       bundle(qcodeeditor) = 0~git
Provides:       bundle(qcustomplot) = 0~git
Provides:       bundle(qtcsv) = 0~git
Provides:       bundle(WAF) = 0~git
Provides:       bundle(%{srcname1}) = 0~git%{shortcommit1}
Provides:       bundle(%{srcname2}) = 0~git%{shortcommit2}
Provides:       bundle(%{srcname3}) = 0~git%{shortcommit3}
Provides:       bundle(%{srcname4}) = 0~git%{shortcommit4}


%description
jamesDSP is an audio effect processor for PipeWire clients.


%package pulse
Summary:        An audio effect processor for Pulseaudio clients
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(libpulse)
Requires:       %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundle(asyncplusplus) = 0~git
Provides:       bundle(http-flaviotordini) = 0~git
Provides:       bundle(libqtadvanceddocking) = 0~git
Provides:       bundle(qtpromise) = 0~git
Provides:       bundle(qcodeeditor) = 0~git
Provides:       bundle(qcustomplot) = 0~git
Provides:       bundle(qtcsv) = 0~git
Provides:       bundle(WAF) = 0~git
Provides:       bundle(%{srcname1}) = 0~git%{shortcommit1}
Provides:       bundle(%{srcname2}) = 0~git%{shortcommit2}
Provides:       bundle(%{srcname3}) = 0~git%{shortcommit3}
Provides:       bundle(%{srcname4}) = 0~git%{shortcommit4}

%description pulse
jamesDSP-pulse is an audio effect processor for Pulseaudio clients.


%package common
Summary:        Common files for %{name}
Requires:       hicolor-icon-theme
BuildArch:      noarch


%package libs
Summary:        Library for jamesDSP

%description libs
Library for jamesDSP.


%description common
Common %{name} files.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

tar -xf %{S:11} -C src/subprojects/%{srcname1} --strip-components 1
tar -xf %{S:12} -C src/subprojects/%{srcname2} --strip-components 1
tar -xf %{S:13} -C src/subprojects/%{srcname3} --strip-components 1
tar -xf %{S:14} -C src/subprojects/%{srcname4} --strip-components 1

for dir in asyncplusplus qtcsv qtpromise WAF ;do
  cp -p 3rdparty/${dir}/LICENSE LICENSE.${dir}
done
cp -p 3rdparty/qcustomplot/GPL.txt LICENSE.qcustomplot

sed \
  -e '/TARGET =/s|lib%{name}|%{name}|g' \
  -e '/staticlib/s|^|#|g' \
  -e 's| -O2||g' \
  -i lib%{name}/lib%{name}.pro

sed \
  -e 's|$$system(git describe --tags --long --always)|%{version}%{?with_snapshot:-g%{shortcommit}}|g' \
  -i src/src.pro

cat > %{name}.desktop <<EOF
[Desktop Entry]
Name=JamesDSP (Pipewire)
GenericName=Audio effect processor
Comment=An audio effect processor for PipeWire clients
Keywords=equalizer;audio;effect
Categories=AudioVideo;Audio;
Exec=%{name}
Icon=%{name}
StartupNotify=false
Terminal=false
Type=Application
EOF

cat > %{name}-pulse.desktop <<EOF
[Desktop Entry]
Name=JamesDSP (Pulseaudio)
GenericName=Audio effect processor
Comment=An audio effect processor for Pulseaudio clients
Keywords=equalizer;audio;effect
Categories=AudioVideo;Audio;
Exec=%{name}-pulse
Icon=%{name}
StartupNotify=false
Terminal=false
Type=Application
EOF


%build
pushd lib%{name}
%qmake_qt6 lib%{name}.pro PREFIX=%{_prefix} LIBDIR=%{_libdir}
%make_build
popd

mkdir buildpw
pushd buildpw
%qmake_qt6 ../src/src.pro PREFIX=%{_prefix}
%make_build
popd

mkdir buildpa
pushd buildpa
%qmake_qt6 ../src/src.pro "CONFIG += USE_PULSEAUDIO"
%make_build
popd


%install
%make_install INSTALL_ROOT=%{buildroot} -C lib%{name}

rm -f %{buildroot}%{_libdir}/*.so

mkdir -p %{buildroot}%{_bindir}
install -pm0755 buildpw/%{name} %{buildroot}%{_bindir}/%{name}

install -pm0755 buildpa/%{name} %{buildroot}%{_bindir}/%{name}-pulse

mkdir -p %{buildroot}%{_datadir}/applications
for desktop in %{name} %{name}-pulse ;do
  desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    ${desktop}.desktop
done

for res in 16 24 32 48 64 96 128 192 256 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick resources/icons/icon.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm644 resources/icons/icon.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-pulse.desktop


%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop


%files pulse
%{_bindir}/%{name}-pulse
%{_datadir}/applications/%{name}-pulse.desktop


%files libs
%{_libdir}/lib%{name}.so.*


%files common
%license LICENSE*
%doc README.md
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/apps/*.svg


%changelog
* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 2.7.0-1.20240325gitdd5ae3c
- 2.7.0
- Qt 6

* Sat Sep 16 2023 Phantom X <megaphantomx at hotmail dot com> - 2.4-3.20220908git49994d2
- Update qt5advanceddocking BR

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 2.4-2.20220908git49994d2
- gcc 13 build fix

* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 2.4-1.20220908git49994d2
- 2.4

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 2.3-3.20220313gita11f428
- Bump

* Wed Feb 16 2022 Phantom X <megaphantomx at hotmail dot com> - 2.3-2.20220212gitd85332f
- Bump

* Thu Jan 06 2022 Phantom X <megaphantomx at hotmail dot com> - 2.3-1.20220105git66b7cb5
- 2.3
- Bundle new libraries and liveprogide (EELEditor)

* Mon Dec 13 2021 Phantom X <megaphantomx at hotmail dot com> - 2.2-1.20211212git885a8c9
- Initial spec
