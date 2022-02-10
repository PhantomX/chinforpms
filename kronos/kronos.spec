%global commit 4334b688d65944c9ba49e38b21be76b456d13214
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220208
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

# Enable EGL/GLESV2
%global with_egl 0

# Enable system libchdr
%global with_libchdr 1

%undefine _hardened_build
%undefine _cmake_shared_libs

# Disable LTO. Build fails
%global _lto_cflags %{nil}

%global pkgname Kronos
%global vc_url https://github.com/FCare/%{pkgname}

Name:           kronos
Version:        2.2.0
Release:        4%{?gver}%{?dist}
Summary:        A Sega Saturn emulator

License:        GPLv2+
URL:            http://fcare.github.io/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch0:         0001-libchdr-system-libraries.patch


BuildRequires:  cmake3
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
%if 0%{?with_egl}
BuildRequires:  pkgconfig(glesv2)
%else
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xmu)
%endif
%if 0%{?with_libchdr}
BuildRequires:  pkgconfig(libchdr)
%else
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(lzmasdk-c)
BuildRequires:  pkgconfig(zlib)
%endif
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(sdl2)
#BuildRequires:  cmake(OpenAL)
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5Multimedia)
BuildRequires:  cmake(Qt5OpenGL)
BuildRequires:  cmake(Qt5Widgets)
Requires:       hicolor-icon-theme

%description
Kronos is a Sega Saturn emulator forked from uoYabause.


%prep
%autosetup -n %{pkgname}-%{?gver:%{commit}}%{!?gver:%{version}} -p1

rm -rf win_template
rm -rf yabause/.vs

%if 0%{?with_libchdr}
rm -rf yabause/src/tools/libchdr/*
%else
rm -rf yabause/src/tools/libchdr/deps/{flac,lzma,zlib}*
%endif

cp -p yabause/{COPYING,AUTHORS,README} .

# fix end-of-line encoding
find \( -name "*.cpp" -or -name \*.c\* -or -name \*.h\* -or -name AUTHORS \) -exec sed -i 's/\r$//' {} \;

#fix permissions
find \( -name "*.cpp" -or -name \*.c\* -or -name \*.h\* \) -exec chmod -x {} \;

sed \
  -e 's| -Wno-format -march=native -funroll-loops||g' \
  -e 's| -march=native -funroll-loops||g' \
  -i yabause/src/CMakeLists.txt

sed -e 's|share/pixmaps|share/icons/hicolor/32x32/apps|g' \
  -i yabause/src/port/qt/CMakeLists.txt

sed \
  -e '/^install(/d' \
  -e '/mini18n-shared/d' \
  -i yabause/src/tools/mini18n/src/CMakeLists.txt


%build
%global optflags %(echo "%{optflags}" | sed -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//')
export LDFLAGS="%{build_ldflags} -Wl,-z,relro -Wl,-z,now"

%cmake3 \
  -S yabause \
  -DYAB_PORTS=qt \
%if 0%{?with_egl}
  -DYAB_FORCE_GLES31:BOOL=ON \
%endif
%if !0%{?with_libchdr}
  -DUSE_SYSTEM_CHDR:BOOL=OFF \
%endif
  -DYAB_OPTIMIZATION=-O3 \
  -DYAB_NETWORK:BOOL=ON \
  -DYAB_USE_SCSPMIDI:BOOL=ON \
  -DYAB_WANT_OPENAL:BOOL=OFF \
  -DYAB_WANT_SOFT_RENDERING:BOOL=ON \
  -DOpenGL_GL_PREFERENCE=GLVND \
%{nil}

%cmake_build


%install
%cmake_install

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license COPYING
%doc AUTHORS README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%changelog
* Wed Feb 09 2022 Phantom X <megaphantomx at hotmail dot com> - 2.2.0-4.20220208git4334b68
- Last snapshot

* Sun Dec 26 2021 Phantom X <megaphantomx at hotmail dot com> - 2.2.0-3.20211221git2302d96
- Update

* Thu Dec 09 2021 Phantom X <megaphantomx at hotmail dot com> - 2.2.0-2.20211208git9c2fe61
- Bump

* Sat Nov 13 2021 Phantom X <megaphantomx at hotmail dot com> - 2.2.0-1.20211022git624e7cf
- 2.2.0

* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 2.1.5-7.20210926git8b9abe8
- Last snapshot

* Sun Aug 29 2021 Phantom X <megaphantomx at hotmail dot com> - 2.1.5-6.20210827git4571698
- Bump

* Sat Aug 07 2021 Phantom X <megaphantomx at hotmail dot com> - 2.1.5-5.20210807gitb2665d7
- Update

* Fri Jun 25 2021 Phantom X <megaphantomx at hotmail dot com> - 2.1.5-4.20210601gita39f95a
- Last snapshot

* Fri May 07 2021 Phantom X <megaphantomx at hotmail dot com> - 2.1.5-3.20210505git13a4512
- Bump

* Sun Feb 28 2021 Phantom X <megaphantomx at hotmail dot com> - 2.1.5-2.20210225gitd48f332
- Update

* Sun Jan 17 2021 Phantom X <megaphantomx at hotmail dot com> - 2.1.5-1.20210114git897c26a
- 2.1.5

* Sat Dec 05 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.4-4.20201102gitdf8cb25
- Update
- mini18n static build is merged now

* Thu Oct 22 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.4-3.20201021gitd92383b
- New snapshot

* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.4-2.20200927git0b0a32b
- Bump

* Thu Sep 03 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.4-1.20200902git7e7251c
- 2.1.4

* Tue Jul 21 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.2-1.20200527git4a5b181
- Initial spec
