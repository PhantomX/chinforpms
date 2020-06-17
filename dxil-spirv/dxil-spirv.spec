%global commit 2b06fd178505c1e22ad9de6c916aa6c74878ba07
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200612
%global with_snapshot 1

%global commit1 11d7637e7a43cd88cfd4e42c99581dcb682936aa
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 SPIRV-Headers

%global commit2 94947035463af174fc84f4f8adfa27252236b483
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 SPIRV-Tools

%global commit3 9e3df69d4e994776103dfa6070c0c343cffac4a4
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 SPIRV-Cross

%global kg_url https://github.com/KhronosGroup

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           dxil-spirv
Version:        0.0.0
Release:        4%{?gver}%{?dist}
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
%cmake . -B %{_target_platform} \
  -DBUILD_SHARED_LIBS:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -GNinja \
%{nil}

%ninja_build -C %{_target_platform}


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
* Tue Jun 16 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0.0-4.20200612git2b06fd1
- Bump

* Sat Jun 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.0.0-3.20200527gitfd082d1
- New snapshot

* Tue May 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.0.0-2.20200515gite2bd025
- Bump

* Wed May 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.0.0-1.20200506gitd6d4efc
- Initial spec

