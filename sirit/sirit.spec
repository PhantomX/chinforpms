Name:           sirit
Version:        1.0.2
Release:        1%{?dist}
Summary:        A runtime SPIR-V assembler

License:        AGPL-3.0-or-later OR GPL-3.0-or-later
URL:            https://github.com/eden-emulator/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0:         0001-cmake-add-soversion.patch

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  spirv-headers-devel


%description
Sirit is a runtime SPIR-V assembler.


%package devel
Summary:        %{summary} development files
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains the development files needed for 
development with %{name} library.


%prep
%autosetup -p1

sed -e 's|_RPM_VERSION_|%{version}|' -i CMakeLists.txt


%build
%cmake \
  -G Ninja \
  -DSIRIT_USE_SYSTEM_SPIRV_HEADERS:BOOL=ON \
  -DSIRIT_BUILD_SHARED:BOOL=ON \
  -DSIRIT_BUILD_STATIC:BOOL=OFF \
  -DSIRIT_TESTS:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install


%files
%license LICENSE*
%doc README.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/*.so


%changelog
* Wed Oct 08 2025 Phantom X <megaphantomx at hotmail dot com> - 1.0.2-1
- Initial spec
