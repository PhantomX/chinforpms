%global commit 72f710ec27d650548dbcbd87f4b4c0e48149df5f
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240116
%bcond snapshot 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global vc_url https://github.com/mciobanu/%{name}
%global binname MP3Diags

Name:           mp3diags
Version:        1.5.03
Release:        1%{?dist}
Summary:        Finds problems in MP3 files

License:        GPL-2.0-or-later
URL:            http://mp3diags.sourceforge.net/

%if %{with snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  qt5-linguist
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Recommends:     mp3gain

%description
Finds problems in MP3 files and helps the user to fix many of them using
included tools. Looks at both the audio part (VBR info, quality, normalization)
and the tags containing track information (ID3.) Also includes a tag editor and
a file renamer.


%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

./AdjustMt.sh


%build
%qmake_qt5 %{name}.pro
%make_build
lrelease-qt5 src/translations/%{name}_*.ts


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 bin/%{binname}-unstable %{buildroot}%{_bindir}/%{binname}

mkdir -p %{buildroot}%{_datadir}/%{name}/translations
install -pm0644 src/translations/*.qm \
  %{buildroot}%{_datadir}/%{name}/translations/

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --mode=0644 \
  --dir %{buildroot}%{_datadir}/applications \
  desktop/%{binname}.desktop

for res in 16 22 24 32 36 48 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  install -pm0644 desktop/%{binname}-unstable${res}.png ${dir}/%{binname}.png
done

%find_lang %{name} --with-qt


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{binname}.desktop


%files -f %{name}.lang
%license COPYING
%doc README.md
%{_bindir}/%{binname}
%{_datadir}/applications/%{binname}.desktop
%{_datadir}/icons/hicolor/*/*/%{binname}.png


%changelog
* Wed Jan 07 2026 Phantom X <megaphantomx at hotmail dot com> - 1.5.03-1.20240116git72f710e
- Initial spec

