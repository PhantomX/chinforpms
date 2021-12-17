%bcond_with static

%if %{with static}
%global debug_package %{nil}
%endif

# Enable system vpx
%global with_sysvpx 1

%global commit0 429a6869e4a164e0aad2d8657db341d56f9a6a6f
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20211212

%global commit1 ad890067f661dc747a975bc55ba3767fe30d4452
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 libyuv

%if 0%{?with_sysvpx}
%global vpxver 1.10.0
%else
%global commit2 5b63f0f821e94f8072eb483014cfc33b05978bb9
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 libvpx
%global bundlevpx 1.9.0
%endif

%global libsrtp_ver 94ac00d
%global pffft_ver 483453d
%global openh264_ver 6f26bce

%global cvc_url https://chromium.googlesource.com

%global gver .%{date}git%{shortcommit0}

Name:           tg_owt
Version:        0
Release:        110%{?gver}%{?dist}
Summary:        WebRTC library for the Telegram messenger

# Main project - BSD
# abseil-cpp - ASL 2.0
# libsrtp - BSD
# libwebm - BSD
# libyuv - BSD
# openh264 - BSD
# pffft - BSD
# rnnoise - BSD
License:        BSD and ASL 2.0
URL:            https://github.com/desktop-app/%{name}

Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Source1:        %{cvc_url}/libyuv/libyuv/+archive/%{shortcommit1}.tar.gz#/%{srcname1}-%{shortcommit1}.tar.gz
%if !0%{?with_sysvpx}
Source2:        %{cvc_url}/webm/libvpx/+archive/%{shortcommit2}.tar.gz#/%{srcname2}-%{shortcommit2}.tar.gz
%endif

# From Gentoo
Patch0:         tg_owt-0_pre20211207-fix-dcsctp-references.patch


BuildRequires:  cmake(absl)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavresample)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libswscale)
#BuildRequires:  pkgconfig(openh264)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(usrsctp)
%if 0%{?with_sysvpx}
BuildRequires:  pkgconfig(vpx) >= %{vpxver}
%else
Provides:       bundled(libvpx) = %{bundlevpx}~git%{shortcommit2}
%endif
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xtst)

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  yasm

Provides:       bundled(base64) = 0~git
Provides:       bundled(dcsctp) = 0~git
Provides:       bundled(fft) = 0~git
Provides:       bundled(fft4g) = 0~git
Provides:       bundled(g711) = 0~git
Provides:       bundled(g722) = 0~git
Provides:       bundled(libsrtp) = 2.2.0~git%{libsrtp_ver}
Provides:       bundled(pffft) = 0~git%{pffft_ver}
Provides:       bundled(portaudio) = 0~git
Provides:       bundled(libwebm) = 0~git
Provides:       bundled(libyuv) = 0~git%{shortcommit1}
Provides:       bundled(openh264) = 1.10.0~git%{openh264_ver}
Provides:       bundled(sigslot) = 0~git
Provides:       bundled(spl_sqrt_floor) = 0~git


%description
Special fork of the OpenWebRTC library for the Telegram messenger.

