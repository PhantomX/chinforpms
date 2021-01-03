%global commit f710ff552869c8a47b05db9522eb3806f8fee020
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200812
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           FAudio
Version:        21.01
Release:        100%{?gver}%{?dist}
Summary:        Accuracy-focused XAudio reimplementation

Epoch:          1

License:        zlib
URL:            https://fna-xna.github.io/

%global vc_url  https://github.com/FNA-XNA/%{name}
%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
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
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -p1
%endif


%build
%cmake \
  -DCMAKE_INSTALL_INCLUDEDIR:PATH=include/%{name} \
  -DGSTREAMER:BOOL=ON \
%{nil}

%cmake_build


%install
%cmake_install

ln -sf %{name}.pc %{buildroot}%{_libdir}/pkgconfig/faudio.pc


%files -n lib%{name}
%license LICENSE
%doc README README.gstreamer
%{_libdir}/*.so.*

%files -n lib%{name}-devel
%{_includedir}/%{name}/
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
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
