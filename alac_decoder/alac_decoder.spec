Name:           alac_decoder
Version:        0.2.0
Release:        1%{?dist}
Summary:        Basic decoder for Apple Lossless Audio Codec files

License:        GPLv2
URL:            http://craz.net/programs/itunes/alac.html
Source0:        ftp://ftp.ussg.iu.edu/pub/linux/gentoo/distfiles/%{name}-%{version}.tgz

%description
alac_decoder is a basic decoder for Apple Lossless Audio Codec files
(ALAC). ALAC is a proprietary lossless audio compression scheme. Apple
never released any documents on the format.


%prep
%autosetup -n %{name}

sed \
  -e "/^CFLAGS=/s|=|?=|g" \
  -e "s:\(-o alac\):\$(LDFLAGS) \1:g" \
  -i Makefile

%build

export CFLAGS="%{optflags}"
export LDFLAGS="%{__global_ldflags}"

%make_build


%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 alac %{buildroot}%{_bindir}/


%files
%doc README
%{_bindir}/alac


%changelog
* Wed Jan 25 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.2.0-1
- Initial spec
