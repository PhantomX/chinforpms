%global commit 0184edd5aea3f0bcbaca418d133023d005d16875
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20240519
%bcond_without snapshot

%if %{with snapshot}
%global dist .%{date}git%{shortcommit}%{?dist}
%endif

Name:           readpe
Version:        0.84
Release:        1%{?dist}
Summary:        PE file analysis toolkit

License:        GPL-2.0-only
URL:            https://github.com/mentebinaria/%{name}

%if %{with snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
%endif

Patch0:         %{name}-optimization.patch


BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libssl)
Requires:       libpe%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      pev < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       pev = %{?epoch:%{epoch}:}%{version}-%{release}


%description
pev is a little command-line based tool for PE (Windows executables) analysis.

%package -n libpe
Summary:        %{summary} library
License:        LGPL-3.0-only

%description -n libpe
The libpe package contains the dynamic libraries needed for %{name} and
plugins.

%package -n libpe-devel
Summary:        %{summary} development files
License:        LGPL-3.0-only
Requires:       libpe%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n libpe-devel
The libpe-devel package contains the development files libraries needed for 
plugins building.

%prep
%autosetup %{?with_snapshot:-n %{name}-%{commit}} -p1

sed -e 's|-O2 ||g' -i src/Makefile lib/libpe/Makefile

%build
%make_build \
  prefix=%{_prefix} \
  libdir=%{_libdir} \
  pluginsdir=%{_libdir}/%{name}/plugins \
  docdir=%{_pkgdocdir} \
  SHAREDIR=%{_datadir}/%{name} \
%{nil}

%install
%make_install \
  prefix=%{_prefix} \
  libdir=%{_libdir} \
  pluginsdir=%{_libdir}/%{name}/plugins \
  docdir=%{_pkgdocdir} \
  SHAREDIR=%{_datadir}/%{name} \
%{nil}

chmod 0755 %{buildroot}%{_libdir}/libpe.so*

mkdir -p %{buildroot}%{_includedir}/%{name}
install -pm 0644 include/*.h %{buildroot}%{_includedir}/%{name}/


%files
%license LICENSE*
%doc README.md
%{_bindir}/ofs2rva
%{_bindir}/pedis
%{_bindir}/pehash
%{_bindir}/peldd
%{_bindir}/pepack
%{_bindir}/peres
%{_bindir}/pescan
%{_bindir}/pesec
%{_bindir}/pestr
%{_bindir}/readpe
%{_bindir}/rva2ofs
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/plugins
%{_mandir}/man1/*.1*
%{_datadir}/%{name}/

%files -n libpe
%license lib/libpe/LICENSE
%doc lib/libpe/README.md
%{_libdir}/libpe.so.*

%files -n libpe-devel
%license lib/libpe/LICENSE
%{_includedir}/%{name}/
%{_libdir}/libpe.so

%changelog
* Sun Sep 22 2024 Phantom X <megaphantomx at hotmail dot com> - 0.84-1.20240519git0184edd
- 0.84
- Renamed from pev

* Tue Mar 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0.81-2.20220203git2d6337b
- Last archived snapshot

* Fri Aug 13 2021 Phantom X <megaphantomx at bol dot com dot br> - 0.81-1.20210223git45dfe03
- 0.81 snapshot

* Fri Jun 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.80-3
- Upstream patches to fix crashes

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.80-2
- Upstream patches for openssl 1.1.0 support

* Tue Jan 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.80-1
- Initial spec
