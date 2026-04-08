Name:           sdl3-testcontroller
Version:        3.4.4
Release:        1%{?dist}
Summary:        Official tool to create SDL3 Game Controller controller mappings

License:        Zlib AND MIT
URL:            http://www.libsdl.org

Source0:        %{url}/release/SDL3-%{version}.tar.gz
Source1:        %{name}-CMakeLists.txt

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  python3
BuildRequires:  cmake(SDL3) >= %{version}
BuildRequires:  SDL3-test >= %{version}
Requires:       SDL3%{_isa} >= %{version}


%description
%{name} is the official tool to create SDL3 Game Controller controller mappings.


%prep
%autosetup -n SDL3-%{version} -p1

cp -p -f %{S:1} test/CMakeLists.txt


%build
%cmake -S test
%cmake_build

%install
%cmake_install


%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}


%changelog
* Wed Apr 08 2026 Phantom X <megaphantomx at hotmail dot com> - 3.4.4-1
- 3.4.4

* Fri Mar 27 2026 Phantom X <megaphantomx at hotmail dot com> - 3.4.2-1
- Initial spec

