# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?__python2: %global __python2 %__python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           gespeaker
Version:        0.8.6
Release:        1%{?dist}
Summary:        A GTK+ front-end for espeak

License:        GPLv2+
URL:            http://www.muflone.com/gespeaker
Source0:        https://github.com/muflone/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  pkgconfig(pygtk-2.0)
BuildRequires:  librsvg2-tools
Requires:       espeak
Requires:       hicolor-icon-theme
Requires(post): desktop-file-utils
Requires(postun): gtk-update-icon-cache
Requires(posttrans): gtk-update-icon-cache

%description
Gespeaker is a GTK+ front-end for espeak. It allows to play a text in
many languages with settings for voice, pitch, volume, speed and word
gap. The text played can also be recorded to WAV file.

%prep
%autosetup

cp -p doc/copyright LICENSE

sed -e '/share\/doc\//d' -i setup.py

sed \
  -e '/%{name}.py/s|^env python |exec %{__python2} |g' \
  -i %{name}

sed -e 's|/usr/bin/env python|%{__python2}|' -i src/%{name}.py

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

desktop-file-edit \
  --set-icon="%{name}" \
  --set-key="Exec" \
  --set-value="%{name}" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

for res in 16 24 32 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert data/icons/%{name}.svg -filter Lanczos -resize ${res}x${res}  \
    ${dir}/%{name}.png
done

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

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

%files -f %{name}.lang
%license LICENSE
%doc doc/dbus doc/README doc/translators
%{_bindir}/%{name}
%{python2_sitelib}/*.egg-info
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_mandir}/man1/*.1*


%changelog
* Tue May 23 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.8.6-1
- First spec
