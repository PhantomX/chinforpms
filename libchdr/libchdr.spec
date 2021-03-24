%global commit 8f080e151cab7ee1fe26a712fb071156d21c3d8f
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210321
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           libchdr
Version:        0.1
Release:        4%{?gver}%{?dist}
Summary:        Standalone library for reading MAME's CHDv1-v5 formats

License:        BSD
URL:            https://github.com/rtissera/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

Patch10:        0001-Shared-library-fixes.patch
Patch11:        0001-Use-system-lzma-sdk.patch
Patch12:        0001-Do-not-build-static-library-if-INSTALL_STATIC_LIBS-O.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(lzmasdk-c)
BuildRequires:  pkgconfig(zlib)

%description
%{name} is a standalone library for reading MAME's CHDv1-v5 formats.

%package        devel
Summary:        Development files for %{name}
Requires:       %{?epoch:%{epoch}:}%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

rm -rf deps/{lzma,zlib}*

sed -e 's| -O3 -flto||g' -i CMakeLists.txt


%build
%cmake \
  -DCMAKE_INSTALL_LIBDIR:PATH="%{_lib}" \
  -DINSTALL_STATIC_LIBS:BOOL=OFF \
  -DWITH_SYSTEM_LZMA:BOOL=ON \
  -DWITH_SYSTEM_ZLIB:BOOL=ON \
  -DCMAKE_BUILD_TYPE=Release \
%{nil}

%cmake_build


%install

%cmake_install

install -pm0644 include/libchdr/chdconfig.h %{buildroot}%{_includedir}/%{name}/


%files
%license LICENSE.txt
%doc README.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Mar 23 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-4.20210321git8f080e1
- Bump
- Remove flac BR, upstream is using dr_flac now

* Tue Jan  5 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-3.20201201git032b0b2
- Parent/clone PR try

* Wed Nov 18 2020 Phantom X <megaphantomx at hotmail dot com> - 0.1-2.20201103git82670d5
- Install missing header

* Fri Nov 06 2020 Phantom X <megaphantomx at hotmail dot com> - 0.1-1.20201103git82670d5
- 0.1

* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0-3.20200913gitd21ac2f
- Bump

* Sat Aug 08 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0-2.20200605git057deda
- System lzma-sdk

* Tue Jul 21 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0-1.20200605git057deda
- Initial spec
