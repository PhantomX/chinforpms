# Disable this. Local lto flags in use.
%global _lto_cflags %{nil}

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}

%global commit b7da32113fab30fb6672a475822d5d3a5bf56d76
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230421
%bcond_without snapshot

%bcond_with gtk2
%bcond_with libao
%bcond_with openal

%if %{with gtk2}
%global toolkit gtk2
%else
%global toolkit gtk3
%endif

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url  https://github.com/ares-emulator/%{name}

Name:           ares
Version:        132
Release:        3%{?dist}
Summary:        Multi-system emulator

License:        GPL-3.0-only AND BSD-2-Clause

URL:            https://ares-emu.net/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-gcc-13-build-fix.patch
# https://aur.archlinux.org/cgit/aur.git/tree/ares-paths.patch?h=ares-emu
Patch10:        ares-paths.patch
Patch11:        0001-Use-system-libraries.patch

BuildRequires:  desktop-file-utils
BuildRequires:  make
BuildRequires:  gcc-c++
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
BuildRequires:  pkgconfig(libchdr)
%if %{with openal}
BuildRequires:  pkgconfig(openal)
%endif
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  vulkan-headers
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xv)

Requires:       hicolor-icon-theme
Requires:       vulkan-loader%{?_isa}


%description
ares is a multi-system emulator with an uncompromising focus on
accuracy and code readability.

%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

rm -rf thirdparty/{libchdr,MoltenVK}

find . -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.hpp" \) -exec chmod -x {} ';'

find -name '.gitignore' -delete

sed -i -e 's|-L/usr/local/lib ||g' -i hiro/GNUmakefile

sed -e "/handle/s|/usr/local/lib|%{_libdir}|g" -i nall/dl.hpp

%if %{without libao}
  sed -e "/ruby +=/s|audio.ao\b||" -i ruby/GNUmakefile
%endif
%if %{without openal}
  sed -e "/ruby +=/s|audio.openal\b||" -i ruby/GNUmakefile
%endif

sed -e '/nall\/main.cpp/d' -i nall/main.hpp


%build
%set_build_flags
export flags="$CXXFLAGS $(pkg-config --cflags libchdr)"
export options="$LDFLAGS $(pkg-config --libs libchdr)"

for build in mia desktop-ui tools/genius ; do
%make_build -C $build verbose compiler=g++ \
  build=optimized local=false system_chdr=true hiro=%{toolkit} \
  lto=true \
%{nil}
done


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 desktop-ui/out/%{name} %{buildroot}%{_bindir}/
install -pm0755 tools/genius/out/genius %{buildroot}%{_bindir}/
install -pm0755 mia/out/mia %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}/
cp -rp %{name}/System/* %{buildroot}%{_datadir}/%{name}/


mkdir -p %{buildroot}%{_datadir}/%{name}/Shaders/
mkdir -p %{buildroot}%{_datadir}/mia/{Database,Firmware}/
cp -rp mia/Database/* %{buildroot}%{_datadir}/mia/Database/
cp -rp mia/Firmware/* %{buildroot}%{_datadir}/mia/Firmware/
cp -rp %{name}/Shaders/* %{buildroot}%{_datadir}/%{name}/Shaders/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  desktop-ui/resource/%{name}.desktop

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  tools/genius/data/genius.desktop

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  mia/resource/mia.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{256x256,scalable}/apps
install -pm0644 desktop-ui/resource/%{name}.png \
  tools/genius/data/genius.png \
  mia/resource/mia.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

install -pm0644 \
  tools/genius/data/genius.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/

for res in 16 22 24 32 36 48 64 72 96 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  for icon in %{name} genius mia ;do
    convert %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/${icon}.png \
      -filter Lanczos -resize ${res}x${res} ${dir}/${icon}.png
  done
done


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/genius
%{_bindir}/mia
%{_datadir}/%{name}
%{_datadir}/mia
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.*


%changelog
* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 132-2.20230316gitbe869f9
- gcc 13 build fix

* Wed Mar 08 2023 Phantom X <megaphantomx at hotmail dot com> - 132-1
- 132

* Thu Dec 29 2022 Phantom X <megaphantomx at hotmail dot com> - 131-1.20221227git92bf0c6
- 131

* Sun Nov 13 2022 Phantom X <megaphantomx at hotmail dot com> - 130.1-1.20221111git1622ac0
- Initial spec
