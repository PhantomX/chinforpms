# Selective LTO.
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

%global commit 16980b0ffc5a3e8b8f4a0960488a3f1c9ac736e1
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250507
%bcond_without snapshot

# Enable system boost
%bcond_without boost
# Enable system cryptopp
%bcond_without cryptopp
# Enable system dynarmic
%bcond_without dynarmic
# Enable system fmt
%bcond_without fmt
# Disable Qt build
%bcond_without qt
%bcond_without soundtouch
# Enable webservice
%bcond_without webservice
%bcond_without vma
# Enable system vulkan
%bcond_without vulkan
# Build tests
%bcond_with tests

%global commit2 60f81a77e0c9a0e7ffc1ca1bc438ddfa2e43b78e
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 cryptopp

%global commit3 278405bd71999ed3f3c77c5f78344a06fef798b9
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 dynarmic

%global commit4 123913715afeb8a437e6388b4473fcc4753e1c9a
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 fmt

%global commit5 00a151f8489daaa32434ab1f340e6750793ddf0c
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 cryptopp-cmake

%global commit6 f4d8659decbfe5d234f04134b5002b82dc515a44
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 nihstro

%global commit7 9ef8458d8561d9471dd20e9619e3be4cfe564796
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 ext-soundtouch

%global commit8 01db7cdd00aabcce559a8dddce8798dabb71949b
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 teakra

%global commit9 c3ca8febc2457ab5c581604f3236a8a511fc2e45
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})
%global srcname9 dds-ktx

%global commit10 0b1d9ccfc2093e5d6620cd9a11d03ee6ff6705f5
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 lodepng

%global commit11 3c27c785ad0f8a742af02e620dc225673f3a12d8
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 ext-boost

%global commit12 4a970bc302d671476122cbc6b43cc89fbf4a96ec
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 cpp-jwt

%global commit13 b3a6aa7b03c51ba976e4f4e96b1e31f77f43f312
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 glslang

%global commit14 37d49d2aa4c0a62f872720d6e5f2eaf90b2c95fa
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global srcname14 sirit

%global commit15 c214f6f2d1a7253bb0e9f195c2dc5b0659dc99ef
%global shortcommit15 %(c=%{commit15}; echo ${c:0:7})
%global srcname15 SPIRV-Headers

%global commit16 c788c52156f3ef7bc7ab769cb03c110a53ac8fcb
%global shortcommit16 %(c=%{commit16}; echo ${c:0:7})
%global srcname16 VulkanMemoryAllocator

%global commit17 d4a196d8c84e032d27f999adcea3075517c1c97f
%global shortcommit17 %(c=%{commit17}; echo ${c:0:7})
%global srcname17 Vulkan-Headers

%global commit18 216f00e8ddba6f2c64caf481a04f1ddd78b93e78
%global shortcommit18 %(c=%{commit18}; echo ${c:0:7})
%global srcname18 faad2

%global ffmpeg_includedir %(pkg-config --variable=includedir libavcodec)

%global cpphttplibver b251668
%global glad_ver 0.1.36
%global vkh_ver 1.4.304

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global appname org.azahar_emu.Azahar
%global vc_url  https://github.com/%{name}-emu

Name:           azahar
Version:        2121.1
Release:        1%{?dist}

Summary:        A 3DS Emulator

License:        GPL-2.0-only AND MIT AND BSD-2-Clause AND BSD-3-Clause%{!?with_dynarmic: AND ( 0BSD AND MIT )}%{!?with_boost: AND BSL-1.0}%{!?with_soundtouch: AND LGPL-2.1}
URL:            https://azahar-emu.org

