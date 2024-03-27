%global commit 1572ea3e8d50514d3adaba1ad17272f57b5b331c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240325
%bcond_without snapshot

%global commit1 800f5422ac9d9e0ad59cd860a2ef3a679588acb4
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 googletest

%global commit2 aab6948fa863bc1cbe5d0850bc46b9ef02ed4c1a
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 sanitizers-cmake

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           cubeb
Version:        0.2
Release:        46%{?dist}
Summary:        Cross platform audio library

License:        ISC
URL:            https://github.com/mozilla/cubeb

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{name}-%{version}.tar.gz
%endif
Source1:        https://github.com/google/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        https://github.com/arsenm/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz

Patch0:         0001-dep-cubeb-Add-cubeb_get_backend_names.patch
Patch1:         %{url}/pull/768.patch#/%{name}-git-pr768.patch

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(speexdsp)

Requires:       pulseaudio-libs%{?_isa}


%description
%{summary}.


%package devel
Summary:        %{summary} development files
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains the development files libraries needed for
development against %{name} libraries.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

tar -xf %{S:1} -C %{srcname1} --strip-components 1
tar -xf %{S:2} -C cmake/%{srcname2} --strip-components 1

rm -rf src/android
rm -rf subprojects/speex

sed -i -e "/^\[!/d" -e "/INSTALL.md/d" README.md

sed -e '/TYPE DOC/d' -i CMakeLists.txt


%build
%cmake \
  -DCMAKE_BUILD_TYPE:STRING="Release" \
  -DBUILD_TESTS:BOOL=OFF \
  -DUSE_PULSE:BOOL=ON \
  -DUSE_ALSA:BOOL=ON \
  -DUSE_JACK:BOOL=ON \
  -DUSE_SNDIO:BOOL=OFF \
  -DUSE_OPENSL:BOOL=OFF \
  -DUSE_KAI:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install


%files
%license LICENSE
%doc AUTHORS README.md
%{_libdir}/*.so.*

%files devel
%license LICENSE
%doc %{__cmake_builddir}/docs/html/
%{_bindir}/%{name}-test
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/cmake/%{name}/


%changelog
* Sun Aug 07 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2-35.20220721gitdc511c6
- Add cubeb_get_backend_names patch

* Thu Aug 04 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2-34.20220721gitdc511c6
- Bump

* Mon Jul 04 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2-33.20220629git6f79fd7
- Update

* Thu Jun 23 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2-32.20220623git744d638
- Bump
- Remove jack-audio-connection-kit BR

* Tue Apr 26 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2-31.20220413git708f52c
- Update

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2-30.20220325gitd97fea4
- Bump

* Wed Mar 16 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2-29.20220308git6e5b9fe
- Fix speex detection

* Wed Mar 02 2022 Phantom X <megaphantomx at hotmail dot com> - 0.2-28.20220228git3a04ed2
- Update

* Sun Dec 12 2021 Phantom X <megaphantomx at hotmail dot com> - 0.2-27.20211207git773f16b
- Last snapshot

* Mon Nov 08 2021 Phantom X <megaphantomx at hotmail dot com> - 0.2-26.20211105git5d93d2d
- Bump

* Wed Jul 14 2021 Phantom X <megaphantomx at hotmail dot com> - 0.2-25.20210713gitb2f60c9
- Update

* Sun Feb 28 2021 Phantom X <megaphantomx at hotmail dot com> - 0.2-24.20210217git8942382
- New snapshot

* Thu Feb 04 2021 Phantom X <megaphantomx at hotmail dot com> - 0.2-23.20210122git8d53747
- Bump

* Mon Dec 14 2020 Phantom X <megaphantomx at hotmail dot com> - 0.2-22.20201209git860bf2b
- Update

* Sat Nov 28 2020 Phantom X <megaphantomx at hotmail dot com> - 0.2-21.20201116gitdf5fe42
- Bump

* Fri Nov 06 2020 Phantom X <megaphantomx at hotmail dot com> - 0.2-20.20201103git4e851e9
- New snapshot

* Thu Oct 22 2020 Phantom X <megaphantomx at hotmail dot com> - 0.2-19.20201020git1d66483
- Update

* Thu Sep 24 2020 Phantom X <megaphantomx at hotmail dot com> - 0.2-18.20200922git1358724
- Bump

* Sun Sep 13 2020 Phantom X <megaphantomx at hotmail dot com> - 0.2-17.20200913gitf39ce8a
- New snapshot

* Sat Sep 05 2020 Phantom X <megaphantomx at hotmail dot com> - 0.2-16.20200826git98253b2
- Bump

* Sun Jul 05 2020 Phantom X <megaphantomx at hotmail dot com> - 0.2-15.20200703gitea39471
- New snapshot

* Fri Jun 19 2020 Phantom X <megaphantomx at hotmail dot com> - 0.2-14.20200610gite2ffb10
- Bump

* Sat May 30 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.2-13.20200529gitd5b033d
- New snapshot

* Wed Apr 15 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.2-12.20200409git9caa5b1
- Bump

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.2-11.20200228git6e7e765
- New snapshot

* Wed Feb 26 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.2-10.20200212git8fd6845
- Bump

* Sat Feb 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.2-9.20200130git2b79f19
- New snapshot

* Sun Dec 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.2-8.20191212gitaa63601
- New snapshot

* Sun Nov 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.2-7.20191022git1e407d4
- New snapshot

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.2-6.20190916git9eb4c89
- New snapshot

* Sun Sep 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.2-5.20190909git7977798
- New snapshot

* Tue Jul 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.2-4.20190718git0b5b52d
- New snapshot

* Tue Jul 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.2-3.20190601git0d1d9d8
- New snapshot

* Thu May 30 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.2-2.20190516gitb9e2c50
- New snapshot

* Fri Apr 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.2-2.20190416git241e3c7
- Initial spec
