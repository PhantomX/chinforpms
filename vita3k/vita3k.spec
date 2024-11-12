%dnl global _lto_cflags -fno-lto
%undefine _hardened_build
%undefine _cmake_shared_libs

%bcond_without clang
%if %{with clang}
%global toolchain clang
%endif

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit 15a9e614aa7d61c803ff36a9b9f51d6afac43342
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20241109

%bcond_with capstone
%bcond_with ffmpeg
%bcond_with fmt
%bcond_with spdlog
%bcond_without vma
%bcond_with yamlcpp
# Needs dispatch header
%bcond_with xxhash

%global commit10 82767fe38823c32536726ea798f392b0b49e66b9
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 LibAtrac9

%global commit11 bccaa94db814af33d8ef05c153e7c34d8bd4d685
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 SPIRV-Cross

%global commit12 f2bf7d00fe8e23eb1ce11b4a7d2c4869432a85df
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 VulkanMemoryAllocator-Hpp

%global commit13 c35576bed0295689540b39873126129adfa0b4c8
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 better-enums

%global commit15 e98f4ee160380d7c39dc1f04e7488bcf0770d391
%global shortcommit15 %(c=%{commit15}; echo ${c:0:7})
%global srcname15 dlmalloc

%global commit16 d8b33e4311fbb41aac376cc8b644c47df03c1549
%global shortcommit16 %(c=%{commit16}; echo ${c:0:7})
%global srcname16 dynarmic

%global commit17 e30b7d7fe228bfb3f6e41ce1040b44a15eb7d5e0
%global shortcommit17 %(c=%{commit17}; echo ${c:0:7})
%global srcname17 ffmpeg-core

%global commit18 b50e685db996c167e6c831dcef582aba6e14276a
%global shortcommit18 %(c=%{commit18}; echo ${c:0:7})
%global srcname18 fmt

%global commit19 76b52ebf77833908dc4c0dd6c70a9c357ac720bd
%global shortcommit19 %(c=%{commit19}; echo ${c:0:7})
%global srcname19 glslang

%global commit20 f8d7d77c06936315286eb55f8de22cd23c188571
%global shortcommit20 %(c=%{commit20}; echo ${c:0:7})
%global srcname20 googletest

%global commit21 1dfbb100d6ca6e7d813102e979c07f66a56546bb
%global shortcommit21 %(c=%{commit21}; echo ${c:0:7})
%global srcname21 imgui

%global commit22 63c7fed4b31c50c8a529b6c15ae7d7d9e89812a6
%global shortcommit22 %(c=%{commit22}; echo ${c:0:7})
%global srcname22 imgui_club

%global commit23 14ec3073358544c70b77702ff6394f09ce349c59
%global shortcommit23 %(c=%{commit23}; echo ${c:0:7})
%global srcname23 libfat16

%global commit24 c099aaee9a24a35ad93e06513b41aeb503d848d0
%global shortcommit24 %(c=%{commit24}; echo ${c:0:7})
%global srcname24 nativefiledialog-extended

%global commit25 c75def6db38f9978c55e8d27227858df911cd727
%global shortcommit25 %(c=%{commit25}; echo ${c:0:7})
%global srcname25 printf

%global commit26 ab1aa9b36388843f6a9f8dc86b1746f1f2a7e557
%global shortcommit26 %(c=%{commit26}; echo ${c:0:7})
%global srcname26 psvpfstools

%global commit27 f7f20f39fe4f206c6f19e26ebfef7b261ee59ee4
%global shortcommit27 %(c=%{commit27}; echo ${c:0:7})
%global srcname27 stb

%global commit28 5d542dc09f3d9378d005092a4ad446bd405f819a
%global shortcommit28 %(c=%{commit28}; echo ${c:0:7})
%global srcname28 tracy

%global commit29 80a767105520abdf070abbb0f0b42bf79bdcb7d4
%global shortcommit29 %(c=%{commit29}; echo ${c:0:7})
%global srcname29 unicorn

%global commit30 61a943c67da5008b100bdcabff812ecd7816425d
%global shortcommit30 %(c=%{commit30}; echo ${c:0:7})
%global srcname30 vita-toolchain

