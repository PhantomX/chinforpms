%global commit 885a8c96b6cd033b0a7af53bf185eedf1fe2a86f
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211212
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname JDSP4Linux

Name:           jamesdsp
Version:        2.2
Release:        1%{?gver}%{?dist}
Summary:        An audio effect processor for PipeWire clients

# asyncplusplus: MIT
# http-flaviotordini: MIT
# qcustomplot: GPLv3
# qtcsv: MIT
# qtpromise: MIT
License:        GPLv3 and MIT
URL:            https://github.com/Audio4Linux/%{pkgname}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch0:         0001-use-shared-and-system-libraries.patch


BuildRequires:  desktop-file-utils
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  liveprogide-devel
BuildRequires:  pkgconfig(glibmm-2.4)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Xml)

Requires:       %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       %{name}-pipewire = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-pipewire%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       bundle(asyncplusplus)
Provides:       bundle(http-flaviotordini)
Provides:       bundle(qtpromise)
Provides:       bundle(qcustomplot)
Provides:       bundle(qtcsv)


%description
jamesDSP is an audio effect processor for PipeWire clients.


%package pulse
Summary:        An audio effect processor for Pulseaudio clients
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(libpulse)
Requires:       %{name}-common = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundle(asyncplusplus)
Provides:       bundle(http-flaviotordini)
Provides:       bundle(qtpromise)
Provides:       bundle(qcustomplot)
Provides:       bundle(qtcsv)

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
%autosetup -n %{name}-%{?gver:%{commit}}%{!?gver:%{version}} -p1

for dir in asyncplusplus http qtcsv qtpromise ;do
  cp -p 3rdparty/${dir}/LICENSE LICENSE.${dir}
done
cp -p 3rdparty/qcustomplot/GPL.txt LICENSE.qcustomplot

sed \
  -e '/TARGET =/s|lib%{name}|%{name}|g' \
  -e '/staticlib/s|^|#|g' \
  -e 's| -O2||g' \
  -e 's|/usr/lib\b|%{_libdir}|g' \
  -i lib%{name}/lib%{name}.pro

sed \
  -e 's|$$system(git describe --tags --long --always)|%{version}%{?gver:-g%{shortcommit}}|g' \
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
%qmake_qt5 lib%{name}.pro
%make_build
popd

mkdir buildpw
pushd buildpw
%qmake_qt5 ../src/src.pro
%make_build
popd

mkdir buildpa
pushd buildpa
%qmake_qt5 ../src/src.pro "CONFIG += USE_PULSEAUDIO"
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
  convert resources/icons/icon.png -filter Lanczos -resize ${res}x${res} \
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
* Mon Dec 13 2021 Phantom X <megaphantomx at hotmail dot com> - 2.2-1.20211212git885a8c9
- Initial spec
