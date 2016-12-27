%global gkplugindir %{_libdir}/gkrellm2/plugins

Name:           gkrellmpc
Version:        0.1_beta10
Release:        2%{?dist}
Summary:        GKrellM plugin to control MPD

License:        GPL
URL:            http://mpd.wikia.com/wiki/Client:GKrellMPC
Source0:        http://mina.naguib.ca/dist/%{name}-%{version}.tar.gz

### Debian
Patch0:         fix-makefile-flags.patch
Patch1:         fix-fd-leak.patch
Patch2:         fix-memleaks.patch
# More fields on tooltip
Patch3:         %{name}-0.1_beta10-more-tooltips.patch

Requires:       gkrellm >= 2.2.0
BuildRequires:  gkrellm-devel >= 2.2.0 curl-devel

%description
GKrellMPC is a GKrellM plugin to control MPD.

%prep
%autosetup

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{__global_ldflags}"

%make_build

%install
rm -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{gkplugindir}
%{__install} -pm0755 %{name}.so \
  %{buildroot}%{gkplugindir}/

%files
%doc README.txt
%{gkplugindir}/%{name}.so

%changelog
* Tue Dec 27 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.1_beta10-2
- First spec.
