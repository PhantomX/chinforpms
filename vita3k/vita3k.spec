%dnl global _lto_cflags -fno-lto
%undefine _hardened_build
%undefine _cmake_shared_libs

%bcond clang 1
%if %{with clang}
%global toolchain clang
%endif

%global with_extra_flags -O3 -Wp,-U_GLIBCXX_ASSERTIONS
%{?with_extra_flags:%global _pkg_extra_cflags %{?with_extra_flags}}
%{?with_extra_flags:%global _pkg_extra_cxxflags %{?with_extra_flags}}
%{!?_hardened_build:%global _pkg_extra_ldflags -Wl,-z,now}

%global commit be6927105e65c0d6d17b707aac2e7f72214997e4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20260726

%bcond capstone 0
%bcond ffmpeg 0
%bcond fmt 0
%bcond nfd 0
%if %{with fmt}
%bcond spdlog 1
%endif
%bcond vma 0
%bcond yamlcpp 0
# Needs dispatch header
%bcond xxhash 1

# Set to build with versioned LLVM packages
%dnl %global llvm_pkgver 19

%global commit10 82767fe38823c32536726ea798f392b0b49e66b9
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 LibAtrac9

%global commit11 d8e3e2b141b8c8a167b2e3984736a6baacff316c
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 SPIRV-Cross

%global commit12 3843082eaa6a6f67e6780715fcd602fc81942c9c
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 VulkanMemoryAllocator-Hpp

%global commit13 c35576bed0295689540b39873126129adfa0b4c8
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 better-enums

%global commit13 319da6b563d8da689f3b9df2fbb839edd41a1943
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 substitute

%global commit15 e98f4ee160380d7c39dc1f04e7488bcf0770d391
%global shortcommit15 %(c=%{commit15}; echo ${c:0:7})
%global srcname15 dlmalloc

%global commit16 86458a0bd369d63ba4c2ef812cacbb6c9080c065
%global shortcommit16 %(c=%{commit16}; echo ${c:0:7})
%global srcname16 dynarmic

%global commit17 02f4f2691b0efffff8923235baf146a87fc37263
%global shortcommit17 %(c=%{commit17}; echo ${c:0:7})
%global srcname17 ffmpeg-core

%global commit18 1be298e1bd68957e4cd352e1f676f00e07dcfb57
%global shortcommit18 %(c=%{commit18}; echo ${c:0:7})
%global srcname18 fmt

%global commit19 fc9889c889561c5882e83819dcaffef5ed45529b
%global shortcommit19 %(c=%{commit19}; echo ${c:0:7})
%global srcname19 glslang

%global commit20 52eb8108c5bdec04579160ae17225d66034bd723
%global shortcommit20 %(c=%{commit20}; echo ${c:0:7})
%global srcname20 googletest

%global commit23 d9a890b712dcdb46d3d33230997efc59f5ad8d62
%global shortcommit23 %(c=%{commit23}; echo ${c:0:7})
%global srcname23 libfat16

%global commit24 fc168e8605bfa51aaec22ab0c4e46b9de665a437
%global shortcommit24 %(c=%{commit24}; echo ${c:0:7})
%global srcname24 nativefiledialog-extended

%global commit25 c75def6db38f9978c55e8d27227858df911cd727
%global shortcommit25 %(c=%{commit25}; echo ${c:0:7})
%global srcname25 printf

%global commit26 e21df9a74852433f48d6593b8ef203dc7c424e05
%global shortcommit26 %(c=%{commit26}; echo ${c:0:7})
%global srcname26 psvpfstools

%global commit27 31c1ad37456438565541f4919958214b6e762fb4
%global shortcommit27 %(c=%{commit27}; echo ${c:0:7})
%global srcname27 stb

%global commit28 05cceee0df3b8d7c6fa87e9638af311dbabc63cb
%global shortcommit28 %(c=%{commit28}; echo ${c:0:7})
%global srcname28 tracy

%global commit30 43fc1e3c686a1fc035eca583fdfeaa5e6419a61a
%global shortcommit30 %(c=%{commit30}; echo ${c:0:7})
%global srcname30 vita-toolchain

%global commit31 56e3bb550c91fd7005566f19c079cb7a503223cf
%global shortcommit31 %(c=%{commit31}; echo ${c:0:7})
%global srcname31 yaml-cpp

%global commit32 022575848782a4801fd150fdbc927effcbca0864
%global shortcommit32 %(c=%{commit32}; echo ${c:0:7})
%global srcname32 capstone

%global commit33 e626a72bc2321cd320e953a0ccf1584cad60f363
%global shortcommit33 %(c=%{commit33}; echo ${c:0:7})
%global srcname33 xxHash

%global commit34 9afb99746f0f5fc94ac8aef737053ae0481ba8d1
%global shortcommit34 %(c=%{commit34}; echo ${c:0:7})
%global srcname34 concurrentqueue

