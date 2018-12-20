%global debian_patch 2.1.1+dfsg-2

%global with_ghostdriver  %{?_with_ghostdriver: 0} %{?!_with_ghostdriver: 1}

Name:           phantomjs
Version:        2.1.1
Release:        1%{?dist}
Summary:        Minimalistic headless WebKit-based browser with JavaScript API

License:        BSD
URL:            http://phantomjs.org/
Source0:        https://github.com/ariya/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        http://http.debian.net/debian/pool/main/p/%{name}/%{name}_%{debian_patch}.debian.tar.xz
Patch0:         %{name}-qmake-qt5.patch

BuildRequires:  gcc-c++
BuildRequires:  python2-devel
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5PrintSupport)
BuildRequires:  pkgconfig(Qt5WebKitWidgets)


%description
PhantomJS is a headless WebKit with JavaScript API. It has fast and native
support for various web standards: DOM handling, CSS selector, JSON, Canvas,
and SVG.
This package is based on Debian dfsg, so some features are missing. See
README.Debian.

%prep
%setup -q -a 1

patch_command='patch -p1 -F1 -s'
${patch_command} -p1 -i debian/patches/build-hardening.patch
%if %{with_ghostdriver}
${patch_command} -p1 -i debian/patches/build-no-ghostdriver.patch
%endif
${patch_command} -p1 -i debian/patches/build-qt-components.patch
${patch_command} -p1 -i debian/patches/build-qt55-evaluateJavaScript.patch
${patch_command} -p1 -i debian/patches/build-qt55-no-websecurity.patch
${patch_command} -p1 -i debian/patches/build-qt55-print.patch
${patch_command} -p1 -i debian/patches/build-qtpath.patch
${patch_command} -p1 -i debian/patches/unlock-qt.patch

%patch0 -p1

%build
%set_build_flags

%{__python2} build.py --skip-git --skip-qtbase --skip-qtwebkit --confirm --release

%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 bin/%{name} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 debian/%{name}.1 %{buildroot}%{_mandir}/man1/

%files
%license LICENSE.BSD
%doc debian/README.Debian README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Fri Dec 29 2017 Phantom X <megaphantomx at bol dot com dot br> - 2.1.1-1
- Initial spec
