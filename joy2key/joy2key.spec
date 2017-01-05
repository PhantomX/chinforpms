Name:           joy2key
Version:        1.6.3
Release:        1%{?dist}
Summary:        Translate joystick movements into equivalent keystrokes

License:        GPLv2
URL:            http://sourceforge.net/projects/joy2key
Source0:        http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

# Debian
Patch0:         button_list_segfault.patch

BuildRequires:  pkgconfig(x11)
#Requires:       

%description
joy2key allows one to choose keyboard events for joystick axes and buttons, so
that a joystick or gamepad can be used with an application that doesn't have
native joystick support.

%prep
%autosetup -p1


%build
%configure \
  --disable-silent-rules

%make_build


%install
rm -rf %{buildroot}
%make_install


%files
%license COPYING
%doc AUTHORS ChangeLog joy2keyrc.sample rawscancodes README TODO
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Fri Dec 30 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-1
- Initial spec.
