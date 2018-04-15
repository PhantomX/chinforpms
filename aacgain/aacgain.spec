%global mp3gainver 1_5_2
%global mp4v2ver 1.9.1
%global faadver 2.7

Name:           aacgain
Version:        1.9
Release:        2%{?dist}
Summary:        Normalizes the volume of digital music AAC files

License:        GPLv2
URL:            http://altosdesign.com/aacgain/
Source0:        http://sbriesen.de/gentoo/distfiles/%{name}-%{version}.tar.xz
Source1:        http://downloads.sourceforge.net/mp3gain/mp3gain-%{mp3gainver}-src.zip
Source2:        https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/mp4v2/mp4v2-%{mp4v2ver}.tar.bz2
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
%setup -c

tar xvf %{SOURCE0}
mkdir mp3gain
unzip %{SOURCE1} -d mp3gain
tar xvf %{SOURCE2}
tar xvf %{SOURCE3}

mv faad2-%{faadver} faad2
mv mp4v2-%{mp4v2ver} mp4v2

cp faad2/COPYING COPYING.faad2
cp faad2/COPYING COPYING.mp4v2
cp mp3gain/lgpl.txt COPYING.mp3gain

sed -i -e 's:iquote :I:' faad2/libfaad/Makefile.am
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

autoreconf -ivf

pushd faad2
  autoreconf -ivf
popd

pushd mp4v2
  patch -p1 -i ../%{name}/mp4v2.patch
  patch -p1 -i %{PATCH0}
popd

%build

%global conf2 --disable-shared --enable-static

pushd faad2
%configure \
  %{conf2} \
  --without-xmms \
  --without-mpeg4ip
popd

pushd mp4v2

CXXFLAGS="%{optflags} -fpermissive" \
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
%doc aacgain/README
%{_bindir}/%{name}


%changelog
* Sat Jun 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.9-2
- -fpermissive

* Wed Jan 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.9-1
- Initial spec
