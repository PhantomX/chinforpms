%global commit 241e3c7b8a6ce76ad9e075ee5761cd4d0906bc16
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190416
%global with_snapshot 1

%global commit1 800f5422ac9d9e0ad59cd860a2ef3a679588acb4
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 googletest

%global commit2 aab6948fa863bc1cbe5d0850bc46b9ef02ed4c1a
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 sanitizers-cmake

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           cubeb
Version:        0.2
Release:        1%{?gver}%{?dist}
Summary:        Cross platform audio library

License:        ISC
URL:            https://github.com/kinetiknz/cubeb

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{name}-%{version}.tar.gz
%endif #{?with_snapshot}
Source1:        https://github.com/google/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        https://github.com/arsenm/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz

Patch0:         0001-Add-soversion-to-library.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(libpulse)

Requires:       jack-audio-connection-kit%{?_isa}
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
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

tar -xf %{S:1} -C %{srcname1} --strip-components 1
tar -xf %{S:2} -C cmake/%{srcname2} --strip-components 1

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}

%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DBUILD_TESTS:BOOL=OFF \
  -DUSE_PULSE:BOOL=ON \
  -DUSE_ALSA:BOOL=ON \
  -DUSE_JACK:BOOL=ON \
  -DUSE_SNDIO:BOOL=OFF \
  -DUSE_OPENSL:BOOL=OFF \
  -DUSE_KAI:BOOL=OFF \
%{nil}

%make_build


%install
%make_install -C %{_target_platform}


%files
%license LICENSE
%doc AUTHORS README.md
%{_bindir}/%{name}-test
%{_libdir}/*.so.*

%files devel
%license LICENSE
%doc %{_target_platform}/docs/html/
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/cmake/%{name}/


%changelog
* Fri Apr 19 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.2-2.20190416git241e3c7
- Initial spec
