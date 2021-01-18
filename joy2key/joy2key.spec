Name:           joy2key
Version:        1.6.3
Release:        2%{?dist}
Summary:        Translate joystick movements into equivalent keystrokes

License:        GPLv2
URL:            https://sourceforge.net/projects/joy2key
Source0:        https://gentoo.osuosl.org/distfiles/%{name}-%{version}.tar.bz2

# Debian
Patch0:         button_list_segfault.patch
Patch1:         home_not_set_segfault.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  pkgconfig(x11)

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

%make_install


%files
%license COPYING
%doc AUTHORS ChangeLog joy2keyrc.sample rawscancodes README TODO
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Wed Jul 29 2020 Phantom X <megaphantomx at hotmail dot com> - 1.6.3-2
- Use Gentoo mirror to Source0, SourceForge page is dead
- Add another patch from Debian

* Fri Dec 30 2016 Phantom X <megaphantomx at bol dot com dot br> - 1.6.3-1
- Initial spec.
