%global vc_url   https://github.com/zyantific/%{name}

Name:           zydis
Version:        4.0.0
Release:        1%{?dist}
Summary:        Fast and lightweight x86/x86-64 disassembler and code generation library

License:        MIT
URL:            https://zydis.re/

Source:         %{vc_url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  cmake(zycore)
BuildRequires:  doxygen
BuildRequires:  python3

%description
Zydis is fast and lightweight x86/x86-64 disassembler and code generation
library.


%package        devel
Summary:        Development libraries and header files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       zycore-c-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        tools
Summary:        Tools for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description tools
The %{name}-tools package contains tools about %{name}.

%package        docs
Summary:        HTML documentation for %{name}

%description    docs
Provides the documentation files for use with %{name}.


%prep
%autosetup -p1

%build
%cmake \
  -DZYAN_SYSTEM_ZYCORE:BOOL=ON \
  -DZYDIS_BUILD_SHARED_LIB:BOOL=ON \
%{nil}

%cmake_build

%install
%cmake_install

mv %{buildroot}%{_datadir}/doc/Zydis _docs


%check
cd tests/
./regression.py test ../%{_vpath_builddir}/ZydisInfo
./regression_encoder.py ../%{_vpath_builddir}/Zydis{Fuzz{ReEncoding,Encoder},TestEncoderAbsolute}


%files
%license LICENSE
%doc README.md
%{_libdir}/libZydis.so.*

%files devel
%{_includedir}/Zydis/
%{_libdir}/cmake/zydis/
%{_libdir}/libZydis.so

%files tools
%{_bindir}/ZydisDisasm
%{_bindir}/ZydisInfo

%files docs
%doc _docs/*


%changelog
* Thu Oct 19 2023 Phantom X <megaphantomx at hotmail dot com> - 4.0.0-1
- Initial spec