%if %{with snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
%endif
%if %{without cryptopp}
Source2:        https://github.com/weidai11/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source5:        https://github.com/abdes/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
%endif
%if %{without dynarmic}
Source3:        https://github.com/MerryMage/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
%endif
%if %{without fmt}
Source4:        https://github.com/fmtlib/%{srcname4}/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
%endif
Source6:        https://github.com/neobrain/%{srcname6}/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
%if %{without soundtouch}
Source7:        %{vc_url}/%{srcname7}/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
%endif
Source8:        https://github.com/wwylele/%{srcname8}/archive/%{commit8}/%{srcname8}-%{shortcommit8}.tar.gz
Source9:        https://github.com/septag/%{srcname9}/archive/%{commit9}/%{srcname9}-%{shortcommit9}.tar.gz
Source10:       https://github.com/lvandeve/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
%if %{without boost}
Source11:       %{vc_url}/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
%endif
%if %{with webservice}
Source12:       https://github.com/arun11299/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz
%endif
Source13:       https://github.com/KhronosGroup/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
Source14:       %{vc_url}/%{srcname14}/archive/%{commit14}/%{srcname14}-%{shortcommit14}.tar.gz
Source15:       https://github.com/KhronosGroup/%{srcname15}/archive/%{commit15}/%{srcname15}-%{shortcommit15}.tar.gz
%if %{without vma}
Source16:       https://github.com/GPUOpen-LibrariesAndSDKs/%{srcname16}/archive/%{commit16}/%{srcname16}-%{shortcommit16}.tar.gz
%endif
%if %{without vulkan}
Source17:       https://github.com/KhronosGroup/%{srcname17}/archive/%{commit17}/%{srcname17}-%{shortcommit17}.tar.gz
%endif
Source18:       https://github.com/knik0/%{srcname18}/archive/%{commit18}/%{srcname18}-%{shortcommit18}.tar.gz

Source20:       compatibility_list.qrc


Patch10:        0001-Use-system-libraries.patch
Patch11:        0001-dumping-ffmpeg-7-buld-fix.patch
Patch500:       0001-glslang-gcc-15-build-fix.patch

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
BuildRequires:  pkgconfig(libbacktrace)
%else
Provides:       bundled(boost) = 0~git%{shortcommit11}
%endif
%if %{with cryptopp}
BuildRequires:  pkgconfig(libcryptopp)
%else
Provides:       bundled(cryptopp) = 0~git%{shortcommit2}
%endif
BuildRequires:  cmake(cubeb)
%if %{with dynarmic}
BuildRequires:  cmake(dynarmic) >= 6.6.1
%else
Provides:       bundled(dynarmic) = 0~git%{?shortcommit3}
%endif
BuildRequires:  pkgconfig(gamemode)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavfilter)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  ffmpeg-devel >= 4.2
%if %{with tests}
BuildRequires:  pkgconfig(catch2) >= 3.3.2
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
BuildRequires:  pkgconfig(libzstd) >= 1.5.5
BuildRequires:  pkgconfig(nlohmann_json) >= 3.9.0
BuildRequires:  cmake(OpenAL) >= 1.23.1
BuildRequires:  pkgconfig(sdl2)
%if %{with qt}
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6Core) >= 6.7.2
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Multimedia)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  qt6-qtbase-private-devel
%endif
%if %{with soundtouch}
BuildRequires:  cmake(SoundTouch)
%else
Provides:       bundled(soundtouch) = 0~git%{shortcommit7}
%endif
BuildRequires:  cmake(tsl-robin-map)
%if %{with vma}
BuildRequires:  cmake(VulkanMemoryAllocator) >= 3.1.0
%else
Provides:       bundled(vma) = ~git%{?shortcommit16}
%endif
%if %{with vulkan}
BuildRequires:  cmake(VulkanHeaders) >= %{vkh_ver}
%endif
BuildRequires:  cmake(xbyak)
BuildRequires:  pkgconfig(xkbcommon)

Requires:       hicolor-icon-theme
Requires:       shared-mime-info

Requires:       libGL%{?_isa}
Requires:       vulkan-loader%{?_isa}

Provides:       bundled(cpp-httplib) = 0~git%{?cpphttplibver}
Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(nihstro) = 0~git%{shortcommit6}
Provides:       bundled(teakra) = 0~git%{shortcommit8}
Provides:       bundled(dds-ktx) = 0~git%{shortcommit9}
Provides:       bundled(lodepng) = 0~git%{shortcommit10}
%if %{with webservice}
Provides:       bundled(cpp-jwt) = 0~git%{shortcommit12}
%endif
Provides:       bundled(glslang) = 0~git%{shortcommit13}
Provides:       bundled(sirit) = 0~git%{?shortcommit14}
Provides:       bundled(faad2) = ~git%{?shortcommit18}