%global commit31 f7320141120f720aecc4c32be25586e7da9eb978
%global shortcommit31 %(c=%{commit31}; echo ${c:0:7})
%global srcname31 yaml-cpp

%global commit32 097c04d9413c59a58b00d4d1c8d5dc0ac158ffaa
%global shortcommit32 %(c=%{commit32}; echo ${c:0:7})
%global srcname32 capstone

%global commit33 bbb27a5efb85b92a0486cf361a8635715a53f6ba
%global shortcommit33 %(c=%{commit33}; echo ${c:0:7})
%global srcname33 xxHash

%global commit34 6dd38b8a1dbaa7863aa907045f32308a56a6ff5d
%global shortcommit34 %(c=%{commit34}; echo ${c:0:7})
%global srcname34 concurrentqueue

%global commit35 27cb4c76708608465c413f6d0e6b8d99a4d84302
%global shortcommit35 %(c=%{commit35}; echo ${c:0:7})
%global srcname35 spdlog

%global commit120 66afe099f1cf1f79c270471e9c0f02139072057d
%global shortcommit120 %(c=%{commit120}; echo ${c:0:7})
%global srcname120 VulkanMemoryAllocator

%global commit260 3896b7a74c70baed0e2f6039a1dbd723e5d5cc8f
%global shortcommit260 %(c=%{commit260}; echo ${c:0:7})
%global srcname260 libb64

%global commit262 7d1e69bee7d2f08ea5754eff4463c041aacd49af
%global shortcommit262 %(c=%{commit262}; echo ${c:0:7})
%global srcname262 libzrif

%global commit263 4094450bcaac2256236d61ae3a730425ae47bd39
%global shortcommit263 %(c=%{commit263}; echo ${c:0:7})
%global srcname263 psvpfsparser

%global commit300 9e0f4913866431aef48967cfb7667b085e79428b
%global shortcommit300 %(c=%{commit300}; echo ${c:0:7})
%global srcname300 psp2rela

%global dist .%{date}git%{shortcommit}%{?dist}

%global ffmpeg_ver 5.1.4
%global glad_ver 2.0.4
%global miniz_ver 3.0.0
%global vk_ver 1.3.261

%global pkgname Vita3K
%global vc_url  https://github.com/%{pkgname}
%global kg_url https://github.com/KhronosGroup
%global oc_url https://github.com/ocornut
%global kw_url https://github.com/korewawatchful

%global sbuild %%(echo %{version} | cut -d. -f4)

Name:           vita3k
Version:        0.2.0.3686
Release:        1%{?dist}
Summary:        Experimental PlayStation Vita emulator

License:        GPL-2.0-or-later AND BSD-2-Clause AND MIT AND ( 0BSD AND MIT ) AND GPL-3.0-or-later AND BSD-3-Clause AND Apache-2.0 AND GPL-2.0-only AND CC0-1.0
URL:            https://vita3k.org/

Source0:        %{vc_url}/%{pkgname}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz

