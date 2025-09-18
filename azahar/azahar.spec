# Selective LTO.
%global _lto_cflags %{nil}
%undefine _cmake_shared_libs
%undefine _hardened_build

%bcond clang 0
%if %{with clang}
%global toolchain clang
%endif

%global with_extra_flags -O3 -Wp,-U_GLIBCXX_ASSERTIONS
%{?with_extra_flags:%global _pkg_extra_cflags %{?with_extra_flags}}
%{?with_extra_flags:%global _pkg_extra_cxxflags %{?with_extra_flags}}
%{!?_hardened_build:%global _pkg_extra_ldflags -Wl,-z,now}

%global commit eb1197a65c9bbd795aa904a53a49b977688e3dde
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250916
%bcond snapshot 1

%bcond sse42 1
# Enable system boost
%bcond boost 1
# Enable system cryptopp
%bcond cryptopp 1
# Enable system dynarmic
%bcond dynarmic 0
# Enable system fmt
%bcond fmt 1
%bcond glslang 1
# Disable Qt build
%bcond qt 1
%bcond soundtouch 1
# Enable webservice
%bcond webservice 1
%bcond vma 1
# Enable system vulkan
%bcond vulkan 1
%bcond xbyak 0
%bcond zstd 1
# Build tests
%bcond tests 0

%global commit1 a36decbe43d0e5a570ac3d3ba9a0b226dc832a17
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 compatibility-list

%global commit2 60f81a77e0c9a0e7ffc1ca1bc438ddfa2e43b78e
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 cryptopp

%global commit3 278405bd71999ed3f3c77c5f78344a06fef798b9
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 dynarmic

%global commit300 7b08d83418f628b800dfac1c9a16c3f59036fbad
%global shortcommit300 %(c=%{commit300}; echo ${c:0:7})
%global srcname300 mcl

%global commit301 0b2432ced0884fd152b471d97ecf0258ff4d859f
%global shortcommit301 %(c=%{commit301}; echo ${c:0:7})
%global srcname301 zycore-c

%global commit302 bffbb610cfea643b98e87658b9058382f7522807
%global shortcommit302 %(c=%{commit302}; echo ${c:0:7})
%global srcname302 zydis

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

%global commit13 fc9889c889561c5882e83819dcaffef5ed45529b
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 glslang

%global commit14 37d49d2aa4c0a62f872720d6e5f2eaf90b2c95fa
%global shortcommit14 %(c=%{commit14}; echo ${c:0:7})
%global srcname14 sirit

%global commit15 aa6cef192b8e693916eb713e7a9ccadf06062ceb
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

%global commit19 a62abcb402009b9ca5975e6167c09f237f630e0e
%global shortcommit19 %(c=%{commit19}; echo ${c:0:7})
%global srcname19 SPIRV-Tools

%global commit20 f8745da6ff1ad1e7bab384bd1f9d742439278e99
%global shortcommit20 %(c=%{commit20}; echo ${c:0:7})
%global srcname20 zstd

%global commit21 0d67fd1530016b7c56f3cd74b3fca920f4c3e2b4
%global shortcommit21 %(c=%{commit21}; echo ${c:0:7})
%global srcname21 xbyak

%global ffmpeg_includedir %(pkg-config --variable=includedir libavcodec)

%global cpphttplibver b251668
%global glad_ver 0.1.36
%global vkh_ver 1.4.304
%global xbyak_ver 7.23.1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global appname org.azahar_emu.Azahar
%global vc_url  https://github.com/%{name}-emu

%global ver     %%{lua:ver = string.gsub(rpm.expand("%{version}"), "~", "-"); print(ver)}
%global verb    %%{lua:verb = string.gsub(rpm.expand("%%{ver}"), "%.", "-"); print(verb)}

Name:           azahar
Version:        2123~rc2.32
Release:        1%{?dist}

Summary:        A 3DS Emulator

License:        GPL-2.0-only AND MIT AND BSD-2-Clause AND BSD-3-Clause%{!?with_dynarmic: AND ( 0BSD AND MIT )}%{!?with_boost: AND BSL-1.0}%{!?with_glslang: AND Apache-2.0}%{!?with_soundtouch: AND LGPL-2.1}
URL:            https://azahar-emu.org

