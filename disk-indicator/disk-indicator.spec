%global commit 7620d561ac4d965eb7822b7922ed458de23ee9a6
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20151215
%global use_snapshot 1

%if 0%{?use_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           disk-indicator
Version:        0.2.1
Release:        1%{?gver}%{?dist}
Summary:        Turns keyboard LEDs into hard disk indicator

License:        GPLv3
URL:            https://github.com/MeanEYE/Disk-Indicator/
%if 0%{?use_snapshot}
Source0:        https://github.com/MeanEYE/Disk-Indicator/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%else
Source0:        https://github.com/MeanEYE/Disk-Indicator/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif

Patch0:         disk-indicator-homedir.patch

BuildRequires:  libX11-devel

%description
Small program for Linux that will turn your Scroll, Caps or Num Lock LED or LED
on your ThinkPad laptop into hard disk indicator.

%prep
%if 0%{?use_snapshot}
%autosetup -n Disk-Indicator-%{commit} -p0
%else
%autosetup -n Disk-Indicator-%{version} -p0
%endif

sed \
  -e '/^LINK_FLAGS=/s|=|\0$(LDFLAGS) |g' \
  -e '/^COMPILE_FLAGS=/s|$|\0 $(CFLAGS)|g' \
  -i Makefile 

%build

export CFLAGS="%{optflags} -Wno-error=unused-result"
export LDFLAGS="%{__global_ldflags}"

%make_build 

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
install -pm0755 disk_indicator %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d
cat > %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/%{name}.sh <<EOF
#!/bin/sh
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
* Tue Dec 27 2016 Phantom X <megaphantomx at bol dot com dot br> - 0.2.1-1.20151215git7620d56
- Initial spec.
