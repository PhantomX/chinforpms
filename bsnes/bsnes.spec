# Disable this. Local lto flags in use.
%global _lto_cflags %{nil}

%global with_extra_flags -O3
%{?with_extra_flags:%global _pkg_extra_cflags %{?with_extra_flags}}
%{?with_extra_flags:%global _pkg_extra_cxxflags %{?with_extra_flags}}

%global commit 385b34933d48eadfcbe7b11efda4b24b439d94a2
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250903
%bcond snapshot 1

%bcond libao 0
%bcond openal 0

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           bsnes
Version:        115
Release:        12%{?dist}
Summary:        SNES emulator

License:        GPL-3.0-only AND BSD-2-Clause

URL:            https://github.com/%{name}-emu/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(alsa)
%if %{with libao}
BuildRequires:  pkgconfig(ao)
%endif
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-simple)
%if %{with openal}
BuildRequires:  pkgconfig(openal)
%endif
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xv)
Requires:       hicolor-icon-theme

%description
bsnes is a SNES / SFC emulator that began development on
October 14th, 2004. It focuses on performance, features, and ease of use.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

find . -type f \( -name '*.c*' -o -name '*.h*' \) -exec chmod -x {} ';'

sed -e 's|-L/usr/local/lib ||g' -i hiro/GNUmakefile

sed -e 's|-O[23] ||g' -i nall/GNUmakefile

sed -e "/handle/s|/usr/local/lib|%{_libdir}|g" -i nall/dl.hpp

%if %{without libao}
  sed -e "/pkg_check/s|audio.ao\b||" -i ruby/GNUmakefile
%endif
%if %{without openal}
  sed -e "/pkg_check/s|audio.openal\b||" -i ruby/GNUmakefile
%endif


%build
export flags="$CXXFLAGS"
export options="$LDFLAGS"

%make_build -C %{name} target=%{name} verbose \
  build=performance local=false hiro=gtk3 \
  lto=true \
%{nil}


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}/out/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}/{Database,Firmware,Locale,Shaders}/
cp -rp %{name}/Database/* %{buildroot}%{_datadir}/%{name}/Database/
cp -rp %{name}/Locale/* %{buildroot}%{_datadir}/%{name}/Locale/
cp -rp shaders/* %{buildroot}%{_datadir}/%{name}/Shaders/
cp -rp extras/*.bml %{buildroot}%{_datadir}/%{name}/

find %{buildroot}%{_datadir} -name '.gitgnore' -delete

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}/target-%{name}/resource/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{256x256,scalable}/apps
install -pm0644 %{name}/target-%{name}/resource/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

install -pm0644 %{name}/target-%{name}/resource/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

for res in 16 22 24 32 36 48 64 72 96 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick %{name}/target-%{name}/resource/%{name}.png \
    -filter Lanczos -resize ${res}x${res} ${dir}/%{name}.png
done


%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.*


%changelog
* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 115-6.20210906gite580974
- Last snapshot

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 115-5.20210414git55e05c8
- Update

* Tue Mar 23 2021 Phantom X <megaphantomx at hotmail dot com> - 115-4.20210312gitf57657f
- Bump
- Update URL
- Remove gtksourceview BR

* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 115-3.20200623git3808e8e
- New snapshot

* Wed Apr 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 115-2
- LTO build

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 115-1
- 115

* Wed Dec 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 113-1
- 113

* Sat Sep 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 109-1
- Initial spec
