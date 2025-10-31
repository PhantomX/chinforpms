%undefine _cmake_shared_libs

%global commit 447b289701e6427d828d41ebcfc74e5008b8729e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20251019

%global commit10 e4393ff85585d91400bcbad2e7266c011075b673
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 rpmalloc

%global dist .%{date}git%{shortcommit}%{?dist}

%global pkgname BennuGD_libretro
%global vc_url  https://github.com/diekleinekuh/%{pkgname}

Name:           bennugd
Version:        1.0.0
Release:        9%{?dist}
Summary:        A programming language to create games

License:        Zlib AND MIT
URL:            https://www.bennugd.org

Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
Source10:       https://github.com/mjansson/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz

Patch0:         0001-Build-without-git.patch

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(sdl)
BuildRequires:  pkgconfig(SDL_mixer)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(zlib)
Provides:       %{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{name}-libs < %{?epoch:%{epoch}:}%{version}-%{release}

%description
Bennugd is a programming language to create games.


%prep
%autosetup -n %{pkgname}-%{commit} -N

find \( -name '*.c*' -or -name '*.h*' -or -name README \) -exec sed -i 's/\r$//' {} \;

%autopatch -p1

for file in */COPYING */README ; 
do
  sed 's/\r//' -i ${file}
  iconv -f iso8859-1 -t utf-8 ${file} -o ${file}.conv && mv -f ${file}.conv ${file}
done;

mkdir core/rpmalloc
tar -xf %{S:10} -C core/rpmalloc/ --strip-components 1
cp -p core/rpmalloc/LICENSE LICENSE.rpmalloc

sed -e '/CMAKE_BUILD_RPATH/d' -i CMakeLists.txt

sed \
  -e 's|_RPM_BRANCH_|master|g' \
  -e 's|_RPM_COMMIT_|%{commit}|g' \
  -i core/common/bgd_version.c


%build
%cmake \
  -GNinja \
  -Dlibretro_core:BOOL=OFF \
  -DNO_SYSTEM_DEPENDENCIES:BOOL=OFF \
  -DCMAKE_BUILD_TYPE=Release \
%{nil}

%cmake_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{_vpath_builddir}/bin/bgdi %{buildroot}%{_bindir}/bgdi


%files
%license core/COPYING LICENSE.*
%doc README.md
%{_bindir}/bgdi


%changelog
* Mon Jul 21 2025 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-8.20250307git84c186a
- Change to BennuGD_libretro fork, with proper 64 bit support
- Remove libs package

* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-7.20220801gitd49f718
- Add -std=gnu17 to build flags

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-5.20211122svn356
- build_type_safety_c

* Sun Jan 07 2024 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-4.20211122svn356
- Remove strip from LDFLAGS

* Tue May 16 2023 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-3.20211122svn356
- Add patch to fix sdl12-compat support

* Tue Aug 17 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-2.20190530svn353
- Fix some rpmlint issues

* Mon Aug 16 2021 Phantom X <megaphantomx at hotmail dot com> - 1.0.0-1.20190530svn353
- Initial spec
