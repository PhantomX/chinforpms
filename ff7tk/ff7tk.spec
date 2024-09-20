%undefine _package_note_file

%global commit 562bc35098a2702836920b47a16ca847d45e0223
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240908
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           ff7tk
Version:        1.2.0.0
Release:        1%{?dist}
Summary:        A toolkit for making programs that edit final fantasy 7

License:        LGPL-3.0-or-later
URL:            https://github.com/sithlord48/%{name}

Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

Patch10:        0001-cmake-do-not-install-dbg-files.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
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
  -e '/\/licenses\//d' \
  -i CMakeLists.txt

sed -e 's|Qt6LinguistTools|Qt6 COMPONENTS LinguistTools|' -i translations/CMakeLists.txt


%build
%cmake \
  -G Ninja \
  -DQt6_LRELEASE_EXECUTABLE=lrelease-qt6 \
  -DTESTS:BOOL=OFF \
  -DCMAKE_SKIP_RPATH:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
%{nil}

%cmake_build


%install
%cmake_install

mv %{buildroot}%{_datadir}/%{name}/sbom-%{name}-*.spdx .
rmdir -p %{buildroot}%{_datadir}/%{name} || :

%find_lang %{name} --with-qt


%files -f %{name}.lang
%license COPYING.TXT sbom-%{name}-*.spdx
%doc README.md
%{_libdir}/*.so.*

%files devel
%license COPYING.TXT sbom-%{name}-*.spdx
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/*.so


%changelog
* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1.2.0.0-1.20240908git562bc35
- 1.2.0.0

* Tue Mar 26 2024 Phantom X <megaphantomx at hotmail dot com> - 1.0.0.0-1.20240310git9006e58
- 1.0.0.0

* Fri Sep 15 2023 Phantom X <megaphantomx at hotmail dot com> - 0.83.3.0-1.20230908gitf63b4db
- 0.83.3.0

* Wed Mar 15 2023 Phantom X <megaphantomx at hotmail dot com> - 0.83.2.0-1.20230314git9bb3310
- 0.83.2.0

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
