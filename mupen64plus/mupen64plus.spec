%global commit b7b56fea513e8734b982347d5b965c4a8e6f2074
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200525
%global with_snapshot 1

%global commit1 5c431df0638885044bc45d2976ffec16c24fa087
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 %{name}-audio-sdl

%global commit2 954a5dc74267d67ef065f41472eaaf6970fb1c85
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 %{name}-input-sdl

%global commit3 abd5b15498eb86101c2a56eb49460a264365b3ba
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 %{name}-rom

%global commit4 2df8038d5f8fb722326c98d717b2d571a6d716ed
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 %{name}-rsp-hle

%global commit5 77a2adea93ffe4d6630bbe2e815650819a1cf260
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 %{name}-ui-console

%global commit6 b4d4503dd0a3733815d62eab04d2c1c7c466e157
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 %{name}-video-glide64mk2

%global commit7 e409d749a53bd6fbb764ef4012614d21779a20fb
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 %{name}-video-rice

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

#undefine _hardened_build
%global _legacy_common_support 1

%global vc_url  https://github.com/%{name}

Name:           mupen64plus
Version:        2.5.9
Release:        104%{?gver}%{?dist}
Summary:        A Nintendo 64 Emulator

Epoch:          1

License:        GPLv2 and LGPLv2
URL:            http://www.mupen64plus.org/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/%{name}-core/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        %{vc_url}/%{name}-audio-sdl/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        %{vc_url}/%{name}-input-sdl/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        %{vc_url}/%{name}-rom/archive/%{commit3}/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        %{vc_url}/%{name}-rsp-hle/archive/%{commit4}/%{srcname4}-%{shortcommit4}.tar.gz
Source5:        %{vc_url}/%{name}-ui-console/archive/%{commit5}/%{srcname5}-%{shortcommit5}.tar.gz
Source6:        %{vc_url}/%{name}-video-glide64mk2/archive/%{commit6}/%{srcname6}-%{shortcommit6}.tar.gz
Source7:        %{vc_url}/%{name}-video-rice/archive/%{commit7}/%{srcname7}-%{shortcommit7}.tar.gz
%else
Source0:        %{vc_url}/%{name}-core/releases/download/%{version}/%{name}-bundle-src-%{version}.tar.gz
%endif

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
%if 0%{?with_snapshot}
%setup -q -c -T -n %{name}-%{commit}

for i in core rom ui-console audio-sdl input-sdl rsp-hle video-rice video-glide64mk2 ;do
  mkdir -p source/%{name}-$i
done

tar -xf %{S:0} -C source/%{name}-core --strip-components 1
tar -xf %{S:1} -C source/%{name}-audio-sdl --strip-components 1
tar -xf %{S:2} -C source/%{name}-input-sdl --strip-components 1
tar -xf %{S:3} -C source/%{name}-rom --strip-components 1
tar -xf %{S:4} -C source/%{name}-rsp-hle --strip-components 1
tar -xf %{S:5} -C source/%{name}-ui-console --strip-components 1
tar -xf %{S:6} -C source/%{name}-video-glide64mk2 --strip-components 1
tar -xf %{S:7} -C source/%{name}-video-rice --strip-components 1

tar xf source/%{name}-core/tools/m64p_helper_scripts.tar.gz

%else
%autosetup -n %{name}-bundle-src-%{version}
%endif


chmod 0755 ./m64p_build.sh ./m64p_install.sh

sed -i -e '/projects\/unix install/g' ./m64p_build.sh


%build
# Disable this. Local lto flags in use.
%define _lto_cflags %{nil}

cat > %{name}-env <<'EOF'
export OPTFLAGS="$(echo %{optflags} | sed -e 's/-O2\b/-O3/') -flto=%{_smp_build_ncpus} -fuse-linker-plugin"
export LDFLAGS="$OPTFLAGS %{build_ldflags} -Wl,-z,relro -Wl,-z,now"
export V=1
export LDCONFIG=/bin/true
export PREFIX=/usr
export LIBDIR=%{_libdir}
export INCDIR=%{_includedir}/%{name}
export SHAREDIR=%{_datadir}/%{name}
export MANDIR=%{_mandir}
export LIRC=1
export PIC=1
export PIE=1
EOF

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
* Thu Jun 25 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.9-104.20200525gitb7b56fe
- New snapshot

* Mon Apr 27 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.5.9-103.20200422git4edc53c
- Snapshot

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:2.5.9-102
- gcc 10 fix

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
