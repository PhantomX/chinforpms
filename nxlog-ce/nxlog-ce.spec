%global rname   nxlog
%global tarver  2.11.13
%global dl_id   348

Name:           %{rname}-ce
Version:        2.11.2190
Release:        1%{?dist}
Summary:        A modular, multi-threaded, high-performance log management solution

License:        NXLog Public License
URL:            http://nxlog.org

Source0:        https://nxlog.co/system/files/products/files/%{dl_id}/%{name}-%{version}.tar.gz
Source1:       %{name}-sysusers.conf
Source2:       %{name}.systemd

BuildRequires:  asciidoctor
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(apr-1)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(dbi)
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(libssl)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  perl-interpreter
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-ExtUtils-Embed
%{?systemd_requires}

Conflicts:      %{rname}


%description
nxlog is a modular, multi-threaded, high-performance log management
solution.


%prep
%autosetup -n %{name}-%{tarver}


%build
%configure \
  --with-moduledir=%{_libdir}/%{rname}/modules \
  --with-cachedir=%{_localstatedir}/spool/%{rname} \
  --with-pidfile=/run/%{rname}/%{rname}.pid \
  --enable-static=no \
  --enable-documentation \
%{nil}

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool


%make_build


%install
%make_install

find %{buildroot} -name '*.la' -delete

mkdir -p %{buildroot}%{_sysconfdir}/%{rname}
install -m 664 packaging/redhat/%{rname}.conf %{buildroot}%{_sysconfdir}/%{rname}/%{rname}.conf

mkdir -p %{buildroot}%{_sharedstatedir}/%{rname}/cert
mkdir -p %{buildroot}%{_localstatedir}/log/%{rname}
mkdir -p %{buildroot}%{_localstatedir}/spool/%{rname}
mkdir -p %{buildroot}%{_rundir}/%{rname}

mkdir _docs
mv %{buildroot}%{_datadir}/doc/%{name}/* _docs/
rm -rf %{buildroot}%{_datadir}/doc

mkdir -p %{buildroot}%{_sysusersdir}
install -pm0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{rname}.conf

mkdir -p %{buildroot}%{_unitdir}
install -pm0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{rname}.service

mkdir -p %{buildroot}%{_tmpfilesdir}
cat >> %{buildroot}%{_tmpfilesdir}/%{rname}.conf <<EOF
d /run/%{rname} 1770 %{rname} %{rname} -
EOF


%pre
%sysusers_create_compat %{SOURCE1}


%files
%license LICENSE
%doc _docs/*
%config %{_sysconfdir}/%{rname}/%{rname}.conf
%{_bindir}/%{rname}
%{_bindir}/%{rname}-processor
%{_bindir}/%{rname}-stmnt-verifier
%{_libdir}/%{rname}
%{perl_vendorlib}/Log/Nxlog.pm
%{_datadir}/%{name}
%{_mandir}/man8/*.8*
%attr(0770, %{rname}, %{rname}) %dir %{_sharedstatedir}/%{rname}
%attr(0770, %{rname}, %{rname}) %dir %{_sharedstatedir}/%{rname}/cert
%attr(0770, %{rname}, %{rname}) %dir %{_localstatedir}/log/%{rname}
%attr(0770, %{rname}, %{rname}) %dir %{_localstatedir}/spool/%{rname}
%attr(1770, %{rname}, %{rname}) %dir %{_rundir}/%{rname}
%{_sysusersdir}/%{rname}.conf
%{_tmpfilesdir}/%{rname}.conf
%{_unitdir}/%{rname}.service


%changelog
* Fri Aug 06 2021 Phantom X <megaphantomx at hotmail dot com> - 2.11.2190-1
- Initial spec
