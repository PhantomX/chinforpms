%global fontname bh
%global fontconf 43-luxi.conf
%global fontconfm 42-luxi-mono.conf

%global archivename font-bh-ttf-%{version}

Name:           bh-fonts
Version:        1.0.3
Release:        1%{?dist}
Summary:        X.Org BH TTF fonts

License:        Proprietary
URL:            http://www.x.org
Source0:        http://xorg.freedesktop.org/releases/individual/font/%{archivename}.tar.bz2
Source1:        43-luxi.conf

BuildArch:      noarch
BuildRequires:  fontpackages-devel
Requires:       fontpackages-filesystem

%description
X.Org BH TTF fonts.

%prep
%autosetup -n %{archivename}

%build
%configure \
  --with-fontdir=%{_fontdir} \
  --with-fc-confdir=%{_datadir}/fontconfig
%make_build
%install
rm -fr %{buildroot}
%make_install

install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

rm -fv  %{buildroot}%{_fontdir}/fonts.*
rm -rfv %{buildroot}%{_datadir}/fontconfig/conf.d

install -m 0644 -p %{SOURCE1} \
  %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} \
  %{buildroot}%{_fontconfig_confdir}/%{fontconf}

ln -sf %{_fontconfig_templatedir}/%{fontconfm} \
  %{buildroot}%{_fontconfig_confdir}/%{fontconfm}

%clean
rm -fr %{buildroot}


%_font_pkg -f %{fontconf} *.ttf

%license COPYING
%doc ChangeLog README
%{_fontconfig_templatedir}/%{fontconfm}
%{_fontconfig_confdir}/%{fontconfm}

%changelog
* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.0.3-1
- Initial spec.
