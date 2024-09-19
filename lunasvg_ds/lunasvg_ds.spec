%global commit 9af1ac7b90658a279b372add52d6f77a4ebb482c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240825

%global dist .%{date}git%{shortcommit}%{?dist}

%global pkgname lunasvg


Name:           %{pkgname}_ds
Version:        2.4.1
Release:        2%{?dist}
Summary:        Standalone SVG rendering library in C++

License:        MIT AND FTL
URL:            https://github.com/stenzek/%{pkgname}

Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz

Patch0:         0001-Rename-to-patched.patch

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  stb_image_write-devel

# Vendored copy under 3rdparty/plutovg
# License: FTL
Provides:       bundled(plutovg)

%description
LunaSVG is a standalone SVG rendering library in C++.

This build is patched for some emulators.

%package        devel
Summary:        Development headers and libraries for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
This package contains development headers and libraries for %{name}.

%prep
%autosetup -n %{pkgname}-%{commit} -p1

# Replace bundled libraries with the system ones
ln -sf %{_includedir}/stb/stb_image_write.h 3rdparty/stb/

%build
%cmake \
  -G Ninja \
  -DLUNASVG_BUILD_EXAMPLES:BOOL=OFF \
%{nil}

%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE 3rdparty/plutovg/FTL.TXT
%doc README.md
%{_libdir}/lib%{name}.so.2{,.*}

%files devel
%{_includedir}/%{name}_c.h
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/%{name}


%changelog
* Mon Sep 16 2024 Phantom X <megaphantomx at hotmail dot com> - 2.4.1-2.20240825git9af1ac7
- Rename to lunasvg_ds

* Wed Aug 28 2024 Phantom X <megaphantomx at hotmail dot com> - 2.4.1-1.20240825git9af1ac7
- Initial spec

