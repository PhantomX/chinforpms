%global commit ec2d2f6833f038f07a72d15e2d52625c23e10b12
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20181218
%bcond snapshot 1

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

%global pkgname Disk-Indicator

Name:           disk-indicator
Version:        0.2.1
Release:        2%{?dist}
Summary:        Turns keyboard LEDs into hard disk indicator

License:        GPL-3.0-only
URL:            https://github.com/MeanEYE/Disk-Indicator
%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{pkgname}-%{version}.tar.gz
%endif

Patch0:         disk-indicator-homedir.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(x11)

%description
Small program for Linux that will turn your Scroll, Caps or Num Lock LED or LED
on your ThinkPad laptop into hard disk indicator.

%prep
%autosetup -n %{pkgname}-%{?with_snapshot:%{commit}}%{!?with_snapshot:%{version}} -p1

sed \
  -e '/^LINK_FLAGS=/s|=|\0$(LDFLAGS) |g' \
  -e '/^COMPILE_FLAGS=/s|-O2 -march=native|-Wno-error=unused-result $(CFLAGS)|g' \
  -i Makefile 

%build
./configure.sh --all
%make_build 

%install

mkdir -p %{buildroot}%{_bindir}
install -pm0755 disk_indicator %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d
cat > %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/%{name}.sh <<EOF
#!/usr/bin/sh
# Hangs without forking
/usr/bin/disk_indicator &
EOF
chmod 0755 %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/%{name}.sh

%files
%license COPYING
%doc AUTHORS README.md
%{_bindir}/disk_indicator
%{_sysconfdir}/X11/xinit/xinitrc.d/%{name}.sh


%changelog
* Fri Feb 15 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.2.1-2.20181218gitec2d2f6
- New snapshot

* Tue Dec 27 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.2.1-1.20151215git7620d56
- Initial spec.
