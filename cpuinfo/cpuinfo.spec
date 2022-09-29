%global commit de2fa78ebb431db98489e78603e4f77c1f6c5c57
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20220914
%global with_snapshot 1

%global commit1 1.6.1
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 benchmark

%global commit2 1.11.0
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 googletest

%bcond_without tests

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           cpuinfo
Version:        0
Release:        1%{?gver}%{?dist}
Summary:        CPU INFOrmation library

License:        BSD
URL:            https://github.com/pytorch/%{name}

%if 0%{?with_snapshot}
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif
%if %{with tests}
Source1:        https://github.com/google/%{srcname1}/archive/v%{shortcommit1}/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        https://github.com/google/%{srcname2}/archive/release-%{shortcommit2}/%{srcname2}-%{shortcommit2}.tar.gz
%endif

Patch0:         0001-Versioned-shared-lib.patch

BuildRequires:  cmake
BuildRequires:  gcc-g++

Provides:       bundled(clog) = 0~git

%description
%{name} is a library to detect essential for performance optimization
information about host CPU.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        tools
Summary:        Tools binaries for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    tools
The %{name}-tools package contains tools binaries for testing %{name} library.


%prep
%autosetup %{?gver:-n %{name}-%{commit}} -p1

%if %{with tests}
mkdir -p deps/{googlebenchmark,%{srcname2}}
tar -xf %{S:1} -C deps/googlebenchmark --strip-components 1
tar -xf %{S:2} -C deps/%{srcname2} --strip-components 1

sed -e 's|cmake/Download|cmake/Disabled_Download|g' -i CMakeLists.txt deps/clog/CMakeLists.txt
sed \
  -e '/GetGitVersion/d' \
  -e '/get_git_version/d' \
  -e 's|${GIT_VERSION}|0.0.0|g' \
  -i deps/googlebenchmark/CMakeLists.txt
%endif

sed -e 's|CMAKE_INSTALL_DATAROOTDIR}|CMAKE_INSTALL_LIBDIR}/cmake|g' -i CMakeLists.txt

sed \
  -e 's|^Version: |\0%{version}|g' \
  -e 's|@PROJECT_HOMEPAGE_URL@|%{url}|g' \
  -i libcpuinfo.pc.in

cp deps/clog/LICENSE LICENSE.clog


%build
%cmake \
  -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir}/%{name} \
%if %{with tests}
  -DGOOGLEBENCHMARK_SOURCE_DIR:PATH=deps/googlebenchmark \
  -DGOOGLETEST_SOURCE_DIR:PATH=deps/%{srcname2} \
  -DBENCHMARK_ENABLE_INSTALL:BOOL=OFF \
  -DINSTALL_GTEST:BOOL=OFF \
%else
  -DCPUINFO_BUILD_UNIT_TESTS:BOOL=OFF \
  -DCPUINFO_BUILD_MOCK_TESTS:BOOL=OFF \
  -DCPUINFO_BUILD_BENCHMARKS:BOOL=OFF \
  -DCLOG_BUILD_TESTS:BOOL=OFF \
%endif
%{nil}

%cmake_build


%install
%cmake_install

# Rename library
mv %{buildroot}%{_libdir}/libclog.a \
   %{buildroot}%{_libdir}/libclog-%{name}.a

sed \
  -e 's|libclog\.a|libclog-%{name}.a|g' \
  -i %{buildroot}%{_libdir}/cmake/%{name}/%{name}-targets-noconfig.cmake

mv %{buildroot}%{_includedir}/%{name}/clog.h %{buildroot}%{_includedir}/%{name}/clog-%{name}.h

pushd %{buildroot}%{_bindir}
for i in * ;do
 mv ${i} %{name}-${i}
done
popd


%files
%license LICENSE*
%doc README.md
%{_libdir}/lib%{name}.so.*

%files devel
%license LICENSE*
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/libclog-%{name}.a
%{_libdir}/cmake/%{name}
%{_libdir}/pkgconfig/*.pc

%files tools
%license LICENSE
%{_bindir}/%{name}-*


%changelog
* Fri Sep 16 2022 Phantom X <megaphantomx at hotmail dot com> - 0-1.20220914gitde2fa78
- Initial spec