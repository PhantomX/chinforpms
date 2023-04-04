%global commit 9efc66d3c8b72af5a31f962b9ee5d0d71d231c04
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20221226
%bcond_without snapshot

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           mcomix
Version:        2.1.0
Release:        1%{?dist}
Summary:        User-friendly, customizable image viewer for comic books

License:        GPL-2.0-or-later
URL:            https://mcomix.sourceforge.net/

%if %{with snapshot}
# To regenerate a snapshot:
# Use your regular webbrowser to open https://sourceforge.net/p/mcomix/git/ci/%%{commit}/tarball
# This triggers the SourceForge instructure to generate a snapshot
# After that you can pull in the archive with:
# spectool -g mcomix.spec
Source0:        https://sourceforge.net/code-snapshots/git/m/mc/%{name}/git.git/%{name}-git-%{commit}.zip#/%{name}-%{shortcommit}.zip
%else
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%endif
Source1:        https://github.com/multiSnow/mcomix3/raw/cb63d286a0357af45b2b5defd70618c70b9e709d/mcomix/comicthumb.py

Patch0:         0001-Search-gettext-files-in-system-wide-directory.patch
Patch1:         0001-Set-small-toolbar.patch

BuildRequires:  python3-devel >= 3.8
BuildRequires:  /usr/bin/pathfix.py
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
Requires:       gtk3
Requires:       hicolor-icon-theme

Obsoletes:      mcomix3 < 1
Obsoletes:      comix < 4.0.5
Provides:       mcomix3 = %{version}


%description
MComix is a user-friendly, customizable image viewer.


%prep
%autosetup %{?with_snapshot:-n %{name}-git-%{commit}} -p1

cp -f %{S:1} mime/comicthumb

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" mime/comicthumb

sed \
  -e 's|%{name}.1.gz|%{name}.1|g' \
  -e 's|share/appdata|share/metainfo|g' \
  -i setup.py

gunzip %{name}.1.gz mime/comicthumb.1.gz

mv %{name}/messages locale

%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install

%pyproject_save_files %{name}

# locale files
find locale/* -type f -name '*.mo' | while read f
do
  dir=$(dirname $f)
  localedir=%{buildroot}%{_datadir}/$dir
  mkdir -p $localedir
  install -pm0644 $f $localedir/
done

install -pm0755 mime/comicthumb %{buildroot}%{_bindir}/comicthumb

mkdir -p %{buildroot}%{_datadir}/thumbnailers
install -pm0644 mime/comicthumb.thumbnailer \
  %{buildroot}%{_datadir}/thumbnailers/comicthumb.thumbnailer

install -pm0644 mime/comicthumb.1 %{buildroot}%{_mandir}/man1/

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 mime/%{name}.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%find_lang %{name}


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files -f %{pyproject_files} -f %{name}.lang
%license  COPYING
%doc ChangeLog README*
%{_bindir}/%{name}
%{_bindir}/comicthumb
# Do not own %%{_datadir}/icons/hicolor explicitly
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/*/mimetypes/application-x-*.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/thumbnailers/comicthumb.thumbnailer
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/comicthumb.1*
%{_metainfodir}/%{name}.appdata.xml


%changelog
* Tue Dec 27 2022 Phantom X <megaphantomx at hotmail dot com> - 2.1.0-1.20221226git9efc66d
- 2.1.0

* Wed Dec 14 2022 Phantom X <megaphantomx at hotmail dot com> - 2.1.0-0.1.20221212git01e7d62
- Initial spec

