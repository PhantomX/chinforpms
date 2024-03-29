#undefine _hardened_build

%global with_optim 3
%{?with_optim:%global optflags %(echo %{optflags} | sed -e 's/-O2 /-O%{?with_optim} /')}
%{!?_hardened_build:%global build_ldflags %{build_ldflags} -Wl,-z,now}

%global commit 2ac8682c60e7df3581b9167fa67d47e263d2b9da
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220930
%global with_snapshot 1

%global commit1 df0770215f743f70244b09978c123a0a8b2a7d9d
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 %{name}-audio-sdl

%global commit2 9cbe63f8e80f4dfc6dcdd8408b51358d248a050e
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 %{name}-input-sdl

%global commit3 abd5b15498eb86101c2a56eb49460a264365b3ba
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 %{name}-rom

%global commit4 aa0ea78030d3c2b80184a35bbb36909fd7a28e70
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 %{name}-rsp-hle

%global commit5 42546ab00b23a8052b9c974882628912609990c2
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})
%global srcname5 %{name}-ui-console

%global commit6 79809753e83180e6bbc3b5b3dc65120fef3e7a43
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})
%global srcname6 %{name}-video-glide64mk2

%global commit7 51582f9e62082f2937a17ac3acfaab08cb7f46ef
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})
%global srcname7 %{name}-video-rice

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global xxhash_ver 0.8.1

%global vc_url  https://github.com/%{name}

Name:           mupen64plus
Version:        2.5.9
Release:        114%{?gver}%{?dist}
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

ExcludeArch:    s390x

BuildRequires:  make
BuildRequires:  boost-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
BuildRequires:  nasm
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  minizip-compat-devel
BuildRequires:  pkgconfig(libpng)
#BuildRequires:  pkgconfig(lirc)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(zlib)
Requires:       dejavu-sans-fonts
Requires:       hicolor-icon-theme

Obsoletes:      %{name}-libs < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-plugins < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{name}-plugins%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       %{srcname1}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{srcname2}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{srcname3}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{srcname4}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{srcname5}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{srcname6}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{srcname7}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

Provides:       bundled(xxhash) = %{xxhash_ver}

Conflicts:      %{name}-qt
Conflicts:      %{name}-cli


%description
Mupen64Plus is a plugin-based N64 emulator for Linux which is capable of
accurately playing many games. Included are four MIPS R4300 CPU emulators,
with dynamic recompilers for 32-bit x86 and 64-bit amd64 systems, and necessary
plugins for audio, graphical rendering (RDP), signal co-processor (RSP), and
input. There are 3 OpenGL video plugins included: glN64, RiceVideoLinux, and
Glide64.

%package devel
Summary:        %{summary}
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

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

%autopatch -p1

%else
%autosetup -n %{name}-bundle-src-%{version}
%endif


chmod 0755 ./m64p_build.sh ./m64p_install.sh

sed -i -e '/projects\/unix install/g' ./m64p_build.sh


%build

cat > %{name}-env <<'EOF'
export OPTFLAGS="%{optflags}"
export V=1
export LDCONFIG=/bin/true
export PREFIX=/usr
export LIBDIR=%{_libdir}
export INCDIR=%{_includedir}/%{name}
export SHAREDIR=%{_datadir}/%{name}
export MANDIR=%{_mandir}
export LIRC=0
export PIC=1
export PIE=1
%ifarch %{arm}
export NEON=1 VFP_HARD=1
%endif
%ifarch %{arm} aarch64 ppc ppc64 ppc64le
export NO_SSE=1
%endif
EOF

source ./%{name}-env

./m64p_build.sh %{?_smp_mflags}

%install
%set_build_flags
source ./%{name}-env
./m64p_install.sh INSTALL="install -p" INSTALL_STRIP_FLAG= DESTDIR="%{buildroot}"

chmod +x %{buildroot}%{_libdir}/lib%{name}.so.*
chmod +x %{buildroot}%{_libdir}/%{name}/%{name}-*.so

ln -sf libmupen64plus.so.2 %{buildroot}%{_libdir}/libmupen64plus.so

rm -f %{buildroot}%{_datadir}/%{name}/font.ttf
ln -sf ../fonts/dejavu-sans-fonts/DejaVuSans.ttf %{buildroot}%{_datadir}/%{name}/font.ttf

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license test/doc/gpl-license
%doc test/doc/README-* test/doc/RELEASE-*
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.*
%{_libdir}/%{name}/
%{_mandir}/man6/%{name}.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%files devel
%{_includedir}/%{name}/*.h
%{_libdir}/lib%{name}.so


%changelog
* Mon Nov 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.9-114.20220930git2ac8682
- Fedora sync

* Thu Aug 11 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.9-112.20220809gitf299843
- Update
- Vulkan updates from Logan McNaughton fork

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.9-111.20220218git49dd0bf
- Bump

* Mon Feb 14 2022 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.9-110.20220214git1f495d5
- Update

* Tue Aug 24 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.9-109.20210727gita605261
- Bump

* Mon Jun 07 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.9-108.20210511gitc9f49e2
- Last snapshot

* Tue Jan 05 2021 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.9-107.20210102gitaf81231
- Update

* Wed Oct 21 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.9-106.20201016git872751d
- Bump

* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1:2.5.9-105.20200525gitb7b56fe
- Use Fedora lto flags

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
