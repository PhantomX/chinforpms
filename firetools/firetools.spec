Name:           firetools
Version:        0.9.72
Release:        1%{?dist}
Summary:        GUI tools for firejail

License:        GPL-2.0-only
URL:            https://firejail.wordpress.com/
Source0:        https://downloads.sourceforge.net/firejail/%{name}-%{version}.tar.xz

Patch0:         0001-fstats-replace-link-flags-to-fix-linking.patch

BuildRequires:  make
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  ImageMagick
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Svg)
Requires:       firejail
Requires:       hicolor-icon-theme

%description
Firetools is the graphical user interface of Firejail security sandbox.

%prep
%autosetup -p1

sed \
  -e '/strip \*;/d' \
  -e '/$(DOCDIR)/d' \
  -e 's|/$(PREFIX)/lib/|@libdir@/|g' \
  -i Makefile.in

sed -e 's|-lrt|-pthread \0|g' -i src/fstats/fstats.pro


%build
%configure \
  --with-qmake=%{_qt5_qmake}
%make_build DESTDIR=


%install
%make_install \
  STRIP=/bin/true

rm -rf %{buildroot}/usr/share/doc

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-edit \
  --remove-category=Utility \
  --add-category=System \
   %{buildroot}%{_datadir}/applications/firejail-ui.desktop

for res in 16 22 24 32 36 48 64 72 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  magick src/firetools/resources/%{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
  magick src/firejail-ui/resources/firejail-ui.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/firejail-ui.png
done


%files
%license COPYING
%doc README RELNOTES
%{_bindir}/%{name}
%{_bindir}/firejail-ui
%{_libdir}/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/pixmaps/*.png
%{_mandir}/man1/*.1*

%changelog
* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 0.9.72-1
- 0.9.72

* Mon Nov 15 2021 Phantom X <megaphantomx at hotmail dot com> - 0.9.64-1
- 0.9.64

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.9.62-1
- 0.9.62

* Tue Apr 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.9.52-1
- 0.9.52

* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.50-1
- 0.9.50

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.46-2
- BR: ImageMagick

* Tue May 09 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.46-1
- new version

* Mon Jan 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.9.44-1
- Initial spec.
