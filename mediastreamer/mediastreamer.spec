%global ffmpeg 0

Name:           mediastreamer
Version:        2.16.1
Release:        1%{?dist}
Summary:        Mediastreaming library for telephony application

Group:          System Environment/Libraries
License:        GPLv2
URL:            http://www.linphone.org/technical-corner/mediastreamer2.html
Source0:        https://www.linphone.org/releases/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  doxygen
BuildRequires:  gettext-devel
BuildRequires:  graphviz
BuildRequires:  intltool
BuildRequires:  libtool
BuildRequires:  vim-common
BuildRequires:  bzrtp-devel
BuildRequires:  gsm-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(bctoolbox)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsrtp)
BuildRequires:  pkgconfig(libupnp)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(ortp)
BuildRequires:  pkgconfig(spandsp)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xv)
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

sed -e 's|(git: " MS2_GIT_VERSION ")||g' -i src/base/msfactory.c

intltoolize -f
autoreconf -ivf

%build
%configure \
  --disable-tests \
  --disable-silent-rules \
  --disable-static \
  --disable-rpath \
  --disable-strict \
%if !0%{?ffmpeg}
  --disable-ffmpeg \
%endif
  --enable-ortp \
  --enable-external-ortp \
  --enable-gsm \
  --disable-portaudio \
  --enable-pulseaudio \
  --enable-spandsp \
  --enable-speex \
  --disable-theora \
  --enable-upnp \
  --enable-vp8 \
  --enable-x11 \
  --enable-xv \
  --enable-glx \
  --enable-zrtp \
  --with-srtp=/usr

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install

find %{buildroot} -name '*.la' -delete

mkdir -p %{buildroot}%{_libdir}/%{name}/plugins

rm -f help/doc/html/html.tar
rm -rf %{buildroot}%{_datadir}/doc

%find_lang %{name}

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/mediastream
%{_bindir}/msaudiocmp
%{_datadir}/images/nowebcamCIF.jpg

%files libs
%{_libdir}/lib%{name}*.so.*
%dir %{_libdir}/%{name}/plugins

%files devel
%doc help/doc/html
%{_includedir}/%{name}2
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Tue Jul 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.16.1-1
- 2.16.1

* Tue Jun 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.15.1-1
- Initial spec
