Name:           rapidyaml
Version:        0.3.0
Release:        1%{?dist}
Summary:        A library to parse and emit YAML, and do it fast

License:        MIT
URL:            https://github.com/biojppm/%{name}

Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}-src.tgz


BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  make


%description
ryml is a C++ library to parse and emit YAML, and do it fast, on everything
from x64 to bare-metal chips without operating system.

%package        devel
Summary:        Development files for %{name}
Requires:       %{?epoch:%{epoch}:}%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version}-src -p1

sed -e '/_INSTALL_DIR/s| lib/|%{_lib}|g' -i ext/c4core/cmake/c4Project.cmake

%build
%cmake \
%{nil}

%cmake_build


%install

%cmake_install


%files
%license LICENSE.txt
%doc README.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/c4
%{_includedir}/ryml*.*
%{_libdir}/*.so
%{_libdir}/cmake/c4core
%{_libdir}/cmake/ryml


%changelog
* Sat Jan 29 2022 Phantom X <megaphantomx at hotmail dot com> - 0.3.0-1
- Initial spec
