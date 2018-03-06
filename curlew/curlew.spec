Name:           curlew
Version:        0.2.4
Release:        1%{?dist}
Summary:        Multimedia converter for Linux

License:        Waqf
URL:            https://curlew.sourceforge.io/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  desktop-file-utils
BuildRequires:  gettext intltool
BuildRequires:  librsvg2-tools
Requires:       python3-gobject
Requires:       ffmpeg
Requires:       mencoder
Requires:       mediainfo
Requires:       hicolor-icon-theme

%description
Easy to use, Free and Open-Source Multimedia converter for Linux.
Curlew written in python and GTK3 and it depends on (ffmpeg/avconv, mencoder).

%prep
%autosetup

%build
%py3_build

%install
%py3_install

%{__rm} -rf %{buildroot}/%{_datadir}/doc

desktop-file-edit  \
  --remove-key=Encoding \
  --add-category=GTK \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files -f %{name}.lang
%license LICENSE-ar.txt LICENSE-en.txt
%doc AUTHORS ChangeLog README
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.cfg
%{_datadir}/%{name}/modules/*
%exclude %{python3_sitelib}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/pixmaps/%{name}.*

%changelog
* Thu Jun 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.2.4-1
- 0.2.4

* Tue Jan 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.2.2-2
- rebuilt

* Sat Mar 26 2016 Phantom X - 0.2.2-1
- 0.2.2.

* Sun Dec 27 2015 Phantom X - 0.2.0-1.beta
- First spec.
