# Disable LTO. Crash.
%global _lto_cflags %{nil}
%undefine _cmake_shared_libs
%undefine _hardened_build

%bcond_with clang
%if %{with clang}
%global toolchain clang
%endif

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit 2a2ee8bc968232058fe77a06e95d4f3fa1b851e7
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230411
%bcond_without snapshot

# Enable system boost
%bcond_without boost
# Enable system dynarmic
%bcond_without dynarmic
# Enable ffmpeg support
%bcond_without ffmpeg
# Enable system fmt
%bcond_without fmt
# Disable Qt build
%bcond_without qt
# Build tests
%bcond_with tests

%global commit2 511806c0eba8ba5b5cedd4b4a814e96df92864a6
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 cryptopp

%global commit3 b3a92ab54dadd26a0c2a87d2677b80249d2e1a5a
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 dynarmic

%global commit4 a33701196adfad74917046096bf5a2aa0ab0bb50
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 fmt

%global commit5 15798ac9c2611d5c7f9ba832e2c9159bdd8945f2
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 cryptopp-cmake

%global commit6 fd69de1a1b960ec296cc67d32257b0f9e2d89ac6
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 nihstro

%global commit7 060181eaf273180d3a7e87349895bd0cb6ccbf4a
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 ext-soundtouch

%global commit8 01db7cdd00aabcce559a8dddce8798dabb71949b
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 teakra

%global commit10 18964554bc769255401942e0e6dfd09f2fab2093
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 lodepng

%global commit11 66937ea62d126a92b5057e3fd9ceac7c44daf4f5
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 ext-boost

%global commit12 e12ef06218596b52d9b5d6e1639484866a8e7067
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 cpp-jwt

%global cpphttplibver b251668

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url  https://github.com/citra-emu

Name:           citra
Version:        0
Release:        41%{?dist}
Summary:        A Nintendo 3DS Emulator

License:        GPL-2.0-only AND MIT%{!?with_dynarmic: AND ( 0BSD AND MIT )}%{!?with_boost: AND BSL-1.0}
URL:            https://citra-emu.org

%if %{with snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source2:        https://github.com/weidai11/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
%if %{without dynarmic}
Source3:        https://github.com/MerryMage/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
%endif
%if %{without fmt}
Source4:        https://github.com/fmtlib/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
%endif
Source5:        https://github.com/abdes/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        https://github.com/neobrain/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        %{vc_url}/%{srcname7}/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
Source8:        https://github.com/wwylele/%{srcname8}/archive/%{commit8}/%{srcname8}-%{shortcommit8}.tar.gz
Source10:       https://github.com/lvandeve/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
%if %{without boost}
Source11:       %{vc_url}/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
%endif
Source12:       https://github.com/arun11299/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz

Source20:       https://api.citra-emu.org/gamedb#/compatibility_list.json

Patch2:         %{vc_url}/%{name}/pull/6221.patch#/%{name}-gh-pr6221.patch
Patch3:         0001-general-fixes-for-gcc-13.patch

Patch10:        0001-Use-system-libraries.patch
Patch11:        0001-Optional-tests.patch
Patch12:        0001-Disable-telemetry-initial-dialog.patch

BuildRequires:  cmake
BuildRequires:  ninja-build
%if %{with clang}
BuildRequires:  compiler-rt
BuildRequires:  clang
BuildRequires:  llvm
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  desktop-file-utils
%if %{with boost}
BuildRequires:  boost-devel >= 1.71.0
%else
Provides:       bundled(boost) = 0~git%{shortcommit11}
%endif
BuildRequires:  cmake(cubeb)
%if %{with dynarmic}
BuildRequires:  cmake(dynarmic) >= 6.4.6
%else
BuildRequires:  cmake(tsl-robin-map)
Provides:       bundled(dynarmic) = 0~git%{?shortcommit3}
%endif
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  ffmpeg-devel
%endif
%if %{with tests}
BuildRequires:  pkgconfig(catch2) >= 3.1.0
%endif
%if %{with fmt}
BuildRequires:  cmake(fmt)
%else
Provides:       bundled(fmt) = 0~git%{shortcommit4}
%endif
BuildRequires:  pkgconfig(INIReader)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(libenet)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(nlohmann_json) >= 3.9.0
BuildRequires:  pkgconfig(sdl2)
%if %{with qt}
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Multimedia)
BuildRequires:  cmake(Qt5Widgets)
%endif
BuildRequires:  cmake(xbyak)

Requires:       hicolor-icon-theme
Requires:       shared-mime-info

Provides:       bundled(cpp-httplib) = 0~git%{?cpphttplibver}
Provides:       bundled(cryptopp) = 0~git%{shortcommit2}
Provides:       bundled(nihstro) = 0~git%{shortcommit6}
Provides:       bundled(soundtouch) = 0~git%{shortcommit7}
Provides:       bundled(teakra) = 0~git%{shortcommit8}
Provides:       bundled(lodepng) = 0~git%{shortcommit10}
Provides:       bundled(cpp-jwt) = 0~git%{shortcommit12}


