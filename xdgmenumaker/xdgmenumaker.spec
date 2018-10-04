Name:           xdgmenumaker
Version:        1.5
Release:        1%{?dist}
Summary:        Generates application menus using xdg information

License:        GPLv3
URL:            http://www.salixos.org/wiki/index.php/Xdgmenumaker
Source0:        https://github.com/gapan/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Search applications/kde4, applications/wine and support X-Wine in desktop files
Patch0:         %{name}-more-search.patch

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel
BuildRequires:  txt2tags
Requires:       gobject-introspection
Requires:       python3-gobject
Requires:       python3-pillow
Requires:       python3-pyxdg

%description
%{name} is a command line tool, written in python, that generates
application menus using xdg information, by scanning *.desktop files
in all $XDG_DATA_DIRS/applications directories.

%prep
%autosetup -p0

sed -e '/^#!/s|/usr/bin/env python|%{__python3}|1 g' \
  -i src/%{name}

%build
export PREFIX=/usr
%make_build man

%install

export PREFIX=/usr
%make_install

for desktop in %{buildroot}%{_datadir}/desktop-directories/*.directory ;do
  desktop-file-edit \
    --remove-key="Encoding" \
    ${desktop}
done


%files
%license COPYING
%doc AUTHORS README.md
%{_bindir}/%{name}
%{_datadir}/desktop-directories/%{name}-*.directory
%{_mandir}/man1/%{name}.1*


%changelog
* Thu Oct 04 2018 Phantom X <megaphantomx at bol dot com dot br> - 1.5-1
- 1.5

* Sat Jan  7 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.4-1
- Initial spec.
