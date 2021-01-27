%global commit0 be23804afce3bb2e80a1d57a7c1318c71b82b7de
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date 20210124

%global commit1 ad890067f661dc747a975bc55ba3767fe30d4452
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 libyuv

%global commit2 2392fe53ab3033fe5c679514dce448f55843fd51
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 libvpx

%global cvc_url https://chromium.googlesource.com

%global gver .%{date}git%{shortcommit0}

Name:           tg_owt
Version:        0
Release:        103%{?gver}%{?dist}
Summary:        WebRTC library for the Telegram messenger

# Main project - BSD
# abseil-cpp - ASL 2.0
# libsrtp - BSD
# libwebm - BSD
# libyuv - BSD
# openh264 - BSD
# pffft - BSD
# rnnoise - BSD
# usrsctp - BSD
License:        BSD and ASL 2.0
URL:            https://github.com/desktop-app/%{name}

Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Source1:        %{cvc_url}/libyuv/libyuv/+archive/%{shortcommit1}.tar.gz#/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        %{cvc_url}/webm/libvpx/+archive/%{shortcommit2}.tar.gz#/%{srcname2}-%{shortcommit2}.tar.gz

Patch0:         0001-Fix-undefined-references.patch

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavresample)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xtst)

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  yasm

Provides:       bundled(abseil-cpp) = 0~gitfba8a31
Provides:       bundled(base64) = 0~git
Provides:       bundled(fft) = 0~git
Provides:       bundled(fft4g) = 0~git
Provides:       bundled(g711) = 0~git
Provides:       bundled(g722) = 0~git
Provides:       bundled(libevent) = 1.4.15
Provides:       bundled(libsrtp) = 2.2.0~git94ac00d
Provides:       bundled(libvpx) = 1.8.2~git%{shortcommit2}
Provides:       bundled(libwebm) = 0~git
Provides:       bundled(libyuv) = 0~git%{shortcommit1}
Provides:       bundled(openh264) = 1.10.0~git6f26bce
Provides:       bundled(pffft) = 0~git483453d
Provides:       bundled(portaudio) = 0~git
Provides:       bundled(rnnoise) = 0~git91ef40
Provides:       bundled(sigslot) = 0~git
Provides:       bundled(spl_sqrt_floor) = 0~git
Provides:       bundled(usrsctp) = 1.0.0~gitbee946a

%description
Special fork of the OpenWebRTC library for the Telegram messenger.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       pkgconfig(alsa)
Requires:       pkgconfig(libavcodec)
Requires:       pkgconfig(libavformat)
Requires:       pkgconfig(libavresample)
Requires:       pkgconfig(libavutil)
Requires:       pkgconfig(libjpeg)
Requires:       pkgconfig(libpulse)
Requires:       pkgconfig(libswscale)
Requires:       pkgconfig(openssl)
Requires:       pkgconfig(opus)


%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{commit0} -p1

tar -xf %{S:1} -C src/third_party/libyuv
tar -xf %{S:2} -C src/third_party/libvpx/source/libvpx

sed -e 's/STATIC/SHARED/g' -i CMakeLists.txt
echo 'set_target_properties(tg_owt PROPERTIES SOVERSION 0 VERSION 0.0.0)' >> CMakeLists.txt

mkdir legal
cp -f -p src/third_party/abseil-cpp/LICENSE legal/LICENSE.abseil-cpp
cp -f -p src/third_party/abseil-cpp/README.chromium legal/README.abseil-cpp
cp -f -p src/third_party/libsrtp/LICENSE legal/LICENSE.libsrtp
cp -f -p src/third_party/libsrtp/README.chromium legal/README.libsrtp
cp -f -p src/third_party/libvpx/source/libvpx/LICENSE legal/LICENSE.libvpx
cp -f -p src/third_party/libvpx/source/libvpx/PATENTS legal/PATENTS.libvpx
cp -f -p src/third_party/libvpx/README.chromium legal/README.libvpx
cp -f -p src/third_party/libyuv/LICENSE legal/LICENSE.libyuv
cp -f -p src/third_party/libyuv/PATENTS legal/PATENTS.libyuv
cp -f -p src/third_party/libyuv/README.chromium legal/README.libyuv
cp -f -p src/third_party/openh264/src/LICENSE legal/LICENSE.openh264
cp -f -p src/third_party/openh264/README.chromium legal/README.openh264
cp -f -p src/third_party/pffft/LICENSE legal/LICENSE.pffft
cp -f -p src/third_party/pffft/README.chromium legal/README.pffft
cp -f -p src/third_party/rnnoise/COPYING legal/LICENSE.rnnoise
cp -f -p src/third_party/rnnoise/README.chromium legal/README.rnnoise
cp -f -p src/third_party/usrsctp/LICENSE legal/LICENSE.usrsctp
cp -f -p src/third_party/usrsctp/README.chromium legal/README.usrsctp
cp -f -p src/third_party/libvpx/source/libvpx/third_party/libwebm/LICENSE.TXT legal/LICENSE.libwebm
cp -f -p src/third_party/libvpx/source/libvpx/third_party/libwebm/PATENTS.TXT legal/PATENTS.libwebm
cp -f -p src/third_party/libvpx/source/libvpx/third_party/libwebm/README.libvpx legal/README.libwebm
cp -f -p src/base/third_party/libevent/LICENSE legal/LICENSE.libevent
cp -f -p src/base/third_party/libevent/README.chromium legal/README.libevent
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
cp -f -p src/rtc_base/third_party/base64/LICENSE legal/LICENSE.base64
cp -f -p src/rtc_base/third_party/base64/README.chromium legal/README.base64
cp -f -p src/rtc_base/third_party/sigslot/LICENSE legal/LICENSE.sigslot
cp -f -p src/rtc_base/third_party/sigslot/README.chromium legal/README.sigslot


%build
# CMAKE_BUILD_TYPE should always be Release due to some hardcoded checks.
%cmake \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON \
  -DTG_OWT_USE_PROTOBUF:BOOL=ON \
  -DTG_OWT_PACKAGED_BUILD:BOOL=ON
%cmake_build

%install
%cmake_install

%files
%doc src/AUTHORS src/OWNERS legal/README.*
%license LICENSE src/PATENTS legal/LICENSE.* legal/PATENTS.*
%{_libdir}/lib%{name}.so.0*

%files devel
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%{_libdir}/lib%{name}.so

%changelog
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