Source10:       %{vc_url}/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
Source11:       %{kg_url}/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
%if %{without vma}
Source12:       https://github.com/Macdu/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz
Source120:      https://github.com/GPUOpen-LibrariesAndSDKs/%{srcname120}/archive/%{commit120}/%{srcname120}-%{shortcommit120}.tar.gz
%endif
Source13:       https://github.com/aantron/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
Source15:       %{vc_url}/%{srcname15}/archive/%{commit15}/%{srcname15}-%{shortcommit15}.tar.gz
Source16:       %{vc_url}/%{srcname16}/archive/%{commit16}/%{srcname16}-%{shortcommit16}.tar.gz
%if %{without ffmpeg}
Source17:       %{vc_url}/%{srcname17}/archive/%{commit17}/%{srcname17}-%{shortcommit17}.tar.gz
Source170:      https://ffmpeg.org/releases/ffmpeg-%{ffmpeg_ver}.tar.xz
Source171:      ffmpeg-linux_x86-64.sh
%endif
%if %{without fmt}
Source18:       https://github.com/fmtlib/%{srcname18}/archive/%{commit18}/%{srcname18}-%{shortcommit18}.tar.gz
%endif
Source19:       %{kg_url}/%{srcname19}/archive/%{commit19}/%{srcname19}-%{shortcommit19}.tar.gz
Source20:       https://github.com/google/%{srcname20}/archive/%{commit20}/%{srcname20}-%{shortcommit20}.tar.gz
Source21:       %{oc_url}/%{srcname21}/archive/%{commit21}/%{srcname21}-%{shortcommit21}.tar.gz
Source22:       %{oc_url}/%{srcname22}/archive/%{commit22}/%{srcname22}-%{shortcommit22}.tar.gz
Source23:       %{vc_url}/%{srcname23}/archive/%{commit23}/%{srcname23}-%{shortcommit23}.tar.gz
Source24:       https://github.com/btzy/%{srcname24}/archive/%{commit24}/%{srcname24}-%{shortcommit24}.tar.gz
Source25:       %{vc_url}/%{srcname25}/archive/%{commit25}/%{srcname25}-%{shortcommit25}.tar.gz
Source26:       %{vc_url}/%{srcname26}/archive/%{commit26}/%{srcname26}-%{shortcommit26}.tar.gz
Source260:      %{kw_url}/%{srcname260}/archive/%{commit260}/%{srcname260}-%{shortcommit260}.tar.gz
Source262:      %{kw_url}/%{srcname262}/archive/%{commit262}/%{srcname262}-%{shortcommit262}.tar.gz
Source263:      %{vc_url}/%{srcname263}/archive/%{commit263}/%{srcname263}-%{shortcommit263}.tar.gz
Source27:       https://github.com/nothings/%{srcname27}/archive/%{commit27}/%{srcname27}-%{shortcommit27}.tar.gz
Source28:       https://github.com/wolfpld/%{srcname28}/archive/%{commit28}/%{srcname28}-%{shortcommit28}.tar.gz
Source29:       %{vc_url}/%{srcname29}/archive/%{commit29}/%{srcname29}-%{shortcommit29}.tar.gz
Source30:       https://github.com/vitasdk/%{srcname30}/archive/%{commit30}/%{srcname30}-%{shortcommit30}.tar.gz
Source300:      https://github.com/Princess-of-Sleeping/%{srcname300}/archive/%{commit300}/%{srcname300}-%{shortcommit300}.tar.gz
%if %{without yamlcpp}
Source31:       https://github.com/jbeder/%{srcname31}/archive/%{commit31}/%{srcname31}-%{shortcommit31}.tar.gz
%endif
%if %{without capstone}
Source32:       https://github.com/aquynh/%{srcname32}/archive/%{commit32}/%{srcname32}-%{shortcommit32}.tar.gz
%endif
%if %{without xxhash}
Source33:       https://github.com/Cyan4973/%{srcname33}/archive/%{commit33}/%{srcname33}-%{shortcommit33}.tar.gz
%endif
Source34:       https://github.com/cameron314/%{srcname34}/archive/%{commit34}/%{srcname34}-%{shortcommit34}.tar.gz
%if %{without spdlog}
Source35:       https://github.com/gabime/%{srcname35}/archive/%{commit35}/%{srcname35}-%{shortcommit35}.tar.gz
%endif

Patch10:        0001-Use-system-libraries.patch
Patch11:        0001-Fix-shared_path.patch
Patch12:        0001-Fix-update-settings.patch
Patch500:       0001-Disable-ffmpeg-download.patch
Patch501:       0001-vma-set-missing-namespace.patch

%if %{without ffmpeg}
ExclusiveArch:  x86_64
%endif

