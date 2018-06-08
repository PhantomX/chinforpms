Name:           chinfo-extramimetypes
Version:        11.2
Release:        1%{?dist}
Summary:        Extra mimetypes for DEs

License:        GPLv2
URL:            https://github.com/PhantomX/%{name}
Source0:        %{url}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  shared-mime-info


%description
This package contains extra unusual mimetypes for DEs.

%prep
%autosetup


%build
mkdir build
pushd build
%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DCHINFO_LEGACY:BOOL=OFF

%make_build

popd

%install

%make_install -C build

rm -f %{buildroot}%{_datadir}/mime/packages/%{name}-cdimage.xml


%files
%license COPYING
%doc ChangeLog COPYING
%{_datadir}/mime/packages/%{name}-*.xml


%changelog
* Thu Jun 07 2018 Phantom X <megaphantomx at bol dot com dot br> - 11.2-1
- 11.2

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 11.1-2
- BR: shared-mime-info

* Fri Mar 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 11.1-1
- Initial spec
