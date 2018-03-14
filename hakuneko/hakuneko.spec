Name:           hakuneko
Version:        1.4.2
Release:        3%{?dist}
Summary:        manga Downloader

License:        MIT
URL:            http://sourceforge.net/projects/legacy.hakuneko.p/
Source0:        http://downloads.sourceforge.net/legacy.%{name}.p/%{name}_%{version}_src.tar.gz

Patch0:         %{name}-noupdate.patch

BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  desktop-file-utils
BuildRequires:  wxGTK3-devel
Requires:       hicolor-icon-theme

%description
HakuNeko allows you to download manga images from some selected online
manga reader websites.

%prep
%autosetup -n %{name}_%{version}_src -p1

find . -name '*.a' -print -delete

%{__sed} -i \
  -e "s|-O2|%{optflags}|g" \
  -e '/LDFLAGS=/s|\"-s\"|"%{build_ldflags}"|g' \
  configure config_default.sh

%build
%configure
%make_build


%install

%make_install

rm -rf %{buildroot}%{_datadir}/doc
rm -rf %{buildroot}%{_datadir}/menu
rm -rf %{buildroot}%{_datadir}/pixmaps

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license LICENSE
%doc README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%changelog
* Thu Sep 14 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4.2-3
- Disable update checking

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4.2-2
- Update links

* Sun Feb 26 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4.2-1
- 1.4.2

* Sat Oct 15 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.4.1
- First spec.
