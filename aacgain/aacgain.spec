%global commit 0421ca2b5f9a50bc2408b983eb8c807aebaf0f2a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200102
%bcond snapshot 1

%global commit1 a65ecabd13a6b991781d75856e1b6870ce00fc70
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 faad2

%global commit2 cf634bb7ed2d3bd453d707a5c7896dcd6f12e458
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 mp4v2

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url  https://github.com/dgilman

Name:           aacgain
Version:        2.0.0
Release:        1%{?dist}
Summary:        Normalizes the volume of digital music AAC files

License:        GPL-2.0-only
URL:            http://aacgain.altosdesign.com/

%if %{with snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{vc_url}/%{srcname1}/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        %{vc_url}/%{srcname2}/archive/%{commit2}/%{srcname2}-%{shortcommit2}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  make

Provides:       bundle(libfaad2) = 0~git
Provides:       bundle(libmp4v2) = 0~git


%description
Gain normalizes the volume of digital music files using the Replay Gain
algorithm. It works by modifying the global_gain fields in the mp4 samples.
Free-form metadata tags are added to the file to save undo information,
making the normalization process reversable.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

pushd 3rdparty
sed \
  -e '/ProcessorCount/d' \
  -e 's|${N}|%{_smp_build_ncpus}|g' \
  -i CMakeLists.txt


tar -xf %{S:1} -C faad2 --strip-components 1
tar -xf %{S:2} -C mp4v2 --strip-components 1

cp -p faad2/COPYING ../COPYING.faad2
cp -p faad2/COPYING ../COPYING.mp4v2
popd
cp -p mp3gain/lgpl.txt COPYING.mp3gain


%build
%cmake \
%{nil}

%cmake_build


%install
%cmake_install


%files
%license aacgain/COPYING COPYING.*
%doc README
%{_bindir}/%{name}


%changelog
* Sat Feb 01 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.0.0-1.20200102git0421ca2
- 2.0.0
- cmake
- Remove old release support

* Mon Dec 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.9.1-1.20191215git9344079
- 1.9.1 dgilman fork

* Sat Jun 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.9-2
- -fpermissive

* Wed Jan 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.9-1
- Initial spec