%if %{with snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/%{ver}/%{name}-%{ver}.tar.gz
%endif
Source1:        %{vc_url}/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
%if %{without cryptopp}
Source2:        https://github.com/weidai11/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source5:        https://github.com/abdes/%{srcname5}/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
%endif
%if %{without dynarmic}
Source3:        %{vc_url}/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source300:      %{vc_url}/%{srcname300}/archive/%{commit300}/%{srcname300}-%{shortcommit300}.tar.gz
Source301:      https://github.com/zyantific/%{srcname301}/archive/%{commit301}/%{srcname301}-%{shortcommit301}.tar.gz
Source302:      https://github.com/zyantific/%{srcname302}/archive/%{commit302}/%{srcname302}-%{shortcommit302}.tar.gz
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
%if %{without glslang}
Source13:       https://github.com/KhronosGroup/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
%endif
Source14:       %{vc_url}/%{srcname14}/archive/%{commit14}/%{srcname14}-%{shortcommit14}.tar.gz
%if %{without glslang}
Source15:       https://github.com/KhronosGroup/%{srcname15}/archive/%{commit15}/%{srcname15}-%{shortcommit15}.tar.gz
%endif
%if %{without vma}
Source16:       https://github.com/GPUOpen-LibrariesAndSDKs/%{srcname16}/archive/%{commit16}/%{srcname16}-%{shortcommit16}.tar.gz
%endif
%if %{without vulkan}
Source17:       https://github.com/KhronosGroup/%{srcname17}/archive/%{commit17}/%{srcname17}-%{shortcommit17}.tar.gz
%endif
Source18:       https://github.com/knik0/%{srcname18}/archive/%{commit18}/%{srcname18}-%{shortcommit18}.tar.gz
%if %{without glslang}
Source19:       https://github.com/KhronosGroup/%{srcname19}/archive/%{commit19}/%{srcname19}-%{shortcommit19}.tar.gz
%endif
Source20:       https://github.com/facebook/%{srcname20}/archive/%{commit20}/%{srcname20}-%{shortcommit20}.tar.gz
%if %{without xbyak}
Source21:       https://github.com/herumi/%{srcname21}/archive/%{commit21}/%{srcname21}-%{shortcommit21}.tar.gz
%endif

Patch10:        0001-Use-system-libraries.patch
Patch11:        0001-dumping-ffmpeg-7-buld-fix.patch
Patch500:       0001-glslang-gcc-15-build-fix.patch

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
%if %{with zstd}
BuildRequires:  pkgconfig(libzstd) >= 1.5.7
%else
Provides:       bundled(libzstd) = 0~git%{shortcommit20}
%endif
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
%if %{with glslang}
BuildRequires:  cmake(glslang)
BuildRequires:  cmake(SPIRV-Tools)
BuildRequires:  spirv-headers-devel
%endif
%if %{with vma}
BuildRequires:  cmake(VulkanMemoryAllocator) >= 3.1.0
%else
Provides:       bundled(vma) = ~git%{?shortcommit16}
%endif
%if %{with vulkan}
BuildRequires:  cmake(VulkanHeaders) >= %{vkh_ver}
%endif
%if %{with xbyak}
BuildRequires:  cmake(xbyak) >= %{xbyak_ver}
%else
Provides:       bundled(xbyak) = %{xbyak_ver}
%endif
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

tar -xf %{S:1} -C dist/compatibility_list --strip-components 1
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
tar -xf %{S:300} -C externals/dynarmic/externals/mcl --strip-components 1
tar -xf %{S:301} -C externals/dynarmic/externals/zycore --strip-components 1
tar -xf %{S:302} -C externals/dynarmic/externals/zydis --strip-components 1
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
%if %{without glslang}
tar -xf %{S:13} -C externals/glslang --strip-components 1
%patch -P 500 -p1
%endif
tar -xf %{S:14} -C externals/sirit/sirit --strip-components 1
%if %{without glslang}
tar -xf %{S:15} -C externals/spirv-headers --strip-components 1
rm -rf externals/sirit/sirit/externals/SPIRV-Headers
ln -sf ../../../spirv-headers externals/sirit/sirit/externals/SPIRV-Headers
tar -xf %{S:19} -C externals/spirv-tools --strip-components 1
%else
sed -e '/add_subdirectory(spirv-tools/d' -i externals/CMakeLists.txt
%endif
%if %{without vma}
tar -xf %{S:16} -C externals/vma --strip-components 1
%endif
%if %{without vulkan}
tar -xf %{S:17} -C externals/vulkan-headers/ --strip-components 1
%endif
tar -xf %{S:18} -C externals/faad2/faad2 --strip-components 1
%if %{with zstd}
zstdcommom='zstd-*/lib/common'
tar -xf %{S:20} -C externals/zstd --strip-components 1 \
  'zstd-*/lib/common'/{compiler,debug,mem,portability_macros,zstd_deps}.h \
  'zstd-*/lib/common/xxhash.*' 'zstd-*/contrib/seekable_format'
%else
tar -xf %{S:20} -C externals/zstd --strip-components 1
%endif
%if %{without xbyak}
tar -xf %{S:21} -C externals/xbyak --strip-components 1
%endif

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
%if %{without glslang}
cp -p glslang/LICENSE.txt LICENSE.glslang
cp -p spirv-tools/LICENSE LICENSE.spirv-tools
%endif
cp -p lodepng/lodepng/LICENSE LICENSE.lodepng
cp -p nihstro/license.txt LICENSE.nihstro
cp -p sirit/sirit/LICENSE.txt LICENSE.sirit
%if %{without soundtouch}
cp -p soundtouch/COPYING.txt COPYING.soundtouch
%endif
cp -p teakra/LICENSE LICENSE.teakra
%if %{without vma}
cp -p vma/LICENSE.txt LICENSE.vma
%endif
%if %{without xbyak}
cp -p xbyak/COPYRIGHT LICENSE.xbyak
%endif
%if %{without zstd}
cp -p zstd/COPYING COPYING.zstd
cp -p zstd/LICENSE LICENSE.zstd
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

sed -e 's|zstd/contrib/seekable_format/||' -i src/common/zstd_compression.cpp

sed -e '/find_package/s|Git|\0_DISABLED|g' -i CMakeModules/GenerateSCMRev.cmake

sed -e '/pkg_check_modules/s|libopanal|openal|' -i externals/cmake-modules/FindOpenAL.cmake

%if %{with snapshot}
  sed \
    -e 's|@GIT_REV@|%{commit}|g' \
    -e 's|@GIT_BRANCH@|HEAD|g' \
    -e 's|@GIT_DESC@|%{shortcommit}|g' \
    -e 's|@BUILD_FULLNAME@|chinforpms %{version}-%{release}|g' \
    -e 's|@BUILD_DATE@|%(date +%F)|g' \
    -e 's|@BUILD_VERSION@|%{verb}-g%{shortcommit}|g' \
    -i src/common/scm_rev.cpp.in
%endif


%build
%if %{with snapshot}
export CI=true
export GITHUB_ACTIONS=true
export GITHUB_REF_NAME=%{name}/%{name}
export GITHUB_REF_TYPE=tag
export GITHUB_REPOSITORY="%{vc_url}/%{azahar}"
%endif

%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DCITRA_WARNINGS_AS_ERRORS:BOOL=OFF \
  -DENABLE_LTO:BOOL=ON \
  %{!?with_sse42:-DENABLE_SSE42:BOOL=OFF} \
%if %{with qt}
  -DUSE_SYSTEM_QT:BOOL=ON \
  -DENABLE_QT_TRANSLATION:BOOL=ON \
  -DENABLE_QT_UPDATER:BOOL=OFF \
%else
  -DENABLE_QT:BOOL=OFF \
%endif
  %{?with_dynarmic:-DUSE_SYSTEM_DYNARMIC:BOOL=ON} \
  %{?with_fmt:-DUSE_SYSTEM_FMT:BOOL=ON} \
  -DUSE_SYSTEM_CPP_JWT:BOOL=OFF \
  %{!?with_webservice:-DENABLE_WEB_SERVICE:BOOL=OFF} \
  -DUSE_DISCORD_PRESENCE:BOOL=OFF \
  %{?with_cryptopp:-DUSE_SYSTEM_CRYPTOPP:BOOL=ON} \
  -DUSE_SYSTEM_CUBEB:BOOL=ON \
  -DUSE_SYSTEM_ENET:BOOL=ON \
  -DUSE_SYSTEM_INIH:BOOL=ON \
  -DUSE_SYSTEM_JSON:BOOL=ON \
  -DUSE_SYSTEM_LIBUSB:BOOL=ON \
  -DUSE_SYSTEM_OPENAL:BOOL=ON \
  -DUSE_SYSTEM_SDL2:BOOL=ON \
  -DUSE_SYSTEM_OPENSSL:BOOL=ON \
%if %{with glslang}
  -DUSE_SYSTEM_GLSLANG:BOOL=ON \
  -DUSE_SYSTEM_SPIRV_HEADERS:BOOL=ON \
  -DSIRIT_USE_SYSTEM_SPIRV_HEADERS:BOOL=ON \
%endif
  %{?with_vma:-DUSE_SYSTEM_VMA:BOOL=ON} \
  %{?with_vulkan:-DUSE_SYSTEM_VULKAN_HEADERS:BOOL=ON} \
  %{?with_xbyak:-DUSE_SYSTEM_XBYAK:BOOL=ON} \
  %{?with_zstd:-DUSE_SYSTEM_ZSTD:BOOL=ON} \
  %{?with_boost:-DUSE_SYSTEM_BOOST:BOOL=ON} \
  %{?with_soundtouch:-DUSE_SYSTEM_SOUNDTOUCH:BOOL=ON} \
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
* Fri Jun 13 2025 Phantom X <megaphantomx at hotmail dot com> - 2122~rc1.2-1.20250609git63f5258
- 2122-rc1

* Fri Jun 06 2025 Phantom X <megaphantomx at hotmail dot com> - 2121.2-1.20250606git868e946
- 2121.2

* Thu May 08 2025 Phantom X <megaphantomx at hotmail dot com> - 2121.1-1.20250507git16980b0
- Initial spec

