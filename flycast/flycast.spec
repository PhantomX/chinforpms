%global commit 18790901b1241c1fab9e69aaa180fcc27c4bc866
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200606
%global with_snapshot 1

%undefine _hardened_build

%bcond_with     native

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           flycast
Version:        7
Release:        12%{?gver}%{?dist}
Summary:        Sega Dreamcast emulator

License:        GPLv2 and BSD
URL:            https://github.com/flyinghead/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/r%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{name}.appdata.xml

Patch0:         0001-Build-fixes.patch
Patch1:         0001-Use-system-libs.patch
Patch2:         0001-Change-configdir-name.patch
Patch3:         0001-Save-logfile-to-writable_data_path.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python3-devel
BuildRequires:  xxhash-devel
Requires:       hicolor-icon-theme
Requires:       vulkan-loader%{?_isa}


%description
%{name} is a multi-platform Sega Dreamcast emulator.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup %{name}-r%{version} -p1
%endif

rm -rf core/deps/{flac,libzip,SDL2-*,xxHash,zlib}

find . -type f \( -name "*.cpp" -o -name "*.h" \) -exec chmod -x {} ';'

pushd shell/linux

rename reicast %{name} * man/* tools/*

# Rebranding
sed -e 's|reicast|%{name}|g' \
  -i Makefile *.desktop man/*.1 tools/*.py

sed -e 's|REICAST|FLYCAST|g' -i man/*.1
sed -e 's|Reicast|Flycast|g' -i *.desktop tools/*.py

%if ! %{with native}
sed -e 's|grep flags /proc/cpuinfo|/bin/true|g' -i Makefile
%endif

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" tools/%{name}-joyconfig.py

popd

sed \
  -e 's|@GIT_VERSION@|%{version}-%{release}|g' \
  -i core/version.h*

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
* Sun Jun 07 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-12.20200606git1879090
- New snapshot

* Sat May 30 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-11.20200530git002a05f
- Bump

* Sun May 17 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-10.20200515gitdf97c42
- New snapshot

* Wed Apr 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-9.20200421git8b7fcc4
- Bump

* Wed Apr 08 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-8.20200408git786c8e7
- New snapshot
- Remove libpng BR

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-7.20200320git0c2e951
- Bump

* Sun Mar 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 7-6.20200314git1abfdaf
- New snapshot

* Mon Nov 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 7-5.20191110git8f86be3
- New snapshot

* Sun Nov 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 7-4.20191027gitb9970fc
- New snapshot

* Sat Sep 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 7-3.20190919gitb693d1c
- New snapshot

* Sun Sep 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 7-2.20190915git732e685
- New snapshot
- Enable pulseaudio support

* Thu Aug 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 7-1.20190815gitb2475c4
- Initial spec
