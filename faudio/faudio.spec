%global pkgname FAudio

Name:           faudio
Version:        19.02
Release:        1%{?dist}
Summary:        Accuracy-focused XAudio reimplementation

License:        zlib
URL:            https://github.com/FNA-XNA/FAudio

Source0:        %{url}/archive/%{version}/%{pkgname}-%{version}.tar.gz
Source1:        %{name}.pc

Patch0:         %{name}-soversion.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(sdl2)


%description
FAudio is a XAudio reimplementation that focuses solely on developing
fully accurate DirectX Audio runtime libraries for the FNA project,
including XAudio2, X3DAudio, XAPO, and XACT3.


%package devel
Summary:        %{summary} development files
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
The %{name}-devel package contains the development files needed for 
development with %{name} library.


%prep
%autosetup -n %{pkgname}-%{version} -p1

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
  -DCMAKE_INSTALL_INCLUDEDIR:PATH=include/%{pkgname} \
  -DFFMPEG:BOOL=OFF \
%{nil}

%make_build
popd


%install
%make_install -C %{_target_platform}

mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -pm0644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/


%files
%license LICENSE
%doc README
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{pkgname}/
%{_libdir}/cmake/%{pkgname}/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so


%changelog
* Mon Feb 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.02-1
- 19.02

* Fri Jan 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 19.01-1
- Initial spec
