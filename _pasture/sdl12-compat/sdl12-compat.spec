%global commit 4d814ba89a6e87cd02e148d9d1504f77848e97dd
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220903
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           sdl12-compat
Version:        1.2.54
Release:        0.0%{?gver}%{?dist}
Summary:        SDL 1.2 runtime compatibility library using SDL 2.0

# mp3 decoder code is MIT-0/PD
# SDL_opengl.h is zlib and MIT
License:        zlib and (Public Domain or MIT-0) and MIT
URL:            https://github.com/libsdl-org/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

# Multilib aware-header stub
Source1:        SDL_config.h

# Backports from upstream (0001~0500)

# Proposed patches (0501~1000)

# Fedora specific patches (1001+)
Patch1001:      sdl12-compat-sdlconfig-multilib.patch


BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  make
BuildRequires:  SDL2-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
# This replaces SDL
Obsoletes:      SDL < 1.2.15-49
Conflicts:      SDL < 1.2.50
Provides:       SDL = %{version}
Provides:       SDL%{?_isa} = %{version}
# This dlopens SDL2 (?!), so manually depend on it
Requires:       SDL2%{?_isa} >= 2.0.18

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio device.

This code is a compatibility layer; it provides a binary-compatible API for
programs written against SDL 1.2, but it uses SDL 2.0 behind the scenes.

If you are writing new code, please target SDL 2.0 directly and do not use
this layer.

%package devel
Summary:        Files to develop SDL 1.2 applications using SDL 2.0
Requires:       %{name}%{?_isa} = %{version}-%{release}
# This replaces SDL-devel
Obsoletes:      SDL-devel < 1.2.15-49
Conflicts:      SDL-devel < 1.2.50
Provides:       SDL-devel = %{version}
Provides:       SDL-devel%{?_isa} = %{version}
# We don't provide the static library, but we want to replace SDL-static anyway
Obsoletes:      SDL-static < 1.2.15-49
Conflicts:      SDL-static < 1.2.50
# Add deps required to compile SDL apps
## For SDL_opengl.h
Requires:       pkgconfig(gl)
Requires:       pkgconfig(glu)
## For SDL_syswm.h
Requires:       pkgconfig(x11)
Requires:       pkgconfig(xproto)

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library
designed to provide fast access to the graphics frame buffer and audio device.

This code is a compatibility layer; it provides a source-compatible API for
programs written against SDL 1.2, but it uses SDL 2.0 behind the scenes.

If you are writing new code, please target SDL 2.0 directly and do not use
this layer.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif


%build
%cmake \
%{nil}

%cmake_build


%install
%cmake_install

# Rename SDL_config.h to SDL_config-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_config.h wrapper
mv %{buildroot}/%{_includedir}/SDL/SDL_config.h %{buildroot}/%{_includedir}/SDL/SDL_config-%{_arch}.h
install -m644 %{SOURCE1} %{buildroot}/%{_includedir}/SDL/SDL_config.h

# Delete leftover static files
rm -f %{buildroot}%{_libdir}/*.a


%files
%license LICENSE.txt
%doc README.md BUGS.md
%{_libdir}/libSDL-1.2.so.*

%files devel
%{_bindir}/sdl-config
%{_datadir}/aclocal/sdl.m4
%{_includedir}/SDL/
%{_libdir}/libSDL-1.2.so
%{_libdir}/libSDL.so
%{_libdir}/pkgconfig/sdl12_compat.pc


%changelog
* Sun Aug 15 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.50-4.20210814gita3bfcb2
- Bump

* Sat Jul 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.50-3.20210628gitcf47f88
- Last snapshot

* Sun May 23 2021 Phantom X <megaphantomx at hotmail dot com> - 1.2.50-2.20210519gitebcbb11
- Bump

* Tue Oct 29 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.2.50-1.20190403gitdc55edfe5d2f
- Initial spec
