%global commit 6a5450f91f7b2b6b1ad852957a111377d37b9023
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20260905
%bcond snapshot 0

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global appname gay.pancake.lsfg-vk-ui
%global vc_url https://git.lsfg-vk.dev/%{name}

Name:           lsfg-vk
Version:        2.0.0
Release:        1
Summary:        Lossless Scaling Frame Generation on Linux via DXVK/Vulkan.

License:        CC-BY-NC-ND-4.0
URL:            https://lsfg-vk.dev

%if %{with snapshot}
Source0:        %{vc_url}/snapshot/%{name}-%{commit}.tar.xz#/%{name}-%{shortcommit}.tar.xz
%else
Source0:        %{vc_url}/snapshot/%{name}-%{version}.tar.xz
%endif

Patch0:         0001-vk-layer-do-not-enable-automatically.patch

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Lossless Scaling Frame Generation on Linux.

%package libs
Summary:        The %{name} libraries
Requires:       vulkan-loader%{?_isa}
Recommends:     (%{name}-libs(x86-32) if glibc(x86-32))
%description libs
%{summary}.

This packages provides the Vulkan Layer.


%package ui
Summary:        C++/Qt-based GUI for modifying lsfg-vk configuration
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Quick)
%description ui
%{summary}.

This package provides the GUI for modifying configuration of lsfg-vk.


%prep
%autosetup -n %{name}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

%build
%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DLSFGVK_LAYER_MULTILIB_X86:BOOL=OFF \
  -DLSFGVK_BUILD_CLI:BOOL=ON \
  -DLSFGVK_BUILD_LAYER:BOOL=ON \
  -DLSFGVK_BUILD_UI:BOOL=ON \
  -DLSFGVK_MANAGED:BOOL=ON \
%{nil}

%cmake_build


%install
%cmake_install

desktop-file-edit \
  --set-key=StartupWMClass \
  --set-value="%{name}-ui" \
  %{buildroot}%{_datadir}/applications/%{appname}.desktop

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 dist/flatpak/%{name}-ui/%{appname}.metainfo.xml \
  %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appname}.desktop
appstream-util validate-relax --nonet \
  %{buildroot}%{_metainfodir}/%{appname}.metainfo.xml


%files
%license LICENSE.txt
%{_bindir}/%{name}-cli
%{_datadir}/vulkan/implicit_layer.d/VkLayer_LSFGVK_frame_generation.json

%files libs
%{_libdir}/liblsfg-vk-layer.so

%files ui
%{_bindir}/%{name}-ui
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{appname}.png
%{_metainfodir}/%{appname}.metainfo.xml


%changelog
* Mon Sep 07 2026 Phantom X <megaphantomx at hotmail dot com> - 2.0.0-1
- Initial spec

