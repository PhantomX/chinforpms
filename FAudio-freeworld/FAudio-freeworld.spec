%global pkgname FAudio

Name:           %{pkgname}-freeworld
Version:        19.04
Release:        1%{?dist}
Summary:        Accuracy-focused XAudio reimplementation - freeworld
Epoch:          1

License:        zlib
URL:            https://fna-xna.github.io/

Source0:        https://github.com/FNA-XNA/%{pkgname}/archive/%{version}/%{pkgname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
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
%autosetup -n %{pkgname}-%{version} -p1


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DCMAKE_INSTALL_INCLUDEDIR:PATH=include/%{pkgname} \
  -DFFMPEG:BOOL=ON \
%{nil}

%make_build
popd


%install
%make_install -C %{_target_platform}

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
