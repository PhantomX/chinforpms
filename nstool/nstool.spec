%global optflags %{optflags} -Wp,-U_GLIBCXX_ASSERTIONS

%global commit10 b03b081e026ceb1226b45de926babe629d6c0688
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})
%global srcname10 libfmt

%global commit11 74346376dd035e9fbc161cdb80afc646b72fde86
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})
%global srcname11 libmbedtls

%global commit12 5d50d02f8f3b8918bdfbbb599b8c4c1628660d89
%global shortcommit12 %(c=%{commit12}; echo ${c:0:7})
%global srcname12 libpietendo

%global commit13 578d170f5b294e4a9feb3cc2d504896e846f204e
%global shortcommit13 %(c=%{commit13}; echo ${c:0:7})
%global srcname13 libtoolchain

%bcond_without fmt

%global fmt_ver 10
%global mbedtls_ver 2.16.12
%global pietendo_ver 0.7.2
%global toolchain_ver 0.7.0

%global vc_url  https://github.com/jakcron

Name:           nstool
Version:        1.9.2
Release:        1%{?dist}
Summary:        A tool to view information about file formats for the NX console

License:        MIT AND Apache-2.0
URL:            %{vc_url}/%{name}

Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

%if %{without fmt}
Source10:       %{vc_url}/%{srcname10}/archive/%{commit10}/%{srcname10}-%{shortcommit10}.tar.gz
%endif
Source11:       %{vc_url}/%{srcname11}/archive/%{commit11}/%{srcname11}-%{shortcommit11}.tar.gz
Source12:       %{vc_url}/%{srcname12}/archive/%{commit12}/%{srcname12}-%{shortcommit12}.tar.gz
Source13:       %{vc_url}/%{srcname13}/archive/%{commit13}/%{srcname13}-%{shortcommit13}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
%if %{with fmt}
BuildRequires:  pkgconfig(fmt) >= %{fmt_ver}
%endif
BuildRequires:  pkgconfig(liblz4) >= 1.9.4
Provides:       bundled(mbedtls) = %{mbedtls_ver}
Provides:       bundled(libpietendo) = %{pietendo_ver}
Provides:       bundled(libtoolchain) = %{toolchain_ver}

%description
%{name} is a tool to view information about, decrypt, and extract common file
formats for the NX console, especially NCA files.


%prep
%autosetup -p1

pushd deps
%if %{without fmt}
tar -xf %{S:10} -C libfmt --strip-components 1
cp -p libfmt/LICENSE.rst libfmt/LICENSE.rst.fmt
%endif
tar -xf %{S:11} -C libmbedtls --strip-components 1
cp -p libmbedtls/LICENSE LICENSE.mbedtls
tar -xf %{S:12} -C libpietendo --strip-components 1
cp -p libpietendo/LICENSE LICENSE.libpietendo
tar -xf %{S:13} -C libtoolchain --strip-components 1
cp -p libtoolchain/LICENSE LICENSE.libtoolchain
popd

sed \
  -e 's|^CXXFLAGS =|CXXFLAGS +=|' \
  -e 's|^CFLAGS =|CFLAGS +=|' \
  -e 's|@ar|ar|g' \
  -e 's|@$(CC)|$(CC)|g' \
  -e 's|@$(CXX)|$(CXX)|g' \
  -i makefile deps/*/makefile


%build
%set_build_flags
export LIB="$LDFLAGS"
export ROOT_PROJECT_NAME=%{name}
export ROOT_PROJECT_DEPENDENCY_PATH="$(pwd)/deps"
%if %{without fmt}
%make_build -C deps/libfmt static_lib
%endif
%make_build -C deps/libmbedtls static_lib
%make_build -C deps/libtoolchain static_lib
%make_build -C deps/libpietendo static_lib
%make_build


%install
mkdir -p %{buildroot}%{_bindir}
install -pm0755 bin/%{name} %{buildroot}%{_bindir}/


%files
%license LICENSE deps/LICENSE*
%doc README.md SWITCH_KEYS.md
%{_bindir}/%{name}


%changelog
* Wed Mar 19 2025 Phantom X <megaphantomx at hotmail dot com> - 1.9.2-1
- 1.9.2

* Fri Sep 20 2024 Phantom X <megaphantomx at hotmail dot com> - 1.9.1-1
- 1.9.1

* Mon Mar 25 2024 Phantom X <megaphantomx at hotmail dot com> - 1.9.0-1
- Initial spec
