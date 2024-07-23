%global commit 4bcbf5ff51e6fc0d2125e93ceb455f1411461aad
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230627
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           qt-jpegxl-image-plugin
Version:        0.6.3
Release:        1%{?dist}
Summary:        Qt plug-in to allow Qt and KDE based applications to read/write JXL images

License:        GPL-3.0-only
URL:            https://github.com/novomesk/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif


BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libjxl) >= 0.8
BuildRequires:  pkgconfig(libjxl_threads)


%description
Qt plug-in to allow Qt and KDE based applications to read/write JXL images.


%package -n qt5-jpegxl-image-plugin
Summary:        JXL Qt5 plugin
BuildRequires:  cmake(Qt5Gui)

%description -n qt5-jpegxl-image-plugin
Qt5 plug-in to allow Qt and KDE based applications to read/write JXL images.


%package -n qt6-jpegxl-image-plugin
Summary:        JXL Qt6 plugin
BuildRequires:  cmake(Qt6Gui)

%description -n qt6-jpegxl-image-plugin
Qt6 plug-in to allow Qt and KDE based applications to read/write JXL images.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1


%build
%cmake \
  -DQT_MAJOR_VERSION:STRING=5 \
  -DKDE_INSTALL_QTPLUGINDIR:PATH=%{_qt5_plugindir} \
%{nil}

mkdir qt6build
pushd qt6build
%define _vpath_srcdir ..
%{cmake} \
  -DQT_MAJOR_VERSION:STRING=6 \
  -DKDE_INSTALL_QTPLUGINDIR:PATH=%{_qt6_plugindir} \
%{nil}

popd

%cmake_build

pushd qt6build
%cmake_build
popd

%install
%cmake_install

pushd qt6build
%cmake_install
popd


%files -n qt5-jpegxl-image-plugin
%license LICENSE
%doc README.md
%{_qt5_plugindir}/imageformats/libqjpegxl5.so


%files -n qt6-jpegxl-image-plugin
%license LICENSE
%doc README.md
%{_qt6_plugindir}/imageformats/libqjpegxl6.so


%changelog
* Mon Jul 08 2024 Phantom X <megaphantomx at hotmail dot com> - 0.6.3-1
- 0.6.3

* Sat Jan 06 2024 Phantom X <megaphantomx at hotmail dot com> - 0.5.0-1
- 0.5.0

* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 0-2.20220910git26af559
- Bump

* Mon Apr 25 2022 Phantom X <megaphantomx at hotmail dot com> - 0-1.20220414git0c99516
- Initial spec
