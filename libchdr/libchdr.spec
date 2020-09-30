%global commit d21ac2f069203cc8e8d4c0ae7b2d305a0f28e36a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200913
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           libchdr
Version:        0.0
Release:        3%{?gver}%{?dist}
Summary:        Standalone library for reading MAME's CHDv1-v5 formats

License:        BSD
URL:            https://github.com/rtissera/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Optional-static-library.patch
Patch1:         0001-Shared-library-fixes.patch
Patch3:         0001-Use-system-lzma-sdk.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  pkgconfig(flac)
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

rm -rf deps/{flac,lzma,zlib}*


%build
%cmake \
  -B %{__cmake_builddir} \
  -DCMAKE_INSTALL_LIBDIR:PATH="%{_lib}" \
  -DBUILD_STATIC_LIBS:BOOL=OFF \
  -DWITH_SYSTEM_FLAC:BOOL=ON \
  -DWITH_SYSTEM_LZMA:BOOL=ON \
  -DWITH_SYSTEM_ZLIB:BOOL=ON \
%{nil}

%cmake_build


%install

%cmake_install


%files
%license LICENSE.txt
%doc README.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0-3.20200913gitd21ac2f
- Bump

* Sat Aug 08 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0-2.20200605git057deda
- System lzma-sdk

* Tue Jul 21 2020 Phantom X <megaphantomx at hotmail dot com> - 0.0-1.20200605git057deda
- Initial spec
