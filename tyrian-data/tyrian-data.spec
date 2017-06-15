Name:           tyrian-data
Version:        2.1
Release:        1%{?dist}
Summary:        Tyrian data files

License:        Redistributable
URL:            https://www.camanis.net/
%global pver %(c=%{version}; echo ${c//\.})
Source0:        http://camanis.net/tyrian/tyrian%{pver}.zip

BuildArch:      noarch

Requires:       opentyrian

%description
%{summary}.

%prep
%autosetup -n tyrian%{pver}


%build

%install
mkdir -p %{buildroot}%{_datadir}/tyrian
rm -f *.exe
rm -f setup.*

install -m0644 * %{buildroot}%{_datadir}/tyrian/

%files
%dir %{_datadir}/tyrian
%{_datadir}/tyrian/*


%changelog
* Sun Jan 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1-1
- Initial spec
