%undefine _cmake_shared_libs
# Disable this. Local lto flags in use.
%global _lto_cflags %{nil}

%global commit 046d3913a35700239a994626602a0506de73c2ea
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190823
%global with_snapshot 0

%global with_bin 0

%if 0%{?with_bin}
%global debug_package %{nil}
%global _build_id_links none
%global __strip /bin/true
%endif

%ifarch %{ix86}
%global icd_arch i686
%else
%global icd_arch %{_arch}
%endif

%global pkgname amdvlk

%global commit1 a85ea7baf89016f72d7cb7c94db4c996d70d9898
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 %{pkgname}-llvm-project

%global commit2 c89f405e3632f0b639faafe61cd03cb851492f4e
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 %{pkgname}-llpc

%global commit3 14397c77fbc0c760397dd3162482407b2721a825
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 %{pkgname}-xgl

%global commit4 02ac99ba650afb3aebff3eb8006862ce93d31968
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 %{pkgname}-pal

%global commit5 faf9ff1722d3eac902481401252c2529c6988782
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 %{pkgname}-spvgen

%global commit6 3c566dd9cda44ca7fd97659e0b53ac953f9037d2
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 %{pkgname}-MetroHash

%global commit7 7387247eb9889ddcabbc1053b9c2052e253b088e
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 %{pkgname}-CWPack

%global commit8 ecdd9a3e6bd384bf51d096b507291faa10f14685
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 SPIRV-Tools

%global commit9 f5417a4b6633c3217c9a1bc2f0c70b1454975ba7
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})
%global srcname9 SPIRV-Headers

%global commit10 2e1b5fb39ebc2ef4cb77005f8267e4f3a6241ba1
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 SPIRV-Cross

%global commit11 fe15158676657bf965e41c32e15ae5db7ea2ab6a
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 glslang


%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global optflags %(echo %{optflags} | sed -e 's/ -g\\b/ -g1/')

%global kg_url  https://github.com/KhronosGroup
%global vc_url  https://github.com/GPUOpen-Drivers

Name:           amdvlk-vulkan-driver
Version:        2021.2.5
Release:        1%{?gver}%{?dist}
Summary:        AMD Open Source Driver For Vulkan
License:        MIT
URL:            %{vc_url}/AMDVLK

%global ver     %(echo %{version} | sed 's/\\./.Q/1')
%if 0%{?with_bin}
Source0:        %{url}/releases/download/v-%{ver}/%{pkgname}_%{ver}_amd64.deb

# Don't have x86 binary release
ExclusiveArch:  x86_64

%else
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v-%{ver}/%{pkgname}-%{ver}.tar.gz
%endif
Source1:        %{vc_url}/llvm-project/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        %{vc_url}/llpc/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        %{vc_url}/xgl/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        %{vc_url}/pal/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        %{vc_url}/spvgen/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        %{vc_url}/MetroHash/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        %{vc_url}/CWPack/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
Source8:        %{kg_url}/%{srcname8}/archive/%{commit8}/%{srcname8}-%{shortcommit8}.tar.gz
Source9:        %{kg_url}/%{srcname9}/archive/%{commit9}/%{srcname9}-%{shortcommit9}.tar.gz
Source10:       %{kg_url}/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
Source11:       %{kg_url}/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
%endif
Source20:       %{url}/raw/master/README.md
Source21:       amdPalSettings.cfg
Source30:       amdvlk-README-switchlayer

%if !0%{?with_bin}
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  perl-interpreter
BuildRequires:  python3
BuildRequires:  glibc-devel
BuildRequires:  libstdc++-devel
BuildRequires:  pkgconfig(gtest)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xshmfence)
BuildRequires:  pkgconfig(wayland-client)
%endif

Requires:       vulkan-loader%{?_isa}

Provides:       bundled(llvm) = 0~git%{shortcommit1}
Provides:       bundled(spirv-tools) = 0~git%{shortcommit8}


%description
The AMD Open Source Driver for Vulkan® is an open-source Vulkan driver
for Radeon™ graphics adapters on Linux®.


%package -n amdvlk-vulkan-switch-layer
Summary:        AMDVLK Vulkan switchable graphics layer
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       vulkan-loader%{?_isa}

%description -n amdvlk-vulkan-switch-layer
AMDVLK switchable graphics layer to switch AMD Vulkan driver between amdvlk and RADV.

This package only enable it by default.


%prep
%if 0%{?with_bin}
%setup -q -c -T
ar p %{S:0} data.tar.xz | tar xJ

cp -p %{S:20} .
mv usr/share/doc/amdvlk/copyright LICENSE.txt

