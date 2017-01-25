Name:           curlew
Version:        0.2.2
Release:        2%{?dist}
Summary:        Multimedia converter for Linux

License:        Waqf
URL:            http://sourceforge.net/projects/curlew
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  desktop-file-utils
BuildRequires:  gettext intltool librsvg2-tools
Requires:       python3-gobject
Requires:       ffmpeg mencoder mediainfo
Requires:       hicolor-icon-theme

%description
Easy to use, Free and Open-Source Multimedia converter for Linux.
Curlew written in python and GTK3 and it depends on (ffmpeg/avconv, mencoder).

%prep
%setup -q -n %{name}-%{version}

%build
%{__python3} setup.py build

%install
rm -rf %{buildroot}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

%{__rm} -rf %{buildroot}/%{_datadir}/doc

desktop-file-edit  \
  --remove-key=Encoding \
  --add-category=GTK \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%license LICENSE-ar.txt LICENSE-en.txt
%doc AUTHORS ChangeLog README
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.cfg
%{_datadir}/%{name}/modules/*
%exclude %{python3_sitelib}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/pixmaps/%{name}.*

%changelog
* Tue Jan 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.2.2-2
- rebuilt

* Sat Mar 26 2016 Phantom X - 0.2.2-1
- 0.2.2.

* Sun Dec 27 2015 Phantom X - 0.2.0-1.beta
- First spec.
