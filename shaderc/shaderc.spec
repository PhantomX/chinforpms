%global commit be8e0879750303a1de09385465d6b20ecb8b380d
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20180511
%global with_snapshot 1

%if 0%{?with_snapshot}
%global commit1 08d5b1f33af8c18785fb8ca02792b5fac81e248f
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global srcname1 googletest

%global commit2 fd9d9ef436017d3464c9ab1a915474a28f284cbe
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global srcname2 glslang

%global commit3 804e8884c483515e4b9fd2bcd5d0535462aa8f52
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global srcname3 SPIRV-Tools

%global commit4 3ce3e49d73b8abbf2ffe33f829f941fb2a40f552
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})
%global srcname4 SPIRV-Headers
%endif

%if 0%{?with_snapshot}
%global gver .%{date}git%{shortcommit}
%endif

Name:           shaderc
Version:        2018.0%{?gver}%{?dist}
Release:        1%{?dist}
Summary:        A collection of tools, libraries and tests for shader compilation

License:        ASL 2.0
URL:            https://github.com/google/shaderc
Source0:        https://github.com/google/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz
%if 0%{?with_snapshot}
Source1:        https://github.com/google/%{srcname1}/archive/%{commit1}.tar.gz#/%{srcname1}-%{shortcommit1}.tar.gz
Source2:        https://github.com/google/%{srcname2}/archive/%{commit2}.tar.gz#/google-%{srcname2}-%{shortcommit2}.tar.gz
Source3:        https://github.com/KhronosGroup/SPIRV-Tools/archive/%{commit3}.tar.gz#/%{srcname3}-%{shortcommit3}.tar.gz
Source4:        https://github.com/KhronosGroup/SPIRV-Headers/archive/%{commit4}.tar.gz#/%{srcname4}-%{shortcommit4}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  python2-devel
# Missing gem
#BuildRequires:  rubygem-asciidoctor
Requires:       glslang
Requires:       spirv-tools

%description
%{summary}.

glslc - Compile shaders into SPIR-V


%prep
%if 0%{?with_snapshot}
%autosetup -n %{name}-%{commit} -p0
%else
%autosetup -n %{name}-%{version} -p0
%endif

%if 0%{?with_snapshot}
mkdir -p third_party/googletest
tar -xf %{S:1} -C third_party/googletest --strip-components 1
mkdir -p third_party/glslang
tar -xf %{S:2} -C third_party/glslang --strip-components 1
mkdir -p third_party/spirv-tools
tar -xf %{S:3} -C third_party/spirv-tools --strip-components 1
mkdir -p third_party/spirv-headers
tar -xf %{S:4} -C third_party/spirv-headers --strip-components 1
%endif

cp -p glslc/README.asciidoc README.glslc.asciidoc

%build
mkdir -p build
pushd build

%cmake .. \
  -GNinja \
  -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON \
  -DPYTHON_EXE=%{__python2} \
  -DPYTHON_EXECUTABLE=%{__python2} \
  -DSHADERC_SKIP_TESTS:BOOL=ON \
  -DSKIP_GLSLANG_INSTALL:BOOL=ON \
  -DSKIP_SPIRV_TOOLS_INSTALL:BOOL=ON \
  -DSKIP_GOOGLETEST_INSTALL:BOOL=ON \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DCMAKE_BUILD_TYPE=None

%ninja_build

popd


%install
%ninja_install -C build

rm -f %{buildroot}/%{_bindir}/{glslang,spirv}*
rm -rf %{buildroot}/%{_libdir}
rm -rf %{buildroot}/%{_includedir}


%files
%license LICENSE third_party/LICENSE.*
%doc AUTHORS README.md README.glslc.asciidoc
%{_bindir}/glslc


%changelog
* Mon May 14 2018 Phantom X <megaphantomx at bol dot com dot br> - 2018.0-1.20180511gitbe8e087
- Initial spec
