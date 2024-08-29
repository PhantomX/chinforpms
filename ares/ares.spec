# Disable this. Local lto flags in use.
%global _lto_cflags %{nil}

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}

%global commit 432c4e3b2a9f233cd742d1de764cced7ff337e48
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20231221
%bcond_with snapshot

%bcond_with native
%bcond_with libao
%bcond_with openal

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global rashader_ver 0.2.7
%global vc_url  https://github.com/ares-emulator/%{name}

Name:           ares
Version:        140
Release:        1%{?dist}
Summary:        Multi-system emulator

License:        ISC AND GPL-3.0-only AND BSD-2-Clause AND BSD-3-Clause AND MIT

URL:            https://ares-emu.net/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch11:        0001-Use-system-libraries.patch
Patch500:       0001-CHD-fix-for-patched-libchdr.patch

BuildRequires:  desktop-file-utils
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(alsa)
%if %{with libao}
BuildRequires:  pkgconfig(ao)
%endif
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(librashader) >= %{rashader_ver}
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
Requires:       librashader%{?_isa} >= %{rashader_ver}
Requires:       vulkan-loader%{?_isa}


%description
ares is a multi-system emulator with an uncompromising focus on
accuracy and code readability.

It requires a CPU with SSE4.2 instructions.


%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -N -p1
%autopatch -M 499 -p1

rm -rf thirdparty/{libchdr,librashader,MoltenVK}

find . -type f \( -name "*.cpp" -o -name "*.h" -o -name "*.hpp" \) -exec chmod -x {} ';'

find -name '.gitignore' -delete

cp -a nall/file.hpp nall/file-chd.hpp
cp -a nall/file-buffer.hpp nall/file-buffer-chd.hpp
%patch -P 500 -p1

sed -i -e 's|-L/usr/local/lib ||g' -i hiro/GNUmakefile

sed -e "/handle/s|/usr/local/lib|%{_libdir}|g" -i nall/dl.hpp

sed -e 's|-flto=auto |-flto=%{_smp_build_ncpus} |' -i nall/GNUmakefile

%if %{without libao}
  sed -e "/ruby +=/s|audio.ao\b||" -i ruby/GNUmakefile
%endif
%if %{without openal}
  sed -e "/ruby +=/s|audio.openal\b||" -i ruby/GNUmakefile
%endif


%build
export flags="$CXXFLAGS $(pkg-config --cflags libchdr)"
export options="$LDFLAGS $(pkg-config --libs libchdr)"

for build in desktop-ui ; do
%make_build -C $build verbose compiler=g++ \
  build=optimized system_chdr=true system_rashader=true hiro=gtk3 \
%if %{without native}
  local=false \
%endif
  lto=true \
%{nil}
done


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 desktop-ui/out/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}/Shaders/
cp -rp thirdparty/slang-shaders/* %{buildroot}%{_datadir}/%{name}/Shaders/
mkdir -p %{buildroot}%{_datadir}/%{name}/Database/
cp -rp mia/Database/* %{buildroot}%{_datadir}/%{name}/Database/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  desktop-ui/resource/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{256x256,scalable}/apps
install -pm0644 desktop-ui/resource/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/

for res in 16 22 24 32 36 48 64 72 96 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  for icon in %{name} ;do
    convert %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/${icon}.png \
      -filter Lanczos -resize ${res}x${res} ${dir}/${icon}.png
  done
done


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/Database/
%{_datadir}/%{name}/Shaders/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.*


%changelog
* Tue Aug 27 2024 Phantom X <megaphantomx at hotmail dot com> - 140-1
- 140

* Thu Jun 20 2024 Phantom X <megaphantomx at hotmail dot com> - 139-1
- 139

* Wed May 15 2024 Phantom X <megaphantomx at hotmail dot com> - 138-1
- 138

* Tue Apr 02 2024 Phantom X <megaphantomx at hotmail dot com> - 137-1
- 137
- BR: librashader

* Thu Mar 28 2024 Phantom X <megaphantomx at hotmail dot com> - 136-1
- 136

* Tue Jan 23 2024 Phantom X <megaphantomx at hotmail dot com> - 135-1
- 135

* Wed Nov 22 2023 Phantom X <megaphantomx at hotmail dot com> - 134-1
- 134

* Sat Jul 22 2023 Phantom X <megaphantomx at hotmail dot com> - 133-1
- 133

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 132-2.20230316gitbe869f9
- gcc 13 build fix

* Wed Mar 08 2023 Phantom X <megaphantomx at hotmail dot com> - 132-1
- 132

* Thu Dec 29 2022 Phantom X <megaphantomx at hotmail dot com> - 131-1.20221227git92bf0c6
- 131

* Sun Nov 13 2022 Phantom X <megaphantomx at hotmail dot com> - 130.1-1.20221111git1622ac0
- Initial spec
