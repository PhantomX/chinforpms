%global commit 7e7251c10a799c649c14175aafa996a5aa2e6a08
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200902
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

# Enable EGL/GLESV2
%global with_egl 0

# Enable system libchdr
%global with_libchdr 1

%undefine _hardened_build

%global pkgname Kronos
%global vc_url https://github.com/FCare/%{pkgname}

Name:           kronos
Version:        2.1.4
Release:        1%{?gver}%{?dist}
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
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  desktop-file-utils
%if 0%{?with_egl}
BuildRequires:  pkgconfig(glesv2)
%else
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(glut)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xmu)
%endif
%if 0%{?with_libchdr}
BuildRequires:  pkgconfig(libchdr)
%else
BuildRequires:  pkgconfig(flac)
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
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif

%if 0%{?with_libchdr}
rm -rf yabause/src/tools/libchdr/*
%else
rm -rf yabause/src/tools/libchdr/deps/{flac,zlib}*
%endif

cp -p yabause/{COPYING,AUTHORS,README} .

# fix end-of-line encoding
find \( -name "*.cpp" -or -name \*.c\* -or -name \*.h\* -or -name AUTHORS \) -exec sed -i 's/\r$//' {} \;

#fix permissions
find \( -name "*.cpp" -or -name \*.c\* -or -name \*.h\* \) -exec chmod -x {} \;

sed \
  -e 's| -Wno-format -mfpmath=sse -m64 -march=native -funroll-loops||g' \
  -e 's| -mfpmath=sse -m64 -march=native -funroll-loops||g' \
  -i yabause/src/CMakeLists.txt

%if 0%{?with_egl}
  sed -e '/FindGLUT/d' -i yabause/src/CMakeLists.txt
%endif

sed -e 's|share/pixmaps|share/icons/hicolor/32x32/apps|g' \
  -i yabause/src/port/qt/CMakeLists.txt

sed -e 's|share/yabause|share/%{name}|g' -i yabause/l10n/CMakeLists.txt


%build
%global optflags %(echo "%{optflags}" | sed -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//')
export LDFLAGS="%{build_ldflags} -Wl,-z,relro -Wl,-z,now"

pushd mini18n
minii18n="$(pwd)"
%cmake3 \
  -B %{__cmake_builddir} \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
%{nil}
%cmake_build
popd

%cmake3 \
  -S yabause \
  -B %{__cmake_builddir} \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
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
  -DMINI18N_INCLUDE_DIR:PATH=${minii18n}/src \
  -DMINI18N_LIBRARY:FILEPATH=${minii18n}/%{__cmake_builddir}/src/libmini18n.a \
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
* Thu Sep 03 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.4-1.20200902git7e7251c
- 2.1.4

* Tue Jul 21 2020 Phantom X <megaphantomx at hotmail dot com> - 2.1.2-1.20200527git4a5b181
- Initial spec
