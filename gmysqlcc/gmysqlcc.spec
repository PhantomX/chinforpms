Name:           gmysqlcc
Version:        0.3.0
Release:        5%{?dist}
Summary:        GUI client for mysql databases in GTK+

%global pversion %(c=%{version}; echo ${c//./_})

License:        GPLv2
URL:            https://github.com/thepozer/%{name}
Source0:        %{url}/archive/GMYSQLCC_%{pversion}.tar.gz

Source1:         http://http.debian.net/debian/pool/main/g/%{name}/%{name}_0.3.0-6.debian.tar.xz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gtksourceview-2.0)
BuildRequires:  mariadb-devel
Requires:       hicolor-icon-theme

%description
gMySQLcc is designed to be a simple, quick, and powerful way to
access your MySQL database. It provides you a powerful way to
create/edit all MySQL database objects most easy and simple way.

%prep
%autosetup -n %{name}-GMYSQLCC_%{pversion} -a 1

patch -p1 -i debian/patches/dont_override_cflags.patch
patch -p1 -i debian/patches/clang-ftbfs.patch

cp -p %{_datadir}/automake*/mkinstalldirs .

autoreconf -ivf

%build
%configure \
  --disable-debug \
  --disable-silent-rules \
  --with-gtksourceview

%make_build

%install
%make_install INSTALL="install -p"

rm -rf %{buildroot}%{_prefix}/doc

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 debian/%{name}.1 %{buildroot}%{_mandir}/man1/

desktop-file-edit  \
  --remove-key=Encoding \
  --remove-category=Database \
  --add-category=Database \
  --set-icon=%{name} \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

for i in 16 32 48 64 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
  mkdir -p ${dir}
  mv %{buildroot}%{_datadir}/pixmaps/%{name}-${i}.png \
    ${dir}/%{name}.png
done

rm -rf %{buildroot}%{_datadir}/pixmaps

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_mandir}/man1/%{name}.1*


%changelog
* Thu Apr 11 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.3.0-5
- Update Debian patches to tarball style

* Mon Jun 19 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.3.0-4
- Update spec

* Wed Dec 07 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.3.0-3
- Rebuild.

* Fri Nov 11 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.3.0-2
- Rebuild.

* Fri Aug 22 2014 Phantom X <megaphantomx at bol dot com dot br> - 0.3.0-1
- Initial.