%package devel
Summary:        Development files for %{name}
%if %{with static}
Requires:       cmake(absl)
Requires:       pkgconfig(alsa)
Requires:       pkgconfig(gio-2.0)
Requires:       pkgconfig(glib-2.0)
Requires:       pkgconfig(gobject-2.0)
Requires:       pkgconfig(gio-unix-2.0)
Requires:       pkgconfig(libavcodec)
Requires:       pkgconfig(libavformat)
Requires:       pkgconfig(libavresample)
Requires:       pkgconfig(libavutil)
Requires:       pkgconfig(libjpeg)
Requires:       pkgconfig(libpipewire-0.3)
Requires:       pkgconfig(libpulse)
Requires:       pkgconfig(libswscale)
#Requires:       pkgconfig(openh264)
Requires:       pkgconfig(openssl)
Requires:       pkgconfig(opus)
Requires:       pkgconfig(usrsctp)
Requires:       pkgconfig(vpx) >= 1.10.0
%if 0%{?with_sysvpx}
Requires:       pkgconfig(vpx) >= %{vpxver}
%else
Provides:       bundled(libvpx) = %{bundlevpx}~git%{shortcommit2}
%endif
Requires:       pkgconfig(x11)
Requires:       pkgconfig(xcomposite)
Requires:       pkgconfig(xdamage)
Requires:       pkgconfig(xext)
Requires:       pkgconfig(xfixes)
Requires:       pkgconfig(xrender)
Requires:       pkgconfig(xrandr)
Requires:       pkgconfig(xtst)
Provides:       %{name}-static%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       bundled(rnnoise) = 0~git91ef40
Provides:       bundled(base64) = 0~git
Provides:       bundled(dcsctp) = 0~git
Provides:       bundled(fft) = 0~git
Provides:       bundled(fft4g) = 0~git
Provides:       bundled(g711) = 0~git
Provides:       bundled(g722) = 0~git
Provides:       bundled(libsrtp) = 2.2.0~git%{libsrtp_ver}
Provides:       bundled(pffft) = 0~git%{pffft_ver}
Provides:       bundled(portaudio) = 0~git
Provides:       bundled(libwebm) = 0~git
Provides:       bundled(libyuv) = 0~git%{shortcommit1}
Provides:       bundled(openh264) = 1.10.0~git%{openh264_ver}
Provides:       bundled(sigslot) = 0~git
Provides:       bundled(spl_sqrt_floor) = 0~git
Provides:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name} < %{?epoch:%{epoch}:}%{version}-%{release}
%else
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%endif

%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{commit0} -p1

tar -xf %{S:1} -C src/third_party/libyuv
%if 0%{?with_sysvpx}
  sed '/include(cmake\/libvpx.cmake)/d' -i CMakeLists.txt
%else
tar -xf %{S:2} -C src/third_party/libvpx/source/libvpx
%endif

mkdir legal
%if %{with static}
cp -f -p src/third_party/abseil-cpp/LICENSE legal/LICENSE.abseil-cpp
cp -f -p src/third_party/abseil-cpp/README.chromium legal/README.abseil-cpp
cp -f -p src/third_party/rnnoise/COPYING legal/LICENSE.rnnoise
cp -f -p src/third_party/rnnoise/README.chromium legal/README.rnnoise
%endif
cp -f -p src/third_party/libsrtp/LICENSE legal/LICENSE.libsrtp
cp -f -p src/third_party/libsrtp/README.chromium legal/README.libsrtp
cp -f -p src/third_party/pffft/LICENSE legal/LICENSE.pffft
cp -f -p src/third_party/pffft/README.chromium legal/README.pffft
%if !0%{?with_sysvpx}
cp -f -p src/third_party/libvpx/source/libvpx/LICENSE legal/LICENSE.libvpx
cp -f -p src/third_party/libvpx/source/libvpx/PATENTS legal/PATENTS.libvpx
cp -f -p src/third_party/libvpx/README.chromium legal/README.libvpx
cp -f -p src/third_party/libvpx/source/libvpx/third_party/libwebm/LICENSE.TXT legal/LICENSE.libwebm
cp -f -p src/third_party/libvpx/source/libvpx/third_party/libwebm/PATENTS.TXT legal/PATENTS.libwebm
cp -f -p src/third_party/libvpx/source/libvpx/third_party/libwebm/README.libvpx legal/README.libwebm
%endif
cp -f -p src/third_party/libyuv/LICENSE legal/LICENSE.libyuv
cp -f -p src/third_party/libyuv/PATENTS legal/PATENTS.libyuv
cp -f -p src/third_party/libyuv/README.chromium legal/README.libyuv
cp -f -p src/third_party/openh264/src/LICENSE legal/LICENSE.openh264
cp -f -p src/third_party/openh264/README.chromium legal/README.openh264
cp -f -p src/rtc_base/third_party/base64/LICENSE legal/LICENSE.base64
cp -f -p src/rtc_base/third_party/base64/README.chromium legal/README.base64
cp -f -p src/rtc_base/third_party/sigslot/LICENSE legal/LICENSE.sigslot
cp -f -p src/rtc_base/third_party/sigslot/README.chromium legal/README.sigslot
cp -f -p src/common_audio/third_party/spl_sqrt_floor/LICENSE legal/LICENSE.spl_sqrt_floor
cp -f -p src/common_audio/third_party/spl_sqrt_floor/README.chromium legal/README.spl_sqrt_floor
cp -f -p src/modules/third_party/fft/LICENSE legal/LICENSE.fft
cp -f -p src/modules/third_party/fft/README.chromium legal/README.fft
cp -f -p src/modules/third_party/g711/LICENSE legal/LICENSE.g711
cp -f -p src/modules/third_party/g711/README.chromium legal/README.g711
cp -f -p src/modules/third_party/g722/LICENSE legal/LICENSE.g722
cp -f -p src/modules/third_party/g722/README.chromium legal/README.g722
cp -f -p src/modules/third_party/portaudio/LICENSE legal/LICENSE.portaudio
cp -f -p src/modules/third_party/portaudio/README.chromium legal/README.portaudio


