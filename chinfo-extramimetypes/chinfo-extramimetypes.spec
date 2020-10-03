Name:           chinfo-extramimetypes
Version:        11.3
Release:        1%{?dist}
Summary:        Extra mimetypes for DEs

License:        GPLv2
URL:            https://github.com/PhantomX/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  shared-mime-info


%description
This package contains extra unusual mimetypes for DEs.

%prep
%autosetup


%build
%cmake \
  -DCHINFO_LEGACY:BOOL=OFF \
%{nil}

%cmake_build


%install

%cmake_install

rm -f %{buildroot}%{_datadir}/mime/packages/%{name}-cdimage.xml


%files
%license COPYING
%doc ChangeLog COPYING
%{_datadir}/mime/packages/%{name}-*.xml


%changelog
* Thu Sep 12 2019 Phantom X <megaphantomx at bol dot com dot br> - 11.3-1
- 11.3

* Thu Jun 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 11.2-1
- 11.2

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 11.1-2
- BR: shared-mime-info

* Fri Mar 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 11.1-1
- Initial spec
