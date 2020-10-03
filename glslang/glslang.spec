%undefine _cmake_shared_libs

%global commit 759ae5aec02bd6fe5f58a9c7cd6c98cc1968c7b5
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global date 20200913
%global gver .%{date}git%{shortcommit}

Name:           glslang
Version:        11.0.0
Release:        100%{?gver}%{?dist}
Summary:        OpenGL and OpenGL ES shader front end and validator

License:        BSD and GPLv3+ and ASL 2.0
URL:            https://github.com/KhronosGroup

Source0:        %{url}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Patch1:         glslang-default-resource-limits_staticlib.patch
# Patch to build against system spirv-tools (rebased locally)
#Patch3:         https://patch-diff.githubusercontent.com/raw/KhronosGroup/glslang/pull/1722.patch#/0001-pkg-config-compatibility.patch
Patch3:         0001-pkg-config-compatibility.patch

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  spirv-tools-devel

%description
%{name} is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
%{name} is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%prep
%autosetup -p1 -n %{name}-%{commit}
# Fix rpmlint warning on debuginfo
find . -name '*.h' -or -name '*.cpp' -or -name '*.hpp'| xargs chmod a-x

%build
%cmake3 \
  -GNinja \
%{nil}

%cmake3_build

%install
%cmake3_install

# we don't want them in here
rm -rf %{buildroot}%{_includedir}/SPIRV

%ifnarch s390x ppc64
%check
pushd Test
./runtests localResults ../%{__cmake_builddir}/StandAlone/glslangValidator ../%{__cmake_builddir}/StandAlone/spirv-remap
popd
%endif

# Install libglslang-default-resource-limits.a
install -pm 0644 %{__cmake_builddir}/StandAlone/libglslang-default-resource-limits.a %{buildroot}%{_libdir}/

%files
%doc README.md README-spirv-remap.txt
%{_bindir}/glslangValidator
%{_bindir}/spirv-remap

%files devel
%{_includedir}/glslang/
%{_libdir}/libHLSL.a
%{_libdir}/libOGLCompiler.a
%{_libdir}/libOSDependent.a
%{_libdir}/libSPIRV.a
%{_libdir}/libSPVRemapper.a
%{_libdir}/libglslang.a
%{_libdir}/libGenericCodeGen.a
%{_libdir}/libMachineIndependent.a
%{_libdir}/libglslang-default-resource-limits.a
%{_libdir}/pkgconfig/glslang.pc
%{_libdir}/pkgconfig/spirv.pc
%{_libdir}/cmake/*

%changelog
* Sun Jul 26 2020 Phantom X <megaphantomx at hotmail dot com> - 11.0.0-100.20200913git8f4251a
- New snapshot
- Fix pkgconfig files

* Wed Apr 22 2020 Dave Airlie <airlied@redhat.com> - 8.13.3559-2
- Update to latest git snapshot

* Wed Jan 29 2020 Dave Airlie <airlied@redhat.com> - 8.13.3559-1
- Update to latest git snapshot

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.13.3496-3.20191102.git7f77b2e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 19 2019 Leigh Scott <leigh123linux@googlemail.com> - 7.13.3496-2.20191102.git7f77b2e
- Add patch for 'Fix a couple relative header paths in header'

* Wed Nov 13 2019 Dave Airlie <airlied@redhat.com> - 7.13.3496-1
- Latest upstream snapshot for validation layers build

* Sat Aug 03 2019 Dave Airlie <airlied@redhat.com> - 7.11.3214-3
- Latest upstream snapshot for validation layers build

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.11.3214-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 01:27:27 CEST 2019 Robert-André Mauchin <zebob.m@gmail.com> - 7.11.3214-1
- Release 7.11.3214
- Add patch to build against system spirv-tools

* Fri Mar 29 2019 Dave Airlie <airlied@redhat.com> - 3.1-0.13.20190329.gite0d59bb
- Update for vulkan 1.1.101.0

* Tue Feb 12 2019 Dave Airlie <airlied@redhat.com> - 3.1-0.12.20190212.git05d12a9
- Update for vulkan 1.1.92.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-0.11.20180727.gite99a268
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.1-0.10.20180727.gite99a268
- Update for vulkan 1.1.82.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-0.9.20180416.git3bb4c48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 23 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.1-0.8.20180416.git3bb4c48
- Update for vulkan 1.1.73.0

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 3.1-0.7.20180205.git2651cca
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Fri Feb 09 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.1-0.6.20180205.git2651cca
- Update for vulkan 1.0.68.0

* Fri Feb 09 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.1-0.5.20171028.git715c353
- Use ninja to build

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-0.4.20171028.git715c353
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.1-0.3.20171028.git715c353
- Exclude s390x and ppc64 from check section

* Wed Jan 03 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.1-0.2.20171028.git715c353
- Add check section to run tests
- Split binaries into main package

* Thu Jul 13 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.1-0.1.20171028.git715c353
- First build
