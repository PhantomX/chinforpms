%global commit 598df2bd5e173f9bcd762ab937e8a04918940c04
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200820
%global with_snapshot 1

%global commit1 3fdabd0da2932c276b25b9b4a988ba134eba1aa6
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 SPIRV-Headers

%global commit2 4dd122392f3ad757e70951a1198479bf233d4cd8
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 SPIRV-Tools

%global commit3 f0fe4442e32a900f49140f8597d54fefb4ba32d0
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 SPIRV-Cross

%global kg_url https://github.com/KhronosGroup

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           dxil-spirv
Version:        0.0.0
Release:        8%{?gver}%{?dist}
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

sed \
  -e 's|"unknown"|"%{shortcommit3}"|' \
  -e 's| unknown | %{shortcommit3} |' \
  -e 's|GIT_FOUND|GIT_FOUND_DISABLED|g' \
  -i third_party/SPIRV-Cross/CMakeLists.txt


%build
%cmake \
  -B %{__cmake_builddir} \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -GNinja \
%{nil}

%cmake_build


%install
%cmake_install


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
* Sat Aug 22 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0.0-8.20200820git598df2b
- Bump

* Sun Aug 02 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0.0-7.20200801git79652dd
- New snapshot

* Sun Jul 26 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0.0-6.20200724gitd3964e0
- Bump

* Fri Jun 26 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0.0-5.20200624git7f6a3fc
- New snapshot

* Tue Jun 16 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0.0-4.20200612git2b06fd1
- Bump

* Sat Jun 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.0.0-3.20200527gitfd082d1
- New snapshot

* Tue May 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.0.0-2.20200515gite2bd025
- Bump

* Wed May 06 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.0.0-1.20200506gitd6d4efc
- Initial spec

