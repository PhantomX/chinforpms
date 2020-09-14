%undefine _cmake_shared_libs

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

%global commit1 30cb97a1d0efebb4317f9abeec8d90a5a83d4837
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 %{pkgname}-llvm-project

%global commit2 9b5cb15acc8ff789420ed9ed593e35c81303d10c
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 %{pkgname}-llpc

%global commit3 598c6832a4983f5b75b38a589fca5be80a2f3bb0
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 %{pkgname}-xgl

%global commit4 609b2b8ad982f4f2028cf4411cc2e55fc5e6fcf3
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 %{pkgname}-pal

%global commit5 4865b574184e261d87e77277282e90e3be14c53a
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 %{pkgname}-spvgen

%global commit6 712f76fee75d69b23a1ea8f6465752c3ccaaf9a2
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 %{pkgname}-MetroHash

%global commit7 7387247eb9889ddcabbc1053b9c2052e253b088e
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 %{pkgname}-CWPack

%global commit8 4dd122392f3ad757e70951a1198479bf233d4cd8
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})
%global srcname8 SPIRV-Tools

%global commit9 3fdabd0da2932c276b25b9b4a988ba134eba1aa6
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})
%global srcname9 SPIRV-Headers

%global commit10 f0fe4442e32a900f49140f8597d54fefb4ba32d0
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 SPIRV-Cross

%global commit11 f257e0ea6b9aeab2dc7af3207ac6d29d2bbc01d0
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 glslang


%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global optflags %(echo %{optflags} | sed -e 's/ -g\\b/ -g1/')

%global kg_url  https://github.com/KhronosGroup
%global vc_url  https://github.com/GPUOpen-Drivers

Name:           amdvlk-vulkan-driver
Version:        2020.3.4
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


%description
The AMD Open Source Driver for Vulkan® is an open-source Vulkan driver
for Radeon™ graphics adapters on Linux®.


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

sed \
  -e '/spirv-compiler-options/s|-Wno-deprecated-declarations|\0 -fPIC|g' \
  -i spvgen/external/SPIRV-cross/CMakeLists.txt


%build
# Disable this. Local lto flags in use.
%define _lto_cflags %{nil}

%if !0%{?with_bin}

extdir=$(pwd)

export CFLAGS="%{build_cflags} -fno-plt -mno-avx"
export CXXFLAGS="%{build_cxxflags} -fno-plt -mno-avx"

%cmake \
  -S xgl \
  -B %{__cmake_builddir} \
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

mkdir _temp_install
%if 0%{?with_bin}
  mv usr/lib/x86_64-linux-gnu/*.so _temp_install/
  mv etc/vulkan/icd.d/amd_icd%{?__isa_bits}.json _temp_install/
%else
  mv %{__cmake_builddir}/icd/amdvlk%{?__isa_bits}.so _temp_install/
  mv %{__cmake_builddir}/spvgen/spvgen.so _temp_install/
  mv AMDVLK/json/Redhat/amd_icd%{?__isa_bits}.json _temp_install/
%endif
install -pm0644 _temp_install/amd_icd%{?__isa_bits}.json \
  %{buildroot}%{_datadir}/vulkan/icd.d/amd_icd.%{icd_arch}.json
install -pm0755 _temp_install/*.so %{buildroot}%{_libdir}/


mkdir -p %{buildroot}%{_sysconfdir}/amd
cp -p %{S:21} %{buildroot}%{_sysconfdir}/amd/amdPalSettings.cfg


%files
%license LICENSE.txt
%doc README.md
%dir %{_sysconfdir}/amd
%config %{_sysconfdir}/amd/amdPalSettings.cfg
%{_datadir}/vulkan/icd.d/amd_icd.%{icd_arch}.json
%{_libdir}/amdvlk%{?__isa_bits}.so
%{_libdir}/spvgen.so


%changelog
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