%global commit35 79524ddd08a4ec981b7fea76afd08ee05f83755d
%global shortcommit35 %(c=%{commit35}; echo ${c:0:7})
%global srcname35 spdlog

%global commit120 c788c52156f3ef7bc7ab769cb03c110a53ac8fcb
%global shortcommit120 %(c=%{commit120}; echo ${c:0:7})
%global srcname120 VulkanMemoryAllocator

%global commit260 3896b7a74c70baed0e2f6039a1dbd723e5d5cc8f
%global shortcommit260 %(c=%{commit260}; echo ${c:0:7})
%global srcname260 libb64

%global commit262 7d1e69bee7d2f08ea5754eff4463c041aacd49af
%global shortcommit262 %(c=%{commit262}; echo ${c:0:7})
%global srcname262 libzrif

%global commit263 d14381f871a69009bd18b2aaec2213a6738bebba
%global shortcommit263 %(c=%{commit263}; echo ${c:0:7})
%global srcname263 psvpfsparser

%global commit300 9e0f4913866431aef48967cfb7667b085e79428b
%global shortcommit300 %(c=%{commit300}; echo ${c:0:7})
%global srcname300 psp2rela

%global dist .%{date}git%{shortcommit}%{?dist}

%global ffmpeg_ver 7.1.2
%global glad_ver 2.0.4
%global miniz_ver 3.0.0
%global vk_ver 1.4.303

%global appname org.vita3k.vita3k
%global pkgname Vita3K
%global vc_url  https://github.com/%{pkgname}
%global kg_url https://github.com/KhronosGroup
%global oc_url https://github.com/ocornut
%global kw_url https://github.com/korewawatchful

%global sbuild %%(echo %{version} | cut -d. -f4)

Name:           vita3k
Version:        0.2.0.4067
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
Source13:       %{vc_url}/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz
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
Source23:       %{vc_url}/%{srcname23}/archive/%{commit23}/%{srcname23}-%{shortcommit23}.tar.gz
%if %{without nfd}
Source24:       https://github.com/btzy/%{srcname24}/archive/%{commit24}/%{srcname24}-%{shortcommit24}.tar.gz
%endif
Source25:       %{vc_url}/%{srcname25}/archive/%{commit25}/%{srcname25}-%{shortcommit25}.tar.gz
Source26:       %{vc_url}/%{srcname26}/archive/%{commit26}/%{srcname26}-%{shortcommit26}.tar.gz
Source260:      %{kw_url}/%{srcname260}/archive/%{commit260}/%{srcname260}-%{shortcommit260}.tar.gz
Source262:      %{kw_url}/%{srcname262}/archive/%{commit262}/%{srcname262}-%{shortcommit262}.tar.gz
Source263:      %{vc_url}/%{srcname263}/archive/%{commit263}/%{srcname263}-%{shortcommit263}.tar.gz
Source27:       https://github.com/nothings/%{srcname27}/archive/%{commit27}/%{srcname27}-%{shortcommit27}.tar.gz
Source28:       https://github.com/wolfpld/%{srcname28}/archive/%{commit28}/%{srcname28}-%{shortcommit28}.tar.gz
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
Patch11:        0001-cmake-do-not-install-docs.patch
Patch12:        0001-Remove-disabled-itens-from-gui.patch
Patch500:       0001-Disable-ffmpeg-download.patch
Patch501:       0001-Remove-ValidationFailedEXTError.patch

%if %{without ffmpeg}
ExclusiveArch:  x86_64
%endif

BuildRequires:  cmake
BuildRequires:  ninja-build
%if %{with clang}
BuildRequires:  compiler-rt%{?llvm_pkgver}
BuildRequires:  clang%{?llvm_pkgver}
BuildRequires:  llvm%{?llvm_pkgver}
BuildRequires:  lld%{?llvm_pkgver}
%else
BuildRequires:  gcc
BuildRequires:  gcc-c++
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
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
BuildRequires:  make
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(libva-x11)
BuildRequires:  pkgconfig(x11)
Provides:       bundled(ffmpeg) = %{ffmpeg_ver}
%endif
%if %{with fmt}
BuildRequires:  pkgconfig(fmt) >= 11.1.4
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
%if %{with nfd}
BuildRequires:  nativefiledialog-extended-devel >= 1.2.0
%else
Provides:       bundled(%{srcname24}) = 0~git%{shortcommit24}
%endif
BuildRequires:  cmake(pugixml)
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Multimedia)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
%if %{with spdlog}
BuildRequires:  cmake(spdlog) >= 1.15.2
%else
Provides:       bundled(%{srcname35}) = 0~git%{shortcommit35}
%endif
BuildRequires:  pkgconfig(sdl3)
BuildRequires:  cmake(VulkanHeaders) >= %{vk_ver}
%if %{with vma}
BuildRequires:  cmake(VulkanMemoryAllocator) >= 3.2.1
BuildRequires:  cmake(VulkanMemoryAllocator-Hpp) >= 3
%else
Provides:       bundled(VulkanMemoryAllocator-Hpp) = 0~git%{shortcommit12}
%endif
%if %{with yamlcpp}
BuildRequires:  cmake(yaml-cpp)
%else
Provides:       bundled(%{srcname31}) = 0~git%{shortcommit31}
%endif
BuildRequires:  pkgconfig(zlib)

