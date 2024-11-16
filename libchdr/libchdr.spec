%global commit b3974651d869c2f804e9879b063c23280d2ae617
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20241110
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global drflac_ver 0.12.42

Name:           libchdr
Version:        0.2
Release:        26%{?dist}
Summary:        Standalone library for reading MAME's CHDv1-v5 formats

License:        BSD-3-Clause AND (Unlicense OR MIT-0)
URL:            https://github.com/rtissera/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

Patch10:        0001-Shared-library-fixes.patch
Patch11:        0001-Use-system-lzma-sdk.patch
Patch12:        0001-Do-not-build-static-library-if-INSTALL_STATIC_LIBS-O.patch
Patch13:        0001-Use-system-libzstd.patch
Patch14:        0001-Updates-from-Stenzek.patch
Patch15:        0001-3rdparty-libchdr-Allow-cancelling-precache.patch
Patch16:        0001-Export-needed-functions.patch


BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(libzstd) >= 1.5.6
BuildRequires:  pkgconfig(lzmasdk-c) >= 24.05
BuildRequires:  pkgconfig(zlib)

Provides:       bundled(dr_flac) = %{drflac_ver}


%description
%{name} is a standalone library for reading MAME's CHDv1-v5 formats.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

rm -rf deps/{lzma,zlib,zstd}*

sed -e 's| -O3||g' -i CMakeLists.txt
sed -e 's|chdr-static|chdr|g' -i tests/CMakeLists.txt


%build
%cmake \
  -DCMAKE_INSTALL_LIBDIR:PATH="%{_lib}" \
  -DINSTALL_STATIC_LIBS:BOOL=OFF \
  -DWITH_SYSTEM_LZMA:BOOL=ON \
  -DWITH_SYSTEM_ZLIB:BOOL=ON \
  -DWITH_SYSTEM_ZSTD:BOOL=ON \
  -DCMAKE_BUILD_TYPE=Release \
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
* Wed Nov 06 2024 Phantom X <megaphantomx at hotmail dot com> - 0.2-23.20240929gitaaca599
- Patchset cleanup

* Fri Oct 25 2024 Phantom X <megaphantomx at hotmail dot com> - 0.2-21.20240929gitaaca599
- Duckstation patchset update

* Mon Sep 02 2024 Phantom X <megaphantomx at hotmail dot com> - 0.2-19.20240615gitaa34b14
- Duckstation patchset update

* Wed Jun 12 2024 Phantom X <megaphantomx at hotmail dot com> - 0.2-17.20240519git86b2720
- PCSX2 modification

* Fri May 31 2024 Phantom X <megaphantomx at hotmail dot com> - 0.2-16.20240519git86b2720
- lzma-sdk rebuild

* Sun Feb 11 2024 Phantom X <megaphantomx at hotmail dot com> - 0.2-14.20240210git2648c22
- BR: libzstd

* Sun Dec 24 2023 Phantom X <megaphantomx at hotmail dot com> - 0.2-13.20230918git9108f34
- Duckstation patchset update

* Thu Nov 09 2023 Phantom X <megaphantomx at hotmail dot com> - 0.2-12.20230918git9108f34
- Duckstation patchset update

* Sun Aug 20 2023 Phantom X <megaphantomx at hotmail dot com> - 0.2-10.20230508git54bfb87
- More patches pulled from Duckstation

* Thu Jun 29 2023 Phantom X <megaphantomx at hotmail dot com> - 0.2-9.20230508git54bfb87
- lzma-sdk rebuild

* Wed Aug 31 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2-1.20220817git9882eea
- 0.2

* Tue Jun 21 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-16.20220523git045f2a7
- lzma-sdk rebuild

* Wed Jun 01 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-15.20220523git045f2a7
- Bump

* Mon Apr 04 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-14.20220209gita03e693
- Add chd_precache_progress patch from Connor McLaughlin

* Sat Feb 19 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-13.20220209gita03e693
- Bump

* Fri Jan 07 2022 Phantom X <megaphantomx at hotmail dot com> - 0.1-12.20220104git8df1fb1
- Update

* Fri Dec 24 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-11.20211127git929a8d6
- Bump

* Fri Nov 26 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-10.20211123git7972daa
- Last one

* Thu Nov 11 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-9.20211108git5de1a59
- Update

* Thu Sep 30 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-8.20210921git9bf1265
- Bump

* Fri Jun 25 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-7.20210609git783f48d
- Last snapshot

* Fri May 07 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-6.20210429git00319cf
- Bump
- New lzma-sdk rebuild

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.1-5.20210410gita17c0da
- Update

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
