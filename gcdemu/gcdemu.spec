%global debug_package %{nil}

Name:           gcdemu
Version:        3.2.6
Release:        1%{?dist}
Summary:        Gtk3-based CDEmu client

License:        GPLv2
URL:            https://cdemu.sourceforge.io/
Source0:        https://downloads.sourceforge.net/cdemu/%{name}-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  intltool
BuildRequires:  librsvg2-tools
BuildRequires:  /usr/bin/pathfix.py
BuildRequires:  python3-devel
Requires:       python3
Requires:       python3-gobject
Requires:       gobject-introspection
Requires:       gtk3
Requires:       gdk-pixbuf2
Requires:       libnotify
Requires:       hicolor-icon-theme

%description
gCDEmu is a Gtk3-based client for controlling CDEmu devices. It is part
of CDEmu, a CD/DVD-ROM device emulator for Linux.

%prep
%autosetup

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" src/%{name}


%build
%cmake \
  -DPOST_INSTALL_HOOKS:BOOL=OFF \
%{nil}

%cmake_build


%install
%cmake_install

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
ln -sf ../../../../pixmaps/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert data/%{name}.svg -h ${res} -w ${res} \
    -o ${dir}/%{name}.png
done

%find_lang %{name}


%files -f %{name}.lang
%license COPYING
%doc AUTHORS README ChangeLog
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.svg
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/icons/hicolor/*/*/%{name}*


%changelog
* Mon Nov 01 2021 Phantom X <megaphantomx at hotmail dot com> - 3.2.6-1
- 3.2.6

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 3.2.5-1
- 3.2.5

* Mon Feb 24 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.2.4-1
- 3.2.4

* Sun Sep 01 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.2.3-1
- 3.2.3

* Tue Aug 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.2.2-1
- 3.2.2

* Sun Mar 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.2.1-1
- 3.2.1

* Wed Jul 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.2.0-1
- 3.2.0

* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.1.0-2
- chinforpms release

* Sat Jun 10 2017 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.1.0-1
- Updated to 3.1.0

* Tue Oct 11 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.3-1
- Updated to 3.0.3

* Sun Oct  9 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.2-1
- Updated to 3.0.2

* Sat Apr 23 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.1-4
- Fixed rpmlint errors and warnings
- Added desktop-file-utils dependency

* Thu Apr 21 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.1-3
- Added python2-devel as build dependency, to satisfy CMake check
- Dropped glib2 explicit dependency
- Use noarch

* Thu Apr 21 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.1-2
- Changed python dependency to python2

* Sat Nov 21 2015 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.1-1
- Updated to 3.0.1

* Sun Jun 29 2014 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.0-1
- Updated to 3.0.0

* Thu Sep 19 2013 Rok Mandeljc <rok.mandeljc@gmail.com> - 2.1.1-1
- Updated to 2.1.1

* Fri Jun  7 2013 Rok Mandeljc <rok.mandeljc@gmail.com> - 2.1.0-1
- Updated to 2.1.0

* Mon Dec 24 2012 Rok Mandeljc <rok.mandeljc@gmail.com> - 2.0.0-1
- RPM release for new version