Requires:       hicolor-icon-theme
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
Provides:       bundled(%{srcname23}) = 0~git%{shortcommit23}
Provides:       bundled(%{srcname25}) = 0~git%{shortcommit25}
Provides:       bundled(%{srcname26}) = 0~git%{shortcommit26}
Provides:       bundled(%{srcname27}) = 0~git%{shortcommit27}
Provides:       bundled(%{srcname28}) = 0~git%{shortcommit28}
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
%patch -P 501 -p1 -d %{srcname12}
sed -e '/find_package/s|VulkanMemoryAllocator|\0_DISABLED|g' -i CMakeLists.txt
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
tar -xf %{S:23} -C %{srcname23} --strip-components 1
%if %{without nfd}
tar -xf %{S:24} -C %{srcname24} --strip-components 1
sed -e '/find_package/s|nfd|\0_DISABLED|g' -i CMakeLists.txt
cp -p nativefiledialog-extended/LICENSE LICENSE.nativefiledialog-extended
%endif
tar -xf %{S:25} -C %{srcname25} --strip-components 1
tar -xf %{S:26} -C %{srcname26} --strip-components 1
tar -xf %{S:260} -C %{srcname26}/%{srcname260} --strip-components 1
tar -xf %{S:262} -C %{srcname26}/%{srcname262} --strip-components 1
tar -xf %{S:263} -C %{srcname26}/%{srcname263} --strip-components 1
tar -xf %{S:27} -C %{srcname27} --strip-components 1
tar -xf %{S:28} -C %{srcname28} --strip-components 1
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
cp -p substitute/LICENSE.txt LICENSE.substitute
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
cp -p libfat16/LICENSE LICENSE.libfat16
cp -p miniz/LICENSE LICENSE.miniz
cp -p printf/LICENSE LICENSE.printf
cp -p SPIRV-Cross/LICENSE LICENSE.SPIRV-Cross
cp -p stb/LICENSE LICENSE.stb
cp -p tracy/LICENSE LICENSE.tracy
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

%if %{with clang}
export CC=clang%{?llvm_pkgver:-%{llvm_pkgver}}
export CXX=clang++%{?llvm_pkgver:-%{llvm_pkgver}}
export AR=llvm-ar%{?llvm_pkgver:-%{llvm_pkgver}}
export AS=llvm-as%{?llvm_pkgver:-%{llvm_pkgver}}
export NM=llvm-nm%{?llvm_pkgver:-%{llvm_pkgver}}
export RANLIB=llvm-ranlib%{?llvm_pkgver:-%{llvm_pkgver}}
%endif

%if %{without ffmpeg}
pushd external/ffmpeg/include
sed \
  -e "/extra-cflags/s|-O3|$CFLAGS|g" \
  -i ffmpeg-linux_*.sh
chmod +x ffmpeg-linux_*.sh
%ifarch x86_64
./ffmpeg-linux_x86-64.sh
%endif
%make_build
make install
popd
mkdir -p %{_vpath_builddir}/external/ffmpeg/lib
mv external/ffmpeg/include/linux/x86_64/lib/*.a %{_vpath_builddir}/external/ffmpeg/lib/
%endif

%cmake \
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
%cmake_install

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}
rm -rf %{buildroot}%{_datadir}/cmake

%find_lang %{name} --with-qt


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files -f %{name}.lang
%license COPYING.txt external/{COPYING,LICENSE,copyright}.*
%doc README.md
%{_bindir}/%{pkgname}
%{_datadir}/%{pkgname}/data
%{_datadir}/%{pkgname}/icons
%{_datadir}/%{pkgname}/shaders-builtin
%dir %{_datadir}/%{pkgname}/translations
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.*
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Mon Jul 27 2026 Phantom X <megaphantomx at hotmail dot com> - 0.2.0.4067-1.20260726gitbe69271
- Qt6

* Thu Jul 24 2025 Phantom X <megaphantomx at hotmail dot com> - 0.2.0.3806-1.20250714gitcf3d627
- SDL3

* Thu Feb 01 2024 Phantom X <megaphantomx at hotmail dot com> - 0.2.0.3561-1.202401295gitac73ee8
- 0.2.0.3561

* Sun Nov 12 2023 Phantom X <megaphantomx at hotmail dot com> - 0.1.9.3477-1.20231112git6030dae
- Initial spec
