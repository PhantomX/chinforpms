%global debpatchver 16

Name:           xwit
Version:        3.4
Release:        1%{?dist}
Summary:        Vollection of simple routines to call some X11 functions

License:        Public Domain
URL:            https://packages.debian.org/unstable/x11/xwit
Source0:        https://deb.debian.org/debian/pool/main/x/%{name}/%{name}_%{version}.orig.tar.gz
Source1:        https://deb.debian.org/debian/pool/main/x/%{name}/%{name}_%{version}-%{debpatchver}.debian.tar.xz

BuildRequires:  gcc
BuildRequires:  pkgconfig(x11)


%description
xwit allows one to call some X11 functions from the command line or a
shell script.

xwit will resize, iconify, pop, and move windows given by name or id,
change an icon, title or name, set the screen saver going, and change
individual key autorepeat settings, move the mouse cursor, etc.


%prep
%autosetup -n %{name}-%{version}.orig -a 1
for i in $(<debian/patches/series);do
  patch -p1 -F1 -s -i debian/patches/$i
done

cp -p debian/copyright LICENSE


%build
%set_build_flags
CFLAGS+=" -Wall -Wmissing-prototypes -Wstrict-prototypes"
LDFLAGS+=" -Wl,-z,defs"
%make_build


%install
mkdir -p %{buildroot}%{_bindir}
%make_install

mkdir -p %{buildroot}%{_mandir}/man1
install -pm0644 xwit.man %{buildroot}%{_mandir}/man1/%{name}.1


%files
%license LICENSE
%doc README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*


%changelog
* Mon Oct 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 3.4-1
- Initial spec
