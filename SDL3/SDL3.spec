# For the generated library symbol suffix
%if 0%{?__isa_bits} == 32
%global libsymbolsuffix %{nil}
%else
%global libsymbolsuffix ()(%{__isa_bits}bit)
%endif

# For declaring rich dependency on libdecor
%global libdecor_majver 0

%if 0%{?rhel}
# Disable static library on RHEL
%bcond static 0
%else
%bcond static 1
%endif


Name:           SDL3
Version:        3.2.22
Release:        100%{?dist}
Summary:        Cross-platform multimedia library
License:        Zlib AND MIT AND Apache-2.0 AND (Apache-2.0 OR MIT)
URL:            http://www.libsdl.org/
Source0:        http://www.libsdl.org/release/%{name}-%{version}.tar.gz
Source1:        SDL3_revision.h

# Patches from upstream

# Patches proposed upstream

BuildRequires:  git-core
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
# While SDL3 supports this, Xwayland does not expose XScrnSaver.
# BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(systemd)
# For building man pages
BuildRequires:  perl-interpreter
BuildRequires:  pkgconfig(libusb-1.0)
# PulseAudio
BuildRequires:  pkgconfig(libpulse-simple)
# Jack
BuildRequires:  pkgconfig(jack)
# PipeWire
BuildRequires:  pkgconfig(libpipewire-0.3)
# D-Bus
BuildRequires:  pkgconfig(dbus-1)
# IBus
BuildRequires:  pkgconfig(ibus-1.0)
# Wayland
BuildRequires:  pkgconfig(libdecor-%{libdecor_majver})
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)
# Vulkan
BuildRequires:  vulkan-devel
# KMS
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libdrm)

# Ensure libdecor is pulled in when libwayland-client is (rhbz#1992804)
Requires:       (libdecor-%{libdecor_majver}.so.%{libdecor_majver}%{libsymbolsuffix} if libwayland-client)

# Long ago forked hidraw customized for SDL
Provides:       bundled(hidraw)

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package devel
Summary:        Files needed to develop Simple DirectMedia Layer applications
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Add deps required to compile SDL apps
## For SDL_opengl.h
Requires:       pkgconfig(gl)
Requires:       pkgconfig(glu)
## For SDL_syswm.h
Requires:       pkgconfig(x11)
Requires:       pkgconfig(xproto)
%if ! %{with static}
# Remove any leftover -static subpackages
Obsoletes:      %{name}-static < %{version}-%{release}
%endif

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

%if %{with static}
%package static
Summary:        Static libraries for SDL3
# Needed to keep CMake happy
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static libraries for SDL3.
%endif

%package test
Summary:        Testing libraries for SDL3
# Needed to keep CMake happy
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description test
Testing libraries for SDL3.


%prep
%autosetup -S git_am
sed -e 's/\r//g' -i README.md WhatsNew.txt BUGS.txt LICENSE.txt CREDITS.md


%build
# Deal with new CMake policy around whitespace in LDFLAGS...
export LDFLAGS="%{shrink:%{build_ldflags}}"

%cmake \
    -DSDL_INSTALL_DOCS=ON \
    -DSDL_DLOPEN=ON \
    -DSDL_VIDEO_KMSDRM=ON \
    -DSDL_ARTS=OFF \
    -DSDL_ESD=OFF \
    -DSDL_NAS=OFF \
    -DSDL_PULSEAUDIO_SHARED=ON \
    -DSDL_JACK_SHARED=ON \
    -DSDL_PIPEWIRE_SHARED=ON \
    -DSDL_ALSA=ON \
    -DSDL_VIDEO_WAYLAND=ON \
    -DSDL_LIBDECOR_SHARED=ON \
    -DSDL_VIDEO_VULKAN=ON \
    -DSDL_SSE3=OFF \
    -DSDL_RPATH=OFF \
    %{?with_static:-DSDL_STATIC=ON} \
    %{?with_static:-DSDL_STATIC_PIC=ON} \
%ifarch ppc64le
    -DSDL_ALTIVEC=OFF \
%endif

%cmake_build


%install
%cmake_install

# Rename SDL_revision.h to SDL_revision-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_revision.h wrapper
# TODO: Figure out how in the hell the SDL_REVISION changes between architectures on the same SRPM.
mv %{buildroot}%{_includedir}/SDL3/SDL_revision.h %{buildroot}%{_includedir}/SDL3/SDL_revision-%{_arch}.h
install -p -m 644 %{SOURCE1} %{buildroot}%{_includedir}/SDL3/SDL_revision.h


%files
%license LICENSE.txt
%doc BUGS.txt CREDITS.md README.md
%{_libdir}/libSDL3.so.0{,.*}

%files devel
%doc README.md WhatsNew.txt
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/sdl3.pc
%dir %{_libdir}/cmake/SDL3
%{_libdir}/cmake/SDL3/SDL3Config*.cmake
%{_libdir}/cmake/SDL3/SDL3headersTargets*.cmake
%{_libdir}/cmake/SDL3/SDL3sharedTargets*.cmake
%{_includedir}/SDL3
%{_mandir}/man3/SDL*.3*

%if %{with static}
%files static
%license LICENSE.txt
%{_libdir}/libSDL3.a
%{_libdir}/cmake/SDL3/SDL3staticTargets*.cmake
%endif

%files test
%license LICENSE.txt
%{_libdir}/libSDL3_test.a
%{_libdir}/cmake/SDL3/SDL3testTargets*.cmake


%changelog
* Tue Sep 09 2025 Phantom X <megaphantomx at hotmail dot com> - 3.2.22-100
- 3.2.22

* Tue Aug 05 2025 Phantom X <megaphantomx at hotmail dot com> - 3.2.20-100
- 3.2.20

* Tue Jul 15 2025 Phantom X <megaphantomx at hotmail dot com> - 3.2.18-100
- 3.2.18

* Tue Jun 10 2025 Phantom X <megaphantomx at hotmail dot com> - 3.2.16-100
- 3.2.16

* Mon May 26 2025 Phantom X <megaphantomx at hotmail dot com> - 3.2.14-100
- 3.2.14

* Fri May 09 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.12-1
- Update to 3.2.12

* Fri Apr 11 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.10-1
- Update to 3.2.10

* Sun Mar 16 2025 Simone Caronni <negativo17@gmail.com> - 3.2.8-1
- Update to 3.2.8.
- Drop merged patch.

* Mon Feb 10 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.4-2
- Add fix for building against PipeWIre 1.3.x

* Sat Feb 08 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.4-1
- Update to 3.2.4

* Mon Feb 03 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.2-1
- Update to 3.2.2

* Wed Jan 22 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0 (SDL3 GA)

* Thu Jan 16 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.1.10-1
- Update to 3.1.10

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.1.8-2
- Disable static library subpackage on RHEL

* Thu Jan 09 2025 Neal Gompa <ngompa@fedoraproject.org> - 3.1.8-1
- Update to 3.1.8
- Enable man pages

* Mon Dec 02 2024 Neal Gompa <ngompa@fedoraproject.org> - 3.1.6-1
- Update to 3.1.6
- Split testing library into subpackage

* Fri Oct 04 2024 Neal Gompa <ngompa@fedoraproject.org> - 3.1.3-1
- Initial package

