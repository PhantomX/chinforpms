%global commit 012a7dc055768367eead09a606f5d378e1c7d914
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200917
%global with_snapshot 1

%global commit1 7d33fee11ec480beae4c28ad09ca56d974140a72
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 gmock

%global commit2 800f5422ac9d9e0ad59cd860a2ef3a679588acb4
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 gtest

%bcond_without qt

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           barrier
Version:        2.3.3
Release:        2%{?gver}%{?dist}
Summary:        Share mouse and keyboard between multiple computers over the network

License:        GPLv2
URL:            https://github.com/debauchee/%{name}
%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif
Source1:        https://github.com/google/googlemock/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        https://github.com/google/googletest/archive/%{commit2less}/%{srcname2}-%{shortcommit2}.tar.gz
Source3:        %{name}.appdata.xml

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(avahi-compat-libdns_sd)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libssl)
%if %{with qt}
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Widgets)
Requires:       hicolor-icon-theme
%endif

%description
Barrier is software that mimics the functionality of a KVM switch, which
historically would allow you to use a single keyboard and mouse to control
multiple computers by physically turning a dial on the box to switch the machine
you're controlling at any given moment. Barrier does this in software, allowing
you to tell it which machine to control by moving your mouse to the edge of the
screen, or by using a keypress to switch focus to a different system.


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
%else
%autosetup -n %{name}-%{version} -p1
%endif

tar -xf %{S:1} -C ext/gmock --strip-components 1
tar -xf %{S:2} -C ext/gtest --strip-components 1

cp -p %{S:3} %{name}.appdata.xml
sed -e 's|_VERSION_|%{?epoch:%{epoch}:}%{version}|g' -i %{name}.appdata.xml

sed \
  -e 's|EQUAL 8 OR|EQUAL 7 OR|g' \
  -e 's|\.b${BARRIER_BUILD_NUMBER}||g' \
  -e 's|-${BARRIER_VERSION_STAGE}||g' \
  -i cmake/Version.cmake


%build
%{cmake3} \
%if %{without qt}
  -DBARRIER_BUILD_GUI:BOOL=OFF \
%endif
%if 0%{?with_snapshot}
  -DBARRIER_VERSION_STAGE:STRING=snapshot \
  -DBARRIER_REVISION="%{shortcommit}" \
  -DBARRIER_BUILD_NUMBER="%{shortcommit}" \
%else
  -DBARRIER_VERSION_STAGE:STRING=stable \
%endif
%{nil}

%cmake_build


%install
%cmake_install

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 doc/%{name}{c,s}.1 %{buildroot}%{_mandir}/man1/

%if %{with qt}
mkdir -p %{buildroot}%{_metainfodir}
install -pm0644 %{name}.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml

desktop-file-edit \
  --remove-category=DesktopUtility \
  %{buildroot}%{_datadir}/applications/%{name}.desktop


appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml
%endif


%files
%license LICENSE
%doc README.md doc/%{name}.conf.example*
%{_bindir}/%{name}c
%{_bindir}/%{name}s
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*.1*
%if %{with qt}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_metainfodir}/%{name}.appdata.xml
%endif


%changelog
* Tue Sep 29 2020 Phantom X <megaphantomx at hotmail dot com> - 2.3.3-2.20200917git012a7dc
- Bump

* Sat Aug 15 2020 Phantom X <megaphantomx at hotmail dot com> - 2.3.3-1.20200807gitd186548
- 2.3.3

* Fri Jun 12 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.3.2-3.20200611git965cd70
- Bump

* Sat May 09 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.3.2-2.20200507git2d2e929
- New snapshot

* Sun Apr 19 2020 Phantom X <megaphantomx at bol dot com dot br> - 2.3.2-1.20200326gitb6a1b57
- Initial spec