%description
Citra is an experimental open-source Nintendo 3DS emulator/debugger
written in C++.


%package qt
Summary:        A Nintendo 3DS Emulator (Qt frontend)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme

%description qt
Citra is an experimental open-source Nintendo 3DS emulator/debugger
written in C++.

This is the Qt frontend.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

mkdir -p externals/cryptopp
tar -xf %{S:2} -C externals/cryptopp --strip-components 1
tar -xf %{S:5} -C externals/cryptopp-cmake --strip-components 1
%if %{without dynarmic}
tar -xf %{S:3} -C externals/dynarmic --strip-components 1
rm -rf externals/dynarmic/externals/{catch,fmt,robin-map,xbyak}
sed -e '/find_package/s|dynarmic|\0_DISABLED|g' -i externals/CMakeLists.txt
%endif
%if %{without fmt}
tar -xf %{S:4} -C externals/fmt --strip-components 1
%endif
tar -xf %{S:6} -C externals/nihstro --strip-components 1
tar -xf %{S:7} -C externals/soundtouch --strip-components 1
tar -xf %{S:8} -C externals/teakra --strip-components 1
tar -xf %{S:10} -C externals/lodepng/lodepng --strip-components 1
%if %{without boost}
tar -xf %{S:11} -C externals/boost --strip-components 1
%endif
tar -xf %{S:12} -C externals/cpp-jwt --strip-components 1

find . -type f \( -name '*.c*' -o -name '*.h*' \) -exec chmod -x {} ';'

pushd externals
%if %{without boost}
cp -p boost/LICENSE_1_0.txt LICENSE.boost
%endif
cp -p cpp-jwt/LICENSE LICENSE.cpp-jwt
%dnl cp -p cryptopp/cryptopp/License.txt LICENSE.cpp-jwt
%if %{without dynarmic}
cp -p dynarmic/LICENSE.txt LICENSE.dynarmic
%endif
%if %{without fmt}
cp -p fmt/LICENSE.rst LICENSE.fmt.rst
%endif
cp -p lodepng/lodepng/LICENSE LICENSE.lodepng
cp -p nihstro/license.txt LICENSE.nihstro
cp -p soundtouch/COPYING.txt COPYING.soundtouch
cp -p teakra/LICENSE LICENSE.teakra
sed -e 's/\r//' -i LICENSE.cpp-jwt
popd


rm -f externals/json/json.hpp
ln -sf %{_includedir}/nlohmann/json.hpp \
  externals/json/json.hpp

rm -rf externals/teakra/externals/catch/

%if %{without fmt}
sed -e 's|-pedantic-errors||g' -i externals/fmt/CMakeLists.txt
%endif

sed \
  -e 's/-Wfatal-errors\b//g' \
  -e '/-pedantic-errors/d' \
%if %{without dynarmic}
  -i externals/dynarmic/CMakeLists.txt \
%endif
  -i externals/teakra/CMakeLists.txt

sed -e '/^#include <exception>/a#include <system_error>' \
  -i externals/teakra/src/interpreter.h

sed -e '/find_package/s|Git|\0_DISABLED|g' -i CMakeModules/GenerateSCMRev.cmake

%if %{with snapshot}
  sed \
    -e 's|@GIT_REV@|%{commit}|g' \
    -e 's|@GIT_BRANCH@|HEAD|g' \
    -e 's|@GIT_DESC@|%{shortcommit}|g' \
    -e 's|@BUILD_FULLNAME@|chinforpms %{version}-%{release}|g' \
    -e 's|@BUILD_DATE@|%(date +%F)|g' \
    -i src/common/scm_rev.cpp.in
%endif

cp -f %{S:20} .


%build
%if %{with snapshot}
export CI=true
export GITHUB_ACTIONS=true
export GITHUB_REF_NAME=%{name}/%{name}-nightly
export GITHUB_REPOSITORY="%{vc_url}/%{citra}"
%endif

%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
%if %{with qt}
  -DENABLE_QT_TRANSLATION:BOOL=ON \
%else
  -DENABLE_QT:BOOL=OFF \
%endif
  -DUSE_SYSTEM_SDL2:BOOL=ON \
%if %{with boost}
  -DUSE_SYSTEM_BOOST:BOOL=ON \
%endif
%if %{with ffmpeg}
  -DENABLE_FFMPEG:BOOL=ON \
  -DENABLE_FFMPEG_AUDIO_DECODER:BOOL=ON \
  -DENABLE_FFMPEG_VIDEO_DUMPER:BOOL=ON \
