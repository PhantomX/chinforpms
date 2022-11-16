%global commit 1340ac1de39a86a3e368428503580fc132a2b9eb
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220916
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           cropgui
Version:        0.6
Release:        1%{?gver}%{?dist}
Summary:        GTK frontend for lossless cropping of jpeg images

License:        GPLv2+
URL:            https://github.com/jepler/cropgui/

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         0001-Set-data-files-to-datadir.patch

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
BuildRequires:  /usr/bin/pathfix.py
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
%autosetup %{?gver:-n %{name}-%{commit}} -p1

sed -e '1{/env/d;}' -i filechooser.py

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" cropgtk.py

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
convert %{name}.png -filter Lanczos -resize 16x16 \
  %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%changelog
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
