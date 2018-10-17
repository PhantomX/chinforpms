%global ffmpeg 0

Name:           mediastreamer
Version:        2.16.1
Release:        3%{?dist}
Summary:        Mediastreaming library for telephony application

License:        GPLv2
URL:            http://www.linphone.org/technical-corner/mediastreamer2.html
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext-devel
BuildRequires:  git
BuildRequires:  graphviz
BuildRequires:  intltool
BuildRequires:  python
BuildRequires:  vim-common
BuildRequires:  bcmatroska2-devel
BuildRequires:  gsm-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(bctoolbox)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(libbcg729)
BuildRequires:  pkgconfig(libbzrtp)
BuildRequires:  pkgconfig(libturbojpeg)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libupnp)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(ortp)
BuildRequires:  pkgconfig(spandsp)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xv)

%if 0%{?ffmpeg}
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libswscale)
%endif

Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
%{summary}.


%package libs
Summary:        %{summary}

%description libs
%{summary}.


%package devel
Summary:        Development libraries for mediastreamer
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

Development files.

%prep
%autosetup

sed \
  -e 's|@prefix@|%{_prefix}|g' \
  -e 's|@exec_prefix@|%{_exec_prefix}|g' \
  -e 's|@includedir@|%{_includedir}|g' \
  -e 's|@libdir@|%{_libdir}|g' \
  -e "s,@MEDIASTREAMER_VERSION@,$(awk '/mediastreamer2 VERSION/{print $3}' CMakeLists.txt),g" \
%ifarch %{arm} aarch64
  -e 's|@MS_PUBLIC_CFLAGS@|-DMS_FIXED_POINT|g' \
%else
  -e 's| @MS_PUBLIC_CFLAGS@||g' \
%endif
  %{name}.pc.in > %{name}.pc

sed -e 's|(git: " MS2_GIT_VERSION ")||g' -i src/base/msfactory.c

%build
mkdir builddir
pushd builddir
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DENABLE_STATIC:BOOL=OFF \
  -DENABLE_TESTS:BOOL=OFF \
  -DENABLE_STRICT:BOOL=OFF \
%if !0%{?ffmpeg}
  -DENABLE_FFMPEG:BOOL=OFF \
%endif
  -DENABLE_ALSA:BOOL=ON \
  -DENABLE_G726:BOOL=ON \
  -DENABLE_G729:BOOL=ON \
  -DENABLE_G729:BOOL=ON \
  -DENABLE_JPEG:BOOL=ON \
  -DENABLE_SPEEX_CODEC:BOOL=ON \
  -DENABLE_SPEEX_DSP:BOOL=ON \
  -DENABLE_PORTAUDIO:BOOL=OFF \
  -DENABLE_PULSEAUDIO:BOOL=ON \
  -DENABLE_THEORA:BOOL=ON \
  -DENABLE_V4L:BOOL=ON \
  -DENABLE_VIDEO:BOOL=ON \
  -DENABLE_X11:BOOL=ON \
  -DENABLE_XV:BOOL=ON \
  -DENABLE_VPX:BOOL=ON \
  -DENABLE_ZRTP:BOOL=ON

%make_build

%install
%make_install -C builddir

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -pm0644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

mkdir -p %{buildroot}%{_libdir}/%{name}/plugins

rm -f builddir/help/doc/html/html.tar
rm -rf %{buildroot}%{_datadir}/doc


%files
%license COPYING
%doc README.md
%{_bindir}/mediastream
%{_bindir}/mkvstream
%{_datadir}/images/nowebcamCIF.jpg

%files libs
%{_libdir}/lib%{name}*.so.*
%dir %{_libdir}/%{name}/plugins

%files devel
%doc builddir/help/doc/html
%{_includedir}/%{name}2
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/Mediastreamer2/cmake/*.cmake

%changelog
* Mon Oct 08 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.16.1-3
- BR: gcc-c++

* Fri Sep 22 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.16.1-2
- cmake and fixes for it

* Tue Jul 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.16.1-1
- 2.16.1

* Tue Jun 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.15.1-1
- Initial spec