%endif
  -DCRYPTOPP_SOURCES:PATH=$(pwd)/externals/cryptopp \
  -DENABLE_WEB_SERVICE:BOOL=ON \
  %{!?with_tests:-DCITRA_TESTS:BOOL=OFF} \
  -DENABLE_COMPATIBILITY_LIST_DOWNLOAD:BOOL=OFF \
%if %{without dynarmic}
  -DDYNARMIC_ENABLE_CPU_FEATURE_DETECTION:BOOL=ON \
  -DDYNARMIC_NO_BUNDLED_FMT:BOOL=ON \
  -DDYNARMIC_NO_BUNDLED_ROBIN_MAP:BOOL=ON \
  -DDYNARMIC_WARNINGS_AS_ERRORS:BOOL=OFF \
  -DDYNARMIC_FATAL_ERRORS:BOOL=OFF \
  -DDYNARMIC_TESTS=OFF \
%endif
  -DTEAKRA_BUILD_UNIT_TESTS:BOOL=OFF \
%{nil}

cp -f compatibility_list.json %{__cmake_builddir}/dist/compatibility_list/

%cmake_build


%install
%cmake_install

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}
rm -rf %{buildroot}%{_datadir}/cmake

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license license.txt externals/{COPYING,COPYRIGHT,LICENSE}.*
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-room
%{_mandir}/man6/%{name}.6*


%if %{with qt}
%files qt
%license license.txt
%{_bindir}/%{name}-qt
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/%{name}.xml
%{_mandir}/man6/%{name}-qt.6*
%endif


%changelog
* Fri Mar 17 2023 Phantom X <megaphantomx at hotmail dot com> - 0-38.20230317gita2fd43d
- clang optional support
- R: ninja-build

* Thu Mar 16 2023 Phantom X <megaphantomx at hotmail dot com> - 0-37.20230316git27c2805
- gcc 13 build fix

* Tue Dec 06 2022 Phantom X <megaphantomx at hotmail dot com> - 0-30.20221124gitd117132
- System dynarmic, inih and xbyak

* Sun Nov 13 2022 Phantom X <megaphantomx at hotmail dot com> - 0-28.20221113git94d0399
- Optional tests and control Catch dependency

* Sun Jul 31 2022 Phantom X <megaphantomx at hotmail dot com> - 0-23.20220728git6764264
- Update

* Fri Jun 17 2022 Phantom X <megaphantomx at hotmail dot com> - 0-22.20220611git88a4759
- Bump

* Sun May 22 2022 Phantom X <megaphantomx at hotmail dot com> - 0-21.20220522gita6e7a81
- Update

* Tue Apr 26 2022 Phantom X <megaphantomx at hotmail dot com> - 0-20.20220423git1382035
- Bump
- Build with ffmpeg by default

* Mon Mar 07 2022 Phantom X <megaphantomx at hotmail dot com> - 0-19.20220305gitac98458
- Bump to fix upstream issues
- Enable web service

* Sat Feb 26 2022 Phantom X <megaphantomx at hotmail dot com> - 0-18.20220224git25ad002
- Bump
- Reenable system boost

* Wed May 12 2021 Phantom X <megaphantomx at hotmail dot com> - 0-17.20210511gita2f34ea
- Update
- BR: libusb-1.0

* Wed Apr 21 2021 Phantom X <megaphantomx at hotmail dot com> - 0-16.20210403gitb3cab3c
- Bump

* Wed Mar 17 2021 Phantom X <megaphantomx at hotmail dot com> - 0-15.20210306git8e3c767
- Last snapshot

* Fri Feb 12 2021 Phantom X <megaphantomx at hotmail dot com> - 0-14.20210212gite6c479f
- Update

* Sun Jan 17 2021 Phantom X <megaphantomx at hotmail dot com> - 0-13.20210109git7c6d790
- Update

* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 0-12.20201001gitaced133
- Bump

* Sun Sep 06 2020 Phantom X <megaphantomx at hotmail dot com> - 0-11.20200905git316a649
- New snapshot

* Sun Jul 19 2020 Phantom X <megaphantomx at hotmail dot com> - 0-10.20200714gitd88d220
- Bump

* Sun Jun 21 2020 Phantom X <megaphantomx at hotmail dot com> - 0-9.20200620git372c653
- New snapshot

* Sun May 10 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-8.20200509git8d27b07
- Bump
- ext-boost

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-7.20200321git8722b97
- New snapshot

* Sun Mar 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-6.20200312gitad3c464
- Bump

* Thu Feb 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-5.20200204git821a35b
- New snapshot
- libzstd

* Sun Jan 05 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-4.20200101git01686f7
- New snapshot
- lodepng

* Sat Sep 21 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-3.20190921git223bfc9
- New snapshot

* Wed Apr 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-2.20190423gitb9e51f0
- Disable telemetry initial dialog
- Update version strings

* Tue Apr 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 0-1.20190423gitb9e51f0
- Initial spec
