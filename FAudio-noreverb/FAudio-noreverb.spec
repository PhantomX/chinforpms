%global commit 920d2228c982f9a2f97276f2e51fbf8ed507963c
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210321
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname FAudio

Name:           %{pkgname}-noreverb
Version:        21.04
Release:        1%{?gver}%{?dist}
Summary:        Accuracy-focused XAudio reimplementation - noreverb
Epoch:          1

License:        zlib
URL:            https://fna-xna.github.io/

%global vc_url  https://github.com/FNA-XNA/%{pkgname}
%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch0:         0001-Disable-reverb.patch

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

This version is compiled without reverb support, for slow systems.


%package -n lib%{name}
Summary:        %{summary}
Requires:       lib%{pkgname}%{?_isa}
Provides:       lib%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       lib%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n lib%{name}
This is FAudio, an XAudio reimplementation that focuses solely on developing
fully accurate DirectX Audio runtime libraries for the FNA project, including
XAudio2, X3DAudio, XAPO, and XACT3.

This version is compiled without reverb support, for slow systems.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -n %{pkgname}-%{version} -p1
%endif


%build
%cmake \
  -DCMAKE_INSTALL_INCLUDEDIR:PATH=include/%{name} \
  -DGSTREAMER:BOOL=ON \
%{nil}

%cmake_build


%install
%cmake_install

rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_libdir}/cmake
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -f %{buildroot}%{_libdir}/*.so

mkdir -p %{buildroot}%{_libdir}/%{name}
mv %{buildroot}%{_libdir}/*.so.* %{buildroot}%{_libdir}/%{name}/

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/%{name}" \
  > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files -n lib%{name}
%license LICENSE
%doc README
%{_libdir}/%{name}/*.so.*
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf


%changelog
* Thu Apr 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.04-1
- 21.04

* Mon Mar 22 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.03.05-1.20210321git920d222
- Bump

* Fri Mar 12 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.03.05-1.20210312git116e9b0
- 21.03.05

* Mon Mar 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.03-1
- 21.03

* Mon Feb 01 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.02-1
- 21.02

* Tue Jan 26 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.01-2.20210125git8b105a8
- Snapshot

* Sat Jan 02 2021 Phantom X <megaphantomx at hotmail dot com> - 1:21.01-1
- 21.01

* Thu Dec 10 2020 Phantom X <megaphantomx at hotmail dot com> - 20.12-1
- Initial spec
