%global commit 44cbb88d49d5a77f19e353fad4bc7fbab6909ca9
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210323
%global with_snapshot 1

%ifarch x86_64
%global build_with_lto    1
%endif

%global with_gtk2 1
%global with_libao 0
%global with_openal 0

%if 0%{?with_gtk2}
%global toolkit gtk2
%else
%global toolkit gtk3
%endif

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           higan
Version:        110
Release:        3%{?gver}%{?dist}
Summary:        Multi-system emulator

License:        GPLv3 and BSD

URL:            https://github.com/higan-emu/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(alsa)
%if 0%{?with_libao}
BuildRequires:  pkgconfig(ao)
%endif
BuildRequires:  pkgconfig(gl)
%if 0%{?with_gtk2}
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gtksourceview-2.0)
%else
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtksourceview-3.0)
%endif
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-simple)
%if 0%{?with_openal}
BuildRequires:  pkgconfig(openal)
%endif
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xv)
Requires:       hicolor-icon-theme

%description
higan is a multi-system emulator with an uncompromising focus on
accuracy and code readability.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup %{name}-%{version} -p1
%endif

find . -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.hpp" \) -exec chmod -x {} ';'

mv extras/Shaders/LICENSE LICENSE.shader

sed -i -e 's|-L/usr/local/lib ||g' -i hiro/GNUmakefile

sed -e "/handle/s|/usr/local/lib|%{_libdir}|g" -i nall/dl.hpp

%if !0%{?with_ao}
  sed -e "/ruby +=/s|audio.ao\b||" -i ruby/GNUmakefile
%endif
%if !0%{?with_openal}
  sed -e "/ruby +=/s|audio.openal\b||" -i ruby/GNUmakefile
%endif


%build
# Disable this. Local lto flags in use.
%global _lto_cflags %{nil}

export flags="%(echo %{build_cxxflags} | sed -e 's/-O2\b/-O3/')"
export options="%{build_ldflags}"

%make_build -C %{name}-ui target=%{name} verbose \
  build=performance local=false hiro=%{toolkit} \
%if 0%{?build_with_lto}
  lto=true \
%endif
%{nil}

%make_build -C icarus verbose hiro=%{toolkit}


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}-ui/out/%{name} %{buildroot}%{_bindir}/
install -pm0755 icarus/out/icarus %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}/
cp -rp %{name}/System/* %{buildroot}%{_datadir}/%{name}/


mkdir -p %{buildroot}%{_datadir}/icarus/{Database,Firmware,Shaders}/
cp -rp icarus/Database/* %{buildroot}%{_datadir}/icarus/Database/
cp -rp icarus/Firmware/* %{buildroot}%{_datadir}/icarus/Firmware/
cp -rp extras/Shaders/* %{buildroot}%{_datadir}/%{name}/Shaders/

find %{buildroot}%{_datadir} -name '.gitgnore' -delete

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}/target-%{name}/resource/%{name}.desktop

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  icarus/data/icarus.desktop


mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{256x256,scalable}/apps
install -pm0644 %{name}/target-%{name}/resource/%{name}.png \
  icarus/data/icarus.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

install -pm0644 %{name}/target-%{name}/resource/%{name}.svg \
  icarus/data/icarus.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

for res in 16 22 24 32 36 48 64 72 96 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  for icon in %{name} icarus ;do
    convert %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/${icon}.png \
      -filter Lanczos -resize ${res}x${res} ${dir}/${icon}.png
  done
done


%files
%license LICENSE.txt LICENSE.shader
%doc README.md
%{_bindir}/%{name}
%{_bindir}/icarus
%{_datadir}/%{name}
%{_datadir}/icarus
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.*


%changelog
* Tue Mar 23 2021 Phantom X <megaphantomx at hotmail dot com> - 110-3.20210323git44cbb88
- Bump
- Update URL

* Fri Oct  2 2020 Phantom X <megaphantomx at hotmail dot com> - 110-2.20200725git2a110b4
- Snapshot

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 110-1
- 110

* Wed Dec 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 106.233-1.20191209gitd2efef7
- 106.233

* Sat Sep 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 106.215-1.20190916gitf745dcf
- 106.215

* Thu Aug 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 106.193-2.20190807git6d19b54
- Initial spec
