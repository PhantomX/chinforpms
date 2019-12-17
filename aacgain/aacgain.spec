%global commit 93440798a533ea101ff178689fa6ce6724b253b7
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20191215
%global with_snapshot 1


%global mp3gainver 1_5_2
%global mp4v2ver 4.1.0.0
%global faadver 2.8.8

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           aacgain
Version:        1.9.1
Release:        1%{?gver}%{?dist}
Summary:        Normalizes the volume of digital music AAC files

License:        GPLv2
URL:            http://aacgain.altosdesign.com/
%if 0%{?with_snapshot}
Source0:        https://github.com/dgilman/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        http://sbriesen.de/gentoo/distfiles/%{name}-%{version}.tar.xz
Source1:        http://downloads.sourceforge.net/mp3gain/mp3gain-%{mp3gainver}-src.zip
%endif
Source2:        https://github.com/TechSmith/mp4v2/archive/Release-ThirdParty-MP4v2-%{mp4v2ver}.tar.gz
Source3:        https://downloads.sourceforge.net/faac/faad2-%{faadver}.tar.gz

Patch0:         mp4v2-1.9.1-format-security.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  unzip

Provides:       bundle(libfaad2) = %{faadver}
Provides:       bundle(libmp4v2) = %{mp4v2ver}

%description
Gain normalizes the volume of digital music files using the Replay Gain
algorithm. It works by modifying the global_gain fields in the mp4 samples.
Free-form metadata tags are added to the file to save undo information,
making the normalization process reversable.


%prep
%if 0%{?with_snapshot}
%setup -q -n %{name}-%{commit}
%else
%setup -c

tar xvf %{SOURCE0}
mkdir mp3gain
unzip %{SOURCE1} -d mp3gain
%endif

mkdir faad2 mp4v2
tar xvf %{SOURCE2} --strip-components 1 -C mp4v2
tar xvf %{SOURCE3} --strip-components 1 -C faad2

cp -p faad2/COPYING COPYING.faad2
cp -p faad2/COPYING COPYING.mp4v2
cp -p mp3gain/lgpl.txt COPYING.mp3gain

%if !0%{?with_snapshot}
cp -p aacgain/README .
sed -i -e 's:../\(mp4v2/\):\1:g' %{name}/mp4v2.patch
sed -i -e 's:\(libmp4v2\|libfaad/libfaad\)\.la:README:g' \
  -e 's:^\(autoreconf\|pushd\|popd\):# \1:g' %{name}/linux/prepare.sh

pushd %{name}/linux
  sed -i "s|^patch|#patch|" ./prepare.sh
  sh prepare.sh
popd

pushd mp3gain
  patch -p3 -i ../%{name}/linux/mp3gain.patch
popd
%endif

autoreconf -ivf

pushd faad2
  autoreconf -ivf
popd

%if !0%{?with_snapshot}
pushd mp4v2
  #patch -p1 -i ../%{name}/mp4v2.patch
  patch -p1 -i %{PATCH0}
popd
%endif


%build

%global conf2 --disable-shared --enable-static

pushd faad2
%configure \
  %{conf2} \
  --without-xmms \
  --without-mpeg4ip
popd

pushd mp4v2

CXXFLAGS="%{build_cxxflags} -fpermissive" \
%configure \
  %{conf2} \
  --disable-gch
popd

%configure

pushd faad2/libfaad
%make_build
popd

pushd mp4v2
%make_build
popd

%make_build

%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}/%{name} %{buildroot}%{_bindir}/

%files
%license aacgain/COPYING COPYING.*
%doc README
%{_bindir}/%{name}


%changelog
* Mon Dec 16 2019 Phantom X <megaphantomx at bol dot com dot br> - 1.9.1-1.20191215git9344079
- 1.9.1 dgilman fork

* Sat Jun 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.9-2
- -fpermissive

* Wed Jan 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.9-1
- Initial spec
