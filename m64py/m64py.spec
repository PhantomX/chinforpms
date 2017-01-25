Name:           m64py
Version:        0.2.3
Release:        2%{?dist}
Summary:        A frontend for Mupen64Plus 2.0

License:        GPLv3
URL:            http://m64py.sourceforge.net
Source0:        https://github.com/mupen64plus/mupen64plus-ui-python/releases/download/%{version}/%{name}-%{version}.tar.gz

Patch0:         %{name}-0.2.3-path.patch
Patch1:         %{name}-0.2.3-libdir.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python-qt5-devel
BuildRequires:  ImageMagick
Requires:       mupen64plus
Requires:       python-qt5
Requires:       SDL2

%description
M64Py is a Qt5 front-end (GUI) for Mupen64Plus 2.0, a cross-platform
plugin-based Nintendo 64 emulator.


%prep
%autosetup -p0

sed -e 's,^#!/usr/bin/env python,#!%{__python3},' -i %{name}

find -name '*.py' -print0 | xargs -0 \
  sed -i -e 's,^#!/usr/bin/env python,#!%{__python3},'

%build
%{__python3} setup.py build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a src/m64py/* %{buildroot}%{_datadir}/%{name}/

find %{buildroot}%{_datadir}/%{name}/ -name '*.py' -print0 | xargs -0 chmod 0755

find %{buildroot} -name '*.orig' -delete

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key="MimeType" \
  --add-category="Qt" \
  xdg/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/96x96/apps
install -pm0644 xdg/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/96x96/apps/

for res in 16 20 22 24 32 36 48 64 72 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert xdg/%{name}.png -filter Lanczos -resize ${res}x${res} \
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
%license COPYING LICENSES
%doc AUTHORS README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%changelog
* Tue Jan 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.2.3-2
- Fixed shebangs

* Thu Jan  5 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.2.3-1
- Initial spec.
