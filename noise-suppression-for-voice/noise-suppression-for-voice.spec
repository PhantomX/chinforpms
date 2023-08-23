%undefine _cmake_shared_libs

%bcond_without lv2
%bcond_with tests

Name:           noise-suppression-for-voice
Version:        1.03
Release:        1%{?dist}
Summary:        A real-time noise suppression plugin for voice

License:        GPL-3.0 AND BSD-3-Clause
URL:            https://github.com/werman/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0:         %{url}/commit/226f03bbc317e11b0eb2c22d55e17898d79ed0c0.patch#/%{name}-gh-226f03b.patch
Patch1:         %{url}/commit/c1cf4307c75abed8e3ecccdd23a35f7782feaf69.patch#/%{name}-gh-c1cf430.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  libatomic


%description
%{name} a real-time noise suppression plugin for voice based on Xiph's RNNoise.

%package -n     ladspa-%{name}-plugin
Summary:        %{name} LADSPA plugin
BuildRequires:  ladspa-devel
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       ladspa%{?_isa}
Provides:       bundled(rnnoise) = 0~git

%description -n ladspa-%{name}-plugin
%{summary}

This packages provides the LADSPA plugin.


%if %{with lv2}
%package -n     lv2-%{name}-plugin
Summary:        %{name} LADSPA plugin
License:        GPL-3.0 AND BSD-3-Clause AND ISC
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       lv2%{?_isa}
Provides:       bundled(juce) = 7.0.1
Provides:       bundled(rnnoise) = 0~git

%description -n lv2-%{name}-plugin
%{summary}

This packages provides the LV2 plugin.
%endif


%prep
%autosetup -p1

cp -p src/rnnoise/COPYING.txt COPYING.rnnoise.txt
cp -p external/JUCE/LICENSE.md LICENSE.JUCE.md

# use the system version of ladspa.h
rm -f ladspa.h


%build
%cmake \
  -G Ninja \
  %{!?with_tests:-DBUILD_TESTS:BOOL=OFF} \
  -DBUILD_LADSPA_PLUGIN:BOOL=ON \
  %{!?with_lv2:-DBUILD_LV2_PLUGIN:BOOL=OFF} \
  -DBUILD_VST_PLUGIN:BOOL=OFF \
  -DBUILD_VST3_PLUGIN:BOOL=OFF \
  -DBUILD_AU_PLUGIN:BOOL=OFF \
  -DBUILD_AUV3_PLUGIN:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install


%files -n ladspa-%{name}-plugin
%license LICENSE COPYING.rnnoise.txt
%doc README.md
%{_libdir}/ladspa/*.so


%if %{with lv2}
%files -n lv2-%{name}-plugin
%license LICENSE LICENSE.JUCE.md COPYING.rnnoise.txt
%doc README.md
%{_libdir}/lv2/rnnoise_mono.lv2/*.so
%{_libdir}/lv2/rnnoise_mono.lv2/*.ttl
%{_libdir}/lv2/rnnoise_stereo.lv2/*.so
%{_libdir}/lv2/rnnoise_stereo.lv2/*.ttl
%endif


%changelog
* Tue Aug 22 2023 Phantom X <megaphantomx at hotmail dot com> - 1.03-1
- Initial spec

