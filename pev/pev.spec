Name:           pev
Version:        0.80
Release:        2%{?dist}
Summary:        PE file analysis toolkit

License:        GPLv2
URL:            http://pev.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

Patch0:         %{name}-optimization.patch
# https://github.com/merces/pev/pull/104
Patch1:         https://github.com/merces/pev/commit/98f5f22f91f02821be1604bbce61efb45f7e3696.patch
Patch2:         https://github.com/merces/pev/commit/3fc1d6ac863cfb596e8e9263e03871aec8c00d22.patch

BuildRequires:  gcc
BuildRequires:  pkgconfig(libpcre)
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
%autosetup -p1 -n %{name}

sed -e '/DEFAULT_PLUGINS_PATH/s|/usr/local/lib|%{_libdir}|g' -i src/config.c

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

%ldconfig_scriptlets -n libpe

%files
%license LICENSE*
%doc README.md
%{_bindir}/*
%{_libdir}/%{name}
%{_mandir}/man1/*.1*
%{_datadir}/%{name}

%files -n libpe
%license lib/libpe/LICENSE
%doc lib/libpe/README.md
%{_libdir}/libpe.so.*

%files -n libpe-devel
%license lib/libpe/LICENSE
%{_includedir}/%{name}
%{_libdir}/libpe.so

%changelog
* Thu Jun 15 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.80-2
- Upstream patches for openssl 1.1.0 support

* Tue Jan 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.80-1
- Initial spec
