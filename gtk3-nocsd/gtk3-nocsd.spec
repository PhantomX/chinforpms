Name:           gtk3-nocsd
Version:        3
Release:        1%{?dist}
Summary:        Disables the client side decoration of Gtk+ 3

License:        LGPLv2.1
URL:            https://github.com/PCMan/%{name}
Source0:        https://github.com/PCMan/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# AUR - Marco Kundt
Source1:        https://aur.archlinux.org/cgit/aur.git/plain/30-gtk3-nocsd.sh?h=gtk3-nocsd-git#/30-gtk3-nocsd.sh

Patch0:         https://github.com/PCMan/gtk3-nocsd/commit/c64505268575e60322de682ea751660eba8d0e71.patch
Patch1:         https://github.com/PCMan/gtk3-nocsd/commit/82ff5a0da54aa6da27232b55eb93e5f4b5de22f2.patch

BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)

%description
%{name} is a small module used to disable the client side decoration of
Gtk+ 3.

%prep
%autosetup -p1

sed -e 's|$(LDFLAGS_LIB)|\0 $(LDFLAGS)|g' -i Makefile

%build

export CFLAGS="%{optflags}"
export LDFLAGS="%{__global_ldflags}"
export prefix=%{_prefix}
export libdir=%{_libdir}
export bindir=%{_bindir}
export datadir=%{_datadir}
export mandir=%{_mandir}

%make_build


%install
rm -rf %{buildroot}

export prefix=%{_prefix}
export libdir=%{_libdir}
export bindir=%{_bindir}
export datadir=%{_datadir}
export mandir=%{_mandir}

%make_install

chmod +x %{buildroot}%{_libdir}/lib%{name}.so.0

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh

%files
%license COPYING
%doc ChangeLog README.md
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.sh
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.0
%{_datadir}/bash-completion/completions/%{name}
%{_mandir}/man1/%{name}.1*


%changelog
* Fri Feb 10 2017 vinicius-mo <vinicius-mo at segplan.go.gov.br> - 3-1
- Initial spec
