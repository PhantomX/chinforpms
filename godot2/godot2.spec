%global commit b00f8dc35b0f8bd21a00c9f727acaf392cc6eb5c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180525
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global status stable
%global uversion %{version}-%{status}

# Godot 2.1.x has known optimisation bugs with GCC 6+,
# we therefore compile with Clang when necessary.
# Those issues are fixed in upcoming Godot 3.0.
%if ! (0%{?rhel} && 0%{?rhel} < 8)
%define use_clang 1
%endif

%global pkgname godot

Name:           godot2
Version:        2.1.5
Release:        0.1%{?gver}%{?dist}
Summary:        Multi-platform 2D and 3D game engine with a feature-rich editor
# Godot itself is MIT-licensed, the rest is from vendored thirdparty libraries
License:        MIT and CC-BY and ASL 2.0 and BSD and zlib and OFL and FTL and ISC
URL:            https://godotengine.org
%if 0%{?with_snapshot}
Source0:        https://github.com/godotengine/godot/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/godotengine/godot/archive/%{uversion}/%{pkgname}-%{uversion}.tar.gz
%endif

# https://github.com/godotengine/godot/pull/18868
Patch0:         godot-clang6-fix.patch

%if 0%{?use_clang}
BuildRequires:  clang
%else
BuildRequires:  gcc-c++
%endif

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(minizip)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(opusfile)
BuildRequires:  pkgconfig(theora)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(vorbisfile)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  scons


# Version unclear, SVN revision between SV7 and SV8 (r475)
Provides:       bundled(libmpcdec)
# Version unclear, assumed around 1.2rc1
Provides:       bundled(speex)
Provides:       bundled(squish) = 1.15

%description
Godot is an advanced, feature-packed, multi-platform 2D and 3D game engine.
It provides a huge set of common tools, so you can just focus on making
your game without reinventing the wheel.

Godot is completely free and open source under the very permissive MIT
license. No strings attached, no royalties, nothing. Your game is yours,
down to the last line of engine code.


%package        runner
Summary:        Shared binary to play games developed with the Godot engine

%description    runner
This package contains a %{pkgname}-runner binary for the Linux X11 platform,
which can be used to run any game developed with the Godot engine simply
by pointing to the location of the game's data package.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{uversion} -p1
%endif

# Windows-specific
rm -rf thirdparty/rtaudio

%build
# Needs to be in %%build so that system_libs stays in scope
system_libs=""
for lib in freetype glew libogg libpng libtheora libvorbis libwebp minizip openssl opus zlib; do
    system_libs+="builtin_"$lib"=no "
    rm -rf thirdparty/$lib
done

ccflags="%{build_cxxflags}"
%if 0%{?use_clang}
ccflags="%(echo ${ccflags} | sed -e 's/ -fcf-protection//')"
%endif
ldflags="%{build_ldflags}"

%define _scons scons %{?_smp_mflags} CCFLAGS="$ccflags" LINKFLAGS="$ldflags" $system_libs progress=no %{?use_clang:use_llvm=yes} debug_release=yes udev=yes

%if 0%{?fedora}
export BUILD_REVISION="fedora"
%endif
%if 0%{?rhel}
export BUILD_REVISION="rhel"
%endif

# Build game runner (without tools)
%_scons p=x11 tools=no target=release


%install
install -d %{buildroot}%{_bindir}
install -p -m755 bin/%{pkgname}.x11.opt.%{__isa_bits}%{?use_clang:.llvm} %{buildroot}%{_bindir}/%{name}-runner


%files          runner
%license AUTHORS.md COPYRIGHT.txt LICENSE.txt LOGO_LICENSE.md
%license AUTHORS.md COPYRIGHT.txt LICENSE.txt
%{_bindir}/%{name}-runner


%changelog
* Fri May 25 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.1.5-0.1.20180525gitb00f8dc
- Initial spec, only for runner, stripped from Rémi Verschelde original
