# Enable system mbedtls (needs old release, with cmac builtin support)
%bcond_with mbedtls

Name:           hactool
Version:        1.4.0
Release:        1%{?dist}
Summary:        A tool to view information about file formats for the Nintendo Switch

License:        ISC
URL:            https://github.com/SciresM/%{name}

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
# needs mbedtls with
%if %{with mbedtls}
BuildRequires:  mbedtls-devel
%else
Provides:       bundled(mbedtls) = 2.6.1
%endif


%description
%{name} is a tool to view information about, decrypt, and extract common file
formats for the Nintendo Switch, especially Nintendo Content Archives. 


%prep
%autosetup -p1

%if %{with mbedtls}
  rm -rf mbedtls
  sed \
    -e '/mbedtls/d' \
    -e 's|-L $(LIBDIR)||g' \
    -i Makefile
%endif

%global optflags %(echo "%{optflags}" | sed -e 's/-Wp,-D_GLIBCXX_ASSERTIONS//')
cat > config.mk <<EOF
CC = gcc
CFLAGS = %{optflags} -pedantic -std=gnu11 -fPIC
LDFLAGS = %{build_ldflags} -Wl,-z,relro -Wl,-z,now -lmbedtls -lmbedx509 -lmbedcrypto
EOF


%build
%make_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 %{name} %{buildroot}%{_bindir}/


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}


%changelog
* Sun Mar 06 2022 Phantom X <megaphantomx at hotmail dot com> - 1.4.0-1
- Initial spec