sed -e 's|/usr/lib/x86_64-linux-gnu|%{_libdir}|g' -i etc/vulkan/icd.d/*.json

%else
%setup -q -c -n %{name}-%{version} -a 0 -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7 -a 8 -a 9 -a 10 -a 11

%if 0%{?with_snapshot}
ln -sf AMDVLK-%{commit} AMDVLK
%else
ln -sf AMDVLK-v-%{ver} AMDVLK
%endif
ln -sf llvm-project-%{commit1} llvm-project
ln -sf llpc-%{commit2} llpc
ln -sf xgl-%{commit3} xgl
ln -sf pal-%{commit4} pal
ln -sf spvgen-%{commit5} spvgen
mv MetroHash-%{commit6} MetroHash
mv CWPack-%{commit7} CWPack
mv SPIRV-Tools-%{commit8} spvgen/external/SPIRV-tools
mv SPIRV-Headers-%{commit9} spvgen/external/SPIRV-tools/external/SPIRV-Headers
mv SPIRV-Cross-%{commit10} spvgen/external/SPIRV-cross
mv glslang-%{commit11} spvgen/external/glslang

cp -p AMDVLK/LICENSE.txt .
cp -p AMDVLK/README.md .

# workaround for AMDVLK#89
find . -name 'CMakeLists.txt' -exec sed -e 's/-Werror=/-W/g' -e "s/-Werror\b//g" -i "{}" ';'
sed -e "s/-Werror\b//g" -i pal/shared/gpuopen/cmake/AMD.cmake

sed -e '/CMAKE_SHARED_LINKER_FLAGS_RELEASE/s| -s\b| |g' -i xgl/CMakeLists.txt
sed -e '/soname=/s|so.1|so|g' -i xgl/icd/CMakeLists.txt
%endif

cp -p %{S:30} README.switchlayer

sed \
  -e '/spirv-compiler-options/s|-Wno-deprecated-declarations|\0 -fPIC|g' \
  -i spvgen/external/SPIRV-cross/CMakeLists.txt

mkdir _temp_install
sed \
  -e 's|@AMDVLK_INSTALL_PATH@|%{_libdir}|g' \
  -e 's|@ISABITS@|%{?__isa_bits}|g' \
  xgl/icd/Loader/LunarG/Lnx/amd-icd.json > _temp_install/amd_icd%{?__isa_bits}.json


%build

%if !0%{?with_bin}

extdir=$(pwd)

export CFLAGS="%{build_cflags} -fno-plt -mno-avx"
export CXXFLAGS="%{build_cxxflags} -fno-plt -mno-avx"

%cmake \
  -S xgl \
  -DBUILD_WAYLAND_SUPPORT:BOOL=ON \
  -DSPIRV_CROSS_FORCE_PIC:BOOL=ON \
  -DXGL_METROHASH_PATH:PATH=${extdir}/MetroHash \
  -DXGL_CWPACK_PATH:PATH=${extdir}/CWPack \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DCMAKE_AR:FILEPATH=%{_bindir}/gcc-ar \
  -DCMAKE_NM:FILEPATH=%{_bindir}/gcc-nm \
  -DCMAKE_RANLIB:FILEPATH=%{_bindir}/gcc-ranlib \
  -G Ninja \
%{nil}

%cmake_build
%cmake_build -- spvgen

%endif


%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_datadir}/vulkan/icd.d
mkdir -p %{buildroot}%{_datadir}/vulkan/implicit_layer.d

%if 0%{?with_bin}
  mv usr/lib/x86_64-linux-gnu/*.so _temp_install/
  mv etc/vulkan/icd.d/amd_icd%{?__isa_bits}.json _temp_install/
%else
  mv %{__cmake_builddir}/icd/amdvlk%{?__isa_bits}.so _temp_install/
  mv %{__cmake_builddir}/spvgen/spvgen.so _temp_install/
%endif
install -pm0644 _temp_install/amd_icd%{?__isa_bits}.json \
  %{buildroot}%{_datadir}/vulkan/icd.d/amd_icd.%{icd_arch}.json
install -pm0755 _temp_install/*.so %{buildroot}%{_libdir}/

ln -sf ../icd.d/amd_icd.%{icd_arch}.json \
  %{buildroot}%{_datadir}/vulkan/implicit_layer.d/amd_switch_layer.%{icd_arch}.json

mkdir -p %{buildroot}%{_sysconfdir}/amd
cp -p %{S:21} %{buildroot}%{_sysconfdir}/amd/amdPalSettings.cfg


%files
%license LICENSE.txt
%doc README.md README.switchlayer
%dir %{_sysconfdir}/amd
%config %{_sysconfdir}/amd/amdPalSettings.cfg
%{_datadir}/vulkan/icd.d/amd_icd.%{icd_arch}.json
%{_libdir}/amdvlk%{?__isa_bits}.so
%{_libdir}/spvgen.so

%files -n amdvlk-vulkan-switch-layer
%license LICENSE.txt
%doc README.md
%{_datadir}/vulkan/implicit_layer.d/amd_switch_layer.%{icd_arch}.json


%changelog
* Fri Jun 11 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.2.5-1
- 2021.Q2.5

* Tue May 18 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.2.3-1
- 2021.Q2.3

* Wed Apr 28 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.2.2-1
- 2021.Q2.2

* Wed Apr 07 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.2.1-1
- 2021.Q2.1

* Fri Mar 19 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.1.6-1
- 2021.Q1.6

* Fri Mar 12 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.1.5-1
- 2021.Q1.5

* Thu Feb 25 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.1.4-1
- 2021.Q1.4

* Mon Feb 08 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.1.3-1
- 2021.Q1.3

* Sun Jan 31 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.1.2-1
- 2021.Q1.2

* Fri Jan 08 2021 Phantom X <megaphantomx at hotmail dot com> - 2021.1.1-1
- 2021.Q1.1
- Add amdvlk-vulkan-switch-layer package

* Tue Dec 15 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.4.6-1
- 2020.Q4.6

* Thu Nov 19 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.4.5-1
- 2020.Q4.5

* Tue Nov 17 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.4.4-1
- 2020.Q4.4

* Thu Nov 05 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.4.3-1
- 2020.Q4.3

* Thu Oct 29 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.4.2-1
- 2020.Q4.2

* Tue Oct 20 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.4.1-1
- 2020.Q4.1

* Mon Sep 28 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.3.6-1
- 2020.Q3.6

* Mon Sep 14 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.3.5-1
- 2020.Q3.5

* Fri Aug 21 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.3.4-1
- 2020.Q3.4

* Fri Aug 07 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.3.3-1
- 2020.Q3.3

* Thu Jul 23 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.3.2-1
- 2020.Q3.2

* Fri Jul 10 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.3.1-1
- 2020.Q3.1

* Tue Jun 30 2020 Phantom X <megaphantomx at hotmail dot com> - 2020.2.6-1
- 2020.Q2.6

* Wed Jun 24 2020 Phantom X <megaphantomx at bol dot com dot br> - 2020.2.5-1
- 2020.Q2.5

* Thu May 28 2020 Phantom X <megaphantomx at bol dot com dot br> - 2020.2.4-1
- 2020.Q2.4

* Thu May 14 2020 Phantom X <megaphantomx at bol dot com dot br> - 2020.2.3-1
- 2020.Q2.3

* Thu Apr 30 2020 Phantom X <megaphantomx at bol dot com dot br> - 2020.2.2-1
- 2020.Q2.2

* Thu Apr 16 2020 Phantom X <megaphantomx at bol dot com dot br> - 2020.2.1-1
- 2020.Q2.1

* Fri Mar 27 2020 Phantom X <megaphantomx at bol dot com dot br> - 2020.1.4-1
- 2020.Q1.4

* Sat Mar 21 2020 Phantom X <megaphantomx at bol dot com dot br> - 2020.1.3-2
- Fix icd loading order

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 2020.1.3-1
- 2020.Q1.3

* Sat Feb 22 2020 Phantom X <megaphantomx at bol dot com dot br> - 2020.1.2-1
- 2020.Q1.2

* Thu Jan 23 2020 Phantom X <megaphantomx at bol dot com dot br> - 2020.1.1-1
- 2020.Q1.1

* Mon Dec 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.4.5-1
- 2019.Q4.5

* Fri Dec 13 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.4.4-1
- 2019.Q4.4

* Wed Nov 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.4.3-1
- 2019.Q4.3

* Sat Nov 09 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.4.2-1
- 2019.Q4.2

* Tue Oct 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.4.1-1
- 2019.Q4.1
- Improve settings file

* Tue Sep 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.3.6-1
- 2019.Q3.6

* Thu Aug 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.3.5-1
- 2019.Q3.5

* Tue Aug 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 2019.3.4-1
- chinforpms changes and bin support

* Mon Jul 29 2019 Mihai Vultur <xanto@egaming.ro>
- Implement some version autodetection to reduce maintenance work.
- Don't build wsa anymore.
