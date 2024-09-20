Name:           qt-heic-image-plugin
Version:        0.4.2
Release:        1%{?dist}
Summary:        Qt plugin for HEIF/HEIC images

License:        LGPL-2.1-only
URL:            https://github.com/novomesk/qt-heic-image-plugin

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz


BuildRequires:  cmake
BuildRequires:  extra-cmake-modules >= 5.89.0
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libheif) >= 1.10.0


%description
Qt plug-in to allow Qt and KDE based applications to read/write HEIF/HEIC
images.


%package -n qt5-heic-image-plugin
Summary:        HEIF/HEIC Qt5 plugin
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  kf5-rpm-macros

%description -n qt5-heic-image-plugin
Qt5 plug-in to allow Qt and KDE based applications to read/write HEIF/HEIC
images.


%package -n qt6-heic-image-plugin
Summary:        HEIF/HEIC Qt6 plugin
BuildRequires:  cmake(Qt6Gui)

%description -n qt6-heic-image-plugin
Qt6 plug-in to allow Qt and KDE based applications to read/write HEIF/HEIC
images.


%prep
%autosetup -p1


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


%files -n qt5-heic-image-plugin
%license LICENSE
%doc README.md
%{_qt5_plugindir}/imageformats/kimg_heif5.so
%{_kf5_datadir}/kservices5/qimageioplugins/heif.desktop


%files -n qt6-heic-image-plugin
%license LICENSE
%doc README.md
%{_qt6_plugindir}/imageformats/kimg_heif6.so


%changelog
* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 0.4.2-1
- 0.4.2

* Mon Jul 08 2024 Phantom X <megaphantomx at hotmail dot com> - 0.4.1-1
- 0.4.1

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 0.4.0-1
- 0.4.0

* Sat Jan 06 2024 Phantom X <megaphantomx at hotmail dot com> - 0.3.1-1
- Initial spec