%build
# CMAKE_BUILD_TYPE should always be Release due to some hardcoded checks.
%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON \
%if %{with static}
  -DBUILD_SHARED_LIBS:BOOL=OFF \
%endif
  -DTG_OWT_USE_PROTOBUF:BOOL=ON \
  -DTG_OWT_BUILD_AUDIO_BACKENDS:BOOL=OFF \
  -DTG_OWT_PACKAGED_BUILD:BOOL=ON \
%{nil}

%cmake_build

%install
%cmake_install

mkdir _tmpheaders
mv %{buildroot}%{_includedir}/%{name}/rtc_base/third_party/{base64,sigslot} _tmpheaders/
mv %{buildroot}%{_includedir}/%{name}/third_party/libyuv/include _tmpheaders/libyuv_include

rm -rf %{buildroot}%{_includedir}/%{name}/rtc_base/third_party/*
rm -rf %{buildroot}%{_includedir}/%{name}/common_audio/third_party
rm -rf %{buildroot}%{_includedir}/%{name}/modules/third_party
rm -rf %{buildroot}%{_includedir}/%{name}/third_party

mv _tmpheaders/{base64,sigslot} %{buildroot}%{_includedir}/%{name}/rtc_base/third_party/
mkdir -p %{buildroot}%{_includedir}/%{name}/third_party/libyuv/include
mv _tmpheaders/libyuv_include/* %{buildroot}%{_includedir}/%{name}/third_party/libyuv/include/

%if %{without static}
%files
%doc src/AUTHORS src/OWNERS legal/README.*
%license LICENSE src/PATENTS legal/LICENSE.* legal/PATENTS.*
%{_libdir}/lib%{name}.so.*
%endif


%files devel
%if %{with static}
%doc src/AUTHORS src/OWNERS legal/README.*
%endif
%license LICENSE src/PATENTS legal/LICENSE.* legal/PATENTS.*
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%if %{with static}
%{_libdir}/lib%{name}.a
%else
%{_libdir}/lib%{name}.so
%endif


%changelog
* Thu Dec 16 2021 Phantom X <megaphantomx at hotmail dot com> - 0-110.20211212git429a686
- Bump
- Some fixes from Gentoo, like system libvpx and headers cleanup

* Thu Dec 09 2021 Phantom X <megaphantomx at hotmail dot com> - 0-109.20211207gitd5c3d43
- Update

* Mon Nov 29 2021 Phantom X <megaphantomx at hotmail dot com> - 0-108.20211112gitb024786
- Bump
- Shared library conditional

* Sun Oct 31 2021 Phantom X <megaphantomx at hotmail dot com> - 0-107.20211021gitd578c76
- Update

* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 0-106.20210915git575fb17
- Last snapshot

* Tue Jul 06 2021 Phantom X <megaphantomx at hotmail dot com> - 0-105.20210627git91d836d
- Bump

* Sat Jun 26 2021 Phantom X <megaphantomx at hotmail dot com> - 0-104.20210617gitf03ef05
- Static lib only

* Tue Jan 26 2021 Phantom X <megaphantomx at hotmail dot com> - 0-103.20210124gitbe23804
- Update to latest snapshot

* Mon Jan 11 2021 Phantom X <megaphantomx at hotmail dot com> - 0-102.20210105gitd91d618
- Update to latest snapshot

* Wed Dec 16 2020 Phantom X <megaphantomx at hotmail dot com> - 0-101.20201215gitd93d10b
- Update to latest snapshot

* Tue Nov 03 2020 Phantom X <megaphantomx at hotmail dot com> - 0-100.20201102gite8fcae7
- Fix raw_logging missing symbols

* Mon Nov 02 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 0-2.20201102gite8fcae7
- Initial SPEC release.
