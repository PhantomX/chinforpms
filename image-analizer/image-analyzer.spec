Name:           image-analyzer
Version:        3.1.0
Release:        2%{?dist}
Summary:        A libMirage-based CD/DVD-ROM image analyzer

License:        GPLv2
URL:            http://sourceforge.net/projects/cdemu
Source0:        http://downloads.sourceforge.net/cdemu/%{name}-%{version}.tar.bz2

BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  intltool
BuildRequires:  librsvg2-tools

Requires:       python2
Requires:       pygobject3
Requires:       libmirage
Requires:       python2-matplotlib
Requires:       python2-matplotlib-gtk3
Requires:       hicolor-icon-theme

%description
CD/DVD-ROM image analyzer, based on libMirage library.

%prep
%autosetup

%build
mkdir build
pushd build

%cmake .. \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DPOST_INSTALL_HOOKS:BOOL=OFF

%make_build

popd

%install
%make_install -C build

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
ln -sf ../../../../pixmaps/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert data/%{name}.svg -h ${res} -w ${res} \
    -o ${dir}/%{name}.png || exit 1
done

%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README ChangeLog
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/*/%{name}*
%{_datadir}/pixmaps/*

%changelog
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
