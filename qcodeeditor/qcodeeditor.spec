%global commit dc644d41b68978ab9a5591ba891a223221570e74
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200205

%global gver .%{date}git%{shortcommit}

%global pkgname QCodeEditor

Name:           qcodeeditor
Version:        0
Release:        2%{?gver}%{?dist}
Summary:        Qt Code Editor Widget

License:        MIT
URL:            https://github.com/Megaxela/%{pkgname}

Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz

Patch0:         0001-cmake-library-fixes.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
Provides:       %{pkgname}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
%{pkgname} is a widget for editing/viewing code.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{pkgname}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{pkgname}-%{commit} -p1

sed -e '/-ansi/d' -i CMakeLists.txt

%build
%cmake
%cmake_build


%install
%cmake_install

%files
%license LICENSE.MIT
%doc README.md
%{_libdir}/*.so.*


%files devel
%{_includedir}/%{pkgname}
%{_libdir}/*.so


%changelog
* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 0-2.20200205gitdc644d4
- Remove ansi from cmake compiler flags

* Mon Dec 13 2021 Phantom X <megaphantomx at hotmail dot com> - 0-1.20200205gitdc644d4
- Initial spec
