%global gkplugindir %{_libdir}/gkrellm2/plugins
%global pkgname     gkleds

Name:           gkrellm-leds
Version:        0.8.2
Release:        1%{?dist}
Summary:        GKrellM2 plugin for monitoring keyboard LEDs

License:        GPLv2
URL:            http://heim.ifi.uio.no/~oyvinha/gkleds/
Source0:        http://heim.ifi.uio.no/~oyvinha/%{pkgname}/%{pkgname}-%{version}.tar.gz

Requires:       gkrellm >= 2.2.0
BuildRequires:  autoconf libtool
BuildRequires:  gkrellm-devel >= 2.2.0
BuildRequires:  libXtst-devel

%description
gkleds is a GKrellM plugin which monitors the CapsLock, NumLock and ScrollLock
keys and reports their current status via on screen LEDs. This is useful for
people who have keyboards without LEDs, typically cordless keyboards. It also
lets you toggle the indicator state via mouse clicks.

%prep
%autosetup -n %{pkgname}-%{version}

sed -i -e "s|@GK_LDFLAGS@|\$(LDFLAGS)|g" src/Makefile.am

autoreconf -ivf

%build
%configure --libdir=%{gkplugindir}
%make_build

%install
rm -rf %{buildroot}

%make_install

find %{buildroot} -name '*.la' -print -delete

%files
%license COPYING License
%doc AUTHORS README TODO 
%{gkplugindir}/*.so

%changelog
* Tue Dec 27 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.8.2-1
- First spec.
