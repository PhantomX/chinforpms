# Disable this. Local lto flags in use.
%global _lto_cflags %{nil}

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}

%global commit 5cefce5c08f74cfc80eee3f82a32d846144e5277
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230308
%global with_snapshot 1

%bcond_with gtk2
%bcond_with libao
%bcond_with openal

%if %{with gtk2}
%global toolkit gtk2
%else
%global toolkit gtk3
%endif

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           bsnes
Version:        115
Release:        8%{?gver}%{?dist}
Summary:        Nintendo SNES emulator

License:        GPLv3 and BSD

URL:            https://github.com/%{name}-emu/%{name}

%if 0%{?with_snapshot}
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
%if %{with gtk2}
BuildRequires:  pkgconfig(gtk+-2.0)
%else
BuildRequires:  pkgconfig(gtk+-3.0)
%endif
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
bsnes is a Super Nintendo / Super Famicom emulator that began development on
October 14th, 2004. It focuses on performance, features, and ease of use.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

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
%set_build_flags
export flags="$CXXFLAGS"
export options="$LDFLAGS"

%make_build -C %{name} target=%{name} verbose \
  build=performance local=false hiro=%{toolkit} \
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
  convert %{name}/target-%{name}/resource/%{name}.png \
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
