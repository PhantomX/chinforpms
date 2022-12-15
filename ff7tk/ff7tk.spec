%undefine _package_note_file

%global commit f9fba5e4915518fb1747d924b2efe0d891a6bb5a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220911
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           ff7tk
Version:        0.83.0.0
Release:        1%{?gver}%{?dist}
Summary:        A toolkit for making programs that edit final fantasy 7

License:        LGPL-3.0-or-later
URL:            https://github.com/sithlord48/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

Patch10:        0001-cmake-do-not-install-dbg-files.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Linguist)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Xml)
BuildRequires:  qt6-linguist
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(zlib)

Provides:       %{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}

%description
%{name} is a toolkit for making programs that edit final fantasy 7.


%package devel
Summary:        %{summary} development files
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains the development files needed for 
development with %{name} library.


%prep
%autosetup -n %{name}-%{commit} -p1

rm -rf .git

sed \
  -e 's|FIND_PACKAGE(Git)|FIND_PACKAGE(Git_disabled)|g' \
  -e 's|share/pkgconfig|${CMAKE_INSTALL_LIBDIR}/pkgconfig|g' \
  -e '/share\/licenses/d' \
  -i CMakeLists.txt

sed -e 's|Qt6LinguistTools|Qt6 COMPONENTS LinguistTools|' -i translations/CMakeLists.txt


%build
%cmake \
  -DQt6_LRELEASE_EXECUTABLE=lrelease-qt6 \
  -DTESTS:BOOL=OFF \
  -DCMAKE_SKIP_RPATH:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
%{nil}

%cmake_build


%install
%cmake_install

%find_lang %{name} --with-qt


%files -f %{name}.lang
%license COPYING.TXT
%doc README.md
%{_libdir}/*.so.*

%files devel
%license COPYING.TXT
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 0.83.0.0-1.20220911gitf9fba5e
- 0.83.0.0

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 0.82.0.0-1.20220323git94bfe2a
- 0.82.0.0
- Qt6

* Thu Sep 30 2021 Phantom X <megaphantomx at hotmail dot com> - 0.80.21-1.20210928git8fbdd9e
- 0.8.21

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.80.20-2.20210415git28cdfcb
- Bump

* Sat Dec 26 2020 Phantom X <megaphantomx at hotmail dot com> - 0.80.20-1.20201223git5b9f83f
- Initial spec
