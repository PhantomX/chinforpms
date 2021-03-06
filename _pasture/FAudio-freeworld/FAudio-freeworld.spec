%global commit f51d5dfd02f40b91ae44fa5002c163f8750d9949
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200729
%global with_snapshot 1

# Disable reverb for slow systems
%global without_reverb 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname FAudio

Name:           %{pkgname}-freeworld
Version:        20.07
Release:        4%{?gver}%{?dist}
Summary:        Accuracy-focused XAudio reimplementation - freeworld
Epoch:          1

License:        zlib
URL:            https://fna-xna.github.io/

%global vc_url  https://github.com/FNA-XNA/%{pkgname}
%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

%if 0%{?without_reverb}
Patch0:         0001-Disable-reverb.patch
%endif

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswresample)
BuildRequires:  pkgconfig(sdl2)


%description
FAudio is a XAudio reimplementation that focuses solely on developing
fully accurate DirectX Audio runtime libraries for the FNA project,
including XAudio2, X3DAudio, XAPO, and XACT3.

This version is compiled with ffmpeg support.


%package -n lib%{name}
Summary:        %{summary}
Requires:       lib%{pkgname}%{?_isa}
Provides:       lib%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       faudio-freeworld = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       faudio-freeworld%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      faudio-freeworld < %{?epoch:%{epoch}:}%{version}-%{release}

%description -n lib%{name}
This is FAudio, an XAudio reimplementation that focuses solely on developing
fully accurate DirectX Audio runtime libraries for the FNA project, including
XAudio2, X3DAudio, XAPO, and XACT3.

This version is compiled with ffmpeg support.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif


%build
%cmake \
  -DCMAKE_INSTALL_INCLUDEDIR:PATH=include/%{pkgname} \
  -DFFMPEG:BOOL=ON \
%{nil}

%cmake_build


%install
%cmake_install

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}/cmake
rm -rf %{buildroot}%{_libdir}/*.so

mkdir -p %{buildroot}%{_libdir}/%{name}
mv %{buildroot}%{_libdir}/*.so.* %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/%{name}" \
  > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%files -n lib%{name}
%license LICENSE
%doc README
%{_libdir}/%{name}/*.so.*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%changelog
* Thu Dec 10 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.07-4.20200729gitf51d5df
- Switch to disable reverb
- Remove unneeded patch

* Mon Nov 30 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.07-3.20200729gitf51d5df
- Winehq bug 48791 fix try

* Wed Jul 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.07-2.20200729gitf51d5df
- Last snapshot with ffmpeg support

* Wed Jul 01 2020 Phantom X <megaphantomx at hotmail dot com> - 1:20.07-100
- 20.07

* Tue Jun 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.06-1
- 20.06

* Fri May 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.05-1
- 20.05

* Wed Apr 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.04-1
- 20.04

* Mon Mar 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.03-1
- 20.03

* Sat Feb 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.02-1
- 20.02

* Fri Jan 03 2020 Phantom X <megaphantomx at bol dot com dot br> - 1:20.01-1
- 20.01

* Tue Dec 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.12-1
- 19.12

* Sat Nov 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.11-1
- 19.11

* Wed Oct 02 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.10-1
- 19.10

* Tue Sep 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.09-1
- 19.09

* Sat Aug 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.08-1
- 19.08

* Mon Jul 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.07-1
- 19.07

* Wed Jun 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.06.07-1.20190609git68b13c1
- 19.06.07

* Sat Jun 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.06-1
- 19.06

* Fri May 24 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.05-2.20190523gitc724fb2
- 19.05 snapshot

* Fri May 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.05-1
- 19.05

* Mon Apr 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.04-1
- 19.04

* Tue Mar 05 2019 Phantom X <megaphantomx at bol dot com dot br> - 1:19.03-2
- Rename

* Fri Mar 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.03-1
- 19.03
- Drop unneeded soversion patch

* Mon Feb 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.02-1
- 19.02

* Fri Jan 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.01-1
- Initial spec
