%undefine _cmake_shared_libs

%bcond clang 1
%if %{with clang}
%global toolchain clang
%endif

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%bcond cereal 0
%bcond fmt 1
%if 0%{?fedora} > 43
%bcond rtmidi 1
%endif

%global commit 190b8e7c600d06bafd2303c1620067df12dced39
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250714
%bcond snapshot 0

%global commit10 a56bad8bbb770ee266e930c95d37fff2a5be7fea
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 cereal

%global commit11 c68072129c8a5b4025122ca5a0c82ab14b30cb03
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 concurrentqueue

%global commit12 5e6d1e29f7546d9d94fe3d193b788b280bf1f37d
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 cxxopts

%global commit13 353bd895a2bf9d0b1bc5977dc002fb6e0cdb0960
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 fmt

%global commit14 44aa9a4b3a6f27d09a4eb5770d095cbd376dfc4b
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global srcname14 imgui

%global commit15 c9dbe3a6f74b2c2c4a6c9621005c3df213a33eaa
%global shortcommit15 %(c=%{commit15}; echo ${c:0:7})
%global srcname15 mio

%global commit16 f58f558c120e9b32c217290b80bad1a0729fbb2c
%global shortcommit16 %(c=%{commit16}; echo ${c:0:7})
%global srcname16 stb

%global commit17 bf869b0e075c65aa0f81d148b42a90dcce2f95c5
%global shortcommit17 %(c=%{commit17}; echo ${c:0:7})
%global srcname17 tomlplusplus

%global commit18 ab1aca5153379e52e97b85b998b66b61619b7958
%global shortcommit18 %(c=%{commit18}; echo ${c:0:7})
%global srcname18 rtmidi

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global fmt_ver 11.1.0
%global rtmidi_ver 6.0.0

%global appname io.github.strikerx3.%{name}
%global pkgname Ymir

Name:           ymir
Version:        0.1.6
Release:        1%{?dist}
Summary:        A Sega Saturn emulator

License:        GPL-3.0-or-later AND BSD-2-Clause AND MIT AND OFL-1.1%{!?with_cereal: AND BSD-3-Clause}
URL:            https://github.com/StrikerX3/%{pkgname}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif
%if %{without cereal}
Source10:       https://github.com/USCiLab/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
%endif
Source11:       https://github.com/cameron314/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
Source12:       https://github.com/jarro2783/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz
%if %{without fmt}
Source13:       https://github.com/fmtlib/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
%endif
Source14:       https://github.com/ocornut/%{srcname14}/archive/%{commit14}/%{srcname14}-%{shortcommit14}.tar.gz
Source15:       https://github.com/StrikerX3/%{srcname15}/archive/%{commit15}/%{srcname15}-%{shortcommit15}.tar.gz
Source16:       https://github.com/nothings/%{srcname16}/archive/%{commit16}/%{srcname16}-%{shortcommit16}.tar.gz
Source17:       https://github.com/marzer/%{srcname17}/archive/%{commit17}/%{srcname17}-%{shortcommit17}.tar.gz
%if %{without rtmidi}
Source18:       https://github.com/thestk/%{srcname18}/archive/%{commit18}/%{srcname18}-%{shortcommit18}.tar.gz
%endif

Patch0:         0001-Use-system-libraries.patch
Patch1:         0001-Set-SDL-application-name.patch

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
%if %{with cereal}
BuildRequires:  cmake(cereal)
%else
Provides:       bundled(cereal) = 0~git%{shortcommit10}
%endif
%if %{with fmt}
BuildRequires:  cmake(fmt) >= %{fmt_ver}
%else
Provides:       bundled(fmt) = %{fmt_ver}~git%{shortcommit13}
%endif
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libxxhash)
%if %{with rtmidi}
BuildRequires:  pkgconfig(rtmidi) >= %{rtmidi_ver}
%else
BuildRequires:  pkgconfig(alsa)
Provides:       bundled(rtmidi) = %{rtmidi_ver}~git%{shortcommit18}
%endif
BuildRequires:  cmake(SDL3)

Requires:       hicolor-icon-theme

Provides:       bundled(concurrentqueue) = 0~git%{shortcommit11}
Provides:       bundled(cxxopts) = 0~git%{shortcommit12}
Provides:       bundled(imgui) = 0~git%{shortcommit14}
Provides:       bundled(mio) = 0~git%{shortcommit15}
Provides:       bundled(stb) = 0~git%{shortcommit16}
Provides:       bundled(tomlplusplus) = 0~git%{shortcommit17}


%description
%{pkgname} is a Sega Saturn emulator.


%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

pushd vendor
%if %{without cereal}
tar -xf %{S:10} -C cereal/ --strip-components 1
sed -e '/find_package/s|cereal|\0_DISABLED|g' -i CMakeLists.txt
cp -p cereal/LICENSE LICENSE.cereal
%endif
tar -xf %{S:11} -C concurrentqueue/ --strip-components 1
tar -xf %{S:12} -C cxxopts/ --strip-components 1
%if %{without fmt}
tar -xf %{S:13} -C fmt/ --strip-components 1
sed -e '/find_package/s|fmt|\0_DISABLED|g' -i CMakeLists.txt
cp -p fmt/LICENSE LICENSE.fmt
%endif
tar -xf %{S:14} -C imgui/imgui --strip-components 1
tar -xf %{S:15} -C mio/ --strip-components 1
tar -xf %{S:16} -C stb/stb --strip-components 1
tar -xf %{S:17} -C tomlplusplus/ --strip-components 1
%if %{without rtmidi}
tar -xf %{S:18} -C rtmidi/ --strip-components 1
sed -e 's|rtmidi_FOUND|rtmidi_DISABLED|g' -i CMakeLists.txt
cp -p rtmidi/LICENSE LICENSE.rtmidi
%else
rm -rf 3rdparty/rtmidi
%endif

cp -p concurrentqueue/LICENSE.md LICENSE.concurrentqueue.md
cp -p cxxopts/LICENSE LICENSE.cxxopts
cp -p imgui/imgui/LICENSE.txt LICENSE.imgui
cp -p mio/LICENSE LICENSE.mio
cp -p stb/stb/LICENSE LICENSE.stb
cp -p tomlplusplus/LICENSE LICENSE.tomlplusplus
popd

cp -p apps/ymir-sdl3/res/licenses/Spline_Sans/OFL.txt LICENSE.fonts

cat >> %{name}.wrapper <<'EOF'
#!/usr/bin/bash
set -e

XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-${HOME}/.config}"
YMIR_DIR="${XDG_CONFIG_HOME}/%{name}"

mkdir -p "${YMIR_DIR}"
cd "${YMIR_DIR}"
exec %{_libexecdir}/%{name} "$@"
EOF

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
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.wrapper %{buildroot}%{_bindir}/%{name}
install -pm0755 %{_vpath_builddir}/apps/ymdasm/ymdasm %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_libexecdir}
install -pm0755 %{_vpath_builddir}/apps/%{name}-sdl3/%{name}-sdl3 \
  %{buildroot}%{_libexecdir}/%{name}

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
%{_libexecdir}/%{name}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Mon Jul 21 2025 Phantom X <megaphantomx at hotmail dot com> - 0.1.6-1
- 0.1.6

* Mon Jun 30 2025 Phantom X <megaphantomx at hotmail dot com> - 0.1.6-0.1.20250630gitc9879e4
- 0.1.6 snapshot

* Sun May 25 2025 Phantom X <megaphantomx at hotmail dot com> - 0.1.4-0.1.20250524gitafb7a0e
- Initial spec