%description
Azahar is an open-source 3DS emulator/debugger written in C++.


%package qt
Summary:        A 3DS Emulator (Qt frontend)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       hicolor-icon-theme

%description qt
Azahar is an open-source 3DS emulator/debugger written in C++.

This is the Qt frontend.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -N -p1
%autopatch -p1 -M 499

%if %{with cryptopp}
sed -e 's|crypto++|cryptopp|' -i externals/cmake-modules/Findcryptopp.cmake
%else
mkdir -p externals/cryptopp
tar -xf %{S:2} -C externals/cryptopp --strip-components 1
tar -xf %{S:5} -C externals/cryptopp-cmake --strip-components 1
%endif
%if %{without dynarmic}
tar -xf %{S:3} -C externals/dynarmic --strip-components 1
rm -rf externals/dynarmic/externals/{catch,fmt,robin-map,xbyak}
sed -e '/find_package/s|dynarmic|\0_DISABLED|g' -i externals/CMakeLists.txt
%endif
%if %{without fmt}
tar -xf %{S:4} -C externals/fmt --strip-components 1
sed -e '/find_package/s|fmt|\0_DISABLED|g' -i externals/CMakeLists.txt
%endif
tar -xf %{S:6} -C externals/nihstro --strip-components 1
%if %{without soundtouch}
tar -xf %{S:7} -C externals/soundtouch --strip-components 1
%endif
tar -xf %{S:8} -C externals/teakra --strip-components 1
tar -xf %{S:9} -C externals/dds-ktx --strip-components 1
tar -xf %{S:10} -C externals/lodepng/lodepng --strip-components 1
%if %{without boost}
tar -xf %{S:11} -C externals/boost --strip-components 1
%endif
%if %{with webservice}
tar -xf %{S:12} -C externals/cpp-jwt --strip-components 1
%endif
tar -xf %{S:13} -C externals/glslang --strip-components 1
%patch -P 500 -p1
tar -xf %{S:14} -C externals/sirit --strip-components 1
tar -xf %{S:15} -C externals/sirit/externals/SPIRV-Headers --strip-components 1
%if %{without vma}
tar -xf %{S:16} -C externals/vma --strip-components 1
%endif
%if %{without vulkan}
tar -xf %{S:17} -C externals/vulkan-headers/ --strip-components 1
%endif
tar -xf %{S:18} -C externals/faad2/faad2 --strip-components 1

find . -type f \( -name '*.c*' -o -name '*.h*' \) -exec chmod -x {} ';'

pushd externals
%if %{without boost}
cp -p boost/LICENSE_1_0.txt LICENSE.boost
%endif
%if %{with webservice}
cp -p cpp-jwt/LICENSE LICENSE.cpp-jwt
sed -e 's/\r//' -i LICENSE.cpp-jwt
%endif
%if %{without cryptopp}
sed 's/\r//' -i cryptopp/cryptopp/License.txt
cp -p cryptopp/cryptopp/License.txt LICENSE.cryptopp
%endif
cp -p dds-ktx/LICENSE LICENSE.dds-ktx
%if %{without dynarmic}
cp -p dynarmic/LICENSE.txt LICENSE.dynarmic
%endif
cp -p faad2/faad2/COPYING COPYING.faad2
%if %{without fmt}
cp -p fmt/LICENSE LICENSE.fmt
%endif
cp -p glslang/LICENSE.txt LICENSE.glslang
cp -p lodepng/lodepng/LICENSE LICENSE.lodepng
cp -p nihstro/license.txt LICENSE.nihstro
cp -p sirit/LICENSE.txt LICENSE.sirit
%if %{without soundtouch}
cp -p soundtouch/COPYING.txt COPYING.soundtouch
%endif
cp -p teakra/LICENSE LICENSE.teakra
%if %{without vma}
cp -p vma/LICENSE.txt LICENSE.vma
%endif
popd


rm -rf externals/gamemode
rm -f externals/json/json.hpp

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

sed -e '/pkg_check_modules/s|libopanal|openal|' -i externals/cmake-modules/FindOpenAL.cmake

