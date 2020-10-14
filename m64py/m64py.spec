%global commit 0a08a32481f3de8bb91d5f3e2c653ed9114e5347
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200602
%global with_snapshot 1

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global pkgname mupen64plus-ui-python

Name:           m64py
Version:        0.2.5
Release:        5%{?gver}%{?dist}
Summary:        A frontend for Mupen64Plus 2.0

License:        GPLv3
URL:            http://m64py.sourceforge.net
%if 0%{?with_snapshot}
Source0:        https://github.com/mupen64plus/%{pkgname}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/mupen64plus/%{pkgname}/releases/download/%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        %{name}.appdata.xml

Patch0:         %{name}-path.patch
Patch1:         %{name}-libdir.patch

BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel
BuildRequires:  %{py3_dist sdl2}
BuildRequires:  python3-qt5-devel
BuildRequires:  qt5-linguist
BuildRequires:  ImageMagick
Requires:       mupen64plus
Requires:       python3-qt5
Requires:       %{py3_dist sdl2}
Requires:       SDL2
Requires:       hicolor-icon-theme

Provides:       %{pkgname} = %{?epoch:%{epoch}:}%{version}-%{release}


%description
M64Py is a Qt5 front-end (GUI) for Mupen64Plus 2.0, a cross-platform
plugin-based Nintendo 64 emulator.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{pkgname}-%{commit} -p1
%else
%autosetup -p1
%endif

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" bin/%{name}

find -name '*.py' -print0 | xargs -0 \
  pathfix.py -pni "%{__python3} %{py3_shbang_opts}"

sed -e 's|_DATADIR_|%{_datadir}|g' -i bin/%{name}

sed -e 's|"lrelease"|"lrelease-qt5"|' -i setup.py


%build
%py3_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 bin/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/%{name}
cp -a src/m64py/* %{buildroot}%{_datadir}/%{name}/

find %{buildroot}%{_datadir}/%{name}/ -name '*.py' -print0 | xargs -0 chmod 0755

find %{buildroot} -name '*.orig' -delete

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key="MimeType" \
  --add-category="Qt" \
  xdg/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/96x96/apps
install -pm0644 xdg/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/96x96/apps/

for res in 16 22 24 32 36 48 64 72 ;do
  dir=%{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
  mkdir -p ${dir}
  convert xdg/%{name}.png -filter Lanczos -resize ${res}x${res} \
    ${dir}/%{name}.png
done

mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%find_lang %{name} --with-qt


%files -f %{name}.lang
%license COPYING LICENSES
%doc AUTHORS README.rst
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%dir %{_datadir}/%{name}/ui/i18n/
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_metainfodir}/*.xml


%changelog
* Thu Jun 25 2020 Phantom X <megaphantomx at hotmail dot com> - 0.2.5-5.20200602git0a08a32
- New snapshot
- BR: qt5-linguist
- Provides: mupen64plus-ui-python

* Mon Apr 27 2020 Phantom X <megaphantomx at bol dot com dot br> - 0.2.5-4.20200414git9681d46
- Bump

* Thu Mar 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.2.5-3.20190122git30e05dd
- New snapshot

* Fri Jul 20 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.2.5-2.20180306gitfccb772
- New snapshot

* Tue Apr 17 2018 Phantom X <megaphantomx at bol dot com dot br> - 0.2.5-1.20180306git164577e
- New snapshot

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.2.3-3
- Fix python3-qt5 BR

* Tue Jan 24 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.2.3-2
- Fixed shebangs

* Thu Jan  5 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.2.3-1
- Initial spec.
