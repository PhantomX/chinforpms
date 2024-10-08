%global commit b281fda49645c158c2085e1f2e0c3b82c84379ac
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20241001

%global dist .%{date}git%{shortcommit}%{?dist}

%global pkgname soundtouch

Name:           %{pkgname}_ds
Version:        2.3.3
Release:        3%{?dist}
Summary:        Audio Processing library for changing Tempo, Pitch and Playback Rates

License:        LGPL-2.1-or-later
URL:            https://github.com/stenzek/%{pkgname}

Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz

Patch0:         0001-Rename-to-_ds.patch


BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++


%description
SoundTouch is a LGPL-licensed open-source audio processing library for changing
the Tempo, Pitch and Playback Rates of audio streams or files. The SoundTouch
library is suited for application developers writing sound processing tools
that require tempo/pitch control functionality, or just for playing around
with the sound effects.

The SoundTouch library source kit includes an example utility SoundStretch
which allows processing .wav audio files from a command-line interface.

This build is patched for some emulators.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{pkgname}-%{commit} -p1

sed -e '/-Ofast/d' -i CMakeLists.txt

%build
%cmake \
  -G Ninja \
%{nil}

%cmake_build

%install
%cmake_install


%files
%license COPYING.TXT
%doc readme.md
%{_libdir}/lib%{name}.so.*

%files devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/SoundTouch_ds


%changelog
* Mon Sep 16 2024 Phantom X <megaphantomx at hotmail dot com> - 2.3.3-2.20240802git463ade3
- Rename to soundtouch_ds

* Sat Aug 03 2024 Phantom X <megaphantomx at hotmail dot com> - 2.3.3-1.20240802git463ade3
- Initial spec

