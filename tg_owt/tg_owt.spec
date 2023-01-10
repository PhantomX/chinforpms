# shared/static conditional, good luck with unsupported shared one
%bcond_with static
# Use bundled abseil-cpp
%bcond_without absl

%if %{with static}
%global debug_package %{nil}
%endif

%global commit0 5098730b9eb6173f0b52068fe2555b7c1015123a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20230105

%global commit1 00950840d1c9bcbb3eb6ebc5aac5793e71166c8b
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 libyuv

%global commit3 8c0b94e793a66495e0b1f34a5eb26bd7dc672db0
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 abseil-cpp

%global absl_ver 39f46fa
%global libsrtp_ver 94ac00d
%global pffft_ver 483453d
%global openh264_ver 6f26bce

%global cvc_url https://chromium.googlesource.com

%global gver .%{date}git%{shortcommit0}

Name:           tg_owt
Version:        0
Release:        126%{?gver}%{?dist}
Summary:        WebRTC library for the Telegram messenger

# Main project - BSD
# abseil-cpp - Apache-2.0
# libsrtp - BSD-3-Clause
# libyuv - BSD-3-Clause
# openh264 - BSD-2-Clause
# pffft - BSD-3-Clause
# rnnoise - BSD-3-Clause
License:        BSD-3-Clause AND BSD-2-Clause%{!?with_absl: AND Apache-2.0}
URL:            https://github.com/desktop-app/%{name}

ExclusiveArch:  x86_64 aarch64

Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Source1:        %{cvc_url}/libyuv/libyuv/+archive/%{shortcommit1}.tar.gz#/%{srcname1}-%{shortcommit1}.tar.gz
%if !%{with absl}
Source3:        https://github.com/abseil/%{srcname3}/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
%endif

Patch1000:      0001-fix-build-with-bundled-absl.patch

%if %{with absl}
BuildRequires:  cmake(absl) >= 20220623
%endif
BuildRequires:  pkgconfig(alsa)
BuildRequires:  cmake(Crc32c)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libpulse)
#BuildRequires:  pkgconfig(openh264)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(vpx) >= 1.10.0
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

# Fedora now has a stripped ffmpeg. Make sure we're using the full version.
# Telegram Desktop has major issues when built against ffmpeg 5.x:
# https://bugzilla.rpmfusion.org/show_bug.cgi?id=6273
# Upstream refuses to fix this issue:
# https://github.com/telegramdesktop/tdesktop/issues/24855
# https://github.com/telegramdesktop/tdesktop/issues/23899
%if 0%{?fedora} && 0%{?fedora} >= 36
BuildRequires:  compat-ffmpeg4-devel
%else
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(libswscale)
%endif
%if 0%{?fedora} && 0%{?fedora} >= 36
BuildRequires:  openssl1.1-devel
%else
BuildRequires:  pkgconfig(openssl)
%endif

# dlopen
Requires:       libdrm%{?_isa}
Requires:       mesa-libgbm%{?_isa}
Requires:       mesa-libEGL%{?_isa}
Requires:       mesa-libGL%{?_isa}
Requires:       pipewire-libs%{?_isa}

Provides:       bundled(base64) = 0~git
%if !%{with absl}
Provides:       bundled(abseil-cpp) = 0~git%{absl_ver}
%endif
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
Requires:       pkgconfig(alsa)
Requires:       cmake(Crc32c)
Requires:       pkgconfig(egl)
Requires:       pkgconfig(gl)
Requires:       pkgconfig(gbm)
Requires:       pkgconfig(gio-2.0)
Requires:       pkgconfig(glib-2.0)
Requires:       pkgconfig(gobject-2.0)
Requires:       pkgconfig(gio-unix-2.0)
Requires:       pkgconfig(libdrm)
Requires:       pkgconfig(libjpeg)
Requires:       pkgconfig(libpipewire-0.3)
Requires:       pkgconfig(libpulse)
#Requires:       pkgconfig(openh264)
Requires:       pkgconfig(opus)
Requires:       pkgconfig(usrsctp)
Requires:       pkgconfig(vpx) >= 1.10.0
Requires:       pkgconfig(x11)
Requires:       pkgconfig(xcomposite)
Requires:       pkgconfig(xdamage)
Requires:       pkgconfig(xext)
Requires:       pkgconfig(xfixes)
Requires:       pkgconfig(xrender)
Requires:       pkgconfig(xrandr)
Requires:       pkgconfig(xtst)
%if 0%{?fedora} && 0%{?fedora} >= 36
Requires:       compat-ffmpeg4-devel
%else
Requires:       pkgconfig(libavcodec)
Requires:       pkgconfig(libavformat)
Requires:       pkgconfig(libavutil)
Requires:       pkgconfig(libswresample)
Requires:       pkgconfig(libswscale)
%endif
%if 0%{?fedora} && 0%{?fedora} >= 36
Requires:       openssl1.1-devel
%else
BuildRequires:  pkgconfig(openssl)
%endif
Provides:       %{name}-static%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%if !%{with absl}
Provides:       bundled(abseil-cpp) = 0~git%{absl_ver}
%endif
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
%if %{with absl}
Requires:       cmake(absl)
%endif
Requires:       cmake(Crc32c)


