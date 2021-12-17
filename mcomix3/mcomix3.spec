%global commit cff5fc3e8214e56b112e6469e544fa7b97690aa4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210915
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global sitetopdir %{python3_sitelib}/%{name}

Name:           mcomix3
# For now, choose version 0
Version:        0
Release:        0.101%{?gver}%{?dist}
Summary:        User-friendly, customizable image viewer for comic books

# GPL version info is from mcomix/mcomixstarter.py
License:        GPLv2+
URL:            https://github.com/multiSnow/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

# Patches
Patch2:         0002-Change-domain-name-for-gettext.patch
Patch3:         0003-Search-gettext-files-in-system-wide-directory.patch

BuildArch:      noarch

BuildRequires:  python3-devel >= 3.8
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
Requires:       gtk3
Requires:       %{py3_dist pygobject}
Requires:       %{py3_dist pillow}

%if 0%{?fedora} >= 32
Obsoletes:      mcomix < 1.2.2
Obsoletes:      comix < 4.0.5
Provides:       mcomix = 1.2.2
%endif


%description
MComix3 is a user-friendly, customizable image viewer.
It has been forked from the original MComix project and ported to python3.

%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

cat > %{name}.sh <<EOF
#!/usr/bin/bash

SITEDIR="%{sitetopdir}"

export PYTHONPATH="\${SITEDIR}/%{name}"

exec "\${SITEDIR}"/mcomixstarter.py "\$@"
EOF
sed -e 's|mcomixstarter|comicthumb|g' %{name}.sh > comicthumb.sh

mv mime/mcomix.desktop mime/%{name}.desktop
mv mime/mcomix.appdata.xml mime/%{name}.appdata.xml
mv man/mcomix.1 man/%{name}.1

sed -e 's|MComix|MComix3|g' -i mime/%{name}.{desktop,appdata.xml} man/%{name}.1

sed -e 's|mcomix.desktop|%{name}.desktop|g' -i mime/%{name}.appdata.xml


%build
rm -rf localroot
mkdir localroot

python3 installer.py --srcdir=mcomix --target=$(pwd)/localroot/


%install

# Install manually...
DSTTOPDIR=%{buildroot}%{sitetopdir}
mkdir -p ${DSTTOPDIR}
mkdir -p ${DSTTOPDIR}/mcomix3
mkdir -p %{buildroot}%{_datadir}/locale
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/

rm -rf localroot.2
cp -a localroot localroot.2

pushd localroot.2/mcomix

# locale files
find mcomix/messages/* -type f | while read f
do
  dir=$(dirname $f)
  mv $f $dir/%{name}.mo
done
mv mcomix/messages/* %{buildroot}%{_datadir}/locale/
# duplicate icon
for dir in mcomix/images/*x*/
do
  basedir=$(basename $dir)
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/$basedir/apps
  cp -p $dir/*png %{buildroot}%{_datadir}/icons/hicolor/$basedir/apps/%{name}.png
done
# data files
mv mcomix/ ${DSTTOPDIR}/mcomix3/
# Not needed
rm -f comicthumb.py
mv mcomixstarter.py ${DSTTOPDIR}/

# Ensure that all files are installed
popd
rmdir localroot.2/mcomix
rmdir localroot.2

# Wrapper symlink
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name}.sh %{buildroot}%{_bindir}/%{name}
install -pm0755 comicthumb.sh %{buildroot}%{_bindir}/comicthumb

mkdir -p %{buildroot}%{_datadir}/thumbnailers
install -pm0644 mime/comicthumb.thumbnailer \
  %{buildroot}%{_datadir}/thumbnailers/comicthumb.thumbnailer

mkdir -p %{buildroot}%{_mandir}/man1
for i in comicthumb %{name} ;do
  install -pm0644 man/$i.1 %{buildroot}%{_mandir}/man1/
done

# Desktop file
mkdir %{buildroot}%{_datadir}/applications
desktop-file-install \
  --remove-category Application \
  --set-icon=%{name} \
  --set-key=Exec \
  --set-value="%{name} %f" \
  --dir %{buildroot}%{_datadir}/applications/ \
  mime/%{name}.desktop

mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 mime/%{name}.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%find_lang %{name}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files -f %{name}.lang
%license  COPYING
%doc    ChangeLog README* TODO
%{_bindir}/%{name}
%{_bindir}/comicthumb
%{python3_sitelib}/%{name}/
# Do not own %%{_datadir}/icons/hicolor explicitly
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/thumbnailers/comicthumb.thumbnailer
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/comicthumb.1*
%{_metainfodir}/%{name}.appdata.xml


%changelog
* Fri Oct 01 2021 Phantom X <megaphantomx at hotmail dot com> - 0-0.101.20210915gitcff5fc3
- Bump

* Wed Jun 23 2021 Phantom X <megaphantomx at hotmail dot com> - 0-0.100.20210526git9eb4fc7
- Update
- Sync with Rawhide (thumbnailer and appdata)

* Tue Apr 20 2021 Phantom X <megaphantomx at hotmail dot com> - 0-0.9.2020329git523f08f
- Bump

* Fri Jan 22 2021 Phantom X <megaphantomx at hotmail dot com> - 0-0.8.20201222git9ba2f5b
- Latest snapshot

* Wed Jul 01 2020 Phantom X <megaphantomx at hotmail dot com> - 0-0.7.20200610gitb029d08
- New snapshot

* Thu Apr 02 2020 Phantom X <megaphantomx at bol dot com dot br> - 0-0.6.20200401git2f9a4b9
- Bump
- autosetup instead git
- Fix wrapper

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.5.D20191205gita098f81
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 30 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> 0-0.4.D20191205gita098f81
- Update to latest git (20191205)

* Fri Nov  8 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> 0-0.2.D20190616git0405a23
- Reflect package review suggestions (bug 1768447)

* Mon Nov 04 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> 0-0.1.D20190616git0405a23
- Initial packaging
