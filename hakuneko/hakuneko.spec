Name:           hakuneko
Version:        1.4.2
Release:        1%{?dist}
Summary:        manga Downloader

License:        MIT
URL:            http://sourceforge.net/projects/hakuneko/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}_%{version}_src.tar.gz

BuildRequires:  wxGTK3-devel curl-devel openssl-devel
Requires:       hicolor-icon-theme

%description
HakuNeko allows you to download manga images from some selected online
manga reader websites.

%prep
%autosetup -n %{name}_%{version}_src

find . -name '*.a' -print -delete

%{__sed} -i \
  -e "s|-O2|%{optflags}|g" \
  -e '/LDFLAGS=/s|\"-s\"|"%{__global_ldflags}"|g' \
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

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license LICENSE
%doc README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%changelog
* Sun Feb 26 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4.2-1
- 1.4.2

* Sat Oct 15 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.4.1
- First spec.
