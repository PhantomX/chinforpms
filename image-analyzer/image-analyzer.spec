Name:           image-analyzer
Version:        3.2.4
Release:        100%{?dist}
Summary:        A libMirage-based CD/DVD-ROM image analyzer

License:        GPLv2
URL:            http://sourceforge.net/projects/cdemu
Source0:        https://downloads.sourceforge.net/cdemu/%{name}-%{version}.tar.bz2

BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  intltool
BuildRequires:  librsvg2-tools
BuildRequires:  /usr/bin/pathfix.py
Requires:       gobject-introspection
Requires:       gtk3
Requires:       libmirage
Requires:       pango
Requires:       python3
Requires:       python3-gobject
Requires:       python3-matplotlib
Requires:       python3-matplotlib-gtk3
Requires:       hicolor-icon-theme

%description
CD/DVD-ROM image analyzer, based on libMirage library.

%prep
%autosetup

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" src/%{name}

%build
%cmake \
  -B %{__cmake_builddir} \
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
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/*/%{name}*
%{_datadir}/pixmaps/*


%changelog
* Mon Feb 24 2020 Phantom X <megaphantomx at bol dot com dot br> - 3.2.4-1
- 3.2.4

* Tue Aug 27 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.2.3-1
- 3.2.3

* Mon Mar 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.2.2-1
- new version

* Sun Mar 03 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.2.1-1
- 3.2.1

* Wed Jul 11 2018 Phantom X <megaphantomx at bol dot com dot br> - 3.2.0-1
- 3.2.0

* Fri Oct 06 2017 Phantom X <megaphantomx at bol dot com dot br> - 3.1.0-2
- chinforpms release

* Sat Jun 10 2017 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.1.0-1
- Updated to 3.1.0

* Sun Oct  9 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.1-1
- Updated to 3.0.1

* Sat Apr 23 2016 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.0-2
- Fixed rpmlint errors and warnings
- Added desktop-file-utils dependency

* Sun Jun 29 2014 Rok Mandeljc <rok.mandeljc@gmail.com> - 3.0.0-1
- Updated to 3.0.0

* Thu Sep 19 2013 Rok Mandeljc <rok.mandeljc@gmail.com> - 2.1.1-1
- Updated to 2.1.1

* Fri Jun  7 2013 Rok Mandeljc <rok.mandeljc@gmail.com> - 2.1.0-1
- Updated to 2.1.0

* Mon Dec 24 2012 Rok Mandeljc <rok.mandeljc@gmail.com> - 2.0.0-1
- RPM release for new version
