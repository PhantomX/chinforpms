%global fullname emojione-picker-ubuntu
%global commit cb5f504235f861586903cf64aec8ed75a9c925b6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20161009
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           emojione-picker
Version:        0.1
Release:        3%{?gver}%{?dist}
Summary:        Emoji Picker for the indicator area using Emoji One

License:        GPLv3
URL:            https://github.com/gentakojima/%{fullname}
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{name}.appdata.xml

Patch1:         %{url}/pull/25/commits/1faaefc71b18f1f982c1a803282a752c53248b0a.patch#/%{name}-gh-pull-25.patch
Patch2:         %{url}/pull/31.patch#/%{name}-gh-pull-31.patch

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  librsvg2-tools
BuildRequires:  python2-rpm-macros
Requires:       python2-gobject-base
Requires:       gtk3
Requires:       libnotify >= 0.7
Requires:       libappindicator-gtk3
Requires:       librsvg2
Requires:       python2
Requires:       xdotool
Requires:       hicolor-icon-theme

%description
%{summary}.
Emoji Picker featuring several menus and a search panel.
You must paste the emojis wherever you want to use them.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{fullname}-%{commit} -p1
%else
%autosetup -n %{fullname}-%{version}
%endif

sed -e 's|/usr/bin/python2.7|%{__python2}|1' -i %{name}

sed -e '/^$/d' -i *.desktop

%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -rp assets %{buildroot}%{_datadir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category="Utility" \
  --remove-key="NoDisplay" \
  %{name}.desktop

mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
desktop-file-install \
  --dir %{buildroot}%{_sysconfdir}/xdg/autostart \
  --add-category="GTK" \
  --add-category="Utility" \
  --remove-key="NoDisplay" \
  %{name}_autostart.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
ln -sf ../../../../%{name}/assets/icon-default.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

for res in 16 22 24 32 36 48 64 72 96 128 192 256 512 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  rsvg-convert assets/icon-default.svg -h ${res} -w ${res} \
    -o ${dir}/%{name}.png || exit 1
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
%license debian/copyright
%doc README.md debian/changelog
%{_bindir}/%{name}
%{_datadir}/%{name}/assets
%{_sysconfdir}/xdg/autostart/%{name}_autostart.desktop
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}*
%{_metainfodir}/*.xml


%changelog
* Tue Apr 23 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.1-3.20161009gitcb5f504
- BR: python2-gobject-base

* Wed May 02 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.1-2.20161009gitcb5f504
- Add GitHub pull requests
- Metainfo file

* Fri Dec  1 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.1-1.20161009gitcb5f504
- Initial spec.
