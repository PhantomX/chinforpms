%global commit 9744a24ffbf4d5ea6ad8b418d740c90336ee33b8
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20211115
%global with_snapshot 1

# Segmentation fault
%global _lto_cflags %{nil}

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/MasterQ32/%{name}

Name:           kristall
Version:        0.3
Release:        1%{?gver}%{?dist}
Summary:        A high-quality visual cross-platform gemini browser

License:        GPLv3
URL:            https://kristall.random-projects.net/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{vc_url}/archive/V%{version}/%{name}-%{version}.tar.gz
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5MultimediaWidgets)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  qt5-linguist
Requires:       hicolor-icon-theme


%description
Kristall is graphical small-internet client, supporting gemini, http,
https, gopher, finger. 


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

sed -e '/^install:/s| kristall||g' -i Makefile

sed \
  -e 's|$(shell cd $$PWD; git describe --tags)|V%{version}-%{release}|g' \
  -i src/%{name}.pro


%build
mkdir %{_vpath_builddir}
pushd %{_vpath_builddir}
%qmake_qt5 ../src/%{name}.pro

%make_build
cp -a %{name} ../
popd
pushd doc
./gen-man.sh
popd

%install
%make_install PREFIX=%{_prefix} MANPATH2=%{_mandir}

desktop-file-validate %{_datadir}/applications/*.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.*
%{_datadir}/mime/packages/*.xml
%{_mandir}/man1/*.1*


%changelog
* Wed Nov 17 2021 Phantom X <megaphantomx at hotmail dot com> - 0.3-1
- Initial spec
