%global commit d6d4efcd8fee4bd28f397f117cad6c42d833368b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200506
%global with_snapshot 1

%global commit1 c0df742ec0b8178ad58c68cff3437ad4b6a06e26
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 SPIRV-Headers

%global commit2 c8590c18bd0c70dcd1caa7d43c5f2d020439b012
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 SPIRV-Tools

%global commit3 b7823ec38921d69977cdefb570da740d85320236
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 SPIRV-Cross

%global kg_url https://github.com/KhronosGroup

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           dxil-spirv
Version:        0.0.0
Release:        1%{?gver}%{?dist}
Summary:        DXIL conversion to SPIR-V for D3D12 translation libraries

License:        LGPLv2+
URL:            https://github.com/HansKristian-Work/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        %{kg_url}/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        %{kg_url}/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        %{kg_url}/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Fix-cmake-and-pkg-config-files-location.patch
Patch1:         0001-bc-add-missing-header.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
%{name} aims to provide translation of DXIL (SM 6.x) shaders to SPIR-V which can
be used in the vkd3d project, which implements D3D12 on top of Vulkan.


%package        libs
Summary:        Library files for %{name}
Provides:       %{name}-libs%{?_isa} = %{version}

%description    libs
Library files for %{name}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
Development files for %{name}


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1

tar -xf %{S:1} -C third_party/spirv-headers --strip-components 1
tar -xf %{S:2} -C third_party/SPIRV-Tools --strip-components 1
tar -xf %{S:3} -C third_party/SPIRV-Cross --strip-components 1

%else
%autosetup -n %{name}-%{version} -p1
%endif

sed -e 's| -L${sharedlibdir}||' -i pkg-config/dxil-spirv-c-shared.pc.in


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}

%cmake .. \
  -DBUILD_SHARED_LIBS:BOOL=ON \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -GNinja \
%{nil}

%ninja_build

popd


%install
%ninja_install -C %{_target_platform}


%files
%license LICENSE
%doc DESCRIPTORS.md README.md
%{_bindir}/dxil-extract
%{_bindir}/%{name}

%files libs
%{_libdir}/lib%{name}-c-shared.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}-c-shared.so
%{_libdir}/cmake/*
%{_libdir}/pkgconfig/%{name}-c-shared.pc


%changelog
* Wed May 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 1-1.20200506gitd6d4efc
- Initial spec

