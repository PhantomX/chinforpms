%global commit 45dfe03aa57db686bd992dc5add45bd76fc03543
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20210223
%global with_snapshot 1

%global commit1 07f90de4e5cc6f7aff8e8b62ca1a39804907848f
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 libpe

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

%global vc_url  https://github.com/merces

Name:           pev
Version:        0.81
Release:        1%{?gver}%{?dist}
Summary:        PE file analysis toolkit

License:        GPLv2
URL:            https://pev.sourceforge.net/

%if 0%{?with_snapshot}
Source0:        %{vc_url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        %{vc_url}/libpe/archive/%{commit1}/%{srcname1}-%{shortcommit1}.tar.gz
%else
Source0:        https://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%endif

Patch0:         %{name}-optimization.patch


BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  pkgconfig(libcrypto)
BuildRequires:  pkgconfig(libssl)
Requires:       libpe%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description
pev is a little command-line based tool for PE (Windows executables) analysis.

%package -n libpe
Summary:        %{summary} library
License:        LGPLv3

%description -n libpe
The libpe package contains the dynamic libraries needed for %{name} and
plugins.

%package -n libpe-devel
Summary:        %{summary} development files
License:        LGPLv3
Requires:       libpe%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n libpe-devel
The libpe-devel package contains the development files libraries needed for 
plugins building.

%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p1
tar xf %{S:1} -C lib/libpe --strip-components 1
%else
%autosetup -n %{name}-%{version} -p1
%endif

%build

%set_build_flags

%make_build \
  prefix=%{_prefix} \
  libdir=%{_libdir}

%install
%make_install INSTALL="install -p" \
  prefix=%{_prefix} \
  libdir=%{_libdir}

chmod 0755 %{buildroot}%{_libdir}/libpe.so*

mkdir -p %{buildroot}%{_includedir}/pev
install -pm 0644 include/*.h %{buildroot}%{_includedir}/%{name}/


%files
%license LICENSE*
%doc README.md
%{_bindir}/*
%{_libdir}/%{name}/
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
* Fri Aug 13 2021 Phantom X <megaphantomx at bol dot com dot br> - 0.81-1.20210223git45dfe03
- 0.81 snapshot

* Fri Jun 07 2019 Phantom X <megaphantomx at bol dot com dot br> - 0.80-3
- Upstream patches to fix crashes

* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.80-2
- Upstream patches for openssl 1.1.0 support

* Tue Jan 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.80-1
- Initial spec
