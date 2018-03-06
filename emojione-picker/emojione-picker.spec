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
Release:        1%{?gver}%{?dist}
Summary:        Emoji Picker for the indicator area using Emoji One

License:        GPLv3
URL:            https://github.com/gentakojima/%{fullname}
%if 0%{?with_snapshot}
Source0:        https://github.com/gentakojima/%{fullname}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/gentakojima/%{fullname}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  librsvg2-tools
BuildRequires:  python2-rpm-macros
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
%autosetup -n %{fullname}-%{commit}
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
  --add-category="GTK" \
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


%files
%license debian/copyright
%doc README.md debian/changelog
%{_bindir}/%{name}
%{_datadir}/%{name}/assets
%{_sysconfdir}/xdg/autostart/%{name}_autostart.desktop
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}*

%changelog
* Fri Dec  1 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.1-1.20161009gitcb5f504
- Initial spec.
