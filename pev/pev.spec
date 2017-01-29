Name:           pev
Version:        0.80
Release:        1%{?dist}
Summary:        PE file analysis toolkit

License:        GPLv2
URL:            http://pev.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

Patch0:         %{name}-optimization.patch

BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(openssl)
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

export CFLAGS="%{optflags}"
export LDFLAGS="%{__global_ldflags}"

%make_build \
  prefix=%{_prefix} \
  libdir=%{_libdir}

%install
rm -rf %{buildroot}
%make_install INSTALL="install -p" \
  prefix=%{_prefix} \
  libdir=%{_libdir}

chmod 0755 %{buildroot}%{_libdir}/libpe.so*

mkdir -p %{buildroot}%{_includedir}/pev
install -pm 0644 include/*.h %{buildroot}%{_includedir}/%{name}/

%post -n libpe -p /sbin/ldconfig

%postun -n libpe -p /sbin/ldconfig

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
* Tue Jan 10 2017 Phantom X <megaphantomx at bol dot com dot br> - 0.80-1
- Initial spec
