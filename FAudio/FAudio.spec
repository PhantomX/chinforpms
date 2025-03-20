%global commit 7eca833536c3e938a67f35bae57d7436c00f0875
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210707
%bcond_with snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           FAudio
Version:        25.03
Release:        100%{?dist}
Summary:        Accuracy-focused XAudio reimplementation

Epoch:          1

License:        Zlib
URL:            https://fna-xna.github.io/

%global vc_url  https://github.com/FNA-XNA/%{name}
%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif


BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(sdl2)


%description
FAudio is a XAudio reimplementation that focuses solely on developing
fully accurate DirectX Audio runtime libraries for the FNA project,
including XAudio2, X3DAudio, XAPO, and XACT3.


%package -n lib%{name}
Summary:        %{summary}
Provides:       faudio = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       faudio%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      faudio < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n lib%{name}
This is FAudio, an XAudio reimplementation that focuses solely on developing
fully accurate DirectX Audio runtime libraries for the FNA project, including
XAudio2, X3DAudio, XAPO, and XACT3.


%package -n lib%{name}-devel
Summary:        Development files for the FAudio library
Requires:       lib%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       faudio-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       faudio-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n lib%{name}-devel
Development files for the FAudio library.


%prep
%if %{with snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -p1
%endif


%build
%cmake \
  -DCMAKE_INSTALL_INCLUDEDIR:PATH=include/%{name} \
  -DGSTREAMER:BOOL=ON \
  -DBUILD_SDL3:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install

ln -sf %{name}.pc %{buildroot}%{_libdir}/pkgconfig/faudio.pc


%files -n lib%{name}
%license LICENSE
%doc README
%{_libdir}/*.so.*

%files -n lib%{name}-devel
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 1:25.03-100
- 25.03

* Sat Feb 08 2025 Phantom X <megaphantomx at hotmail dot com> - 1:25.02-100
- 25.02

* Sat Jan 11 2025 Phantom X <megaphantomx at hotmail dot com> - 1:25.01-100
- 25.01

* Sun Nov 10 2024 Phantom X <megaphantomx at hotmail dot com> - 1:24.11-100
- 24.11

* Wed Oct 02 2024 Phantom X <megaphantomx at hotmail dot com> - 1:24.10-100
- 24.10

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 1:24.09-100
- 24.09

* Mon Jun 03 2024 Phantom X <megaphantomx at hotmail dot com> - 1:24.06-100
- 24.06

* Fri May 10 2024 Phantom X <megaphantomx at hotmail dot com> - 1:24.05-100
- 24.05

* Fri Apr 05 2024 Phantom X <megaphantomx at hotmail dot com> - 1:24.04-100
- 24.04

* Tue Mar 05 2024 Phantom X <megaphantomx at hotmail dot com> - 1:24.03-100
- 24.03

* Fri Feb 09 2024 Phantom X <megaphantomx at hotmail dot com> - 1:24.02-100
- 24.02

* Thu Nov 02 2023 Phantom X <megaphantomx at hotmail dot com> - 1:23.11-100
- 23.11

* Sat Sep 02 2023 Phantom X <megaphantomx at hotmail dot com> - 1:23.09-100
- 23.09

* Tue Aug 01 2023 Phantom X <megaphantomx at hotmail dot com> - 1:23.08-100
- 23.08

* Mon Jul 03 2023 Phantom X <megaphantomx at hotmail dot com> - 1:23.07-100
- 23.07

* Fri Jun 02 2023 Phantom X <megaphantomx at hotmail dot com> - 1:23.06-100
- 23.06

* Thu May 04 2023 Phantom X <megaphantomx at hotmail dot com> - 1:23.05-100
- 23.05

* Sun Apr 02 2023 Phantom X <megaphantomx at hotmail dot com> - 1:23.04-100
- 23.04

* Thu Feb 02 2023 Phantom X <megaphantomx at hotmail dot com> - 1:23.02-100
- 23.02

* Sat Nov 05 2022 Phantom X <megaphantomx at hotmail dot com> - 1:22.11-100
- 22.11

* Fri Sep 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1:22.09.01-100
- 22.09.01

* Tue Aug 02 2022 Phantom X <megaphantomx at hotmail dot com> - 1:22.08-100
- 22.08

* Thu Jul 28 2022 Phantom X <megaphantomx at hotmail dot com> - 1:22.07-100
- 22.07

* Wed Nov 03 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.11-100
- 21.11

* Sat Oct 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.10-100
- 21.10

* Wed Sep 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.09-100
- 21.09

* Sun Aug 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.08-100
- 21.08

* Fri Jul 09 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.07-101.20210707git7eca833
- Snapshot

* Thu Jul 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.07-100
- 21.07

* Tue Jun 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.06-100
- 21.06

* Sat May 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.05-100
- 21.05

* Thu Apr 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.04-100
- 21.04

* Mon Mar 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.03.05-101.20210321git920d222
- Bump

* Fri Mar 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.03.05-100.20210312git116e9b0
- 21.03.05

* Mon Mar 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.03-100
- 21.03

* Mon Feb 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.02-100
- 21.02

* Tue Jan 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.01-101.20210125git8b105a8
- Snapshot

* Sat Jan 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.01-100
- 21.01

* Thu Dec 10 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.12-101
- Remove unneeded patch

* Tue Dec 01 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.12-100
- 20.12
- Upstream pkgconfig file

* Mon Nov  2 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.11-100
- 20.11

* Fri Oct 02 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.10-100
- 20.10

* Tue Sep 01 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.09-100
- 20.09

* Thu Aug 13 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.08-102.20200812gitf710ff5
- Bump

* Wed Aug 05 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.08-101.20200805git242a111
- Snapshot

* Sat Aug 01 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.08-100
- 20.08

* Wed Jul 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.07-101.20200729git7f52bfb
- Snapshot

* Wed Jul 01 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.07-100
- 20.07
- Enable experimental GStreamer support

* Tue Jun 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.06-100
- 20.06

* Fri May 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.05-100
- 20.05

* Wed Apr 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.04-100
- 20.04

* Mon Mar 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.03-100
- 20.03

* Sat Feb 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.02-100
- 20.02

* Fri Jan 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.01-100
- 20.01

* Tue Dec 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.12-100
- 19.12

* Sat Nov 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.11-100
- 19.11

* Wed Oct 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.10-100
- 19.10

* Tue Sep 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.09-100
- 19.09

* Sat Aug 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.08-100
- 19.08

* Mon Jul 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.07-100
- 19.07

* Wed Jun 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.06.07-100.20190609git68b13c1
- 19.06.07

* Sat Jun 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.06-100
- 19.06

* Fri May 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.05-101.20190523gitc724fb2
- 19.05 snapshot

* Fri May 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.05-100
- 19.05

* Mon Apr 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.04-100
- 19.04

* Tue Mar 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.03-100
- Sync with Fedora

* Fri Mar 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.03-1
- 19.03
- Drop unneeded soversion patch

* Mon Feb 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.02-1
- 19.02

* Fri Jan 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.01-1
- Initial spec
