%global commit 3f8328da2524c948d3d2bb7d712a60155c8080f0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190502
%global with_snapshot 1

%undefine _hardened_build

%bcond_with     native

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           reicast
Version:        8.1
Release:        4%{?gver}%{?dist}
Summary:        Sega Dreamcast emulator

License:        GPLv2 and BSD
URL:            http://reicast.com/

%global vc_url  https://github.com/%{name}/%{name}-emulator
%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/r%{version}/%{name}-%{version}.tar.gz
%endif #{?with_snapshot}
Source1:        %{name}.appdata.xml

Patch0:         %{name}-build-fixes.patch
Patch1:         %{name}-use-system-libs.patch
Patch2:         0001-Fix-format-security-error.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libpng)
#BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python2-devel
BuildRequires:  xxhash-devel
Requires:       hicolor-icon-theme
Requires:       python2-evdev


%description
%{name} is a multi-platform Sega Dreamcast emulator.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-emulator-%{commit} -p1
%else
%autosetup -n %{name}-emulator-r%{version} -p1
%endif

rm -f shell/linux/gcwz/enta_viv/*.so
rm -f shell/linux-deps/lib/*.so

rm -rf core/deps/{flac,libpng,libzip,xxhash,zlib}

%if ! %{with native}
sed -e 's|grep flags /proc/cpuinfo|/bin/true|g' -i shell/linux/Makefile
%endif

sed -i '1s|/usr/bin/env python|%{__python2}|' shell/linux/tools/%{name}-joyconfig.py


sed \
  -e 's|`git describe --tags --always`|%{version}-%{release}|g' \
  -i core/core.mk

%if 0%{?with_snapshot}
  sed \
    -e 's|`git rev-parse --short HEAD`|%{shortcommit}|g' \
    -i core/core.mk
%endif


%build
export PREFIX=%{_prefix}
%set_build_flags
export LDFLAGS="$LDFLAGS -Wl,--as-needed"

%make_build -C shell/linux


%install
export PREFIX=%{_prefix}
%make_install -C shell/linux

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
