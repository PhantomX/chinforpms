# Disable this. Local lto flags in use.
%global _lto_cflags %{nil}

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}

%global commit 1622ac00a58954f46c583a0b3d5828963339cd00
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20221111
%global with_snapshot 1

%ifarch x86_64
%global build_with_lto    1
%endif

%global with_gtk2 0
%global with_libao 0
%global with_openal 0

%if 0%{?with_gtk2}
%global toolkit gtk2
%else
%global toolkit gtk3
%global build_with_lto    0
%endif

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/ares-emulator/%{name}

Name:           ares
Version:        130.1
Release:        1%{?gver}%{?dist}
Summary:        Multi-system emulator

License:        GPLv3 and BSD

URL:            https://ares-emu.net/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

# https://aur.archlinux.org/cgit/aur.git/tree/ares-paths.patch?h=ares-emu
Patch10:        ares-paths.patch
Patch11:        0001-Use-system-libraries.patch

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
BuildRequires:  pkgconfig(libchdr)
%if 0%{?with_openal}
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
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup %{name}-%{version} -p1
%endif

rm -rf thirdparty/{libchdr,MoltenVK}

find . -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.hpp" \) -exec chmod -x {} ';'

find -name '.gitignore' -delete

sed -i -e 's|-L/usr/local/lib ||g' -i hiro/GNUmakefile

sed -e "/handle/s|/usr/local/lib|%{_libdir}|g" -i nall/dl.hpp

%if !0%{?with_ao}
  sed -e "/ruby +=/s|audio.ao\b||" -i ruby/GNUmakefile
%endif
%if !0%{?with_openal}
  sed -e "/ruby +=/s|audio.openal\b||" -i ruby/GNUmakefile
%endif


%build
%set_build_flags
export flags="$CXXFLAGS $(pkg-config --cflags libchdr)"
export options="$LDFLAGS $(pkg-config --libs libchdr)"

for build in mia desktop-ui genius ; do
%make_build -C $build verbose \
  build=optimized local=false system_chdr=true hiro=%{toolkit} \
%if 0%{?build_with_lto}
  lto=true \
%endif
%{nil}
done


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 desktop-ui/out/%{name} %{buildroot}%{_bindir}/
install -pm0755 genius/out/genius %{buildroot}%{_bindir}/
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
  genius/data/genius.desktop

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  mia/resource/mia.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{256x256,scalable}/apps
install -pm0644 desktop-ui/resource/%{name}.png \
  genius/data/genius.png \
  mia/resource/mia.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

install -pm0644 \
  genius/data/genius.svg \
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
* Sun Nov 13 2022 Phantom X <megaphantomx at hotmail dot com> - 130.1-1.20221111git1622ac0
- Initial spec