BuildRequires:  cmake
BuildRequires:  ninja-build
%if %{with clang}
BuildRequires:  compiler-rt
BuildRequires:  clang
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  boost-devel
%if %{with capstone}
BuildRequires:  pkgconfig(capstone) >= 5
%else
Provides:       bundled(%{srcname32}) = 0~git%{shortcommit32}
%endif
BuildRequires:  cmake(cubeb)
%if %{with ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  ffmpeg-devel
%else
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(libva-x11)
BuildRequires:  pkgconfig(x11)
Provides:       bundled(ffmpeg) = %{ffmpeg_ver}
%endif
%if %{with fmt}
BuildRequires:  pkgconfig(fmt) >= 11.0.1
%else
Provides:       bundled(%{srcname18}) = 0~git%{shortcommit18}
%endif
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libssl)
%if %{with xxhash}
BuildRequires:  pkgconfig(libxxhash)
%else
Provides:       bundled(libxxhash) = 0~git%{shortcommit33}
%endif
BuildRequires:  cmake(pugixml)
%if %{with spdlog}
BuildRequires:  cmake(spdlog) >= 1.14.1
%else
Provides:       bundled(%{srcname35}) = 0~git%{shortcommit35}
%endif
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  cmake(VulkanHeaders) >= %{vk_ver}
%if %{with vma}
BuildRequires:  cmake(VulkanMemoryAllocator-Hpp) >= 3.1.0
%else
Provides:       bundled(VulkanMemoryAllocator-Hpp) = 0~git%{shortcommit3}
%endif
%if %{with yamlcpp}
BuildRequires:  cmake(yaml-cpp)
%else
Provides:       bundled(%{srcname31}) = 0~git%{shortcommit31}
%endif
BuildRequires:  pkgconfig(zlib)

Requires:       hicolor-icon-theme
Requires:       mplus-1mn-fonts
Requires:       vulkan-loader%{?_isa} >= %{vk_ver}
Requires:       xdg-desktop-portal

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       bundled(%{srcname10}) = 0~git%{shortcommit10}
Provides:       bundled(vma) = 0~git%{shortcommit12}
Provides:       bundled(spirv-cross) = 0~git%{shortcommit11}
Provides:       bundled(%{srcname13}) = 0~git%{shortcommit13}
Provides:       bundled(%{srcname15}) = 0~git%{shortcommit15}
Provides:       bundled(%{srcname16}) = 0~git%{shortcommit16}
Provides:       bundled(%{srcname19}) = 0~git%{shortcommit19}
Provides:       bundled(%{srcname20}) = 0~git%{shortcommit20}
Provides:       bundled(%{srcname21}) = 0~git%{shortcommit21}
Provides:       bundled(%{srcname22}) = 0~git%{shortcommit22}
Provides:       bundled(%{srcname23}) = 0~git%{shortcommit23}
Provides:       bundled(%{srcname24}) = 0~git%{shortcommit24}
Provides:       bundled(%{srcname25}) = 0~git%{shortcommit25}
Provides:       bundled(%{srcname26}) = 0~git%{shortcommit26}
Provides:       bundled(%{srcname27}) = 0~git%{shortcommit27}
Provides:       bundled(%{srcname28}) = 0~git%{shortcommit28}
Provides:       bundled(%{srcname29}) = 0~git%{shortcommit29}
Provides:       bundled(%{srcname30}) = 0~git%{shortcommit30}
Provides:       bundled(glad) = %{glad_ver}
Provides:       bundled(miniz) = %{miniz_ver}

%description
%{pkgname} is an experimental PlayStation Vita emulator.


%prep
%autosetup -n %{pkgname}-%{commit} -N -p1
%autopatch -M 499 -p1

