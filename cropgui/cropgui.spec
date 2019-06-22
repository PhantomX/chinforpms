%global commit 552ae7b472027507d30814cea4242316e65abd20
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180727
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           cropgui
Version:        0.3
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
Requires:       ImageMagick
Requires:       gtk3
Requires:       libjpeg-turbo-utils
Requires:       perl-Image-ExifTool
Requires:       python2
Requires:       python2-gobject-base
Requires:       python2-pillow
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

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/24x24/apps
install -pm0644 %{name}.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%changelog
* Sat Jun 22 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.3-1.20180727git552ae7b
- Initial spec
