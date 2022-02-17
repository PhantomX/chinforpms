%global commit d85332f1f674b6ede81658c3f4e911b9b7b978c3
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220212
%global with_snapshot 1

%global commit1 814a5941ed1e2568b54a07597451ef8b4dc91f98
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 EELEditor

%global commit2 1c72377957c19f21faeccfef57dd5c46a31be7d9
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 GraphicEQWidget

%global commit3 b8218ee319c767c5e9bbcd508d0f621d3f05a218
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 FlatTabWidget

%global commit4 a5d7872d54b6d1d8f82d52aea6bd72eec86eb51d
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 LiquidEqualizerWidget

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/ThePBone

%global pkgname JDSP4Linux

Name:           jamesdsp
Version:        2.3
Release:        2%{?gver}%{?dist}
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
Source11:       %{vc_url}/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source12:       %{vc_url}/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source13:       %{vc_url}/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source14:       %{vc_url}/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz

Patch0:         0001-use-shared-libraries.patch


BuildRequires:  desktop-file-utils
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  qcodeeditor-devel
BuildRequires:  cmake(qtadvanceddocking)
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
Provides:       bundle(asyncplusplus)
Provides:       bundle(http-flaviotordini)
Provides:       bundle(qtpromise)
Provides:       bundle(qcustomplot)
Provides:       bundle(qtcsv)
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
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{version}} -p1

tar -xf %{S:11} -C src/subprojects/%{srcname1} --strip-components 1
tar -xf %{S:12} -C src/subprojects/%{srcname2} --strip-components 1
tar -xf %{S:13} -C src/subprojects/%{srcname3} --strip-components 1
tar -xf %{S:14} -C src/subprojects/%{srcname4} --strip-components 1

for dir in asyncplusplus http qtcsv qtpromise ;do
  cp -p 3rdparty/${dir}/LICENSE LICENSE.${dir}
done
cp -p 3rdparty/qcustomplot/GPL.txt LICENSE.qcustomplot

rm -rf src/subprojects/EELEditor/{3rdparty,QCodeEditor}

sed \
  -e '/QCodeEditor.pri/d' \
  -e '/docking-system/d' \
  -i src/subprojects/EELEditor/src/EELEditor.pri

cat >> src/subprojects/EELEditor/src/EELEditor.pri <<EOF

LIBS += -lqtadvanceddocking -lQCodeEditor
INCLUDEPATH += %{_includedir}/qtadvanceddocking %{_includedir}/QCodeEditor
EOF

sed \
  -e '/TARGET =/s|lib%{name}|%{name}|g' \
  -e '/staticlib/s|^|#|g' \
  -e 's| -O2||g' \
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
%qmake_qt5 lib%{name}.pro PREFIX=%{_prefix} LIBDIR=%{_libdir}
%make_build
popd

mkdir buildpw
pushd buildpw
%qmake_qt5 ../src/src.pro PREFIX=%{_prefix}
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
* Wed Feb 16 2022 Phantom X <megaphantomx at hotmail dot com> - 2.3-2.20220212gitd85332f
- Bump

* Thu Jan 06 2022 Phantom X <megaphantomx at hotmail dot com> - 2.3-1.20220105git66b7cb5
- 2.3
- Bundle new libraries and liveprogide (EELEditor)

* Mon Dec 13 2021 Phantom X <megaphantomx at hotmail dot com> - 2.2-1.20211212git885a8c9
- Initial spec
