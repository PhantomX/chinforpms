%global commit 5b9f83fa9579fe41f5216884a8c9f10bddb351c4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20201223
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           ff7tk
Version:        0.80.20
Release:        1%{?gver}%{?dist}
Summary:        A toolkit for making programs that edit final fantasy 7

License:        LGPLv3+
URL:            https://github.com/sithlord48/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Quick)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5Xml)
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

sed \
  -e '/GenerateExportHeader/aadd_definitions(-DGIT_VERSION="%{shortcommit}")' \
  -e 's|FIND_PACKAGE(Git)|FIND_PACKAGE(Git_disabled)|g' \
  -e 's|share/pkgconfig|${CMAKE_INSTALL_LIBDIR}/pkgconfig|g' \
  -i CMakeLists.txt

%build
%cmake \
  -DQt5_LRELEASE_EXECUTABLE=lrelease-qt5 \
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
* Sat Dec 26 2020 Phantom X <megaphantomx at hotmail dot com> - 0.80.20-1.20201223git5b9f83f
- Initial spec