pushd external
tar -xf %{S:10} -C %{srcname10} --strip-components 1
tar -xf %{S:11} -C %{srcname11} --strip-components 1
%if %{without vma}
tar -xf %{S:12} -C %{srcname12} --strip-components 1
tar -xf %{S:120} -C %{srcname12}/VulkanMemoryAllocator --strip-components 1
%patch -P 501 -p1
cp -p VulkanMemoryAllocator-Hpp/LICENSE COPYING.vma-hpp
%endif
tar -xf %{S:13} -C %{srcname13} --strip-components 1
tar -xf %{S:15} -C %{srcname15} --strip-components 1
tar -xf %{S:16} -C %{srcname16} --strip-components 1
%if %{without ffmpeg}
tar -xf %{S:17} -C ffmpeg --strip-components 1
%patch -P 500 -p1
rm -rf ffmpeg/include/*
rm -rf ffmpeg/lib/*
tar -xf %{S:170} -C ffmpeg/include --strip-components 1
cp -p %{S:171} ffmpeg/include/
%endif
%if %{without fmt}
tar -xf %{S:18} -C %{srcname18} --strip-components 1
sed -e '/find_package/s|fmt|\0_DISABLED|g' -i CMakeLists.txt
cp -p fmt/LICENSE LICENSE.fmt
%endif
tar -xf %{S:19} -C %{srcname19} --strip-components 1
tar -xf %{S:20} -C %{srcname20} --strip-components 1
tar -xf %{S:21} -C %{srcname21} --strip-components 1
tar -xf %{S:22} -C %{srcname22} --strip-components 1
tar -xf %{S:23} -C %{srcname23} --strip-components 1
tar -xf %{S:24} -C %{srcname24} --strip-components 1
tar -xf %{S:25} -C %{srcname25} --strip-components 1
tar -xf %{S:26} -C %{srcname26} --strip-components 1
tar -xf %{S:260} -C %{srcname26}/%{srcname260} --strip-components 1
tar -xf %{S:262} -C %{srcname26}/%{srcname262} --strip-components 1
tar -xf %{S:263} -C %{srcname26}/%{srcname263} --strip-components 1
tar -xf %{S:27} -C %{srcname27} --strip-components 1
tar -xf %{S:28} -C %{srcname28} --strip-components 1
tar -xf %{S:29} -C %{srcname29} --strip-components 1
tar -xf %{S:30} -C %{srcname30} --strip-components 1
tar -xf %{S:300} -C %{srcname30}/%{srcname300} --strip-components 1
%if %{without yamlcpp}
tar -xf %{S:31} -C %{srcname31} --strip-components 1
cp -p yaml-cpp/LICENSE LICENSE.yaml-cpp
sed -e '/find_package/s|yaml-cpp|\0_DISABLED|g' -i CMakeLists.txt
%endif
%if %{without capstone}
tar -xf %{S:32} -C %{srcname32} --strip-components 1
sed -e '/find_package/s|capstone|\0_DISABLED|g' -i CMakeLists.txt
%endif
%if %{without xxhash}
tar -xf %{S:33} -C %{srcname33} --strip-components 1
cp -p xxHash/LICENSE LICENSE.xxhash
sed -e '/pkg_search_module/s|libxxhash|\0_DISABLED|g' -i CMakeLists.txt
%endif
tar -xf %{S:34} -C %{srcname34} --strip-components 1
%if %{without spdlog}
tar -xf %{S:35} -C %{srcname35} --strip-components 1
cp -p spdlog/LICENSE LICENSE.spdlog
sed -e '/find_package/s|spdlog|\0_DISABLED|g' -i CMakeLists.txt
%endif
cp -p LibAtrac9/LICENSE LICENSE.LibAtrac9
cp -p better-enums/LICENSE.md LICENSE.better-enums.md
%if %{without capstone}
cp -p capstone/LICENSE.TXT LICENSE.capstone
%endif
cp -p concurrentqueue/LICENSE.md LICENSE.concurrentqueue.md
cp -p ddspp/LICENSE LICENSE.ddspp
cp -p dynarmic/LICENSE.txt LICENSE.dynarmic
%if %{without ffmpeg}
cp -p ffmpeg/copyright copyright.ffmpeg
%endif
cp -p glslang/LICENSE.txt LICENSE.glslang
cp -p googletest/LICENSE LICENSE.googletest
cp -p imgui/LICENSE.txt LICENSE.imgui
cp -p imgui_club/LICENSE.txt LICENSE.imgui_club
cp -p libfat16/LICENSE LICENSE.libfat16
cp -p miniz/LICENSE LICENSE.miniz
cp -p nativefiledialog-extended/LICENSE LICENSE.nativefiledialog-extended
cp -p printf/LICENSE LICENSE.printf
cp -p SPIRV-Cross/LICENSE LICENSE.SPIRV-Cross
cp -p stb/LICENSE LICENSE.stb
cp -p tracy/LICENSE LICENSE.tracy
cp -p unicorn/COPYING COPYING.unicorn
cp -p vita-toolchain/COPYING COPYING.vita-toolchain
popd

sed \
  -e '/Boost_USE_STATIC_LIBS/s| ON| OFF|' \
  -i CMakeLists.txt

sed \
  -e 's| git | true |g' \
  -e 's|${GIT_COUNT}|%{sbuild}|g' \
  -e '/static-libgcc/d' \
  -e '/rpath=/d' \
  -i vita3k/CMakeLists.txt

sed \
  -e 's|${GIT_COUNT}|%{sbuild}|g' \
  -e 's|${GIT_HASH}|%{shortcommit}|g' \
  -e 's|${VITA3K_GIT_REV}|%{shortcommit}|g' \
  -i vita3k/config/src/version.cpp.in

sed \
  -e 's|"unknown"|"%{shortcommit11}"|' \
  -e 's| unknown | %{shortcommit11} |' \
  -e 's|GIT_FOUND|GIT_FOUND_DISABLED|g' \
  -i external/SPIRV-Cross/CMakeLists.txt

sed \
  -e 's|getenv("APPDIR")|"%{_prefix}"|g' \
  -e 's|usr/share/|share/|' \
  -i vita3k/app/src/app_init.cpp

cat > %{pkgname}.desktop <<'EOF'
[Desktop Entry]
Type=Application
Version=1.0
Name=Vita3K
GenericName=PlayStation Vita Emulator
Comment=Experimental PlayStation Vita emulator
Categories=Game;Emulator;
Icon=%{pkgname}
Exec=%{pkgname}
Terminal=false
EOF

%if %{without ffmpeg}
pushd external/ffmpeg
sed -e '/target_link_libraries/s|INTERFACE|\0 va va-drm va-x11 X11|g' -i CMakeLists.txt
sed \
  -e '/^ARCH=/s|=.*|=%{_target_cpu}|g' \
  -e '/make install/d' \
  -i include/ffmpeg-linux_*.sh
popd
%endif

%build
%if %{without ffmpeg}
pushd external/ffmpeg/include
sed \
  -e "/extra-cflags/s|-O3|$CFLAGS|g" \
  -i ffmpeg-linux_*.sh
chmod +x ffmpeg-linux_*.sh
%ifarch x86_64
%{?with_clang:CFLAGS=} ./ffmpeg-linux_x86-64.sh
%endif
%make_build
make install
popd
mkdir -p %{__cmake_builddir}/external/ffmpeg/lib
mv external/ffmpeg/include/linux/x86_64/lib/*.a %{__cmake_builddir}/external/ffmpeg/lib/
%endif

%cmake \
  -G Ninja \
  -DUSE_LTO:STRING=NEVER \
  -DVITA3K_FORCE_SYSTEM_BOOST:BOOL=ON \
%if %{with ffmpeg}
  -DVITA3K_FORCE_SYSTEM_FFMPEG:BOOL=ON \
%endif
  -DXXH_X86DISPATCH_ALLOW_AVX:BOOL=ON \
  -DUSE_VITA3K_UPDATE:BOOL=OFF \
  -DUSE_DISCORD_RICH_PRESENCE:BOOL=OFF \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{__cmake_builddir}/bin/%{pkgname} %{buildroot}%{_bindir}/%{pkgname}

mkdir -p %{buildroot}%{_datadir}/%{pkgname}/data
cp -rp %{__cmake_builddir}/bin/{data,lang,shaders-builtin} \
  %{buildroot}%{_datadir}/%{pkgname}/

rm -f %{buildroot}%{_datadir}/%{pkgname}/data/fonts/*
ln -sf ../../../fonts/mplus/mplus-1mn-bold.ttf \
  %{buildroot}%{_datadir}/%{pkgname}/data/fonts/mplus-1mn-bold.ttf

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{pkgname}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
ln -s ../../../../%{pkgname}/data/image/icon.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{pkgname}.png

for res in 16 22 24 32 36 48 64 72 96 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick data/image/icon.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{pkgname}.png
done


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{pkgname}.desktop


%files
%license COPYING.txt external/{COPYING,LICENSE,copyright}.*
%doc README.md
%{_bindir}/%{pkgname}
%{_datadir}/%{pkgname}/
%{_datadir}/applications/%{pkgname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{pkgname}.*


%changelog
* Thu Feb 01 2024 Phantom X <megaphantomx at hotmail dot com> - 0.2.0.3561-1.202401295gitac73ee8
- 0.2.0.3561

* Sun Nov 12 2023 Phantom X <megaphantomx at hotmail dot com> - 0.1.9.3477-1.20231112git6030dae
- Initial spec
