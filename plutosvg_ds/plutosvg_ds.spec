%global commit bc845bb6b6511e392f9e1097b26f70cf0b3c33be
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250412

%global dist .%{date}git%{shortcommit}%{?dist}

%global pkgname plutosvg


Name:           %{pkgname}_ds
Version:        0.0.6
Release:        1%{?dist}
Summary:        Tiny SVG rendering library in C

License:        MIT AND FTL
URL:            https://github.com/stenzek/%{pkgname}

Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz

Patch0:         0001-Rename-to-_ds.patch

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  pkgconfig(freetype2)

# Vendored copy under 3rdparty/plutovg
# License: FTL
Provides:       bundled(plutovg)

%description
PlutoSVG is a compact and efficient SVG rendering library written in C.

This build is patched for some emulators.

%package        devel
Summary:        Development headers and libraries for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
This package contains development headers and libraries for %{name}.

%prep
%autosetup -n %{pkgname}-%{commit} -p1

cp plutovg/LICENSE LICENSE.plutovg


%build
%cmake \
  -G Ninja \
  -DPLUTOSVG_ENABLE_FREETYPE:BOOL=ON \
  -DPLUTOSVG_BUILD_EXAMPLES:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install


%check
%ctest


%files
%license LICENSE LICENSE.plutovg
%doc README.md
%{_libdir}/lib%{name}.so.0{,.*}

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/%{name}


%changelog
* Fri Apr 18 2025 Phantom X <megaphantomx at hotmail dot com> - 0.0.6-1.20250412gitbc845bb
- Initial spec
