%global pkgname Qt-Advanced-Docking-System

Name:           libqtadvanceddocking
Version:        3.8.1
Release:        1%{?dist}
Summary:        Advanced Docking System for Qt

License:        LGPLv2.1
URL:            https://github.com/githubuser0xFFFF/%{pkgname}

Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz

Patch0:         %{url}/commit/535b9260958a16858bd30f5b7e0a66e4efedaad8.patch#/%{name}-gh-535b926.patch
Patch10:        0001-cmake-library-fixes.patch


BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  qt5-qtbase-private-devel


%description
Qt Advanced Docking System lets you create customizable layouts using a
full featured window docking system similar to what is found in many
popular integrated development environments (IDEs) such as Visual Studio.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{pkgname}-%{version} -p1


%build
%cmake \
  -DADS_VERSION=%{version} \
  -DBUILD_EXAMPLES:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install


%files
%license LICENSE gnu-lgpl-v2.1.md
%doc README.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/qtadvanceddocking
%{_libdir}/cmake/qtadvanceddocking
%{_libdir}/*.so


%changelog
* Mon Dec 13 2021 Phantom X <megaphantomx at hotmail dot com> - 3.8.1-1
- Initial spec
