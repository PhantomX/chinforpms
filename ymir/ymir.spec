%undefine _cmake_shared_libs

%bcond_without clang
%if %{with clang}
%global toolchain clang
%endif

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%bcond_with cereal
%bcond_without fmt

%global commit afb7a0edff05d49888224745a4d43541e675d6ad
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250524
%bcond_without snapshot

%global commit10 a56bad8bbb770ee266e930c95d37fff2a5be7fea
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 cereal

%global commit11 24b78782bd6ca5a5853ef46917708806112dc142
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 concurrentqueue

%global commit12 dbf4c6a66816f6c3872b46cc6af119ad227e04e1
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 cxxopts

%global commit13 b5266fd3b91accec15d56a8f144b31dceed40d31
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 fmt

%global commit14 e33069ce56d07751ca875eb239f41febef0ebcd3
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global srcname14 imgui

%global commit15 c9dbe3a6f74b2c2c4a6c9621005c3df213a33eaa
%global shortcommit15 %(c=%{commit15}; echo ${c:0:7})
%global srcname15 mio

%global commit16 802cd454f25469d3123e678af41364153c132c2a
%global shortcommit16 %(c=%{commit16}; echo ${c:0:7})
%global srcname16 stb

%global commit17 5abab000e33923f6808f068a081418c0bc7274da
%global shortcommit17 %(c=%{commit17}; echo ${c:0:7})
%global srcname17 tomlplusplus

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global fmt_ver 11.1.0

%global pkgname Ymir

Name:           ymir
Version:        0.1.4
Release:        0.1%{?dist}
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

Patch0:         0001-Use-system-libraries.patch

BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  cmake
BuildRequires:  ninja-build
%if %{with clang}
BuildRequires:  compiler-rt
BuildRequires:  clang
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
Provides:       bundled(fmt) = 0~git%{shortcommit13}
%endif
BuildRequires:  pkgconfig(libchdr)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libxxhash)
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

cat >> %{name}.desktop <<'EOF'
[Desktop Entry]
Name=%{pkgname}
Comment=Sega Saturn Emulator
Exec=%{name} %f
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=Game;Emulator;
PrefersNonDefaultGPU=true
EOF

magick apps/%{name}-sdl3/res/%{name}.ico %{name}.png


%build
%cmake \
  -GNinja \
  -DYmir_AVX2:BOOL=OFF \
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
  %{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
install -pm0644 %{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
  
for res in 16 22 24 32 36 48 64 72 96 128 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick %{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{appname}.png
done


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license LICENSE* vendor/LICENSE.*
%doc README.md
%{_bindir}/%{name}
%{_bindir}/ymdasm
%{_libexecdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png


%changelog
* Sun May 25 2025 Phantom X <megaphantomx at hotmail dot com> - 0.1.4-0.1.20250524gitafb7a0e
- Initial spec
