%global fontname bh
%global priority 42
%global fontconf %{priority}-%{fontname}

%global archivename font-bh-ttf-%{version}

%global common_desc \
X.Org Bigelow & Holmes TrueType fonts.

Name:           bh-fonts
Version:        1.0.3
Release:        3%{?dist}
Summary:        X.Org BH TTF fonts

License:        BH-Luxi
URL:            http://www.x.org
Source0:        http://xorg.freedesktop.org/releases/individual/font/%{archivename}.tar.bz2
Source1:        %{name}-mono.conf
Source2:        %{name}-sans.conf
Source3:        %{name}-serif.conf
Source4:        %{fontname}.metainfo.xml
Source5:        %{fontname}-mono.metainfo.xml
Source6:        %{fontname}-sans.metainfo.xml
Source7:        %{fontname}-serif.metainfo.xml

BuildArch:      noarch
BuildRequires:  fontpackages-devel
BuildRequires:  xorg-x11-font-utils

%description
%common_desc

%package common
Summary:  Common files for the BH font set
Requires: fontpackages-filesystem

Obsoletes: %{name} < %{version}
Obsoletes: %{fontname}-ttf < %{version}

%description common
%common_desc

This package consists of files used by other BH packages.

%package -n %{fontname}-sans-fonts
Summary:  BH variable-width sans-serif font faces
Requires: %{?epoch:%{epoch}:}%{name}-common = %{version}-%{release}

%description -n %{fontname}-sans-fonts
%common_desc

This package consists of the BH Luxi sans-serif variable-width font faces.

%_font_pkg -n sans -f *-%{fontname}-sans.conf luxis*.ttf
%{_datadir}/appdata/%{fontname}-sans.metainfo.xml

%package -n %{fontname}-serif-fonts
Summary:  BH variable-width serif font faces
Requires: %{?epoch:%{epoch}:}%{name}-common = %{version}-%{release}

%description -n %{fontname}-serif-fonts
%common_desc

This package consists of the BH serif variable-width font faces.

%_font_pkg -n serif -f *-%{fontname}-serif.conf luxir*.ttf
%{_datadir}/appdata/%{fontname}-serif.metainfo.xml


%package -n %{fontname}-mono-fonts
Summary:  Monospace font faces
Requires: %{?epoch:%{epoch}:}%{name}-common = %{version}-%{release}

%description -n %{fontname}-mono-fonts
%common_desc

This package consists of the BH sans-serif monospace font faces.

%_font_pkg -n mono -f *-%{fontname}-mono.conf luxim*.ttf
%{_datadir}/appdata/%{fontname}-mono.metainfo.xml


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
rm -fv %{buildroot}%{_fontconfig_templatedir}/*.conf

install -m 0644 -p %{SOURCE1} \
  %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-mono.conf
install -m 0644 -p %{SOURCE2} \
  %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-sans.conf
install -m 0644 -p %{SOURCE3} \
  %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-serif.conf

# Add AppStream metadata
install -Dm 0644 -p %{SOURCE4} \
  %{buildroot}%{_datadir}/appdata/%{fontname}.metainfo.xml
install -Dm 0644 -p %{SOURCE5} \
  %{buildroot}%{_datadir}/appdata/%{fontname}-mono.metainfo.xml
install -Dm 0644 -p %{SOURCE6} \
  %{buildroot}%{_datadir}/appdata/%{fontname}-sans.metainfo.xml
install -Dm 0644 -p %{SOURCE7} \
  %{buildroot}%{_datadir}/appdata/%{fontname}-serif.metainfo.xml

for fconf in \
  %{fontconf}-mono.conf \
  %{fontconf}-sans.conf \
  %{fontconf}-serif.conf
do
  ln -s %{_fontconfig_templatedir}/${fconf} \
    %{buildroot}%{_fontconfig_confdir}/${fconf}
done


%files common
%defattr(0644,root,root,0755)
%license COPYING
%doc ChangeLog README
%{_datadir}/appdata/%{fontname}.metainfo.xml

%changelog
* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.3-3
- BR: xorg-x11-font-utils

* Sun Feb 05 2017 Phantom X <megaphantomx at bol dot com dot br> - 1.0.3-2
- Try to follow Fedora font packaging guidelines

* Wed Dec 28 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.0.3-1
- Initial spec
