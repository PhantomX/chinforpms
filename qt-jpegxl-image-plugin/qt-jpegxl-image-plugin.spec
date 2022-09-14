%global commit 26af559645c86ffc7629c10637834cbd293c9d3f
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220910
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           qt-jpegxl-image-plugin
Version:        0
Release:        2%{?gver}%{?dist}
Summary:        Qt plug-in to allow Qt and KDE based applications to read/write JXL images

License:        GPLv3
URL:            https://github.com/novomesk/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif


BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libjxl)
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
%autosetup %{?gver:-n %{name}-%{commit}} -p1


%build
%cmake \
  -DQT_MAJOR_VERSION:STRING=5 \
  -DKDE_INSTALL_QTPLUGINDIR:PATH=%{_qt5_plugindir} \
%{nil}

mkdir qt6build
pushd qt6build
%{cmake} -S .. \
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
* Tue Sep 13 2022 Phantom X <megaphantomx at hotmail dot com> - 0-2.20220910git26af559
- Bump

* Mon Apr 25 2022 Phantom X <megaphantomx at hotmail dot com> - 0-1.20220414git0c99516
- Initial spec
