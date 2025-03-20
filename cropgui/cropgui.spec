%global commit cd46c9827aef16466e921f41ffdf86c86285dd02
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20230615
%bcond_with snapshot

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           cropgui
Version:        0.9
Release:        1%{?dist}
Summary:        GTK frontend for lossless cropping of jpeg images

License:        GPL-2.0-or-later
URL:            https://github.com/jepler/cropgui/

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Set-data-files-to-datadir.patch

BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  python3-devel
Requires:       ImageMagick
Requires:       gtk3
Requires:       libjpeg-turbo-utils
Requires:       perl-Image-ExifTool
Requires:       python3
Requires:       python3-gobject
Requires:       python3-gobject-base
Requires:       python3-pillow
Requires:       hicolor-icon-theme


%description
cropgui is a a GTK GUI for lossless JPEG cropping


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed -e '1{/env/d;}' -i filechooser.py

%py3_shebang_fix cropgtk.py

sed -e 's|_RPM_DATADIR_|%{_datadir}/%{name}|g' -i cropgtk.py


%build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 cropgtk.py %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_datadir}/%{name}
install -pm0644 \
  cropgui_common.py filechooser.py cropgui.glade stock-rotate-*.png \
  %{buildroot}%{_datadir}/%{name}


desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --set-key=Exec --set-value="%{name}" \
  --remove-key="X-GNOME-DocPath" \
  %{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{24x24,16x16}/apps
install -pm0644 %{name}.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/
magick %{name}.png -filter Lanczos -resize 16x16 \
  %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%changelog
* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 0.9-1
- 0.9

* Thu Sep 19 2024 Phantom X <megaphantomx at hotmail dot com> - 0.8-1
- 0.8

* Wed Mar 27 2024 Phantom X <megaphantomx at hotmail dot com> - 0.7-1
- 0.7

* Wed Nov 16 2022 Phantom X <megaphantomx at hotmail dot com> - 0.6-1.20220916git1340ac1
- 0.6

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0.5-1.20210419git9dbf930
- 0.5

* Wed Mar 18 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.3-3.20200309gitd7eaf1f
- Bump

* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.3-2.20190904git78db49a
- Python 3

* Sat Jun 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.3-1.20180727git552ae7b
- Initial spec
