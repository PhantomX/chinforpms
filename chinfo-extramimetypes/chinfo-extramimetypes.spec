Name:           chinfo-extramimetypes
Version:        11.1
Release:        1%{?dist}
Summary:        Extra mimetypes for DEs

License:        GPLv2
URL:            http://github.com/PhantomX/%{name}
Source0:        http://dl.bintray.com/phantomx/tarballs/%{name}-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  cmake
Requires(postun): shared-mime-info
Requires(posttrans): shared-mime-info

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

%post
touch --no-create %{_datadir}/mime/packages &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/mime/packages &>/dev/null || :
  update-mime-database %{_datadir}/mime &>/dev/null || :
fi

%posttrans
update-mime-database %{?fedora:-n} %{_datadir}/mime &>/dev/null || :

%files
%license COPYING
%doc ChangeLog COPYING
%{_datadir}/mime/packages/%{name}-*.xml


%changelog
* Fri Mar 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 11.1-1
- Initial spec
