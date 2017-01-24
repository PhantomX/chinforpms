Name:           firetools
Version:        0.9.44
Release:        1%{?dist}
Summary:        GUI tools for firejail

License:        GPLv2
URL:            https://firejail.wordpress.com/
Source0:        http://downloads.sourceforge.net/firejail/%{name}-%{version}.tar.bz2

BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(Qt5Svg)
Requires:       firejail
Requires:       hicolor-icon-theme

%description
Firetools is the graphical user interface of Firejail security sandbox.

%prep
%autosetup

sed \
  -e '/strip \*;/d' \
  -e '/$(DOCDIR)/d' \
  -i Makefile.in

%build
%configure \
  --with-qmake=%{_qt5_qmake}
%make_build


%install
rm -rf %{buildroot}
%make_install \
<<<<<<< HEAD
  STRIP=/bin/true
=======
  STRIP=/bin/true DOCDIR=/dev/null
>>>>>>> 9b6ea099155fd2da0b07a2a287d1c1f5e923a530

rm -rf %{buildroot}/usr/share/doc

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

for res in 16 20 22 24 32 36 48 64 72 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert src/firetools/resources/%{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%license COPYING
%doc README RELNOTES
%{_bindir}/%{name}
%{_bindir}/firemgr
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/pixmaps/*.png
%{_mandir}/man1/*.1*

%changelog
* Mon Jan 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.44-1
- Initial spec.
