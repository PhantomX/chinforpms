%global commit c724fb28c784fee8d9db2f784e1f55b5ce6710fb
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190523
%global with_snapshot 0

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           FAudio
Version:        19.06
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
Source1:        %{name}.pc

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
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

cp -p %{S:1} .
sed \
  -e 's|_LIB_|%{_lib}|g' \
  -e 's|_VERSION_|%{version}|g' \
  -i %{name}.pc


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DCMAKE_INSTALL_INCLUDEDIR:PATH=include/%{name} \
  -DFFMPEG:BOOL=OFF \
%{nil}

%make_build
popd


%install
%make_install -C %{_target_platform}

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -pm0644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/
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
