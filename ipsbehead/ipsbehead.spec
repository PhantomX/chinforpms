Name:           ipsbehead
Version:        0.3
Release:        1%{?dist}
Summary:        Utility to remove the SNES ROM header requirement from IPS patches

License:        BSD-2-Clause
URL:            https://github.com/heuripedes/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make


%description
ipsbehead is an utility to adjust IPS patches that require a header in the
target SNES ROM in order to use these patches with a headerless SNES ROM. It
does so by discarding any alterations before 0x200 and recalculating offsets
of the other records.


%prep
%autosetup

sed \
  -e 's|CFLAGS=|CFLAGS+=|' \
  -e 's|-Wall -O2 -g ||g' \
  -i Makefile


%build
%make_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}


%changelog
* Fri May 14 2021 Phantom X <megaphantomx at hotmail dot com> - 0.3-1
- Initial spec

