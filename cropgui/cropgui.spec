%global commit 78db49a17788b2db78e5502a8d5617b11c2f0b26
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20190904
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           cropgui
Version:        0.3
Release:        2%{?gver}%{?dist}
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
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -p1
%endif

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
* Wed Sep 18 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.3-2.20190904git78db49a
- Python 3

* Sat Jun 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.3-1.20180727git552ae7b
- Initial spec