%if %{with snapshot}
  sed \
    -e 's|@GIT_REV@|%{commit}|g' \
    -e 's|@GIT_BRANCH@|HEAD|g' \
    -e 's|@GIT_DESC@|%{shortcommit}|g' \
    -e 's|@BUILD_FULLNAME@|chinforpms %{version}-%{release}|g' \
    -e 's|@BUILD_DATE@|%(date +%F)|g' \
    -e 's|@BUILD_VERSION@|%{version}-g%{shortcommit}|g' \
    -i src/common/scm_rev.cpp.in
%endif

cp -p %{S:20} dist/compatibility_list/
touch dist/compatibility_list/compatibility_list.json


%build
%if %{with snapshot}
export CI=true
export GITHUB_ACTIONS=true
export GITHUB_REF_NAME=%{name}/%{name}
export GITHUB_REF_TYPE=tag
export GITHUB_REPOSITORY="%{vc_url}/%{azahar}"
%endif

export CXXFLAGS+=" -fpermissive"
%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DCITRA_WARNINGS_AS_ERRORS:BOOL=OFF \
  -DENABLE_LTO:BOOL=ON \
%if %{with qt}
  -DUSE_SYSTEM_QT:BOOL=ON \
  -DENABLE_QT_TRANSLATION:BOOL=ON \
  -DENABLE_QT_UPDATER:BOOL=OFF \
%else
  -DENABLE_QT:BOOL=OFF \
%endif
%if %{with dynarmic}
  -DUSE_SYSTEM_DYNARMIC:BOOL=ON \
%endif
%if %{with fmt}
  -DUSE_SYSTEM_FMT:BOOL=ON \
%endif
  -DUSE_SYSTEM_CPP_JWT:BOOL=OFF \
%if %{without webservice}
  -DENABLE_WEB_SERVICE:BOOL=OFF \
%endif
  -DUSE_DISCORD_PRESENCE:BOOL=OFF \
%if %{with cryptopp}
  -DUSE_SYSTEM_CRYPTOPP:BOOL=ON \
%endif
  -DUSE_SYSTEM_CUBEB:BOOL=ON \
  -DUSE_SYSTEM_ENET:BOOL=ON \
  -DUSE_SYSTEM_INIH:BOOL=ON \
  -DUSE_SYSTEM_JSON:BOOL=ON \
  -DUSE_SYSTEM_LIBUSB:BOOL=ON \
  -DUSE_SYSTEM_OPENAL:BOOL=ON \
  -DUSE_SYSTEM_SDL2:BOOL=ON \
  -DUSE_SYSTEM_OPENSSL:BOOL=ON \
%if %{with vma}
  -DUSE_SYSTEM_VMA:BOOL=ON \
%endif
%if %{with vulkan}
  -DUSE_SYSTEM_VULKAN_HEADERS:BOOL=ON \
%endif
  -DUSE_SYSTEM_XBYAK:BOOL=ON \
  -DUSE_SYSTEM_ZSTD:BOOL=ON \
%if %{with boost}
  -DUSE_SYSTEM_BOOST:BOOL=ON \
%endif
%if %{with soundtouch}
  -DUSE_SYSTEM_SOUNDTOUCH:BOOL=ON \
%endif
  -DUSE_SYSTEM_FFMPEG_HEADERS:BOOL=ON \
  -DSYSTEM_FFMPEG_INCLUDES:PATH=%{ffmpeg_includedir} \
  -DCRYPTOPP_SOURCES:PATH=$(pwd)/externals/cryptopp \
%if %{with tests}
  -DUSE_SYSTEM_CATCH2:BOOL=ON \
%else
  -DENABLE_TESTS:BOOL=OFF \
%endif
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


%cmake_build


%install
%cmake_install

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}
rm -rf %{buildroot}%{_datadir}/cmake


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop


%files
%license license.txt externals/{COPYING,COPYRIGHT,LICENSE}.*
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-room


%if %{with qt}
%files qt
%license license.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/%{appname}.xml
%endif


%changelog
* Thu May 08 2025 Phantom X <megaphantomx at hotmail dot com> - 2121.1-1.20250507git16980b0
- Initial spec

