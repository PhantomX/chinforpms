%global commit a4092eb4f2927ce5d600444d0b10c308148ca34d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20250625
%bcond snapshot 1

BuildArch:      noarch

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           mcomix
Version:        3.1.0
Release:        3%{?dist}
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

Patch0:         0001-Search-gettext-files-in-system-wide-directory.patch
Patch1:         0001-Set-small-toolbar.patch
Patch2:         0001-7zip-use-7za.patch

BuildRequires:  python3-devel >= 3.8
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
Requires:       %{_bindir}/7za
Requires:       gtk3
Requires:       hicolor-icon-theme
Recommends:     mupdf

Obsoletes:      mcomix3 < 1
Obsoletes:      comix < 4.0.5
Provides:       mcomix3 = %{version}


%description
MComix is a user-friendly, customizable image viewer.


%prep
%autosetup %{?with_snapshot:-n %{name}-git-%{commit}} -p1

gunzip share/man/man1/*.1.gz

mv %{name}/messages locale
find locale/ -name '*.py' -delete

sed -e '/binary/s|/provides|/binary|' -i share/metainfo/mcomix.metainfo.xml

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

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  share/applications/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor
cp -rp share/icons/hicolor/* %{buildroot}%{_datadir}/icons/hicolor/

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 share/man/man1/*.1 %{buildroot}%{_mandir}/man1/

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 share/metainfo/mcomix.metainfo.xml \
  %{buildroot}%{_metainfodir}/

mkdir -p %{buildroot}%{_datadir}/mime/packages
install -pm0644 share/mime/packages/%{name}.xml \
  %{buildroot}%{_datadir}/mime/packages/


%find_lang %{name}


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml


%files -f %{pyproject_files} -f %{name}.lang
%license  COPYING
%doc ChangeLog.md README.md
%{_bindir}/%{name}
# Do not own %%{_datadir}/icons/hicolor explicitly
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/icons/hicolor/*/mimetypes/application-x-*.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_mandir}/man1/%{name}.1*
%{_metainfodir}/%{name}.metainfo.xml


%changelog
* Sun Jul 20 2025 Phantom X <megaphantomx at hotmail dot com> - 3.1.0-3.20250625gita4092eb
- Requires 7za

* Sun Jun 08 2025 Phantom X <megaphantomx at hotmail dot com> - 3.1.0-2.20250129git7be084d
- Snapshot
- Fix start

* Thu Mar 07 2024 Phantom X <megaphantomx at hotmail dot com> - 3.1.0-1
- 3.1.0

* Sun Oct 01 2023 Phantom X <megaphantomx at hotmail dot com> - 3.0.0-1
- 3.0.0

* Sun Sep 03 2023 Phantom X <megaphantomx at hotmail dot com> - 2.3.0-1
- 2.3.0

* Thu Jun 08 2023 Phantom X <megaphantomx at hotmail dot com> - 2.1.1-1
- 2.1.1

* Tue Dec 27 2022 Phantom X <megaphantomx at hotmail dot com> - 2.1.0-1.20221226git9efc66d
- 2.1.0

* Wed Dec 14 2022 Phantom X <megaphantomx at hotmail dot com> - 2.1.0-0.1.20221212git01e7d62
- Initial spec

