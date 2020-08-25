Name:           fcrackzip
Version:        1.0
Release:        1%{?dist}
Summary:        Password cracker for zip archives

License:        GPLv2
URL:            http://oldhome.schmorp.de/marc/%{name}.html

Source0:        http://oldhome.schmorp.de/marc/data/%{name}-%{version}.tar.gz
Source1:        http://archive.ubuntu.com/ubuntu/pool/universe/f/fcrackzip/fcrackzip_1.0-9.debian.tar.xz

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  gcc
Requires:       unzip


%description
fcrackzip is a fast password cracker partly written in assembler. It is able to
crack password protected zip files with brute force or dictionary based attacks,
optionally testing with unzip its results. It can also crack cpmask'ed images.


%prep
%autosetup -a 1

for i in $(<debian/patches/series);do
  patch -p1 -F1 -s -i debian/patches/$i
done

sed -e '/funroll/d' -i configure.in

mv configure.in configure.ac
autoreconf -ivf


%build
%configure
%make_build


%install
%make_install

mv %{buildroot}%{_bindir}/zipinfo %{buildroot}%{_bindir}/fcrack-zipinfo


%files
%license COPYING
%doc AUTHORS NEWS README THANKS
%{_bindir}/%{name}
%{_bindir}/fcrack-zipinfo
%{_mandir}/man1/%{name}.1*


%changelog
* Tue Aug 25 2020 Phantom X <megaphantomx at hotmail dot com> - 1.0-1
- Initial spec
