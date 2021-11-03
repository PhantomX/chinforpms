Name:           gtk3-nocsd
Version:        3.0.8
Release:        1%{?dist}
Summary:        Disables the client side decoration of Gtk+ 3

License:        LGPLv2.1
URL:            https://github.com/ZaWertun/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# AUR - Marco Kundt
Source1:        https://aur.archlinux.org/cgit/aur.git/plain/30-%{name}.sh?h=%{name}-git#/30-%{name}.sh

Patch0:         %{name}-multilib.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)

%description
%{name} is a small module used to disable the client side decoration of
Gtk+ 3.

%prep
%autosetup -p1

cp -p %{SOURCE1} %{name}.sh

sed \
  -e "/x\"$GTK_CSD\"x/s,\],\0 \&\& echo \$LD_PRELOAD | grep -v -q -F \'/usr/\${LIB}/libgtk3-nocsd.so.0\'," \
  -i %{name}.sh

sed -e 's|$(LDFLAGS_LIB)|\0 $(LDFLAGS)|g' -i Makefile

%build

%set_build_flags
export prefix=%{_prefix}
export libdir=%{_libdir}
export bindir=%{_bindir}
export datadir=%{_datadir}
export mandir=%{_mandir}

%make_build


%install

export prefix=%{_prefix}
export libdir=%{_libdir}
export bindir=%{_bindir}
export datadir=%{_datadir}
export mandir=%{_mandir}

%make_install

chmod +x %{buildroot}%{_libdir}/lib%{name}.so.0

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm0644 %{name}.sh %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh

%files
%license COPYING
%doc ChangeLog README.md
%{_sysconfdir}/profile.d/%{name}.sh
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.0
%{_datadir}/bash-completion/completions/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Mon Nov 01 2021 Phantom X <megaphantomx at hotmail dot com> - 3.0.8-1
- 3.0.8 from ZaWertun fork

* Mon Feb 20 2017 Phantom X <megaphantomx at bol dot com dot br> - 3-3
- Tweak profile script
- Drop %%config from profile script

* Sun Feb 19 2017 Phantom X <megaphantomx at bol dot com dot br> - 3-2
- Fix multilib

* Fri Feb 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 3-1
- Initial spec
