#undefine _hardened_build

Name:           mupen64plus
Version:        2.5.9
Release:        101%{?dist}
Summary:        A Nintendo 64 Emulator

Epoch:          1

License:        GPLv2 and LGPLv2
URL:            http://www.mupen64plus.org/
Source0:        https://github.com/%{name}/%{name}-core/releases/download/%{version}/%{name}-bundle-src-%{version}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  nasm
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
%if 0%{?fedora} >= 30
BuildRequires:  minizip-compat-devel
%else
BuildRequires:  minizip-devel
%endif
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(lirc)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(zlib)
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       dejavu-sans-fonts
Requires:       hicolor-icon-theme

%description
Mupen64Plus is a plugin-based N64 emulator for Linux which is capable of
accurately playing many games. Included are four MIPS R4300 CPU emulators,
with dynamic recompilers for 32-bit x86 and 64-bit amd64 systems, and necessary
plugins for audio, graphical rendering (RDP), signal co-processor (RSP), and
input. There are 3 OpenGL video plugins included: glN64, RiceVideoLinux, and
Glide64.

%package libs
Summary:        %{summary}
Provides:       lib%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lib%{name} < 2.5

%description libs
The %{name}-libs package contains the dynamic libraries needed for %{name} and
plugins.

%package devel
Summary:        %{summary}
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      lib%{name}-devel < 2.5
Obsoletes:      %{name}-libs-devel < 2.5

%description devel
The %{name}-devel package contains the development files libraries needed for 
plugins building.

%prep
%autosetup -n %{name}-bundle-src-%{version}

chmod 0755 ./m64p_build.sh ./m64p_install.sh

sed -i -e '/projects\/unix install/g' ./m64p_build.sh

cat > %{name}-env <<'EOF'
export OPTFLAGS="$(echo %{optflags} | sed -e 's/-O2\b/-O3/') -flto=%{_smp_build_ncpus} -fuse-linker-plugin -fdisable-ipa-cdtor"
export LDFLAGS="$OPTFLAGS %{build_ldflags}"
export V=1
export LDCONFIG=/bin/true
export PREFIX=/usr
export LIBDIR=%{_libdir}
export INCDIR=%{_includedir}/%{name}
export SHAREDIR=%{_datadir}/%{name}
export MANDIR=%{_mandir}
export LIRC=1
EOF

%build
source ./%{name}-env

./m64p_build.sh %{?_smp_mflags}

%install
source ./%{name}-env
./m64p_install.sh INSTALL="install -p" INSTALL_STRIP_FLAG= DESTDIR="%{buildroot}"

chmod +x %{buildroot}%{_libdir}/lib%{name}.so.*
chmod +x %{buildroot}%{_libdir}/%{name}/%{name}-*.so

rm -f %{buildroot}%{_datadir}/%{name}/font.ttf
ln -sf ../fonts/dejavu/DejaVuSans.ttf %{buildroot}%{_datadir}/%{name}/font.ttf

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license test/doc/gpl-license test/doc/LICENSES-*
%doc test/doc/README-* test/doc/RELEASE-*
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_mandir}/man6/%{name}.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%files libs
%license test/doc/lgpl-license
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}/*.h


%changelog
* Sun Apr 14 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:2.5.9-101
- Fedora 30 minizip devel mess

* Thu Mar 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 2.5.9-100
- 2.5.9
- BR: nasm
- Update to -flto flags
- Link font instead file sed

* Tue May 22 2018 Phantom X <megaphantomx at bol dot com dot br> - 2.5-4.chinfo
- BR: lirc

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.5-3
- Make library executable

* Tue Jan 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.5-2
- rebuilt

* Thu Jan  5 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.5-1
- Initial spec.
