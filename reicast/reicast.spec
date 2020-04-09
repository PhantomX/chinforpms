%global commit 3bccd0bc77fba1cf0e2c11f2604d59ae102ef313
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200408
%global with_snapshot 1

%undefine _hardened_build

%bcond_with     native

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           reicast
Version:        20.02
Release:        3%{?gver}%{?dist}
Summary:        Sega Dreamcast emulator

License:        GPLv2 and BSD
URL:            http://reicast.com/

%global vc_url  https://github.com/%{name}/%{name}-emulator
%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/r%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{name}.appdata.xml

Patch0:         0001-Build-fixes.patch
Patch1:         0001-Use-system-libs.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python3-devel
BuildRequires:  xxhash-devel
BuildRequires:  /usr/bin/pathfix.py
Requires:       hicolor-icon-theme
Requires:       python3-evdev


%description
%{name} is a multi-platform Sega Dreamcast emulator.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-emulator-%{commit} -p1
%else
%autosetup -n %{name}-emulator-r%{version} -p1
%endif

rm -rf %{name}/linux-deps/*

rm -rf libswirl/deps/{flac,libpng,libzip,lua,xxhash,zlib}

%if ! %{with native}
sed -e 's|grep flags /proc/cpuinfo|/bin/true|g' -i %{name}/linux/detect-platform.make
%endif

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{name}/linux/tools/%{name}-joyconfig.py

sed \
  -e 's|`git describe --tags --always`|%{version}-%{release}|g' \
  -i libswirl/core.mk

%if 0%{?with_snapshot}
  sed \
    -e 's|`git rev-parse --short HEAD`|%{shortcommit}|g' \
    -i libswirl/core.mk
%endif


%build
export PREFIX=%{_prefix}
%set_build_flags
export CXXFLAGS="$CXXFLAGS -DGLES"
export LDFLAGS="$LDFLAGS -Wl,--as-needed"

%make_build -C %{name}/linux SUPPORT_EGL=1


%install
export PREFIX=%{_prefix}
%make_install -C %{name}/linux

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

for res in 16 22 24 32 36 48 64 72 96 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert %{buildroot}%{_datadir}/pixmaps/%{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-joyconfig
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}/
%{_mandir}/man1/%{name}*.1*
%{_metainfodir}/*.xml


%changelog
* Wed Apr 08 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.02-3.20200408git3bccd0b
- New snapshot

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.02-2.20200320git3f07c32
- Bump

* Sun Mar 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 20.02-1.20200312git1e5a875
- New snapshot

* Sun Sep 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.07.4-2.20190830gitd350e68
- New snapshot
- Enable pulseaudio support

* Thu Aug 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.07.4-1.20190815git49f1f58
- 19.07.4
- Enable EGL

* Sat Jul 20 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.07.3-1.20190720git44d5487
- 19.07.3

* Sat Jun 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 8.1-6.20190614git41b7499
- New snapshot
- Python 3

* Sun Jun 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 8.1-5.20190527git605e00e
- New snapshot

* Fri May 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 8.1-4.20190502git3f8328d
- New snapshot

* Tue Apr 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 8.1-3.20190412gitce90d43
- System libs
- Disable broken pulseaudio support

* Tue Apr 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 8.1-2.20190412gitce90d43
- Snapshot
- BR: libudev

* Tue Sep 25 2018 Phantom X <megaphantomx at bol dot com dot br> - 8.1-1
- Initial spec
