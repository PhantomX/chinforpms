%global commit b029d085837d8227118b7dc217ea26e98a4b9aac
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200610
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           mcomix3
# For now, choose version 0
Version:        0
Release:        0.7%{?gver}%{?dist}
Summary:        User-friendly, customizable image viewer for comic books

# GPL version info is from mcomix/mcomixstarter.py
License:        GPLv2+
URL:            https://github.com/multiSnow/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

# Borrow some desktop related files
Source10:       %{name}.desktop

# Patches
Patch2:         0002-Change-domain-name-for-gettext.patch
Patch3:         0003-Search-gettext-files-in-system-wide-directory.patch

BuildArch:      noarch

BuildRequires:  python3-devel
#BuildRequires:  %%{_bindir}/appstream-util
BuildRequires:  %{_bindir}/desktop-file-install
BuildRequires:  gettext
Requires:       gtk3
Requires:       python3-gobject
Requires:       python3-pillow

%if 0%{?fedora} >= 32
Obsoletes:      mcomix < 1.2.2
Obsoletes:      comix < 4.0.5
Provides:       mcomix = 1.2.2
%endif


%description
MComix3 is a user-friendly, customizable image viewer.
It has been forked from the original MComix project and ported to python3.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif


%build
rm -rf localroot
mkdir localroot

python3 installer.py --srcdir=mcomix --target=$(pwd)/localroot/


%install

# Install manually...
SITETOPDIR=%{python3_sitelib}/%{name}
DSTTOPDIR=%{buildroot}${SITETOPDIR}
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

cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/usr/bin/bash

SITEDIR="${SITETOPDIR}"

export PYTHONPATH="\${SITEDIR}/%{name}"

exec "\${SITEDIR}"/mcomixstarter.py "\$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}


# Desktop file
mkdir %{buildroot}%{_datadir}/applications
desktop-file-install \
  --remove-category Application \
  --dir %{buildroot}%{_datadir}/applications/ \
  %{SOURCE10}

%find_lang %{name}

%files -f %{name}.lang
%license  COPYING
%doc    ChangeLog
%doc    README*
%doc    TODO

%{_bindir}/%{name}
%{python3_sitelib}/%{name}/
# Do not own %%{_datadir}/icons/hicolor explicitly
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop
# TODO: appdata file, not available yet (should item)

%changelog
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
