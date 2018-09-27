%global commit 91ffb109a9e2a1c02e98e6924af69b7e55df6915
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180923
%global with_snapshot 0

%undefine _hardened_build

%bcond_with     native

Name:           reicast
Version:        8.1
Release:        1%{?dist}
Summary:        Sega Dreamcast emulator

License:        GPLv2 and BSD
URL:            http://reicast.com/

%if 0%{?with_snapshot}
Source0:        https://github.com/%{name}/%{name}-emulator/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/%{name}/%{name}-emulator/archive/r%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif #{?with_snapshot}
Source1:        %{name}.appdata.xml

Patch0:         %{name}-build-fixes.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(x11)
BuildRequires:  python2-devel
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

%if ! %{with native}
sed -e 's|grep flags /proc/cpuinfo|/bin/true|g' -i shell/linux/Makefile
%endif

sed -i '1s|/usr/bin/env python|%{__python2}|' shell/linux/tools/%{name}-joyconfig.py

%build
export PREFIX=%{_prefix}
export CFLAGS="%{build_cflags}"
export CXXFLAGS="%{build_cxxflags}"
export LDFLAGS="%{build_ldflags} -Wl,--as-needed"

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
%{_datadir}/%{name}
%{_mandir}/man1/%{name}*.1*
%{_metainfodir}/*.xml


%changelog
* Tue Sep 25 2018 Phantom X <megaphantomx at bol dot com dot br> - 8.1-1
- Initial spec
