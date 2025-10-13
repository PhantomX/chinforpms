%undefine _cmake_shared_libs

%bcond clang 1
%if %{with clang}
%global toolchain clang
%endif

%global with_extra_flags -O3 -Wp,-U_GLIBCXX_ASSERTIONS
%{?with_extra_flags:%global _pkg_extra_cflags %{?with_extra_flags}}
%{?with_extra_flags:%global _pkg_extra_cxxflags %{?with_extra_flags}}
%{!?_hardened_build:%global _pkg_extra_ldflags -Wl,-z,now}

%if 0%{?fedora} > 43
%bcond rtmidi 1
%endif

%global commit b3ab7f541c057804c9d66532f3ab861b7dd5a2d5
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20251012
%bcond snapshot 1

%global commit10 c68072129c8a5b4025122ca5a0c82ab14b30cb03
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 concurrentqueue

%global commit11 8de97d14d8f43e23d30a06aca15bbf3dad121374
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 imgui

%global commit12 4e4cdc711d73d9dc96c0cb9475e6951f476218e6
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 mio

%global commit13 f58f558c120e9b32c217290b80bad1a0729fbb2c
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 stb

%global commit14 ab1aca5153379e52e97b85b998b66b61619b7958
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global srcname14 rtmidi

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global fmt_ver 11.1.0
%global rtmidi_ver 6.0.0

%global appname io.github.strikerx3.%{name}
%global pkgname Ymir

Name:           ymir
Version:        0.2.1
Release:        0.1%{?dist}
Summary:        A Sega Saturn emulator

License:        GPL-3.0-or-later AND BSD-2-Clause AND BSD-3-Clause AND MIT AND OFL-1.1
URL:            https://github.com/StrikerX3/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
Source10:       https://github.com/cameron314/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
Source11:       https://github.com/ocornut/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
Source12:       https://github.com/StrikerX3/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz
Source13:       https://github.com/nothings/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
%if %{without rtmidi}
Source14:       https://github.com/thestk/%{srcname14}/archive/%{commit14}/%{srcname14}-%{shortcommit14}.tar.gz
%endif

Patch0:         0001-Use-system-libraries.patch
Patch1:         0001-Set-SDL-application-name.patch
Patch3:         0001-Remove-update-checker.patch

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  ImageMagick
BuildRequires:  cmake
BuildRequires:  ninja-build
%if %{with clang}
BuildRequires:  compiler-rt
BuildRequires:  clang
BuildRequires:  llvm
BuildRequires:  lld
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  cmake(cereal)
BuildRequires:  cmake(cxxopts)
BuildRequires:  cmake(date)
BuildRequires:  cmake(fmt) >= %{fmt_ver}
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libxxhash)
%if %{with rtmidi}
BuildRequires:  pkgconfig(rtmidi) >= %{rtmidi_ver}
%else
BuildRequires:  pkgconfig(alsa)
Provides:       bundled(rtmidi) = %{rtmidi_ver}~git%{shortcommit14}
%endif
BuildRequires:  cmake(SDL3)
BuildRequires:  cmake(tomlplusplus)

Requires:       hicolor-icon-theme

Provides:       bundled(concurrentqueue) = 0~git%{shortcommit10}
Provides:       bundled(imgui) = 0~git%{shortcommit11}
Provides:       bundled(mio) = 0~git%{shortcommit12}
Provides:       bundled(stb) = 0~git%{shortcommit13}


%description
%{pkgname} is a Sega Saturn emulator.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

rm -f apps/ymir-sdl3/src/app/update_checker.*

pushd vendor
tar -xf %{S:10} -C concurrentqueue/ --strip-components 1
tar -xf %{S:11} -C imgui/imgui --strip-components 1
tar -xf %{S:12} -C mio/ --strip-components 1

cp -p concurrentqueue/LICENSE.md LICENSE.concurrentqueue.md
cp -p imgui/imgui/LICENSE.txt LICENSE.imgui
cp -p mio/LICENSE LICENSE.mio
popd

pushd apps/ymir-sdl3
mkdir -p stb/stb
tar -xf %{S:13} -C stb/stb --strip-components 1
sed -e '/find_package/s|Stb|Stb_DISABLED|g' -i CMakeLists.txt
cp -p stb/stb/LICENSE ../../vendor/LICENSE.stb
%if %{without rtmidi}
mkdir -p rtmidi
tar -xf %{S:14} -C rtmidi/ --strip-components 1
sed -e '/find_package/s|rtmidi|rtmidi_DISABLED|g' -i CMakeLists.txt
cp -p rtmidi/LICENSE ../../vendor/LICENSE.rtmidi
%endif
popd

cp -p apps/ymir-sdl3/res/licenses/Spline_Sans/OFL.txt LICENSE.fonts

sed -e \
  '1i <?xml version="1.0" encoding="UTF-8"?>' \
  -i apps/%{name}-sdl3/res/%{appname}.xml


%build
%cmake \
  -GNinja \
  -DYmir_AVX2:BOOL=OFF \
%if %{without snapshot}
  -DYmir_DEV_BUILD:BOOL=OFF \
%endif
  -DYmir_ENABLE_DEVLOG:BOOL=OFF \
  -DYmir_ENABLE_IMGUI_DEMO:BOOL=OFF \
  -DYmir_ENABLE_IPO:BOOL=OFF \
  -DYmir_ENABLE_SANDBOX:BOOL=OFF \
  -DYmir_ENABLE_TESTS:BOOL=OFF \
  -DYmir_EXTRA_INLINING:BOOL=ON \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{_vpath_builddir}/apps/%{name}-sdl3/%{name}-sdl3 \
  %{buildroot}%{_bindir}/%{name}
install -pm0755 %{_vpath_builddir}/apps/ymdasm/ymdasm %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key="Exec" \
  --set-value="%{name} %f" \
  --set-icon="%{appname}" \
  apps/%{name}-sdl3/res/%{appname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -pm0644 apps/%{name}-sdl3/res/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{appname}.png
  
for res in 16 22 24 32 36 48 64 72 96 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick apps/%{name}-sdl3/res/%{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{appname}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 apps/%{name}-sdl3/res/%{appname}.xml \
  %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license LICENSE* vendor/LICENSE.*
%doc README.md
%{_bindir}/%{name}
%{_bindir}/ymdasm
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Mon Aug 11 2025 Phantom X <megaphantomx at hotmail dot com> - 0.1.7-1
- 0.1.7

* Mon Jul 21 2025 Phantom X <megaphantomx at hotmail dot com> - 0.1.6-1
- 0.1.6

* Mon Jun 30 2025 Phantom X <megaphantomx at hotmail dot com> - 0.1.6-0.1.20250630gitc9879e4
- 0.1.6 snapshot

* Sun May 25 2025 Phantom X <megaphantomx at hotmail dot com> - 0.1.4-0.1.20250524gitafb7a0e
- Initial spec
