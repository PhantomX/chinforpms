%global gkplugindir %{_libdir}/gkrellm2/plugins

Name:           gkrellmpc
Version:        0.1_beta10
Release:        3%{?dist}
Summary:        GKrellM plugin to control MPD

License:        GPLv2
URL:            http://mpd.wikia.com/wiki/Client:GKrellMPC

Source0:        http://mina.naguib.ca/dist/%{name}-%{version}.tar.gz

### Debian
Patch0:         fix-makefile-flags.patch
Patch1:         fix-fd-leak.patch
Patch2:         fix-memleaks.patch
Patch3:         fix-crash.patch
Patch4:         %{name}-g_path_get_basename.patch
Patch5:         %{name}-playlist-append.patch
# More fields on tooltip
Patch6:         %{name}-0.1_beta10-more-tooltips.patch
Patch7:         %{name}-volume-check-null.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(gkrellm) >= 2.2.0
BuildRequires:  pkgconfig(libcurl)

Requires:       gkrellm >= 2.2.0

%description
GKrellMPC is a GKrellM plugin to control MPD.

%prep
%autosetup -p1

%build
%set_build_flags

%make_build


%install
mkdir -p %{buildroot}%{gkplugindir}
install -pm0755 %{name}.so \
  %{buildroot}%{gkplugindir}/


%files
%doc README.txt
%{gkplugindir}/%{name}.so


%changelog
* Fri Jan 25 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.1_beta10-3
- Add some patches from Simon Marchi
- Fix console Glib g_strtod warnings

* Tue Dec 27 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.1_beta10-2
- First spec.