%description devel
%{summary}.

%prep
%autosetup -N -n %{name}-%{commit0} -p1
%autopatch -p1 -M 999

tar -xf %{S:1} -C src/third_party/libyuv

rm -rf src/third_party/crc32c
sed -e '/libcrc32c.cmake/d' -i CMakeLists.txt

mkdir legal
%if %{with static}
cp -f -p src/third_party/rnnoise/COPYING legal/LICENSE.rnnoise
cp -f -p src/third_party/rnnoise/README.chromium legal/README.rnnoise
%endif
%if %{with absl}
sed -e '/libabsl.cmake/d' -i CMakeLists.txt
%else
%patch1000 -p1
tar -xf %{S:3} -C src/third_party/abseil-cpp --strip-components 1
cp -f -p src/third_party/abseil-cpp/LICENSE legal/LICENSE.abseil-cpp
cp -f -p src/third_party/abseil-cpp/README.chromium legal/README.abseil-cpp
%endif
cp -f -p src/third_party/libsrtp/LICENSE legal/LICENSE.libsrtp
cp -f -p src/third_party/libsrtp/README.chromium legal/README.libsrtp
cp -f -p src/third_party/pffft/LICENSE legal/LICENSE.pffft
cp -f -p src/third_party/pffft/README.chromium legal/README.pffft
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

sed \
  -e '/if (BUILD_SHARED_LIBS)/{n;n;s/WARNING/DEBUG/}' \
  -i CMakeLists.txt


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
  -DTG_OWT_DLOPEN_PIPEWIRE:BOOL=OFF \
  -DTG_OWT_PACKAGED_BUILD:BOOL=ON \
%{nil}

%cmake_build

%install
%cmake_install

mkdir _tmpheaders
mv %{buildroot}%{_includedir}/%{name}/rtc_base/third_party/{base64,sigslot} _tmpheaders/
mv %{buildroot}%{_includedir}/%{name}/third_party/libyuv/include _tmpheaders/libyuv_include
%if !%{with absl}
mv %{buildroot}%{_includedir}/%{name}/third_party/abseil-cpp/absl _tmpheaders/abseil-cpp_absl
%endif

rm -rf %{buildroot}%{_includedir}/%{name}/rtc_base/third_party/*
rm -rf %{buildroot}%{_includedir}/%{name}/common_audio/third_party
rm -rf %{buildroot}%{_includedir}/%{name}/modules/third_party
rm -rf %{buildroot}%{_includedir}/%{name}/third_party

mv _tmpheaders/{base64,sigslot} %{buildroot}%{_includedir}/%{name}/rtc_base/third_party/
mkdir -p %{buildroot}%{_includedir}/%{name}/third_party/libyuv/include
mv _tmpheaders/libyuv_include/* %{buildroot}%{_includedir}/%{name}/third_party/libyuv/include/
%if !%{with absl}
mkdir -p %{buildroot}%{_includedir}/%{name}/third_party/abseil-cpp/absl/
mv _tmpheaders/abseil-cpp_absl/* %{buildroot}%{_includedir}/%{name}/third_party/abseil-cpp/absl/
%endif

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
* Sat Dec 31 2022 Phantom X <megaphantomx at hotmail dot com> - 0-125.20221230git1eab2d7
- External crc32c

* Mon Sep 19 2022 Phantom X <megaphantomx at hotmail dot com> - 0-123.20220914git621f3da
- RPMFusion sync

* Sat Sep 17 2022 Phantom X <megaphantomx at hotmail dot com> - 0-122.20220914git621f3da
- Rebuild (abseil-cpp)

* Fri May 13 2022 Phantom X <megaphantomx at hotmail dot com> - 0-119.20220508git10d5f4b
- Last snapshot

* Wed May 04 2022 Phantom X <megaphantomx at hotmail dot com> - 0-118.20220504git442d5bb
- Bump

* Thu Apr 14 2022 Phantom X <megaphantomx at hotmail dot com> - 0-117.20220413git63a934d
- Update

* Wed Mar 30 2022 Phantom X <megaphantomx at hotmail dot com> - 0-116.20220314git1fe5e68
- Bump

* Tue Mar 01 2022 Phantom X <megaphantomx at hotmail dot com> - 0-115.20220225gita264028
- Bump

* Tue Feb 08 2022 Phantom X <megaphantomx at hotmail dot com> - 0-114.20220207gitdb7d469
- Bundled abseil-cpp optional support

* Sun Feb 06 2022 Phantom X <megaphantomx at hotmail dot com> - 0-113.20220206git347400d
- Update

* Tue Feb 01 2022 Phantom X <megaphantomx at hotmail dot com> - 0-112.20220130git1fd131d
- Update

* Thu Dec 23 2021 Phantom X <megaphantomx at hotmail dot com> - 0-111.20211223git6708e0d
- Bump

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
