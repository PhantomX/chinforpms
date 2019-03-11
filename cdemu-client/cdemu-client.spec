%global debug_package %{nil}

Name:           cdemu-client
Version:        3.2.1
Release:        1%{?dist}
Summary:        CDEmu CLI client

License:        GPLv2
URL:            https://sourceforge.net/projects/cdemu
Source:         https://downloads.sourceforge.net/cdemu/%{name}-%{version}.tar.bz2

BuildArch:      noarch

BuildRequires:  bash-completion
BuildRequires:  cmake
BuildRequires:  intltool
BuildRequires:  python3-devel
BuildRequires:  /usr/bin/pathfix.py
Requires:       gobject-introspection
Requires:       python3
Requires:       python3-gobject
Requires:       hicolor-icon-theme

%description
cdemu-client is a command-line interface client for controlling CDEmu
devices. It is part of CDEmu, a CD/DVD-ROM device emulator for Linux.

%prep
%autosetup

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" src/cdemu


%build
mkdir %{_target_platform}
pushd %{_target_platform}

%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DPOST_INSTALL_HOOKS:BOOL=OFF

%make_build

popd

%install
%make_install -C %{_target_platform}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
ln -sf ../../../../pixmaps/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%find_lang cdemu

%files -f cdemu.lang
%license COPYING
%doc AUTHORS README ChangeLog
%doc %{_mandir}/man1/*
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.svg
%{_datadir}/bash-completion/completions/cdemu
%{_datadir}/icons/hicolor/scalable/apps/*.svg


%changelog
* Sun Mar 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.2.1-1
- 3.2.1

* Wed Jul 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.2.0-1
- 3.2.0

* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.1.0-2
- chinforpms release

* Sat Jun 10 2017 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.1.0-1
- Updated to 3.1.0

* Tue Oct 11 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.4-1
- Updated to 3.0.4

* Sun Oct  9 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.3-1
- Updated to 3.0.3

* Sun Oct  9 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.2-1
- Updated to 3.0.2

* Sat Apr 23 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.1-5
- Fixed rpmlint errors and warnings
- Added desktop-file-utils dependency
- Moved bash completion script to /usr/share/bash-completion/completions

* Thu Apr 21 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.1-4
- Added python2-devel as build dependency, to satisfy CMake check
- Use noarch

* Thu Apr 21 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.1-3
- Changed python dependency to python2

* Sat Nov 21 2015 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.1-2
- Added dbus-python dependency

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
